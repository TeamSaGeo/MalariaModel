# Form implementation generated from reading ui file '.\mainwindow.ui'
#
# Created by: PyQt6 UI code generator 6.5.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(678, 678)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_4.setHorizontalSpacing(60)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.logo_pmi = QtWidgets.QLabel(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.logo_pmi.sizePolicy().hasHeightForWidth())
        self.logo_pmi.setSizePolicy(sizePolicy)
        self.logo_pmi.setObjectName("logo_pmi")
        self.gridLayout_4.addWidget(self.logo_pmi, 0, 1, 1, 1)
        self.logo_ipm = QtWidgets.QLabel(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.logo_ipm.sizePolicy().hasHeightForWidth())
        self.logo_ipm.setSizePolicy(sizePolicy)
        self.logo_ipm.setScaledContents(False)
        self.logo_ipm.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.logo_ipm.setObjectName("logo_ipm")
        self.gridLayout_4.addWidget(self.logo_ipm, 0, 3, 1, 1)
        self.logo_app = QtWidgets.QLabel(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.logo_app.sizePolicy().hasHeightForWidth())
        self.logo_app.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        self.logo_app.setFont(font)
        self.logo_app.setAutoFillBackground(False)
        self.logo_app.setStyleSheet("background-color : white; border-radius: 10px;")
        self.logo_app.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.logo_app.setObjectName("logo_app")
        self.gridLayout_4.addWidget(self.logo_app, 1, 0, 1, 4)
        self.logo_usaid = QtWidgets.QLabel(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.logo_usaid.sizePolicy().hasHeightForWidth())
        self.logo_usaid.setSizePolicy(sizePolicy)
        self.logo_usaid.setAutoFillBackground(False)
        self.logo_usaid.setObjectName("logo_usaid")
        self.gridLayout_4.addWidget(self.logo_usaid, 0, 2, 1, 1)
        self.logo_minsan = QtWidgets.QLabel(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.logo_minsan.sizePolicy().hasHeightForWidth())
        self.logo_minsan.setSizePolicy(sizePolicy)
        self.logo_minsan.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        self.logo_minsan.setScaledContents(False)
        self.logo_minsan.setObjectName("logo_minsan")
        self.gridLayout_4.addWidget(self.logo_minsan, 0, 0, 1, 1)
        self.tabWidget = QtWidgets.QTabWidget(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_1 = QtWidgets.QWidget()
        self.tab_1.setObjectName("tab_1")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab_1)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.radioBtn_daily = QtWidgets.QRadioButton(parent=self.tab_1)
        font = QtGui.QFont()
        font.setBold(False)
        self.radioBtn_daily.setFont(font)
        self.radioBtn_daily.setChecked(True)
        self.radioBtn_daily.setObjectName("radioBtn_daily")
        self.gridLayout_2.addWidget(self.radioBtn_daily, 1, 1, 1, 1)
        self.btn_tempFileName = QtWidgets.QToolButton(parent=self.tab_1)
        self.btn_tempFileName.setObjectName("btn_tempFileName")
        self.gridLayout_2.addWidget(self.btn_tempFileName, 4, 5, 1, 1)
        self.radioBtn_monthly = QtWidgets.QRadioButton(parent=self.tab_1)
        font = QtGui.QFont()
        font.setBold(False)
        self.radioBtn_monthly.setFont(font)
        self.radioBtn_monthly.setObjectName("radioBtn_monthly")
        self.gridLayout_2.addWidget(self.radioBtn_monthly, 1, 3, 1, 1)
        self.btn_clear_input = QtWidgets.QPushButton(parent=self.tab_1)
        self.btn_clear_input.setObjectName("btn_clear_input")
        self.gridLayout_2.addWidget(self.btn_clear_input, 5, 2, 1, 1)
        self.label_parcelFileName = QtWidgets.QLabel(parent=self.tab_1)
        font = QtGui.QFont()
        font.setBold(False)
        self.label_parcelFileName.setFont(font)
        self.label_parcelFileName.setObjectName("label_parcelFileName")
        self.gridLayout_2.addWidget(self.label_parcelFileName, 0, 0, 1, 1)
        self.label_rainFileName = QtWidgets.QLabel(parent=self.tab_1)
        font = QtGui.QFont()
        font.setBold(False)
        self.label_rainFileName.setFont(font)
        self.label_rainFileName.setObjectName("label_rainFileName")
        self.gridLayout_2.addWidget(self.label_rainFileName, 3, 0, 1, 1)
        self.btn_rainFileName = QtWidgets.QToolButton(parent=self.tab_1)
        self.btn_rainFileName.setObjectName("btn_rainFileName")
        self.gridLayout_2.addWidget(self.btn_rainFileName, 3, 5, 1, 1)
        self.btn_load_input = QtWidgets.QPushButton(parent=self.tab_1)
        self.btn_load_input.setObjectName("btn_load_input")
        self.gridLayout_2.addWidget(self.btn_load_input, 5, 1, 1, 1)
        self.rainFileName = QtWidgets.QLineEdit(parent=self.tab_1)
        self.rainFileName.setEnabled(False)
        font = QtGui.QFont()
        font.setBold(False)
        self.rainFileName.setFont(font)
        self.rainFileName.setObjectName("rainFileName")
        self.gridLayout_2.addWidget(self.rainFileName, 3, 1, 1, 4)
        self.label_tempFileName = QtWidgets.QLabel(parent=self.tab_1)
        font = QtGui.QFont()
        font.setBold(False)
        self.label_tempFileName.setFont(font)
        self.label_tempFileName.setObjectName("label_tempFileName")
        self.gridLayout_2.addWidget(self.label_tempFileName, 4, 0, 1, 1)
        self.label_type_data = QtWidgets.QLabel(parent=self.tab_1)
        font = QtGui.QFont()
        font.setBold(False)
        self.label_type_data.setFont(font)
        self.label_type_data.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeading|QtCore.Qt.AlignmentFlag.AlignLeft|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_type_data.setObjectName("label_type_data")
        self.gridLayout_2.addWidget(self.label_type_data, 1, 0, 1, 1)
        self.btn_parcelFileName = QtWidgets.QToolButton(parent=self.tab_1)
        self.btn_parcelFileName.setObjectName("btn_parcelFileName")
        self.gridLayout_2.addWidget(self.btn_parcelFileName, 0, 5, 1, 1)
        self.tempFileName = QtWidgets.QLineEdit(parent=self.tab_1)
        self.tempFileName.setEnabled(False)
        font = QtGui.QFont()
        font.setBold(False)
        self.tempFileName.setFont(font)
        self.tempFileName.setObjectName("tempFileName")
        self.gridLayout_2.addWidget(self.tempFileName, 4, 1, 1, 4)
        self.parcelFileName = QtWidgets.QLineEdit(parent=self.tab_1)
        self.parcelFileName.setEnabled(False)
        font = QtGui.QFont()
        font.setBold(False)
        self.parcelFileName.setFont(font)
        self.parcelFileName.setObjectName("parcelFileName")
        self.gridLayout_2.addWidget(self.parcelFileName, 0, 1, 1, 4)
        self.radioBtn_weekly = QtWidgets.QRadioButton(parent=self.tab_1)
        font = QtGui.QFont()
        font.setBold(False)
        self.radioBtn_weekly.setFont(font)
        self.radioBtn_weekly.setObjectName("radioBtn_weekly")
        self.gridLayout_2.addWidget(self.radioBtn_weekly, 1, 2, 1, 1)
        self.groupBox_paramKL = QtWidgets.QGroupBox(parent=self.tab_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_paramKL.sizePolicy().hasHeightForWidth())
        self.groupBox_paramKL.setSizePolicy(sizePolicy)
        self.groupBox_paramKL.setTitle("")
        self.groupBox_paramKL.setObjectName("groupBox_paramKL")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_paramKL)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.table_gites = QtWidgets.QTableWidget(parent=self.groupBox_paramKL)
        self.table_gites.setEnabled(True)
        self.table_gites.setMinimumSize(QtCore.QSize(330, 240))
        self.table_gites.setMaximumSize(QtCore.QSize(16777215, 240))
        font = QtGui.QFont()
        font.setBold(False)
        self.table_gites.setFont(font)
        self.table_gites.setObjectName("table_gites")
        self.table_gites.setColumnCount(0)
        self.table_gites.setRowCount(0)
        self.gridLayout_3.addWidget(self.table_gites, 0, 0, 5, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 0, 1, 1, 1)
        self.table_meteo = QtWidgets.QTableWidget(parent=self.groupBox_paramKL)
        self.table_meteo.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.table_meteo.sizePolicy().hasHeightForWidth())
        self.table_meteo.setSizePolicy(sizePolicy)
        self.table_meteo.setMinimumSize(QtCore.QSize(270, 220))
        self.table_meteo.setMaximumSize(QtCore.QSize(16777215, 220))
        self.table_meteo.setRowCount(0)
        self.table_meteo.setColumnCount(0)
        self.table_meteo.setObjectName("table_meteo")
        self.gridLayout_3.addWidget(self.table_meteo, 0, 2, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox_paramKL, 6, 0, 1, 6)
        self.tabWidget.addTab(self.tab_1, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.groupBox_SEIR = QtWidgets.QGroupBox(parent=self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_SEIR.sizePolicy().hasHeightForWidth())
        self.groupBox_SEIR.setSizePolicy(sizePolicy)
        self.groupBox_SEIR.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setBold(True)
        self.groupBox_SEIR.setFont(font)
        self.groupBox_SEIR.setFlat(False)
        self.groupBox_SEIR.setObjectName("groupBox_SEIR")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.groupBox_SEIR)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.label_date_intro = QtWidgets.QLabel(parent=self.groupBox_SEIR)
        font = QtGui.QFont()
        font.setBold(False)
        self.label_date_intro.setFont(font)
        self.label_date_intro.setObjectName("label_date_intro")
        self.gridLayout_10.addWidget(self.label_date_intro, 1, 0, 1, 1)
        self.date_intro = QtWidgets.QDateEdit(parent=self.groupBox_SEIR)
        font = QtGui.QFont()
        font.setBold(False)
        self.date_intro.setFont(font)
        self.date_intro.setCalendarPopup(True)
        self.date_intro.setObjectName("date_intro")
        self.gridLayout_10.addWidget(self.date_intro, 1, 1, 1, 1)
        self.label_pers_infectes = QtWidgets.QLabel(parent=self.groupBox_SEIR)
        font = QtGui.QFont()
        font.setBold(False)
        self.label_pers_infectes.setFont(font)
        self.label_pers_infectes.setObjectName("label_pers_infectes")
        self.gridLayout_10.addWidget(self.label_pers_infectes, 0, 0, 1, 1)
        self.nb_pers_infectes = QtWidgets.QSpinBox(parent=self.groupBox_SEIR)
        font = QtGui.QFont()
        font.setBold(False)
        self.nb_pers_infectes.setFont(font)
        self.nb_pers_infectes.setMinimum(0)
        self.nb_pers_infectes.setObjectName("nb_pers_infectes")
        self.gridLayout_10.addWidget(self.nb_pers_infectes, 0, 1, 1, 1)
        self.gridLayout_5.addWidget(self.groupBox_SEIR, 1, 0, 1, 1)
        self.groupBox_lutte = QtWidgets.QGroupBox(parent=self.tab_2)
        font = QtGui.QFont()
        font.setBold(True)
        self.groupBox_lutte.setFont(font)
        self.groupBox_lutte.setObjectName("groupBox_lutte")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.groupBox_lutte)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.label_couv_irs = QtWidgets.QLabel(parent=self.groupBox_lutte)
        font = QtGui.QFont()
        font.setBold(False)
        self.label_couv_irs.setFont(font)
        self.label_couv_irs.setObjectName("label_couv_irs")
        self.gridLayout_6.addWidget(self.label_couv_irs, 6, 0, 1, 1)
        self.label_date_irs = QtWidgets.QLabel(parent=self.groupBox_lutte)
        font = QtGui.QFont()
        font.setBold(False)
        self.label_date_irs.setFont(font)
        self.label_date_irs.setObjectName("label_date_irs")
        self.gridLayout_6.addWidget(self.label_date_irs, 5, 0, 1, 1)
        self.couverture_moustiquaire = QtWidgets.QSpinBox(parent=self.groupBox_lutte)
        font = QtGui.QFont()
        font.setBold(False)
        self.couverture_moustiquaire.setFont(font)
        self.couverture_moustiquaire.setMaximum(100)
        self.couverture_moustiquaire.setObjectName("couverture_moustiquaire")
        self.gridLayout_6.addWidget(self.couverture_moustiquaire, 3, 1, 1, 1)
        self.date_moustiquaire = QtWidgets.QDateEdit(parent=self.groupBox_lutte)
        font = QtGui.QFont()
        font.setBold(False)
        self.date_moustiquaire.setFont(font)
        self.date_moustiquaire.setCalendarPopup(True)
        self.date_moustiquaire.setObjectName("date_moustiquaire")
        self.gridLayout_6.addWidget(self.date_moustiquaire, 0, 1, 1, 1)
        self.couverture_irs = QtWidgets.QSpinBox(parent=self.groupBox_lutte)
        font = QtGui.QFont()
        font.setBold(False)
        self.couverture_irs.setFont(font)
        self.couverture_irs.setMaximum(100)
        self.couverture_irs.setObjectName("couverture_irs")
        self.gridLayout_6.addWidget(self.couverture_irs, 6, 1, 1, 1)
        self.date_irs = QtWidgets.QDateEdit(parent=self.groupBox_lutte)
        font = QtGui.QFont()
        font.setBold(False)
        self.date_irs.setFont(font)
        self.date_irs.setCalendarPopup(True)
        self.date_irs.setObjectName("date_irs")
        self.gridLayout_6.addWidget(self.date_irs, 5, 1, 1, 1)
        self.label_couverture_moustiquaire = QtWidgets.QLabel(parent=self.groupBox_lutte)
        font = QtGui.QFont()
        font.setBold(False)
        self.label_couverture_moustiquaire.setFont(font)
        self.label_couverture_moustiquaire.setObjectName("label_couverture_moustiquaire")
        self.gridLayout_6.addWidget(self.label_couverture_moustiquaire, 3, 0, 1, 1)
        self.label_date_moustiquaire = QtWidgets.QLabel(parent=self.groupBox_lutte)
        font = QtGui.QFont()
        font.setBold(False)
        self.label_date_moustiquaire.setFont(font)
        self.label_date_moustiquaire.setObjectName("label_date_moustiquaire")
        self.gridLayout_6.addWidget(self.label_date_moustiquaire, 0, 0, 1, 1)
        self.line = QtWidgets.QFrame(parent=self.groupBox_lutte)
        self.line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_6.addWidget(self.line, 4, 0, 1, 2)
        self.gridLayout_5.addWidget(self.groupBox_lutte, 1, 1, 1, 1)
        self.groupBox_output = QtWidgets.QGroupBox(parent=self.tab_2)
        font = QtGui.QFont()
        font.setBold(True)
        self.groupBox_output.setFont(font)
        self.groupBox_output.setTitle("")
        self.groupBox_output.setObjectName("groupBox_output")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_output)
        self.gridLayout.setObjectName("gridLayout")
        self.outputKML = QtWidgets.QCheckBox(parent=self.groupBox_output)
        font = QtGui.QFont()
        font.setBold(False)
        self.outputKML.setFont(font)
        self.outputKML.setObjectName("outputKML")
        self.gridLayout.addWidget(self.outputKML, 6, 3, 1, 1)
        self.outputCSV = QtWidgets.QCheckBox(parent=self.groupBox_output)
        font = QtGui.QFont()
        font.setBold(False)
        self.outputCSV.setFont(font)
        self.outputCSV.setObjectName("outputCSV")
        self.gridLayout.addWidget(self.outputCSV, 6, 2, 1, 1)
        self.outputSHP = QtWidgets.QCheckBox(parent=self.groupBox_output)
        font = QtGui.QFont()
        font.setBold(False)
        self.outputSHP.setFont(font)
        self.outputSHP.setObjectName("outputSHP")
        self.gridLayout.addWidget(self.outputSHP, 6, 1, 1, 1)
        self.label_output_format = QtWidgets.QLabel(parent=self.groupBox_output)
        font = QtGui.QFont()
        font.setBold(False)
        self.label_output_format.setFont(font)
        self.label_output_format.setObjectName("label_output_format")
        self.gridLayout.addWidget(self.label_output_format, 6, 0, 1, 1)
        self.edate = QtWidgets.QDateEdit(parent=self.groupBox_output)
        self.edate.setEnabled(True)
        font = QtGui.QFont()
        font.setBold(False)
        self.edate.setFont(font)
        self.edate.setCalendarPopup(True)
        self.edate.setObjectName("edate")
        self.gridLayout.addWidget(self.edate, 5, 3, 1, 1)
        self.label_edate = QtWidgets.QLabel(parent=self.groupBox_output)
        font = QtGui.QFont()
        font.setBold(False)
        self.label_edate.setFont(font)
        self.label_edate.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_edate.setObjectName("label_edate")
        self.gridLayout.addWidget(self.label_edate, 5, 2, 1, 1)
        self.bdate_output = QtWidgets.QDateEdit(parent=self.groupBox_output)
        self.bdate_output.setEnabled(True)
        font = QtGui.QFont()
        font.setBold(False)
        self.bdate_output.setFont(font)
        self.bdate_output.setCalendarPopup(True)
        self.bdate_output.setObjectName("bdate_output")
        self.gridLayout.addWidget(self.bdate_output, 5, 1, 1, 1)
        self.label_bdate_output = QtWidgets.QLabel(parent=self.groupBox_output)
        font = QtGui.QFont()
        font.setBold(False)
        self.label_bdate_output.setFont(font)
        self.label_bdate_output.setObjectName("label_bdate_output")
        self.gridLayout.addWidget(self.label_bdate_output, 5, 0, 1, 1)
        self.frequence = QtWidgets.QComboBox(parent=self.groupBox_output)
        font = QtGui.QFont()
        font.setBold(False)
        self.frequence.setFont(font)
        self.frequence.setObjectName("frequence")
        self.gridLayout.addWidget(self.frequence, 4, 2, 1, 1)
        self.frequence_display = QtWidgets.QSpinBox(parent=self.groupBox_output)
        font = QtGui.QFont()
        font.setBold(False)
        self.frequence_display.setFont(font)
        self.frequence_display.setMinimum(1)
        self.frequence_display.setObjectName("frequence_display")
        self.gridLayout.addWidget(self.frequence_display, 4, 1, 1, 1)
        self.label_frequence_display = QtWidgets.QLabel(parent=self.groupBox_output)
        font = QtGui.QFont()
        font.setBold(False)
        self.label_frequence_display.setFont(font)
        self.label_frequence_display.setObjectName("label_frequence_display")
        self.gridLayout.addWidget(self.label_frequence_display, 4, 0, 1, 1)
        self.multidate = QtWidgets.QRadioButton(parent=self.groupBox_output)
        font = QtGui.QFont()
        font.setBold(False)
        self.multidate.setFont(font)
        self.multidate.setObjectName("multidate")
        self.gridLayout.addWidget(self.multidate, 2, 2, 1, 1)
        self.lastdate = QtWidgets.QRadioButton(parent=self.groupBox_output)
        font = QtGui.QFont()
        font.setBold(False)
        self.lastdate.setFont(font)
        self.lastdate.setObjectName("lastdate")
        self.gridLayout.addWidget(self.lastdate, 2, 1, 1, 1)
        self.label_result_type = QtWidgets.QLabel(parent=self.groupBox_output)
        font = QtGui.QFont()
        font.setBold(False)
        self.label_result_type.setFont(font)
        self.label_result_type.setObjectName("label_result_type")
        self.gridLayout.addWidget(self.label_result_type, 2, 0, 1, 1)
        self.btn_pathOutput = QtWidgets.QToolButton(parent=self.groupBox_output)
        self.btn_pathOutput.setObjectName("btn_pathOutput")
        self.gridLayout.addWidget(self.btn_pathOutput, 1, 5, 1, 1)
        self.pathOutput = QtWidgets.QLineEdit(parent=self.groupBox_output)
        self.pathOutput.setEnabled(False)
        font = QtGui.QFont()
        font.setBold(False)
        self.pathOutput.setFont(font)
        self.pathOutput.setObjectName("pathOutput")
        self.gridLayout.addWidget(self.pathOutput, 1, 1, 1, 3)
        self.label_pathOutput = QtWidgets.QLabel(parent=self.groupBox_output)
        font = QtGui.QFont()
        font.setBold(False)
        self.label_pathOutput.setFont(font)
        self.label_pathOutput.setObjectName("label_pathOutput")
        self.gridLayout.addWidget(self.label_pathOutput, 1, 0, 1, 1)
        self.gridLayout_5.addWidget(self.groupBox_output, 0, 0, 1, 2)
        self.groupBox_col_export = QtWidgets.QGroupBox(parent=self.tab_2)
        font = QtGui.QFont()
        font.setBold(True)
        self.groupBox_col_export.setFont(font)
        self.groupBox_col_export.setStyleSheet("")
        self.groupBox_col_export.setObjectName("groupBox_col_export")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.groupBox_col_export)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.humS = QtWidgets.QCheckBox(parent=self.groupBox_col_export)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        self.humS.setFont(font)
        self.humS.setObjectName("humS")
        self.gridLayout_9.addWidget(self.humS, 1, 2, 1, 1)
        self.nymphes = QtWidgets.QCheckBox(parent=self.groupBox_col_export)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        self.nymphes.setFont(font)
        self.nymphes.setObjectName("nymphes")
        self.gridLayout_9.addWidget(self.nymphes, 3, 0, 1, 1)
        self.a1o = QtWidgets.QCheckBox(parent=self.groupBox_col_export)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        self.a1o.setFont(font)
        self.a1o.setObjectName("a1o")
        self.gridLayout_9.addWidget(self.a1o, 3, 1, 1, 1)
        self.ah = QtWidgets.QCheckBox(parent=self.groupBox_col_export)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        self.ah.setFont(font)
        self.ah.setObjectName("ah")
        self.gridLayout_9.addWidget(self.ah, 4, 1, 1, 1)
        self.a2o = QtWidgets.QCheckBox(parent=self.groupBox_col_export)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        self.a2o.setFont(font)
        self.a2o.setObjectName("a2o")
        self.gridLayout_9.addWidget(self.a2o, 1, 1, 1, 1)
        self.adultestot = QtWidgets.QCheckBox(parent=self.groupBox_col_export)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        self.adultestot.setFont(font)
        self.adultestot.setObjectName("adultestot")
        self.gridLayout_9.addWidget(self.adultestot, 6, 0, 1, 1)
        self.ahI = QtWidgets.QCheckBox(parent=self.groupBox_col_export)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        self.ahI.setFont(font)
        self.ahI.setObjectName("ahI")
        self.gridLayout_9.addWidget(self.ahI, 7, 1, 1, 1)
        self.ahE = QtWidgets.QCheckBox(parent=self.groupBox_col_export)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        self.ahE.setFont(font)
        self.ahE.setObjectName("ahE")
        self.gridLayout_9.addWidget(self.ahE, 6, 1, 1, 1)
        self.fkl = QtWidgets.QCheckBox(parent=self.groupBox_col_export)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        self.fkl.setFont(font)
        self.fkl.setObjectName("fkl")
        self.gridLayout_9.addWidget(self.fkl, 9, 1, 1, 1)
        self.oeufs = QtWidgets.QCheckBox(parent=self.groupBox_col_export)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        self.oeufs.setFont(font)
        self.oeufs.setObjectName("oeufs")
        self.gridLayout_9.addWidget(self.oeufs, 1, 0, 1, 1)
        self.humR = QtWidgets.QCheckBox(parent=self.groupBox_col_export)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        self.humR.setFont(font)
        self.humR.setObjectName("humR")
        self.gridLayout_9.addWidget(self.humR, 6, 2, 1, 1)
        self.humI = QtWidgets.QCheckBox(parent=self.groupBox_col_export)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        self.humI.setFont(font)
        self.humI.setObjectName("humI")
        self.gridLayout_9.addWidget(self.humI, 4, 2, 1, 1)
        self.humE = QtWidgets.QCheckBox(parent=self.groupBox_col_export)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        self.humE.setFont(font)
        self.humE.setObjectName("humE")
        self.gridLayout_9.addWidget(self.humE, 3, 2, 1, 1)
        self.select_all = QtWidgets.QCheckBox(parent=self.groupBox_col_export)
        font = QtGui.QFont()
        font.setBold(False)
        self.select_all.setFont(font)
        self.select_all.setObjectName("select_all")
        self.gridLayout_9.addWidget(self.select_all, 0, 2, 1, 1)
        self.larves = QtWidgets.QCheckBox(parent=self.groupBox_col_export)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        self.larves.setFont(font)
        self.larves.setObjectName("larves")
        self.gridLayout_9.addWidget(self.larves, 4, 0, 1, 1)
        self.gridLayout_5.addWidget(self.groupBox_col_export, 3, 0, 1, 2)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayout_16 = QtWidgets.QGridLayout(self.tab_3)
        self.gridLayout_16.setObjectName("gridLayout_16")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_16.addItem(spacerItem1, 1, 0, 1, 1)
        self.btn_execute = QtWidgets.QPushButton(parent=self.tab_3)
        self.btn_execute.setMaximumSize(QtCore.QSize(100, 16777215))
        self.btn_execute.setObjectName("btn_execute")
        self.gridLayout_16.addWidget(self.btn_execute, 1, 1, 1, 1)
        self.btn_cancel = QtWidgets.QPushButton(parent=self.tab_3)
        self.btn_cancel.setMaximumSize(QtCore.QSize(100, 16777215))
        self.btn_cancel.setObjectName("btn_cancel")
        self.gridLayout_16.addWidget(self.btn_cancel, 1, 3, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_16.addItem(spacerItem2, 1, 4, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_16.addItem(spacerItem3, 1, 2, 1, 1)
        self.progressBar = QtWidgets.QProgressBar(parent=self.tab_3)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout_16.addWidget(self.progressBar, 2, 0, 1, 5)
        self.textEdit = QtWidgets.QTextEdit(parent=self.tab_3)
        self.textEdit.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)
        self.textEdit.setStyleSheet("background-color : white; color: black;")
        self.textEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout_16.addWidget(self.textEdit, 0, 0, 1, 5)
        icon = QtGui.QIcon.fromTheme("system-run")
        self.tabWidget.addTab(self.tab_3, icon, "")
        self.gridLayout_4.addWidget(self.tabWidget, 2, 0, 1, 4)
        MainWindow.setCentralWidget(self.centralwidget)
        self.actionBonjourjhhd = QtGui.QAction(parent=MainWindow)
        self.actionBonjourjhhd.setObjectName("actionBonjourjhhd")
        self.actionOuvrir = QtGui.QAction(parent=MainWindow)
        self.actionOuvrir.setObjectName("actionOuvrir")
        self.actionSauvegarder = QtGui.QAction(parent=MainWindow)
        self.actionSauvegarder.setObjectName("actionSauvegarder")
        self.actionQuitter = QtGui.QAction(parent=MainWindow)
        self.actionQuitter.setObjectName("actionQuitter")
        self.actionAide = QtGui.QAction(parent=MainWindow)
        self.actionAide.setObjectName("actionAide")

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ALARM Palu"))
        self.logo_pmi.setText(_translate("MainWindow", "logo_pmi"))
        self.logo_ipm.setText(_translate("MainWindow", "logo_ipm"))
        self.logo_app.setText(_translate("MainWindow", "<html>ALARM-Palu<br>ModélisAtion de la dynamique de popuLAtion des moustiques et du Risque de transMission du paludisme </html>"))
        self.logo_usaid.setText(_translate("MainWindow", "logo_usaid"))
        self.logo_minsan.setText(_translate("MainWindow", "logo_minsan"))
        self.radioBtn_daily.setText(_translate("MainWindow", "journalier"))
        self.btn_tempFileName.setText(_translate("MainWindow", "..."))
        self.radioBtn_monthly.setText(_translate("MainWindow", "mensuel"))
        self.btn_clear_input.setText(_translate("MainWindow", "Effacer"))
        self.label_parcelFileName.setText(_translate("MainWindow", "Fichier environnemental:"))
        self.label_rainFileName.setText(_translate("MainWindow", "Précipitations:"))
        self.btn_rainFileName.setText(_translate("MainWindow", "..."))
        self.btn_load_input.setText(_translate("MainWindow", "Charger"))
        self.label_tempFileName.setText(_translate("MainWindow", "Températures:"))
        self.label_type_data.setText(_translate("MainWindow", "Fréquence de données météo:"))
        self.btn_parcelFileName.setText(_translate("MainWindow", "..."))
        self.radioBtn_weekly.setText(_translate("MainWindow", "hebdomadaire"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), _translate("MainWindow", "Paramètres d\'entrée"))
        self.groupBox_SEIR.setTitle(_translate("MainWindow", "Cas infectés"))
        self.label_date_intro.setText(_translate("MainWindow", "Date d\'introduction des 1ers cas <br>infectés (jj/mm/aaaa)"))
        self.label_pers_infectes.setText(_translate("MainWindow", "Nombre de personnes<br> initalement infectées"))
        self.groupBox_lutte.setTitle(_translate("MainWindow", "Stratégie de lutte"))
        self.label_couv_irs.setText(_translate("MainWindow", "Taux de couverture (%)"))
        self.label_date_irs.setText(_translate("MainWindow", "Date d\'aspersion intra domiciliaire"))
        self.label_couverture_moustiquaire.setText(_translate("MainWindow", "Taux de couverture (%)"))
        self.label_date_moustiquaire.setText(_translate("MainWindow", "Date de distribution des moustiquaires"))
        self.outputKML.setText(_translate("MainWindow", "KML"))
        self.outputCSV.setText(_translate("MainWindow", "CSV"))
        self.outputSHP.setText(_translate("MainWindow", "Shapefile"))
        self.label_output_format.setText(_translate("MainWindow", "Format:"))
        self.label_edate.setText(_translate("MainWindow", "Date de fin:"))
        self.label_bdate_output.setText(_translate("MainWindow", "Date de début :"))
        self.label_frequence_display.setText(_translate("MainWindow", "Tous les "))
        self.multidate.setText(_translate("MainWindow", "Pour une période"))
        self.lastdate.setText(_translate("MainWindow", "Pour une date"))
        self.label_result_type.setText(_translate("MainWindow", "Résultats:"))
        self.btn_pathOutput.setText(_translate("MainWindow", "..."))
        self.label_pathOutput.setText(_translate("MainWindow", "Répertoire de sortie:"))
        self.groupBox_col_export.setTitle(_translate("MainWindow", "Eléments à exportés"))
        self.humS.setText(_translate("MainWindow", "humains susceptibles"))
        self.nymphes.setText(_translate("MainWindow", "nymphes"))
        self.a1o.setText(_translate("MainWindow", "adultes femelles nullipares en recherche de sites de ponte"))
        self.ah.setText(_translate("MainWindow", "adultes femelles nullipares et pares en recherche d\'hôtes"))
        self.a2o.setText(_translate("MainWindow", "adultes femelles pares en recherche de sites de ponte"))
        self.adultestot.setText(_translate("MainWindow", "moustiques adultes"))
        self.ahI.setText(_translate("MainWindow", "adultes femelles en recherche d\'hôtes infectés"))
        self.ahE.setText(_translate("MainWindow", "adultes femelles en recherche d\'hôtes exposés"))
        self.fkl.setText(_translate("MainWindow", "capacité de charge de l\'environnement larves et des nymphes"))
        self.oeufs.setText(_translate("MainWindow", "oeufs"))
        self.humR.setText(_translate("MainWindow", "humains rétablis"))
        self.humI.setText(_translate("MainWindow", "humains infectés"))
        self.humE.setText(_translate("MainWindow", "humains exposés"))
        self.select_all.setText(_translate("MainWindow", "Sélectionner tout"))
        self.larves.setText(_translate("MainWindow", "larves"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Paramètres de sortie"))
        self.btn_execute.setText(_translate("MainWindow", "Executer"))
        self.btn_cancel.setText(_translate("MainWindow", "Annuler"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Simulation"))
        self.actionBonjourjhhd.setText(_translate("MainWindow", "Bonjour jhhd feef fffffffffffffffxxxwdd"))
        self.actionOuvrir.setText(_translate("MainWindow", "Ouvrir"))
        self.actionSauvegarder.setText(_translate("MainWindow", "Sauvegarder"))
        self.actionQuitter.setText(_translate("MainWindow", "Quitter"))
        self.actionAide.setText(_translate("MainWindow", "Aide"))
