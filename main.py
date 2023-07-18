import sys
from PyQt6 import uic, QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap
from mainwindow import Ui_MainWindow

from SEIRmodel import SEIRModel
import geopandas as gpd
import pandas as pd
import ntpath
import os
import resources
from pandas.api.types import is_numeric_dtype

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # On click on bouton select input file
        self.btn_parcelFileName.clicked.connect(lambda : self.selectInputFile(self.parcelFileName, "*.shp"))
        self.btn_rainFileName.clicked.connect(lambda : self.selectInputFile(self.rainFileName,"*.csv"))
        self.btn_tempFileName.clicked.connect(lambda : self.selectInputFile(self.tempFileName,"*.csv"))

        self.logo_minsan.setPixmap(QPixmap(":/images/logo_minsan"))
        self.logo_pmi.setPixmap(QPixmap(":/images/logo_pmi"))
        self.logo_usaid.setPixmap(QPixmap(":/images/logo_usaid"))
        self.logo_ipm.setPixmap(QPixmap(":/images/logo_ipm"))

        # on click on button "charger" et "effacer"
        self.btn_load_input.clicked.connect(self.loadInputFiles)
        self.btn_clear_input.clicked.connect(self.clearInputFiles)

        self.tabWidget.currentChanged.connect(self.next)

        self.btn_pathOutput.clicked.connect(self.selectOutputDir)
        self.btn_execute.clicked.connect(self.run_model)
        self.btn_cancel.clicked.connect(self.cancel)
        self.cancel = False

        rows_gite_larvaires = ["Lieu","Surface des plans d'eau (m2)","Surface des rivières (m2)","Surface des cultures agricoles (m2)",
                                "Surface des rizières (m2)","Surface totale (m2)", "nombre de population (hab)"]
        col_gite_larvaires = ["Gîte larvaire"]
        self.table_gites.setColumnCount(len(col_gite_larvaires))
        self.table_gites.setRowCount(len(rows_gite_larvaires))
        self.table_gites.setHorizontalHeaderLabels(col_gite_larvaires)
        self.table_gites.setVerticalHeaderLabels(rows_gite_larvaires)

        columns = ["Précipitations", "Températures"]
        rows = ["Lieu", "Année", "Mois", "Jour", "Valeur"]
        self.table_meteo.setColumnCount(len(columns))
        self.table_meteo.setRowCount(len(rows))
        self.table_meteo.setHorizontalHeaderLabels(columns)
        self.table_meteo.setVerticalHeaderLabels(rows)

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
                    "Message d'erreur",
                    "Choisir un fichier valide",
                    )

    def EmptyLineEdit(self, input):
        if input.text():
            input.setStyleSheet("border: 1px solid white")
            return False
        else:
            input.setStyleSheet("border: 1px solid red")
            return True

    def loadInputFiles(self):
        if self.EmptyLineEdit(self.parcelFileName) or self.EmptyLineEdit(self.rainFileName) or self.EmptyLineEdit(self.tempFileName):
            button = QMessageBox.information(
                self.centralwidget,
                "Message d'erreur",
                "Remplir les champs requis",
                )
        else:
            self.updateInputParams()

    def clearInputFiles(self):
        self.parcelFileName.setText("")
        self.rainFileName.setText("")
        self.tempFileName.setText("")
        self.updateParamKLRow([])
        self.updateParamMeteo([], [])

    def updateInputParams(self):
        # 1) Instanciation des datafacers : inputs fichiers
        # # Parcelles
        shp = gpd.read_file(self.parcelFileName.text()) # le shapefile avec les parcelles
        filename =  ntpath.basename(self.parcelFileName.text()).split('.')[0]
        # # Donnees meteo
        rainCSVData = pd.read_csv(self.rainFileName.text(),delimiter=";")# le fichier texte (csv) avec les donnees Meteo : pluies
        tempCSVData = pd.read_csv(self.tempFileName.text(),delimiter=";")# le fichier texte (csv) avec les donnees Meteo : temperatures

        self.inputParams = SEIRModel(filename,shp,rainCSVData,tempCSVData)

        # 2) Instanciation des datafacers : inputs paramètres KL
        self.updateParamKLRow(shp.columns)
        self.updateParamMeteo(rainCSVData.columns, tempCSVData.columns)

    def updateParamKLRow(self,items):
        for row in range(self.table_gites.rowCount()):
            field_name = QComboBox()
            field_name.addItems(items)
            self.table_gites.setCellWidget(row, 0, field_name)

    def updateParamMeteo(self,precip_fields,temp_fields):
        for row in range(self.table_meteo.rowCount()):
            for col in range (self.table_meteo.columnCount()):
                field_name = QComboBox()
                if row == 3 and (self.radioBtn_weekly.isChecked() or self.radioBtn_monthly.isChecked()):
                    field_name.setEnabled(False)
                elif col == 0:
                    field_name.addItems(precip_fields)
                else:
                    field_name.addItems(temp_fields)
                self.table_meteo.setCellWidget(row, col, field_name)

        if self.radioBtn_weekly.isChecked():
            self.table_meteo.verticalHeaderItem(2).setText("Semaine")
        else:
            self.table_meteo.verticalHeaderItem(2).setText("Mois")

    def getParamKL(self):
        paramKL = []
        for row in range (self.table_gites.rowCount()):
            paramKL.append(self.table_gites.cellWidget(row,0).currentText())
        return paramKL

    def getParamMeteo(self):
        rainfall = []
        temperature = []
        for col in range(self.table_meteo.columnCount()):
            for row in range(self.table_meteo.rowCount()):
                value = self.table_meteo.cellWidget(row,col).currentText()
                if col == 0:
                    rainfall.append(value)
                else:
                    temperature.append(value)
        return rainfall, temperature

    def doubleParamError(self, rows):
        if len(rows) != len(set(rows)):
            return True

    def notNumericParamKL(self, paramKL):
        for i, column in enumerate(paramKL):
            if not is_numeric_dtype(self.inputParams.shp[column]):
                button = QMessageBox.information(
                    self.centralwidget,
                    "Message d'erreur",
                    "Choisir une colonne de type numérique pour le champ " + self.table_gites.verticalHeaderItem(i+1).text(),
                    )
                return True

    def notNumericParamMeteo(self,paramMeteo,df):
        for i, column in enumerate(paramMeteo):
            if not column or (i == 1 and self.radioBtn_weekly.isChecked()):
                continue
            elif not is_numeric_dtype(df[column]):
                button = QMessageBox.information(
                    self.centralwidget,
                    "Message d'erreur",
                    "Choisir une colonne de type numérique pour le champ " + self.table_meteo.verticalHeaderItem(i+1).text(),
                    )
                return True

    def kl_table_error(self):
        # Obtenir les paramètres KL
        try:
            paramKL = self.getParamKL()
            rainfall, temperature = self.getParamMeteo()
        except:
            button = QMessageBox.information(
                self.centralwidget,
                "Message d'erreur",
                "Remplir les paramètres d'entrée",
                )
            return True

        # si les paramètres KL ne sont pas crées
        if not paramKL and not rainfall and not temperature:
            button = QMessageBox.information(
                self.centralwidget,
                "Message d'erreur",
                "Remplir les paramètres d'entrée",
                )
            return True

        # si les paramètres KL présentent des doublons
        if self.doubleParamError(rainfall) or self.doubleParamError(temperature) or self.doubleParamError(paramKL):
            button = QMessageBox.information(
                self.centralwidget,
                "Message d'erreur",
                "Choisir des différents valeurs pour chaque colonne des paramètres KL ou météo",
                )
            return True

        # si les paramètres KL sont de types non entiers
        if self.notNumericParamKL(paramKL[1:]) or self.notNumericParamMeteo(rainfall[1:], self.inputParams.rainCSVData) or self.notNumericParamMeteo(temperature[1:], self.inputParams.tempCSVData):
            return True

        # mettre à jour les limites des dates de débuts et de fin de sorties
        temp_year_min = self.inputParams.tempCSVData[temperature[1]].min() + 1 # L'année suivant l'année minimum
        temp_year_max = self.inputParams.tempCSVData[temperature[1]].max()
        bdate_output_min = QtCore.QDate(temp_year_min,1,1)
        bdate_output_max = QtCore.QDate(temp_year_max,12,31)
        self.bdate_output.setMinimumDate(bdate_output_min)
        self.bdate_output.setMaximumDate(bdate_output_max)
        self.edate.setMinimumDate(bdate_output_min)
        self.edate.setMaximumDate(bdate_output_max)
        self.date_intro.setMinimumDate(QtCore.QDate(temp_year_min-1,1,1))
        self.date_intro.setMaximumDate(bdate_output_max)

        npop_max = self.inputParams.shp[paramKL[6]].max(numeric_only=True)
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

    # def addParamKL(self):
    #     rowPosition = self.table_gites.rowCount()
    #     self.table_gites.insertRow(rowPosition)
    #     self.updateParamKLRow(row,self.inputParams.shp.columns)
    #
    #     newHeader, ok = QInputDialog.getText(self,'Ajouter un gite larvaire','Nom du Gite:',)
    #     if ok:
    #         self.table_gites.setVerticalHeaderItem(rowPosition,QTableWidgetItem(newHeader))
    #
    # def removeParamKL(self):
    #     lastRow = self.table_gites.rowCount() - 1
    #     if lastRow > 5:
    #         self.table_gites.removeRow(lastRow)













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

    def setOutputParam(self):
        if self.outputSHP.isChecked():
            path = self.createOutputPath(".shp",self.inputParams.filename)
            self.inputParams.setShpExport(path)

        if self.outputCSV.isChecked():
            path = self.createOutputPath(".csv",self.inputParams.filename)
            self.inputParams.setCsvExport(path)

        if self.outputKML.isChecked():
            path = self.createOutputPath(".kml",self.inputParams.filename)
            self.inputParams.setKmlExport(path)

        if self.multidate.isChecked():
            days = 1
            # si frequence de sortie est "tous les mois"
            if self.frequence.currentIndex() == 1 :
                days = 30
            frequence_display = self.frequence_display.value() * days
            self.inputParams.setFrequence_display(frequence_display)
            self.inputParams.setBDateOutput(self.bdate_output.date(),self.bdate_output.minimumDate().addYears(-1))
        else:
            self.inputParams.setFrequence_display(7) # Par défaut la fréquence de sortie est tous les 7 jours
            # Si la sortie est pour une date alors la date du début des sorties = 7 avant la date de fin des sorties
            self.inputParams.setBDateOutput(self.edate.date().addDays(-7), self.bdate_output.minimumDate().addYears(-1))

    def setTextEdit(self):
        msg = "Modèle SEIR prêt à démarrer\n"

        msg += "\n-----------Paramètres d'entrée-----------\n"
        msg += "Fichier environnemental source: "+ self.parcelFileName.text() +"\n"
        msg += "\tNombre de parcelles à traiter: "+ str(self.inputParams.shp.shape[0]) +"\n"
        msg += "Données de précipitations source: "+ self.rainFileName.text() +"\n"
        msg += "\tTaille des données de précipitations: " + str(len(self.inputParams.rainCSVData)) +" lignes\n"
        msg += "Données de températures source: "+ self.tempFileName.text() +"\n"
        msg += "\tTaille des données de températures: " + str(len(self.inputParams.tempCSVData)) +" lignes\n"

        msg += "\n-----------Paramètres de sortie-----------\n"
        msg += "Répertoire de sortie: "+ self.pathOutput.text() +"\n"
        msg += "Date de sortie: Tous les "+ str(self.frequence_display.value()) +" "+self.frequence.currentText()
        msg +=  "de " + self.bdate_output.date().toString("dd/MM/yyyy") + " à " + self.edate.date().toString("dd/MM/yyyy")+ "\n"

        output_format = ""
        if self.outputSHP.isChecked() :
            output_format = "".join([output_format,self.outputSHP.text(),";"])
        if self.outputKML.isChecked() :
            output_format = "".join([output_format,self.outputKML.text(),";"])
        if self.outputCSV.isChecked() :
            output_format = "".join([output_format,self.outputCSV.text(),";"])
        msg += "Format de sortie: " + output_format

        self.textEdit.setText(msg)
        # QtCore.QCoreApplication.processEvents()

    def next(self):
        i = self.tabWidget.currentIndex()

        if i == 1:
            if self.kl_table_error() :
                self.tabWidget.setCurrentIndex(0)

        if i == 2 :
            if self.kl_table_error() :
                self.tabWidget.setCurrentIndex(0)

            elif self.EmptyLineEdit(self.pathOutput) or self.anyCheckedFormat() or self.anyCheckedItem():
                self.tabWidget.setCurrentIndex(1)
                button = QMessageBox.information(
                    self.centralwidget,
                    "Message d'erreur",
                    "Remplir les paramètres de sortie réquis",
                    )
            else:
                self.setTextEdit()

    def cancel(self):
        self.cancel = True

    def run_model(self):
        reply = QMessageBox.question(
            self.centralwidget,
            "Lancement du modèle ...",
            "Voulez vous lancer le modèle?",
        )
        if reply == QMessageBox.StandardButton.Yes:
            # 1) Instanciation des datafacers : outputs
            self.setOutputParam()
            self.textEdit.append("Initialisation ... ")

            # 2) Initialisation
            shp_list = gpd.GeoDataFrame()
            kml_list = gpd.GeoDataFrame()
            now = self.inputParams.bdate
            day = 0
            self.textEdit.append("Simulation start: "+ now.toString("dd/MM/yyyy"))
            paramKL = self.getParamKL()
            paramMeteo = self.getParamMeteo()
            cas_infectes = {
             "date_intro": self.date_intro.date(), # date d'introduction d'un premier cas infecte humI
             "nb_pers": self.nb_pers_infectes.value(), # Nbre de personne initialement infecté
            }
            # # Initialisation des paramètres de résultats
            self.inputParams.initialisation(paramKL)

            # 3) Simulation
            # # Boucle sur les jours
            while now <= self.edate.date() and not self.cancel:
                if self.radioBtn_weekly.isChecked():
                    freq_meteo = "week"
                elif self.radioBtn_monthly.isChecked():
                    freq_meteo = "month"
                elif self.radioBtn_daily.isChecked():
                    freq_meteo = "day"

                if now.daysTo(cas_infectes["date_intro"]) == 0:
                    self.textEdit.append("Introduction de "+ str(cas_infectes["nb_pers"]) + " cas de paludisme: " + now.toString("dd/MM/yyyy"))

                # Boucle sur les parcelles
                test_display = self.inputParams.simulation(now,freq_meteo,day,paramKL,paramMeteo,cas_infectes)
                # Fin de la boucle sur les parcelles

                # Sauvegarde du résultat
                if now >= self.inputParams.bdate_output and test_display == 0 :
                    if self.outputKML.isChecked() and self.multidate.isChecked():
                        kml_list = pd.concat([kml_list,self.inputParams.shp],ignore_index = True)
                    if (self.outputSHP.isChecked() or self.outputCSV.isChecked()) and self.multidate.isChecked():
                        shp_list = pd.concat([shp_list,self.inputParams.shp], ignore_index = True)

                day += 1
                now = now.addDays(1)
            # Fin de la boucle sur les jours

            # # 5) Export Result
            if not self.cancel:
                # Obtenir les colonnes résultats choisit par l'utilisateur
                checked_columns = []
                for checkbox in self.groupBox_col_export.findChildren(QCheckBox):
                    if checkbox.isChecked():
                        checked_columns.append(checkbox.objectName())
                # exporter les résultats
                self.inputParams.exportResult(shp_list,kml_list,self.multidate.isChecked(), checked_columns)
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
