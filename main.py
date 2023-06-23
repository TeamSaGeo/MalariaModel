import sys
from PyQt6 import uic, QtCore
from PyQt6.QtWidgets import *
from mainwindow import Ui_MainWindow

from SEIRmodel import SEIRModel
import geopandas as gpd
import pandas as pd
import ntpath
import os

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.pageInd = self.stackedWidget.currentIndex()

        # On click on bouton select input file
        self.btn_parcelFileName.clicked.connect(lambda : self.selectInputFile(self.parcelFileName, "*.shp"))
        self.btn_rainFileName.clicked.connect(lambda : self.selectInputFile(self.rainFileName,"*.csv"))
        self.btn_tempFileName.clicked.connect(lambda : self.selectInputFile(self.tempFileName,"*.csv"))

        self.listWidget.itemSelectionChanged.connect(self.next)
        self.btn_add_gite.clicked.connect(self.addParamKL)
        self.btn_delete_gite.clicked.connect(self.removeParamKL)

        self.btn_pathOutput.clicked.connect(self.selectOutputDir)
        self.btn_execute.clicked.connect(self.run_model)
        self.btn_cancel.clicked.connect(self.cancel)
        self.cancel = False

        menu = ["Fichiers d'entrées", "Paramètres KL", "Paramètres de sortie", "Lancer le modèle"]
        self.listWidget.addItems(menu)

        rows_gite_larvaires = ["Lieu","Surface des plans d'eau (m2)","Surface des rivières (m2)","Surface des cultures agricoles (m2)",
                                "Surface des rizières (m2)","Surface totale (m2)", "nombre de population (hab)"]
        col_gite_larvaires = ["Gîte larvaire"]
        self.table_gites.setColumnCount(len(col_gite_larvaires))
        self.table_gites.setRowCount(len(rows_gite_larvaires))
        self.table_gites.setHorizontalHeaderLabels(col_gite_larvaires)
        self.table_gites.setVerticalHeaderLabels(rows_gite_larvaires)

        columns = ["Précipitations", "Températures"]
        rows = ["Lieu", "Année","Type de données"]
        self.tableWidget.setColumnCount(len(columns))
        self.tableWidget.setRowCount(len(rows))
        self.tableWidget.setHorizontalHeaderLabels(columns)
        self.tableWidget.setVerticalHeaderLabels(rows)

        frequence_display = ["jours", "mois"]
        self.frequence.addItems(frequence_display)
        self.lastdate.toggled.connect(lambda:self.btnstate(self.lastdate))
        self.multidate.toggled.connect(lambda:self.btnstate(self.multidate))
        self.lastdate.setChecked(True)

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

    def getInputFiles(self):
        # # Parcelles
        filename =  ntpath.basename(self.parcelFileName.text()).split('.')[0]
        shp = gpd.read_file(self.parcelFileName.text()) # le shapefile avec les parcelles

        # Donnees meteo
        rainCSVData = pd.read_csv(self.rainFileName.text(),delimiter=";")# le fichier texte (csv) avec les donnees Meteo : pluies
        tempCSVData = pd.read_csv(self.tempFileName.text(),delimiter=";") # le fichier texte (csv) avec les donnees Meteo : temperatures

        return SEIRModel(filename,shp,rainCSVData,tempCSVData)

    def updateParamKLRow(self,row,items):
        field_name = QComboBox()
        field_name.addItems(items)
        self.table_gites.setCellWidget(row, 0, field_name)

    def addParamKL(self):
        rowPosition = self.table_gites.rowCount()
        self.table_gites.insertRow(rowPosition)
        self.updateParamKLRow(row,self.params.shp.columns)

        newHeader, ok = QInputDialog.getText(self,'Ajouter un gite larvaire','Nom du Gite:',)
        if ok:
            self.table_gites.setVerticalHeaderItem(rowPosition,QTableWidgetItem(newHeader))

    def removeParamKL(self):
        lastRow = self.table_gites.rowCount() - 1
        if lastRow > 5:
            self.table_gites.removeRow(lastRow)

    def getParamKL(self):
        paramKL = []
        for row in range (self.table_gites.rowCount()):
            paramKL.append(self.table_gites.cellWidget(row,0).currentText())
        return paramKL

    def updateParamMeteo(self,table,params):
        precip_fields = params.rainCSVData.columns
        temp_fields = params.tempCSVData.columns
        for row in range(table.rowCount()):
            for col in range (table.columnCount()):
                field_name = QComboBox()
                if row <= 1:
                    if col == 0:
                        field_name.addItems(precip_fields)
                    else:
                        field_name.addItems(temp_fields)
                else:
                    field_name.addItems(["journalier","hebdomadaire", "mensuel"])
                table.setCellWidget(row, col, field_name)

    def getParamMeteo(self):
        rainfall = []
        temperature = []
        for col in range(self.tableWidget.columnCount()):
            for row in range(self.tableWidget.rowCount()):
                value = self.tableWidget.cellWidget(row,col).currentText()
                if col == 0:
                    rainfall.append(value)
                else:
                    temperature.append(value)
        return rainfall, temperature

    def updateInputParams(self):
        self.textEdit.setText("SEIR Model ready to run")
        QtCore.QCoreApplication.processEvents()

        # 1) Instanciation des datafacers : inputs fichiers
        self.params = self.getInputFiles()
        msg = "Reading data ...\n"
        msg += "Found "+ str(self.params.shp.shape[0]) +" parcels\n"
        msg += "Size of rain data file: " + str(len(self.params.rainCSVData)) +"\n"
        msg += "Size of temperature data file: " + str(len(self.params.tempCSVData))
        self.textEdit.append(msg)

        # 2) Instanciation des datafacers : inputs paramètres KL
        for row in range(self.table_gites.rowCount()):
            self.updateParamKLRow(row,self.params.shp.columns)
        self.updateParamMeteo(self.tableWidget,self.params)

    def doubleParamError(self, rows):
        if len(rows) != len(set(rows)):
            return True

    def kl_table_error(self):
        # vérifier si les paramètres KL sont créés
        try:
            paramKL = self.getParamKL()
            rainfall, temperature = self.getParamMeteo()
        except:
            button = QMessageBox.information(
                self.centralwidget,
                "Erreur",
                "Remplir les paramètres KL",
                )
            self.updateInputParams()
            return True

        # si les paramètres KL sont crées, vérifier si les paramètres KL ne présentent pas des doublons
        if self.doubleParamError(rainfall) or self.doubleParamError(temperature) or self.doubleParamError(paramKL):
            button = QMessageBox.information(
                self.centralwidget,
                "Erreur",
                "Choisir des différents valeurs pour chaque colonne",
                )
            return True

        # si les paramètres KL ne présentent pas des doublons, mettre à jour les limites des dates de débuts et de fin de sorties
        # ******** Cas des données météos en hebdomadaire *********
        rainfall, temperature = self.getParamMeteo()
        temp_year_min = self.params.getDateMin(temperature[1])
        bdate_output_min = QtCore.QDate(temp_year_min,1,1)
        bdate_output_max = QtCore.QDate(temp_year_min,12,31)
        npop_max = self.params.shp[paramKL[6]].max(numeric_only=True)

        self.bdate_output.setMinimumDate(bdate_output_min)
        self.bdate_output.setMaximumDate(bdate_output_max)
        self.edate.setMinimumDate(bdate_output_min)
        self.edate.setMaximumDate(bdate_output_max)
        self.date_intro.setMinimumDate(QtCore.QDate(temp_year_min-1,1,1))
        self.date_intro.setMaximumDate(bdate_output_max)
        self.nb_pers_infectes.setMaximum(npop_max)

        return False

    def anyCheckedFormat(self):
        if self.outputSHP.isChecked() or self.outputKML.isChecked() or self.outputCSV.isChecked() :
            self.label_output_format.setStyleSheet("color: black")
            return False
        else:
            self.label_output_format.setStyleSheet("color: red")
            return True

    def anyCheckedItem(self):
        for checkbox in self.groupBox_col_export.findChildren(QCheckBox):
            if checkbox.isChecked():
                self.groupBox_col_export.setStyleSheet("QGroupBox:title {color: rgb(0, 0, 0);}")
                return False
        self.groupBox_col_export.setStyleSheet("QGroupBox:title {color: rgb(255, 0, 0);}")
        return True

    def EmptyLineEdit(self, input):
        if input.text():
            input.setStyleSheet("border: 1px solid white")
            return False
        else:
            input.setStyleSheet("border: 1px solid red")
            return True

    def emptyInputFile(self):
        if self.EmptyLineEdit(self.parcelFileName) or self.EmptyLineEdit(self.rainFileName) or self.EmptyLineEdit(self.tempFileName):
            button = QMessageBox.information(
                self.centralwidget,
                "Erreur",
                "Remplir les champs requis",
                )
            self.listWidget.setCurrentRow(0)
            return True
        else:
            return False

    def selectOutputDir(self):
        foldername = QFileDialog.getExistingDirectory(
            self.centralwidget,"Sélectionner le répertoire de sortie")
        if foldername:
            self.pathOutput.setText(foldername)
            self.pathOutput.setStyleSheet("border: 1px solid white")

    def btnstate(self,b):
      if b.text() == "Pour une date":
         if b.isChecked() :
            self.frequence_display.setEnabled(False)
            self.frequence.setEnabled(False)
            self.bdate_output.setEnabled(False)
         else:
            self.multidate.setChecked(True)

      if b.text() == "Pour une période":
         if b.isChecked() :
            self.frequence_display.setEnabled(True)
            self.frequence.setEnabled(True)
            self.bdate_output.setEnabled(True)
         else:
            self.lastdate.setChecked(True)

    def createOutputPath (self, format,filename):
        extension = self.edate.date().toString("yyyyMMdd") + format
        if self.lastdate.isChecked():
            filename += extension
        else:
            filename += self.bdate_output.date().toString("yyyyMMdd_") + extension
        return os.path.join(self.pathOutput.text(),filename)

    def getOutputParam(self,params):
        if self.outputSHP.isChecked():
            path = self.createOutputPath(".shp",params.filename)
            params.setShpExport(path)

        if self.outputCSV.isChecked():
            path = self.createOutputPath(".csv",params.filename)
            params.setCsvExport(path)

        if self.outputKML.isChecked():
            path = self.createOutputPath(".kml",params.filename)
            params.setKmlExport(path)

        if self.multidate.isChecked():
            days = 1
            if self.frequence.currentIndex() == 1 :
                days = 30
            frequence_display = self.frequence_display.value() * days
            params.setFrequence_display(frequence_display)
            params.setBDateOutput(self.bdate_output.date(),self.bdate_output.minimumDate().addYears(-1))
        else:
            params.setFrequence_display(7) # Par défaut la fréquence de sortie est tous les 7 jours
            # Si la sortie est pour une date alors commencer la date du début des sorties 7 avant la date de fin des sorties
            params.setBDateOutput(self.edate.date().addDays(-7), self.bdate_output.minimumDate().addYears(-1))

    def next(self):
        i = self.listWidget.currentRow()
        if i == 0:
            self.stackedWidget.setCurrentIndex(0)

        if i == 1:
            if not self.emptyInputFile():
                self.stackedWidget.setCurrentIndex(1)
                if not self.table_gites.cellWidget(0,0):
                    self.updateInputParams()

        if i == 2:
            if not self.emptyInputFile():
                if self.kl_table_error() :
                    self.listWidget.setCurrentRow(1)
                else:
                    self.stackedWidget.setCurrentIndex(2)

        if i == 3 :
            # vérifier si paramètres d'entrées sont remplis
            if not self.emptyInputFile():
                # vérifier si les paramètres ne représentent pas d'érreurs
                if self.kl_table_error():
                    self.listWidget.setCurrentRow(1)
                # vérifier si répertoire de sortie ou Format de sortie est vide
                elif self.EmptyLineEdit(self.pathOutput) or self.anyCheckedFormat() or self.anyCheckedItem():
                    self.listWidget.setCurrentRow(2)
                    button = QMessageBox.information(
                        self.centralwidget,
                        "Erreur",
                        "Remplir les champs requis",
                        )
                else:
                    self.stackedWidget.setCurrentIndex(3)
                    self.parcelFileName_2.setText(self.parcelFileName.text())
                    self.rainFileName_2.setText(self.rainFileName.text())
                    self.tempFileName_2.setText(self.tempFileName.text())
                    self.pathOutput_2.setText(self.pathOutput.text())
                    self.frequence_display_2.setValue(self.frequence_display.value())
                    self.frequence_2.setText(self.frequence.currentText())
                    self.bdate_output_2.setDate(self.bdate_output.date())
                    self.edate_2.setDate(self.edate.date())
                    output_format = ""
                    if self.outputSHP.isChecked() :
                        output_format = "".join([output_format,self.outputSHP.text(),";"])
                    if self.outputKML.isChecked() :
                        output_format = "".join([output_format,self.outputKML.text(),";"])
                    if self.outputCSV.isChecked() :
                        output_format = "".join([output_format,self.outputCSV.text(),";"])
                    self.output_format_2.setText(output_format)

    def getWeekNumber(self,w):
        if w < 10:
            return "s0" + str(w)
        elif w == 53:
            return "s52"
        else:
            return "s" + str(w)

    def cancel(self):
        self.cancel = True

    def run_model(self):
        reply = QMessageBox.question(
            self.centralwidget,
            "Question ...",
            "Voulez vous lancer le modèle",
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.textEdit.append("Initialization ... ")

            # 1) Instanciation des datafacers : outputs
            self.getOutputParam(self.params)

            # 2) Initialisation
            shp_list = gpd.GeoDataFrame()
            kml_list = gpd.GeoDataFrame()
            now = self.params.bdate
            day = 0
            self.textEdit.append("Simulation start: "+ now.toString("dd/MM/yyyy"))

            paramKL = self.getParamKL()
            paramMeteo = self.getParamMeteo()
            cas_infectes = {
             "date_intro": self.date_intro.date(), # date d'introduction d'un premier cas infecte humI
             "nb_pers": self.nb_pers_infectes.value(), # Nbre de personne initialement infecté
            }

            self.params.initialisation(paramKL)

            # 3) Simulation
            # # Boucle sur les jours
            while now <= self.edate.date() and not self.cancel:
                # Obtenir la semaine courante (exemple "S1")
                w = self.getWeekNumber(now.weekNumber()[0])
                # self.textEdit.append(now.toString("dd/MM/yyyy") + "; week " + w)
                QtCore.QCoreApplication.processEvents()

                # Obtenir la semaine précédent (exemple "S52")
                w7 = self.getWeekNumber(now.addDays(-7).weekNumber()[0])

                if now.daysTo(cas_infectes["date_intro"]) == 0:
                    self.textEdit.append("Introduction de "+ str(cas_infectes["nb_pers"]) + " cas de paludisme: " + now.toString("dd/MM/yyyy"))

                # Boucle sur les parcelles
                test_display = self.params.simulation(now,w,w7,day,paramKL,paramMeteo,cas_infectes)
                # Fin de la boucle sur les parcelles

                # Sauvegarde du résultat
                if now >= self.params.bdate_output and test_display == 0 :
                    if self.outputKML.isChecked() and self.multidate.isChecked():
                        kml_list = pd.concat([kml_list,self.params.shp],ignore_index = True)
                    if (self.outputSHP.isChecked() or self.outputCSV.isChecked()) and self.multidate.isChecked():
                        shp_list = pd.concat([shp_list,self.params.shp], ignore_index = True)

                day += 1
                now = now.addDays(1)
            # Fin de la boucle sur les jours

            # # 5) Export Result
            if not self.cancel:
                checked_columns = []
                for checkbox in self.groupBox_col_export.findChildren(QCheckBox):
                    if checkbox.isChecked():
                        checked_columns.append(checkbox.objectName())
                self.params.exportResult(shp_list,kml_list,self.multidate.isChecked(), checked_columns)
                self.textEdit.append("Simulation terminée !")
                button = QMessageBox.information(
                    self.centralwidget,
                    "Status",
                    "Simulation terminée !",
                    )
            else:
                self.textEdit.append("Simulation interrompue !")
                button = QMessageBox.information(
                    self.centralwidget,
                    "Status",
                    "Simulation interrompue !",
                    )
                self.cancel = False


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
