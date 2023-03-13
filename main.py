import sys
from PyQt6 import uic, QtCore
from PyQt6.QtWidgets import *
from mainwindow import Ui_MainWindow
from modelCoustani import ModelCoustani
import geopandas as gpd
import pandas as pd

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.pageInd = self.stackedWidget.currentIndex()
        self.btn_parcelFileName.clicked.connect(lambda : self.selectInputFile(self.parcelFileName, "*.shp"))
        self.btn_rainFileName.clicked.connect(lambda : self.selectInputFile(self.rainFileName,"*.csv"))
        self.btn_tempFileName.clicked.connect(lambda : self.selectInputFile(self.tempFileName,"*.csv"))
        self.btn_load.clicked.connect(self.load)
        self.listWidget.itemSelectionChanged.connect(self.next)
        self.btn_pathOutput.clicked.connect(self.selectOutputDir)

        # self.btn_next.clicked.connect(self.next)
        # self.btn_back.clicked.connect(self.previous)



        menu = ["Paramètres d'entrées", "Paramètres de sortie", "Exécuter"]
        columns = ["Paramètres KL", "Précipitations", "Températures"]
        rows = ["Lieu","Année","Type de données","Surface des plans d'eau (m2)",
                                            "Surface des rivieres (m2)",
                                            "Surface des cultures agricoles (m2)",
                                            "Surface des rizières (m2)",
                                            "Surface totale (m2)"]

        self.listWidget.addItems(menu)
        self.columnCount = len(columns)
        self.rowCount = len(rows)
        self.tableWidget.setColumnCount(self.columnCount)
        self.tableWidget.setRowCount(self.rowCount)
        self.tableWidget.setHorizontalHeaderLabels(columns)
        self.tableWidget.setVerticalHeaderLabels(rows)

    def selectInputFile(self, input, extension):
        path, _filter = QFileDialog.getOpenFileName(
            self.centralwidget, "Choisir le fichier", "", extension)
        if _filter:
            input.setText(path)
            input.setStyleSheet("border: 1px solid white")
        else:
            button = QMessageBox.information(
                    self.centralwidget,
                    "Erreur",
                    "Choisir un fichier valide",
                    )

    def selectOutputDir(self):
        foldername = QFileDialog.getExistingDirectory(
            self.centralwidget,"Sélectionner le répertoire de sortie")
        if foldername:
            self.pathOutput.setText(foldername)

    def getWeekNumber(self,w):
        if w < 10:
            return "s0" + str(w)
        elif w == 53:
            return "s52"
        else:
            return "s" + str(w)

    def EmptyLineEdit(self, input):
        if input.text():
            input.setStyleSheet("border: 1px solid white")
            return False
        else:
            input.setStyleSheet("border: 1px solid red")
            return True

    def anyCheckedFormat(self):
        if self.outputSHPAllDates.isChecked() or self.outputKMLAllDates.isChecked() or self.outputKMLLastDate.isChecked() or self.outputSHPLastDate.isChecked():
            return False
        else:
            self.label_output_format.setStyleSheet("color: red")
            return True

    def previous(self):
        if self.pageInd == 1:
            self.pageInd -= 1
            self.stackedWidget.setCurrentIndex(self.pageInd)

    def load(self):
        if self.EmptyLineEdit(self.parcelFileName) or self.EmptyLineEdit(self.rainFileName) or self.EmptyLineEdit(self.tempFileName):
            button = QMessageBox.information(
                self.centralwidget,
                "Erreur",
                "Remplir les champs requis",
                )
        else:
            # 1) Instanciation des datafacers : inputs
            # 2) Instanciation des datafacers : outputs
            self.textEdit.setText("Model ModeleCoustani ready to run")
            QtCore.QCoreApplication.processEvents()

            # 3) Lecture des donnees
            self.model = ModelCoustani(self)
            msg = "Reading data ...\n"
            msg += "found "+ str(self.model.shp.shape[0]) +" parcels\n"
            msg += "Size of rain data file: " + str(len(self.model.rainCSVData)) +"\n"
            msg += "Size of temperature data file: " + str(len(self.model.tempCSVData))
            self.textEdit.append(msg)

            environment_fields = self.model.shp.columns
            precip_fields = self.model.rainCSVData.columns
            temp_fields = self.model.tempCSVData

            self.groupBoxInputParam.setEnabled(False)
            self.tableWidget.setEnabled(True)

            for row in range(self.rowCount):
                for col in range (self.columnCount):
                    field_name = QComboBox()

                    if ((row == 1 or row == 2) and col == 0) or (row >= 3 and col >= 1):
                        field_name = QLineEdit()
                        field_name.setEnabled(False)

                    elif col == 0:
                        field_name.addItems(environment_fields)
                    elif row == 2:
                        field_name.addItems(["journalier","hebdomadaire"])
                    elif col == 1:
                        field_name.addItems(precip_fields)
                    else:
                        field_name.addItems(temp_fields)

                    self.tableWidget.setCellWidget(row, col, field_name)

            bdate_min = self.model.tempCSVData['numero_annee'].min()
            bdate_max = self.model.tempCSVData['numero_annee'].max()
            bdate_output_max = QtCore.QDate(bdate_max,12,31)
            self.bdate.setMinimumDate(QtCore.QDate(bdate_min,1,1))
            self.bdate.setMaximumDate(QtCore.QDate(bdate_max,12,31))
            self.bdate_output.setMinimumDate(QtCore.QDate(bdate_min+1,1,1))
            self.bdate_output.setMaximumDate(bdate_output_max)
            self.edate.setMinimumDate(QtCore.QDate(bdate_min+1,1,1))
            self.edate.setMaximumDate(bdate_output_max)

    def kl_param_error(self):
        for col in range(self.columnCount):
            list_selected_field = []
            for row in range(self.rowCount):
                field_name = self.tableWidget.cellWidget(row,col)
                if field_name.metaObject().className() == "QComboBox" :
                    list_selected_field.append(field_name.currentText())
            if len(list_selected_field) != len(set(list_selected_field)):
                button = QMessageBox.information(
                    self.centralwidget,
                    "Erreur",
                    "Choisir des différents valeurs pour la colonne " + str(col+1),
                    )
                return True
        return False

    def next(self):
        i = self.listWidget.currentRow()
        if i == 0:
            self.stackedWidget.setCurrentIndex(0)

        if i == 1:
            # verifier paramètres KL
            if self.EmptyLineEdit(self.parcelFileName) or self.EmptyLineEdit(self.rainFileName) or self.EmptyLineEdit(self.tempFileName):
                button = QMessageBox.information(
                    self.centralwidget,
                    "Erreur",
                    "Remplir les champs requis",
                    )
                self.listWidget.setCurrentRow(0)
            elif self.kl_param_error():
                self.listWidget.setCurrentRow(0)
            else:
                self.stackedWidget.setCurrentIndex(1)


        if i == 2 :
            if self.stackedWidget.currentIndex() == 0:
                # button = QMessageBox.information(
                #     self.centralwidget,
                #     "Erreur",
                #     "Remplir les paramètres d'entrées",
                #     )
                self.listWidget.setCurrentRow(0)
            elif self.EmptyLineEdit(self.pathOutput) or self.anyCheckedFormat():
                button = QMessageBox.information(
                    self.centralwidget,
                    "Erreur",
                    "Remplir les champs requis",
                    )
            else:
                # self.btn_next.setEnabled(False)
                # # 4) Initialisation
                self.textEdit.append("Initialization ... ")
                self.model.initialisation()

                # # 5) Simulation
                now = self.bdate.date()
                day = 0
                self.textEdit.append("Simulation start: "+ self.bdate.date().toString("dd/MM/yyyy"))

                # fin = now
                # test_display = 0.0
                shp_list = gpd.GeoDataFrame()
                kml_list = gpd.GeoDataFrame()
                # # Boucle sur les jours
                while now < self.edate.date():
                    w = self.getWeekNumber(now.weekNumber()[0])
                    self.textEdit.append(now.toString("dd/MM/yyyy") + "; week " + w)
                    QtCore.QCoreApplication.processEvents()

                    w7 = self.getWeekNumber(now.addDays(-7).weekNumber()[0])
                    # test_display = math.remainder(day,self.FREQUENCE_DISPLAY.value())	# pour l'export des donnees tous les frequencedisplay jours
                    # fin = now.addDays(self.FREQUENCE_DISPLAY.value() - 1)

                    # Boucle sur les parcelles
                    test_display = self.model.simulation(now,w,w7,day)
                    if now > self.model.bdate_output and test_display == 0 :
                        if self.outputKMLAllDates.isChecked() :
                            kml_list = pd.concat([kml_list,self.model.shp],ignore_index = True)
                        if self.outputSHPAllDates.isChecked():
                            shp_list = pd.concat([shp_list,self.model.shp], ignore_index = True)
                    day += 1
                    now = now.addDays(1)
                    # Fin de la boucle sur les jours

                # # 5) Export KML
                self.model.exportResult(shp_list,kml_list)
                button = QMessageBox.information(
                    self.centralwidget,
                    "Status",
                    "Simulation terminee !",
                    )
                # self.btn_next.setEnabled(True)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
