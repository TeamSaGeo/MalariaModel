import sys
from PyQt6 import QtWidgets, uic, QtCore
from mainwindow import Ui_MainWindow
from modelCoustani import ModelCoustani
import geopandas as gpd
import pandas as pd

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.pageInd = self.stackedWidget.currentIndex()
        self.pushButton_parcelFileName.clicked.connect(lambda : self.selectInputFile(self.parcelFileName, "*.shp"))
        self.pushButton_rainFileName.clicked.connect(lambda : self.selectInputFile(self.rainFileName,"*.csv"))
        self.pushButton_tempFileName.clicked.connect(lambda : self.selectInputFile(self.tempFileName,"*.csv"))
        self.pushButton_pathOutput.clicked.connect(self.selectOutputDir)
        self.pushButton_run.clicked.connect(self.run)

    def selectInputFile(self, input, extension):
        path, _filter = QtWidgets.QFileDialog.getOpenFileName(
            self.centralwidget, "Choisir le fichier", "", extension)
        if _filter:
            input.setText(path)
            input.setStyleSheet("border: 1px solid white")
        else:
            button = QtWidgets.QMessageBox.information(
                    self.centralwidget,
                    "Erreur",
                    "Choisir un fichier valide",
                    )

    def selectOutputDir(self):
        foldername = QtWidgets.QFileDialog.getExistingDirectory(
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

    def run(self):
        if self.pageInd == 0:
            if self.EmptyLineEdit(self.parcelFileName) or self.EmptyLineEdit(self.rainFileName) or self.EmptyLineEdit(self.tempFileName):
                button = QtWidgets.QMessageBox.information(
                    self.centralwidget,
                    "Erreur",
                    "Remplir les champs requis",
                    )
            else:
                self.pageInd += 1
                self.stackedWidget.setCurrentIndex(self.pageInd)

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
                QtCore.QCoreApplication.processEvents()

                bdate_min = self.model.tempCSVData['numero_annee'].min()
                bdate_max = self.model.tempCSVData['numero_annee'].max()
                bdate_output_max = QtCore.QDate(bdate_max,12,31)
                self.bdate.setMinimumDate(QtCore.QDate(bdate_min,1,1))
                self.bdate.setMaximumDate(QtCore.QDate(bdate_max,12,31))
                self.bdate_output.setMinimumDate(QtCore.QDate(bdate_min+1,1,1))
                self.bdate_output.setMaximumDate(bdate_output_max)
                self.edate.setMinimumDate(QtCore.QDate(bdate_min+1,1,1))
                self.edate.setMaximumDate(bdate_output_max)

        elif self.pageInd == 1:
            if self.EmptyLineEdit(self.pathOutput) or self.anyCheckedFormat():
                button = QtWidgets.QMessageBox.information(
                    self.centralwidget,
                    "Erreur",
                    "Remplir les champs requis",
                    )
            else:
                self.pushButton_run.setEnabled(False)
                # # 4) Initialisation
                self.textEdit.append("Initialization ... ")
                self.model.initialisation()

                # # 5) Simulation
                now = self.bdate.date()
                day = 0
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
                button = QtWidgets.QMessageBox.information(
                    self.centralwidget,
                    "Status",
                    "Simulation terminee !",
                    )
                self.pushButton_run.setEnabled(True)

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
