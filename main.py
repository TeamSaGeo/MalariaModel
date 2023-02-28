import sys
from PyQt6 import QtWidgets, uic
from mainwindow import Ui_MainWindow
from modelCoustani import ModelCoustani

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
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

    def selectOutputDir(self):
        foldername = QtWidgets.QFileDialog.getExistingDirectory(
            self.centralwidget,"Sélectionner le répertoire de sortie")
        if foldername:
            self.pathOutput.setText(foldername)

    def run(self):
        self.textEdit.setText("Model ModeleCoustani ready to run")
        model = ModelCoustani(self)

        model.readData()

        # 3) Lecture des donnees
        self.textEdit.append("Reading data ... ")
        # Parcelles
        # List of Parcels obtained from the Shapefile datafacer ShpParcelle
        self.textEdit.append("found "+ str(model.shp.shape[0]) +" parcels" )
        #
        # ## Donnees meteo
        self.textEdit.append("Size of rain data file: " + str(len(model.rainCSVData)))
        self.textEdit.append("Size of temperature data file: " + str(len(model.tempCSVData)))

        # # 4) Initialisation
        self.textEdit.append("Initialization ... ")

        #
        # # 5) Simulation
        self.textEdit.append("Simulation start: "+ self.bdate.date().toString("dd/MM/yyyy"))
        model.initialisation()
        self.textEdit.append("Simulation terminee !")

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
