from PyQt6 import QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap, QIcon
import geopandas as gpd
import pandas as pd
import os, sys, ntpath
from mainwindow import Ui_MainWindow
from SEIRmodel import SEIRModel
import resources

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # action en cliquant sur le bouton ""..."" de sélection des fichiers d'entrée
        self.btn_parcelFileName.clicked.connect(lambda : self.selectInputFile(self.parcelFileName, "*.shp"))
        self.btn_rainFileName.clicked.connect(lambda : self.selectInputFile(self.rainFileName,"*.csv"))
        self.btn_tempFileName.clicked.connect(lambda : self.selectInputFile(self.tempFileName,"*.csv"))

        # Obtenir les logos
        self.logo_minsan.setPixmap(QPixmap(":/images/logo_minsan"))
        self.logo_pmi.setPixmap(QPixmap(":/images/logo_pmi"))
        self.logo_usaid.setPixmap(QPixmap(":/images/logo_usaid"))
        self.logo_ipm.setPixmap(QPixmap(":/images/logo_ipm"))
        self.setWindowIcon(QIcon(":/images/icon_model"))

        # action en cliquant sur le bouton "charger" et "effacer"
        self.btn_load_input.clicked.connect(self.loadInputFiles)
        self.btn_clear_input.clicked.connect(self.clearInputFiles)

        # action en basculant vers d'autres onglets
        self.tabWidget.currentChanged.connect(self.next)

        # action en cliquant sur le bouton "..." de sélection de la répertoire de sortie
        self.btn_pathOutput.clicked.connect(self.selectOutputDir)

        # action en cochant la case "Sélectionner tout"
        self.select_all.stateChanged.connect(self.selectAll)

        # action en cliquant sur le bouton "Excecuter" et "Annuler"
        self.btn_execute.clicked.connect(self.run_model)
        self.btn_cancel.clicked.connect(self.cancel)
        # self.cancel = False

        # Initialisation du tableau Paramètres KL
        rows_gite_larvaires = ["Lieu","Surface des plans d'eau (m2)","Surface des rivières (m2)","Surface des cultures agricoles (m2)",
                                "Surface des rizières (m2)","Surface totale (m2)", "nombre de population (hab)"]
        col_gite_larvaires = ["Gîte larvaire"]
        self.table_gites.setColumnCount(len(col_gite_larvaires))
        self.table_gites.setRowCount(len(rows_gite_larvaires))
        self.table_gites.setHorizontalHeaderLabels(col_gite_larvaires)
        self.table_gites.setVerticalHeaderLabels(rows_gite_larvaires)

        # Initialisation du tableau Paramètres Météo
        columns = ["Précipitations", "Températures"]
        rows = ["Lieu", "Année", "Mois", "Jour", "Valeur"]
        self.table_meteo.setColumnCount(len(columns))
        self.table_meteo.setRowCount(len(rows))
        self.table_meteo.setHorizontalHeaderLabels(columns)
        self.table_meteo.setVerticalHeaderLabels(rows)

        # Iintialsation des paramètres de sortie
        self.frequence.addItems(["jours", "mois"])
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
            if not pd.api.types.is_numeric_dtype(self.inputParams.shp[column]):
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
            elif not pd.api.types.is_numeric_dtype(df[column]):
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

        # Si la période de sortie est multidate
        if self.multidate.isChecked():
            # si frequence de sortie est "tous les mois", alors fréquence de sortie = nb *30 jours
            days = 1 if self.frequence.currentIndex() == 0 else 30
            self.inputParams.setFrequence_display( self.frequence_display.value() * days)
            self.inputParams.setBDateOutput(self.bdate_output.date(),self.bdate_output.minimumDate().addYears(-1))

        # Si la période de sortie est une date
        else:
            self.inputParams.setFrequence_display(7) # Par défaut la fréquence de sortie est tous les 7 jours
            # Mettre la date du début des sorties 7 avant la date de fin des sorties
            self.inputParams.setBDateOutput(self.edate.date().addDays(-7), self.bdate_output.minimumDate().addYears(-1))

    def setTextEdit(self):
        msg = "Modèle SEIR prêt à démarrer\n"

        msg += "\n-----------Paramètres d'entrée-----------\n"
        msg += "Fichier environnemental source: "+ self.parcelFileName.text() +"\n"
        msg += "Nombre de parcelles à traiter:\t"+ str(self.inputParams.shp.shape[0]) +"\n\n"
        msg += "Données de précipitations source: "+ self.rainFileName.text() +"\n"
        msg += "Taille des données de précipitations:\t" + str(len(self.inputParams.rainCSVData)) +" lignes\n\n"
        msg += "Données de températures source: "+ self.tempFileName.text() +"\n"
        msg += "Taille des données de températures:\t" + str(len(self.inputParams.tempCSVData)) +" lignes\n"

        msg += "\n-----------Paramètres de sortie-----------\n"
        msg += "Répertoire de sortie: "+ self.pathOutput.text() +"\n"
        msg += "Date de sortie:\tTous les "+ str(self.frequence_display.value()) +" "+self.frequence.currentText()
        msg +=  "\t du " + self.bdate_output.date().toString("dd/MM/yyyy") + " à " + self.edate.date().toString("dd/MM/yyyy")+ "\n"

        output_format = ""
        if self.outputSHP.isChecked() :
            output_format = "".join([output_format,self.outputSHP.text(),","])
        if self.outputKML.isChecked() :
            output_format = "".join([output_format,self.outputKML.text(),","])
        if self.outputCSV.isChecked() :
            output_format = "".join([output_format,self.outputCSV.text(),","])
        msg += "Format de sortie:\t" + output_format

        self.textEdit.setText(msg)

    def next(self):
        i = self.tabWidget.currentIndex()

        if i == 1:
            if self.kl_table_error() :
                self.tabWidget.setCurrentIndex(0)

        if i == 2 :
            self.bdate_output.setStyleSheet("border: 1px solid white")
            self.date_intro.setStyleSheet("border: 1px solid white")

            if self.kl_table_error() :
                self.tabWidget.setCurrentIndex(0)

            elif self.EmptyLineEdit(self.pathOutput) or self.anyCheckedFormat() or self.anyCheckedItem():
                self.tabWidget.setCurrentIndex(1)
                button = QMessageBox.information(
                    self.centralwidget,
                    "Message d'erreur",
                    "Remplir ce paramètre de sortie réquis",
                    )

            elif self.bdate_output.date() and self.bdate_output.date() >= self.edate.date() :
                self.tabWidget.setCurrentIndex(1)
                self.bdate_output.setStyleSheet("border: 1px solid red")
                button = QMessageBox.information(
                    self.centralwidget,
                    "Message d'erreur",
                    "La date du début de sortie devrait être ultérieure à la date de fin de sortie",
                    )

            elif self.nb_pers_infectes.value() != 0 and self.date_intro.date() > self.edate.date():
                self.date_intro.setStyleSheet("border: 1px solid red")
                self.tabWidget.setCurrentIndex(1)
                button = QMessageBox.information(
                    self.centralwidget,
                    "Message d'erreur",
                    "La date d'introduction des premiers cas infectés devrait être ultérieure à la date de fin de sortie",
                    )

            else:
                self.setTextEdit()

    def getValueToExport(self):
        checked_columns = []
        for checkbox in self.groupBox_col_export.findChildren(QCheckBox):
            if checkbox.isChecked() and checkbox != self.select_all:
                checked_columns.append(checkbox.objectName())
        return checked_columns

    def selectAll(self):
        state = self.select_all.checkState()
        for checkbox in self.groupBox_col_export.findChildren(QCheckBox):
            checkbox.setCheckState(state)

    def cancel(self):
        self.cancel = True
        self.btn_execute.setEnabled(True)

    def run_model(self):
        reply = QMessageBox.question(
            self.centralwidget,
            "Lancement de la simulation ...",
            "Voulez vous lancer la simulation?",
        )
        if reply == QMessageBox.StandardButton.Yes:
            # 1) Instanciation des datafacers : outputs
            self.setOutputParam()
            self.textEdit.append("\n-----------Lancement de la simulation-----------")

            # 2) Initialisation
            # # Initialisation des valeurs des dates et celle de la barre de progression
            now = self.inputParams.bdate
            day = progressBar_value = 0
            progressBar_step_value = 100 / now.daysTo(self.edate.date())
            ## Obtenir les paramètresKL, les paramètres météo, les cas infectés
            paramKL = self.getParamKL()
            paramMeteo = self.getParamMeteo()
            if self.radioBtn_weekly.isChecked():
                freq_meteo = "week"
            elif self.radioBtn_monthly.isChecked():
                freq_meteo = "month"
            elif self.radioBtn_daily.isChecked():
                freq_meteo = "day"
            cas_infectes = {
             "date_intro": self.date_intro.date(), # date d'introduction d'un premier cas infecte humI
             "nb_pers": self.nb_pers_infectes.value(), # Nbre de personne initialement infecté
            }
            # # Initialisation des paramètres de résultats
            self.inputParams.initialisation(paramKL)
            # # Création des dataframes de sauvegarde des résultats
            shp_list = gpd.GeoDataFrame()
            kml_list = gpd.GeoDataFrame()

            # 3) Simulation
            # # Boucle sur les jours
            self.btn_execute.setEnabled(False)
            self.cancel = False
            while now <= self.edate.date() and not self.cancel:
                if now.daysTo(cas_infectes["date_intro"]) == 0:
                    self.textEdit.append("Introduction de "+ str(cas_infectes["nb_pers"]) + " cas de paludisme: " + now.toString("dd/MM/yyyy"))

                # Boucle sur les parcelles
                test_display = self.inputParams.simulation(now,freq_meteo,day,paramKL,paramMeteo,cas_infectes)
                QtCore.QCoreApplication.processEvents()
                # Fin de la boucle sur les parcelles

                # Sauvegarde du résultat
                if now >= self.inputParams.bdate_output and test_display == 0 :
                    if self.outputKML.isChecked() and self.multidate.isChecked():
                        kml_list = pd.concat([kml_list,self.inputParams.shp],ignore_index = True)
                    if (self.outputSHP.isChecked() or self.outputCSV.isChecked()) and self.multidate.isChecked():
                        shp_list = pd.concat([shp_list,self.inputParams.shp], ignore_index = True)

                # Mise à jour de la valeur de day, now et de la barre de progression
                day += 1
                now = now.addDays(1)
                progressBar_value += progressBar_step_value
                self.progressBar.setValue(int(progressBar_value))
            # Fin de la boucle sur les jours

            if not self.cancel:
                # 4) Export Result
                self.textEdit.append("Export des résultats ...")

                # Obtenir les colonnes résultats choisit par l'utilisateur
                checked_columns = self.getValueToExport()
                try:
                    self.inputParams.exportResult(shp_list,kml_list,self.multidate.isChecked(), checked_columns)
                    self.textEdit.append("Simulation terminée!")
                    button = QMessageBox.information(
                        self.centralwidget,
                        "Status",
                        "Simulation terminée !",
                        )
                except PermissionError:
                    button = QMessageBox.information(
                        self.centralwidget,
                        "Status",
                        "Fichier d'export déjà ouvert! Veuillez fermer ce fichier CSV (ou SHP ou KML) puis recommencer la simulation!",
                        )
            else:
                self.textEdit.append("Simulation interrompue !")
                button = QMessageBox.information(
                    self.centralwidget,
                    "Status",
                    "Simulation interrompue !",
                    )
                self.cancel = False

            self.btn_execute.setEnabled(True)
            # Sauvegarde des textes dans un fichier log
            log_path = self.createOutputPath(".txt",self.inputParams.filename+"_log")
            with open(log_path,"w") as f:
                f.write(self.textEdit.toPlainText())

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
