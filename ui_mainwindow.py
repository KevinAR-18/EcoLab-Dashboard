# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ecolabWqPhDw.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QPlainTextEdit, QPushButton,
    QSizePolicy, QSpacerItem, QStackedWidget, QVBoxLayout,
    QWidget)
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1920, 1080)
        self.styleSheet = QWidget(MainWindow)
        self.styleSheet.setObjectName(u"styleSheet")
        self.styleSheet.setEnabled(True)
        self.styleSheet.setMinimumSize(QSize(1920, 1080))
        self.styleSheet.setMaximumSize(QSize(1920, 1080))
        self.styleSheet.setStyleSheet(u"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"SET APP STYLESHEET - FULL STYLES HERE\n"
"DARK BLUE THEME - DEEP BLUE PASTEL BASED\n"
"///////////////////////////////////////////////////////////////////////////////////////////////// */\n"
"\n"
"\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Style Label */\n"
"#labelRealStats {\n"
"    font: 12pt \"Segoe UI\";\n"
"    color: white; /* warna teks */\n"
"    background-color: #134686; /* warna latar belakang */\n"
"    border-radius: 8px; /* ujung melengkung */\n"
"    padding: 6px 10px; /* jarak teks dari tepi */\n"
"}\n"
"\n"
"\n"
"\n"
"QWidget{\n"
"	color: rgb(221, 221, 221);\n"
"	font: 10pt \"Segoe UI\";\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Tooltip */\n"
"QToolTip {\n"
"	color: #ffffff;\n"
"	background-color: rgba(0, 63, 125, 180);\n"
"	border: 1px solid "
                        "#005C99;\n"
"	background-image: none;\n"
"	background-position: left center;\n"
"	background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 2px solid #0091E5;\n"
"	text-align: left;\n"
"	padding-left: 8px;\n"
"	margin: 0px;\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Bg App */\n"
"#bgApp {	\n"
"	background-color: #002B5B;\n"
"	border: 1px solid #003F7D;\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Left Menu */\n"
"#leftMenuBg {	\n"
"	background-color: #003F7D;\n"
"}\n"
"#topLogo {\n"
"	background-color: #003F7D;\n"
"	background-image: url(:/images/images/images/logoecolab.png);\n"
"	background-position: centered;\n"
"	background-repeat: no-repeat;\n"
"}\n"
"#titleLeftApp { \n"
"    font:12pt \"Segoe UI Semibold\"; \n"
"    color: #FFFFFF; \n"
"}\n"
"#titleLeftDescription { \n"
"    font: 8pt \"Segoe UI\"; \n"
"    color: #77BEF0;\n"
"}\n"
"\n"
"\n"
"\n"
""
                        "/* MENUS */\n"
"#topMenu .QPushButton {	\n"
"	background-position: left center;\n"
"	background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 22px solid transparent;\n"
"	background-color: transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"	font-weight: 700;\n"
"}\n"
"#topMenu .QPushButton:hover {\n"
"	background-color: #005C99;\n"
"}\n"
"#topMenu .QPushButton:pressed {	\n"
"	background-color: #0091E5;\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"#bottomMenu .QPushButton {	\n"
"	background-position: left center;\n"
"	background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 20px solid transparent;\n"
"	background-color: transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"}\n"
"#bottomMenu .QPushButton:hover {\n"
"	background-color: #005C99;\n"
"}\n"
"#bottomMenu .QPushButton:pressed {	\n"
"	background-color: #0091E5;\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"#leftMenuFrame{\n"
"	border-top: 3px solid #0074CC;\n"
"}\n"
"\n"
"/* Toggle Button */\n"
"#toggleButton {\n"
""
                        "	background-position: left center;\n"
"	background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 20px solid transparent;\n"
"	background-color: #002B5B;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"	color: rgb(210, 230, 255);\n"
"	font-weight: 700;\n"
"}\n"
"#toggleButton:hover {\n"
"	background-color: #003F7D;\n"
"}\n"
"#toggleButton:pressed {\n"
"	background-color: #0074CC;\n"
"}\n"
"\n"
"/* Title Menu */\n"
"#titleRightInfo { padding-left: 10px; }\n"
"#titleRightInfo { \n"
"    font: 12pt \"Segoe UI\"; \n"
"    color: #FFFFFF;\n"
"	font-weight: 700;\n"
"}\n"
"\n"
"#clockInfo { \n"
"    font: 10pt \"Segoe UI\"; \n"
"    color: #FFFFFF;\n"
"\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Extra Tab */\n"
"#extraLeftBox {	\n"
"	background-color: #003F7D;\n"
"}\n"
"#extraTopBg{	\n"
"	background-color: #0091E5;\n"
"}\n"
"\n"
"/* Icon */\n"
"#extraIcon {\n"
"	background-position: center;\n"
"	background-repeat: no-repeat;\n"
""
                        "	background-image: url(:/icons/images/icons/icon_settings.png);\n"
"}\n"
"\n"
"/* Label */\n"
"#extraLabel { color: rgb(255, 255, 255); }\n"
"\n"
"/* Btn Close */\n"
"#extraCloseColumnBtn { background-color: rgba(255, 255, 255, 0); border: none;  border-radius: 5px; }\n"
"#extraCloseColumnBtn:hover { background-color: #005C99; border-style: solid; border-radius: 4px; }\n"
"#extraCloseColumnBtn:pressed { background-color: #0074CC; border-style: solid; border-radius: 4px; }\n"
"\n"
"/* Extra Content */\n"
"#extraContent{\n"
"	border-top: 3px solid #003F7D;\n"
"}\n"
"\n"
"/* Extra Top Menus */\n"
"#extraTopMenu .QPushButton {\n"
"	background-position: left center;\n"
"	background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 22px solid transparent;\n"
"	background-color: transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"}\n"
"#extraTopMenu .QPushButton:hover {\n"
"	background-color: #005C99;\n"
"}\n"
"#extraTopMenu .QPushButton:pressed {	\n"
"	background-color: #0091E5;\n"
"	color: rgb(25"
                        "5, 255, 255);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Content App */\n"
"#contentTopBg{	\n"
"	background-color: #002B5B;\n"
"}\n"
"\n"
"#contentBottom {\n"
"    border-top: 3px solid #005C99;\n"
"\n"
"    background: qlineargradient(\n"
"        x1:0, y1:0, x2:0, y2:1,\n"
"        stop:0 #E1F2FB,\n"
"        stop:1 #F1F9F9\n"
"    );\n"
"\n"
"    border-image: url(:/images/images/images/bg5.png) 0 0 0 0 stretch stretch;\n"
"}\n"
"\n"
"/* Top Buttons */\n"
"#rightButtons .QPushButton { background-color: rgba(255, 255, 255, 0); border: none;  border-radius: 5px; }\n"
"#rightButtons .QPushButton:hover { background-color: #003F7D; border-style: solid; border-radius: 4px; }\n"
"#rightButtons .QPushButton:pressed { background-color: #002B5B; border-style: solid; border-radius: 4px; }\n"
"\n"
"/* Theme Settings */\n"
"#extraRightBox { background-color: #003F7D; }\n"
"#themeSettingsTopDetail { background-color: #0091E5; }\n"
"\n"
"/* Botto"
                        "m Bar */\n"
"#bottomBar { background-color: #003F7D; }\n"
"#bottomBar QLabel { font-size: 11px; color: rgb(210, 230, 255); padding-left: 10px; padding-right: 10px; padding-bottom: 2px; }\n"
"\n"
"/* CONTENT SETTINGS */\n"
"/* MENUS */\n"
"#contentSettings .QPushButton {	\n"
"	background-position: left center;\n"
"	background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 22px solid transparent;\n"
"	background-color: transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"}\n"
"#contentSettings .QPushButton:hover {\n"
"	background-color: #005C99;\n"
"}\n"
"#contentSettings .QPushButton:pressed {	\n"
"	background-color: #0091E5;\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Button */\n"
"#pagesContainer QPushButton {\n"
"	border: 2px solid #005C99;\n"
"	border-radius: 5px;	\n"
"	background-color: #003F7D;\n"
"}\n"
"#pagesContainer QPushButton:hover {\n"
"	background-color: #005C99;\n"
"	bo"
                        "rder: 2px solid #0074CC;\n"
"}\n"
"#pagesContainer QPushButton:pressed {	\n"
"	background-color: #002B5B;\n"
"	border: 2px solid #003F7D;\n"
"}\n"
"\n"
"")
        self.verticalLayout_76 = QVBoxLayout(self.styleSheet)
        self.verticalLayout_76.setObjectName(u"verticalLayout_76")
        self.verticalLayout_76.setContentsMargins(-1, -1, 9, -1)
        self.bgApp = QFrame(self.styleSheet)
        self.bgApp.setObjectName(u"bgApp")
        self.bgApp.setFrameShape(QFrame.Shape.StyledPanel)
        self.bgApp.setFrameShadow(QFrame.Shadow.Raised)
        self.appLayout = QHBoxLayout(self.bgApp)
        self.appLayout.setSpacing(0)
        self.appLayout.setObjectName(u"appLayout")
        self.appLayout.setContentsMargins(0, 0, 0, 0)
        self.leftMenuBg = QFrame(self.bgApp)
        self.leftMenuBg.setObjectName(u"leftMenuBg")
        self.leftMenuBg.setMinimumSize(QSize(0, 0))
        self.leftMenuBg.setMaximumSize(QSize(60, 16777215))
        self.leftMenuBg.setFrameShape(QFrame.Shape.NoFrame)
        self.leftMenuBg.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.leftMenuBg)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.topLogoInfo = QFrame(self.leftMenuBg)
        self.topLogoInfo.setObjectName(u"topLogoInfo")
        self.topLogoInfo.setMinimumSize(QSize(0, 50))
        self.topLogoInfo.setMaximumSize(QSize(16777215, 50))
        self.topLogoInfo.setFrameShape(QFrame.Shape.NoFrame)
        self.topLogoInfo.setFrameShadow(QFrame.Shadow.Raised)
        self.topLogo = QFrame(self.topLogoInfo)
        self.topLogo.setObjectName(u"topLogo")
        self.topLogo.setGeometry(QRect(10, 5, 42, 42))
        self.topLogo.setMinimumSize(QSize(42, 42))
        self.topLogo.setMaximumSize(QSize(42, 42))
        self.topLogo.setFrameShape(QFrame.Shape.NoFrame)
        self.topLogo.setFrameShadow(QFrame.Shadow.Raised)
        self.titleLeftApp = QLabel(self.topLogoInfo)
        self.titleLeftApp.setObjectName(u"titleLeftApp")
        self.titleLeftApp.setGeometry(QRect(70, 8, 160, 20))
        font = QFont()
        font.setFamilies([u"Segoe UI Semibold"])
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        self.titleLeftApp.setFont(font)
        self.titleLeftApp.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.titleLeftDescription = QLabel(self.topLogoInfo)
        self.titleLeftDescription.setObjectName(u"titleLeftDescription")
        self.titleLeftDescription.setGeometry(QRect(70, 27, 160, 16))
        self.titleLeftDescription.setMaximumSize(QSize(16777215, 16))
        font1 = QFont()
        font1.setFamilies([u"Segoe UI"])
        font1.setPointSize(8)
        font1.setBold(False)
        font1.setItalic(False)
        self.titleLeftDescription.setFont(font1)
        self.titleLeftDescription.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)

        self.verticalLayout_5.addWidget(self.topLogoInfo)

        self.leftMenuFrame = QFrame(self.leftMenuBg)
        self.leftMenuFrame.setObjectName(u"leftMenuFrame")
        self.leftMenuFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.leftMenuFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalMenuLayout = QVBoxLayout(self.leftMenuFrame)
        self.verticalMenuLayout.setSpacing(0)
        self.verticalMenuLayout.setObjectName(u"verticalMenuLayout")
        self.verticalMenuLayout.setContentsMargins(0, 0, 0, 0)
        self.toggleBox = QFrame(self.leftMenuFrame)
        self.toggleBox.setObjectName(u"toggleBox")
        self.toggleBox.setMaximumSize(QSize(16777215, 45))
        self.toggleBox.setFrameShape(QFrame.Shape.NoFrame)
        self.toggleBox.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.toggleBox)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.toggleButton = QPushButton(self.toggleBox)
        self.toggleButton.setObjectName(u"toggleButton")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toggleButton.sizePolicy().hasHeightForWidth())
        self.toggleButton.setSizePolicy(sizePolicy)
        self.toggleButton.setMinimumSize(QSize(0, 45))
        self.toggleButton.setMaximumSize(QSize(16777215, 16777215))
        font2 = QFont()
        font2.setFamilies([u"Segoe UI"])
        font2.setPointSize(10)
        font2.setBold(True)
        font2.setItalic(False)
        self.toggleButton.setFont(font2)
        self.toggleButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.toggleButton.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.toggleButton.setStyleSheet(u"background-image: url(:/icons/images/icons/icon_menu.png);")

        self.verticalLayout_4.addWidget(self.toggleButton)


        self.verticalMenuLayout.addWidget(self.toggleBox)

        self.topMenu = QFrame(self.leftMenuFrame)
        self.topMenu.setObjectName(u"topMenu")
        self.topMenu.setFrameShape(QFrame.Shape.NoFrame)
        self.topMenu.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.topMenu)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.btn_growatt = QPushButton(self.topMenu)
        self.btn_growatt.setObjectName(u"btn_growatt")
        sizePolicy.setHeightForWidth(self.btn_growatt.sizePolicy().hasHeightForWidth())
        self.btn_growatt.setSizePolicy(sizePolicy)
        self.btn_growatt.setMinimumSize(QSize(0, 45))
        self.btn_growatt.setFont(font2)
        self.btn_growatt.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_growatt.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.btn_growatt.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-home.png);")

        self.verticalLayout_2.addWidget(self.btn_growatt)

        self.btn_controlroom = QPushButton(self.topMenu)
        self.btn_controlroom.setObjectName(u"btn_controlroom")
        sizePolicy.setHeightForWidth(self.btn_controlroom.sizePolicy().hasHeightForWidth())
        self.btn_controlroom.setSizePolicy(sizePolicy)
        self.btn_controlroom.setMinimumSize(QSize(0, 45))
        self.btn_controlroom.setFont(font2)
        self.btn_controlroom.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_controlroom.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.btn_controlroom.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-gamepad.png);")

        self.verticalLayout_2.addWidget(self.btn_controlroom)

        self.btn_monitoringsensor = QPushButton(self.topMenu)
        self.btn_monitoringsensor.setObjectName(u"btn_monitoringsensor")
        sizePolicy.setHeightForWidth(self.btn_monitoringsensor.sizePolicy().hasHeightForWidth())
        self.btn_monitoringsensor.setSizePolicy(sizePolicy)
        self.btn_monitoringsensor.setMinimumSize(QSize(0, 45))
        self.btn_monitoringsensor.setFont(font2)
        self.btn_monitoringsensor.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_monitoringsensor.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.btn_monitoringsensor.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-cloudy.png);")

        self.verticalLayout_2.addWidget(self.btn_monitoringsensor)

        self.btn_smartsocket = QPushButton(self.topMenu)
        self.btn_smartsocket.setObjectName(u"btn_smartsocket")
        sizePolicy.setHeightForWidth(self.btn_smartsocket.sizePolicy().hasHeightForWidth())
        self.btn_smartsocket.setSizePolicy(sizePolicy)
        self.btn_smartsocket.setMinimumSize(QSize(0, 45))
        self.btn_smartsocket.setFont(font2)
        self.btn_smartsocket.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_smartsocket.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.btn_smartsocket.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-input-power.png);")

        self.verticalLayout_2.addWidget(self.btn_smartsocket)

        self.btn_setting = QPushButton(self.topMenu)
        self.btn_setting.setObjectName(u"btn_setting")
        sizePolicy.setHeightForWidth(self.btn_setting.sizePolicy().hasHeightForWidth())
        self.btn_setting.setSizePolicy(sizePolicy)
        self.btn_setting.setMinimumSize(QSize(0, 45))
        self.btn_setting.setFont(font2)
        self.btn_setting.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_setting.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.btn_setting.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-settings.png);")

        self.verticalLayout_2.addWidget(self.btn_setting)

        self.btn_exit = QPushButton(self.topMenu)
        self.btn_exit.setObjectName(u"btn_exit")
        sizePolicy.setHeightForWidth(self.btn_exit.sizePolicy().hasHeightForWidth())
        self.btn_exit.setSizePolicy(sizePolicy)
        self.btn_exit.setMinimumSize(QSize(0, 45))
        self.btn_exit.setFont(font2)
        self.btn_exit.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_exit.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.btn_exit.setStyleSheet(u"background-image: url(:/icons/images/icons/cil-x.png);")

        self.verticalLayout_2.addWidget(self.btn_exit)


        self.verticalMenuLayout.addWidget(self.topMenu, 0, Qt.AlignmentFlag.AlignTop)


        self.verticalLayout_5.addWidget(self.leftMenuFrame)


        self.appLayout.addWidget(self.leftMenuBg)

        self.contentBox = QFrame(self.bgApp)
        self.contentBox.setObjectName(u"contentBox")
        self.contentBox.setFrameShape(QFrame.Shape.NoFrame)
        self.contentBox.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.contentBox)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.contentTopBg = QFrame(self.contentBox)
        self.contentTopBg.setObjectName(u"contentTopBg")
        self.contentTopBg.setMinimumSize(QSize(0, 50))
        self.contentTopBg.setMaximumSize(QSize(16777215, 50))
        self.contentTopBg.setFrameShape(QFrame.Shape.NoFrame)
        self.contentTopBg.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.contentTopBg)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 10, 0)
        self.leftBox = QFrame(self.contentTopBg)
        self.leftBox.setObjectName(u"leftBox")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.leftBox.sizePolicy().hasHeightForWidth())
        self.leftBox.setSizePolicy(sizePolicy1)
        self.leftBox.setFrameShape(QFrame.Shape.NoFrame)
        self.leftBox.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.leftBox)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.clockInfo = QLabel(self.leftBox)
        self.clockInfo.setObjectName(u"clockInfo")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.clockInfo.sizePolicy().hasHeightForWidth())
        self.clockInfo.setSizePolicy(sizePolicy2)
        self.clockInfo.setMaximumSize(QSize(16777215, 45))
        font3 = QFont()
        font3.setFamilies([u"Segoe UI"])
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setItalic(False)
        self.clockInfo.setFont(font3)
        self.clockInfo.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.clockInfo)

        self.titleRightInfo = QLabel(self.leftBox)
        self.titleRightInfo.setObjectName(u"titleRightInfo")
        sizePolicy2.setHeightForWidth(self.titleRightInfo.sizePolicy().hasHeightForWidth())
        self.titleRightInfo.setSizePolicy(sizePolicy2)
        self.titleRightInfo.setMaximumSize(QSize(16777215, 45))
        font4 = QFont()
        font4.setFamilies([u"Segoe UI"])
        font4.setPointSize(12)
        font4.setBold(True)
        font4.setItalic(False)
        self.titleRightInfo.setFont(font4)
        self.titleRightInfo.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.titleRightInfo)

        self.horizontalSpacer = QSpacerItem(80, 20, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.horizontalLayout.addWidget(self.leftBox)

        self.rightButtons = QFrame(self.contentTopBg)
        self.rightButtons.setObjectName(u"rightButtons")
        self.rightButtons.setMinimumSize(QSize(0, 28))
        self.rightButtons.setFrameShape(QFrame.Shape.NoFrame)
        self.rightButtons.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.rightButtons)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.minimizeAppBtn = QPushButton(self.rightButtons)
        self.minimizeAppBtn.setObjectName(u"minimizeAppBtn")
        self.minimizeAppBtn.setMinimumSize(QSize(28, 28))
        self.minimizeAppBtn.setMaximumSize(QSize(28, 28))
        self.minimizeAppBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon = QIcon()
        icon.addFile(u":/icons/images/icons/icon_minimize.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.minimizeAppBtn.setIcon(icon)
        self.minimizeAppBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.minimizeAppBtn)

        self.maximizeRestoreAppBtn = QPushButton(self.rightButtons)
        self.maximizeRestoreAppBtn.setObjectName(u"maximizeRestoreAppBtn")
        self.maximizeRestoreAppBtn.setMinimumSize(QSize(28, 28))
        self.maximizeRestoreAppBtn.setMaximumSize(QSize(28, 28))
        font5 = QFont()
        font5.setFamilies([u"Segoe UI"])
        font5.setPointSize(10)
        font5.setBold(False)
        font5.setItalic(False)
        font5.setStyleStrategy(QFont.PreferDefault)
        self.maximizeRestoreAppBtn.setFont(font5)
        self.maximizeRestoreAppBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon1 = QIcon()
        icon1.addFile(u":/icons/images/icons/icon_maximize.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.maximizeRestoreAppBtn.setIcon(icon1)
        self.maximizeRestoreAppBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.maximizeRestoreAppBtn)

        self.closeAppBtn = QPushButton(self.rightButtons)
        self.closeAppBtn.setObjectName(u"closeAppBtn")
        self.closeAppBtn.setMinimumSize(QSize(28, 28))
        self.closeAppBtn.setMaximumSize(QSize(28, 28))
        self.closeAppBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon2 = QIcon()
        icon2.addFile(u":/icons/images/icons/icon_close.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.closeAppBtn.setIcon(icon2)
        self.closeAppBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.closeAppBtn)


        self.horizontalLayout.addWidget(self.rightButtons, 0, Qt.AlignmentFlag.AlignRight)


        self.verticalLayout_3.addWidget(self.contentTopBg)

        self.contentBottom = QFrame(self.contentBox)
        self.contentBottom.setObjectName(u"contentBottom")
        self.contentBottom.setFrameShape(QFrame.Shape.NoFrame)
        self.contentBottom.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.contentBottom)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.content = QFrame(self.contentBottom)
        self.content.setObjectName(u"content")
        self.content.setFrameShape(QFrame.Shape.NoFrame)
        self.content.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.content)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.pagesContainer = QFrame(self.content)
        self.pagesContainer.setObjectName(u"pagesContainer")
        self.pagesContainer.setStyleSheet(u"")
        self.pagesContainer.setFrameShape(QFrame.Shape.NoFrame)
        self.pagesContainer.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_15 = QVBoxLayout(self.pagesContainer)
        self.verticalLayout_15.setSpacing(0)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(10, 0, 10, 10)
        self.stackedWidget = QStackedWidget(self.pagesContainer)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setStyleSheet(u"background: transparent;")
        self.page1_growattMonitoring = QWidget()
        self.page1_growattMonitoring.setObjectName(u"page1_growattMonitoring")
        self.horizontalLayout_7 = QHBoxLayout(self.page1_growattMonitoring)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.frameHomeGrowatt = QFrame(self.page1_growattMonitoring)
        self.frameHomeGrowatt.setObjectName(u"frameHomeGrowatt")
        self.frameHomeGrowatt.setMaximumSize(QSize(16777215, 65))
        self.frameHomeGrowatt.setFrameShape(QFrame.Shape.NoFrame)
        self.frameHomeGrowatt.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.frameHomeGrowatt)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, -1, 0)
        self.titleGrowattpage1 = QLabel(self.frameHomeGrowatt)
        self.titleGrowattpage1.setObjectName(u"titleGrowattpage1")
        sizePolicy2.setHeightForWidth(self.titleGrowattpage1.sizePolicy().hasHeightForWidth())
        self.titleGrowattpage1.setSizePolicy(sizePolicy2)
        self.titleGrowattpage1.setMaximumSize(QSize(422, 45))
        font6 = QFont()
        font6.setFamilies([u"Segoe UI"])
        font6.setPointSize(14)
        font6.setBold(True)
        font6.setItalic(False)
        self.titleGrowattpage1.setFont(font6)
        self.titleGrowattpage1.setStyleSheet(u"#titleGrowattpage1 {\n"
"    font: bold 14pt \"Segoe UI\";\n"
"    color: white;\n"
"    background-color: #5775dc;\n"
"    border-radius: 8px;\n"
"    padding: 6px 10px;\n"
"    border: 1px solid #5775dc;\n"
"    \n"
"    /* Tambahan pengaturan ukuran */\n"
"    min-width: 500px;    /* lebar minimum */\n"
"    max-width: 400px;    /* lebar maksimum */\n"
"    qproperty-alignment: AlignCenter; /* biar teks di tengah */\n"
"}\n"
"")
        self.titleGrowattpage1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_6.addWidget(self.titleGrowattpage1)


        self.verticalLayout_7.addWidget(self.frameHomeGrowatt)

        self.layoutpage1 = QHBoxLayout()
        self.layoutpage1.setObjectName(u"layoutpage1")
        self.livestatFrame = QFrame(self.page1_growattMonitoring)
        self.livestatFrame.setObjectName(u"livestatFrame")
        self.livestatFrame.setMinimumSize(QSize(0, 0))
        self.livestatFrame.setMaximumSize(QSize(16777215, 16777215))
        self.livestatFrame.setStyleSheet(u"/*#livestatFrame{*/\n"
"	/*background-color: #c6e1f7;        /* warna latar belakang (gelap elegan)  #c6e1f7 */\n"
"	/* border: 2px solid #cfe7fa;        ketebalan dan warna border */\n"
"	/*border-radius: 10px;               sudut melengkung */\n"
"/*}*/\n"
"")
        self.livestatFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.livestatFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.livestatFrame)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.frametitleFlow = QFrame(self.livestatFrame)
        self.frametitleFlow.setObjectName(u"frametitleFlow")
        self.frametitleFlow.setMaximumSize(QSize(16777215, 90))
        self.frametitleFlow.setFrameShape(QFrame.Shape.NoFrame)
        self.frametitleFlow.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.frametitleFlow)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.titleFlow = QLabel(self.frametitleFlow)
        self.titleFlow.setObjectName(u"titleFlow")
        sizePolicy2.setHeightForWidth(self.titleFlow.sizePolicy().hasHeightForWidth())
        self.titleFlow.setSizePolicy(sizePolicy2)
        self.titleFlow.setMaximumSize(QSize(422, 45))
        self.titleFlow.setFont(font6)
        self.titleFlow.setStyleSheet(u"#titleFlow{\n"
"    font: bold 14pt \"Segoe UI\";\n"
"    color: white;\n"
"    background-color: #33A1E0;\n"
"    border-radius: 8px;\n"
"    padding: 6px 10px;\n"
"    border: 1px solid #33A1E0;\n"
"    \n"
"    /* Tambahan pengaturan ukuran */\n"
"    min-width: 500px;    /* lebar minimum */\n"
"    max-width: 400px;    /* lebar maksimum */\n"
"    qproperty-alignment: AlignCenter; /* biar teks di tengah */\n"
"}\n"
"")
        self.titleFlow.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_8.addWidget(self.titleFlow)


        self.verticalLayout_8.addWidget(self.frametitleFlow)

        self.flowFrame = QFrame(self.livestatFrame)
        self.flowFrame.setObjectName(u"flowFrame")
        self.flowFrame.setMinimumSize(QSize(0, 0))
        self.flowFrame.setStyleSheet(u"#flowFrame{\n"
"	background-color: #def0ff;        /* warna latar belakang (gelap elegan)  #c6e1f7 */\n"
"	border: 2px solid #cfe7fa;        /* ketebalan dan warna border */\n"
"	border-radius: 10px;              /* sudut melengkung */\n"
"}\n"
"")
        self.flowFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.flowFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.flowFrame)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.unusedFrame3 = QFrame(self.flowFrame)
        self.unusedFrame3.setObjectName(u"unusedFrame3")
        self.unusedFrame3.setMinimumSize(QSize(0, 0))
        self.unusedFrame3.setMaximumSize(QSize(1, 1))
        self.unusedFrame3.setFrameShape(QFrame.Shape.NoFrame)
        self.unusedFrame3.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_9.addWidget(self.unusedFrame3)

        self.unusedFrame1 = QFrame(self.flowFrame)
        self.unusedFrame1.setObjectName(u"unusedFrame1")
        self.unusedFrame1.setMinimumSize(QSize(0, 0))
        self.unusedFrame1.setFrameShape(QFrame.Shape.NoFrame)
        self.unusedFrame1.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_9.addWidget(self.unusedFrame1)

        self.frametopFlow = QFrame(self.flowFrame)
        self.frametopFlow.setObjectName(u"frametopFlow")
        self.frametopFlow.setMinimumSize(QSize(0, 150))
        self.frametopFlow.setMaximumSize(QSize(250, 150))
        self.frametopFlow.setStyleSheet(u"\n"
"#frametopFlow{\n"
"	background-color: #f8fbff;\n"
"	border: 1px solid #cddff3;\n"
"	border-radius: 8px;\n"
"	}\n"
"")
        self.frametopFlow.setFrameShape(QFrame.Shape.NoFrame)
        self.frametopFlow.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_10 = QVBoxLayout(self.frametopFlow)
        self.verticalLayout_10.setSpacing(0)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(0, 5, 0, 5)
        self.frame_36 = QFrame(self.frametopFlow)
        self.frame_36.setObjectName(u"frame_36")
        self.frame_36.setMinimumSize(QSize(0, 0))
        self.frame_36.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_36.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_14 = QHBoxLayout(self.frame_36)
        self.horizontalLayout_14.setSpacing(0)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.cur_panelFrame = QFrame(self.frame_36)
        self.cur_panelFrame.setObjectName(u"cur_panelFrame")
        self.cur_panelFrame.setMinimumSize(QSize(80, 80))
        self.cur_panelFrame.setMaximumSize(QSize(80, 80))
        self.cur_panelFrame.setStyleSheet(u"border-image: url(:/images/images/images/035-solar-panel.png) 0 0 0 0 round round;\n"
"")
        self.cur_panelFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.cur_panelFrame.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_14.addWidget(self.cur_panelFrame)


        self.verticalLayout_10.addWidget(self.frame_36)

        self.currentpvpower_value = QLabel(self.frametopFlow)
        self.currentpvpower_value.setObjectName(u"currentpvpower_value")
        sizePolicy2.setHeightForWidth(self.currentpvpower_value.sizePolicy().hasHeightForWidth())
        self.currentpvpower_value.setSizePolicy(sizePolicy2)
        self.currentpvpower_value.setMaximumSize(QSize(422, 45))
        self.currentpvpower_value.setFont(font4)
        self.currentpvpower_value.setStyleSheet(u"    font: bold 12pt \"Segoe UI\";\n"
"    color: Black;\n"
"\n"
"")
        self.currentpvpower_value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_10.addWidget(self.currentpvpower_value)


        self.horizontalLayout_9.addWidget(self.frametopFlow)

        self.unusedFrame2 = QFrame(self.flowFrame)
        self.unusedFrame2.setObjectName(u"unusedFrame2")
        self.unusedFrame2.setMinimumSize(QSize(0, 0))
        self.unusedFrame2.setFrameShape(QFrame.Shape.NoFrame)
        self.unusedFrame2.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_9.addWidget(self.unusedFrame2)

        self.unusedFrame4 = QFrame(self.flowFrame)
        self.unusedFrame4.setObjectName(u"unusedFrame4")
        self.unusedFrame4.setMinimumSize(QSize(0, 0))
        self.unusedFrame4.setMaximumSize(QSize(1, 1))
        self.unusedFrame4.setFrameShape(QFrame.Shape.StyledPanel)
        self.unusedFrame4.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_9.addWidget(self.unusedFrame4)


        self.verticalLayout_9.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.unusedFrame5 = QFrame(self.flowFrame)
        self.unusedFrame5.setObjectName(u"unusedFrame5")
        self.unusedFrame5.setMinimumSize(QSize(0, 0))
        self.unusedFrame5.setFrameShape(QFrame.Shape.NoFrame)
        self.unusedFrame5.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_10.addWidget(self.unusedFrame5)

        self.unusedFrame6 = QFrame(self.flowFrame)
        self.unusedFrame6.setObjectName(u"unusedFrame6")
        self.unusedFrame6.setMinimumSize(QSize(0, 0))
        self.unusedFrame6.setFrameShape(QFrame.Shape.NoFrame)
        self.unusedFrame6.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_10.addWidget(self.unusedFrame6)

        self.downArrowFrame = QFrame(self.flowFrame)
        self.downArrowFrame.setObjectName(u"downArrowFrame")
        self.downArrowFrame.setMinimumSize(QSize(40, 100))
        self.downArrowFrame.setMaximumSize(QSize(40, 100))
        self.downArrowFrame.setStyleSheet(u"")
        self.downArrowFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.downArrowFrame.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_10.addWidget(self.downArrowFrame)

        self.unusedFrame7 = QFrame(self.flowFrame)
        self.unusedFrame7.setObjectName(u"unusedFrame7")
        self.unusedFrame7.setMinimumSize(QSize(0, 0))
        self.unusedFrame7.setFrameShape(QFrame.Shape.NoFrame)
        self.unusedFrame7.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_10.addWidget(self.unusedFrame7)

        self.unusedFrame8 = QFrame(self.flowFrame)
        self.unusedFrame8.setObjectName(u"unusedFrame8")
        self.unusedFrame8.setMinimumSize(QSize(0, 0))
        self.unusedFrame8.setFrameShape(QFrame.Shape.NoFrame)
        self.unusedFrame8.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_10.addWidget(self.unusedFrame8)


        self.verticalLayout_9.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.frameleftFlow = QFrame(self.flowFrame)
        self.frameleftFlow.setObjectName(u"frameleftFlow")
        self.frameleftFlow.setMinimumSize(QSize(190, 135))
        self.frameleftFlow.setMaximumSize(QSize(230, 135))
        self.frameleftFlow.setStyleSheet(u"\n"
"#frameleftFlow{\n"
"	background-color: #f8fbff;\n"
"	border: 1px solid #cddff3;\n"
"	border-radius: 8px;\n"
"	}\n"
"")
        self.frameleftFlow.setFrameShape(QFrame.Shape.NoFrame)
        self.frameleftFlow.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_12 = QVBoxLayout(self.frameleftFlow)
        self.verticalLayout_12.setSpacing(0)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(0, 5, 0, -1)
        self.frame_46 = QFrame(self.frameleftFlow)
        self.frame_46.setObjectName(u"frame_46")
        self.frame_46.setMinimumSize(QSize(0, 0))
        self.frame_46.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_46.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_31 = QHBoxLayout(self.frame_46)
        self.horizontalLayout_31.setSpacing(0)
        self.horizontalLayout_31.setObjectName(u"horizontalLayout_31")
        self.horizontalLayout_31.setContentsMargins(0, 0, 0, 0)
        self.cur_importgridFrame = QFrame(self.frame_46)
        self.cur_importgridFrame.setObjectName(u"cur_importgridFrame")
        self.cur_importgridFrame.setMinimumSize(QSize(80, 80))
        self.cur_importgridFrame.setMaximumSize(QSize(80, 80))
        self.cur_importgridFrame.setStyleSheet(u"border-image: url(:/images/images/images/024-electric-tower.png) 0 0 0 0 round round;\n"
"")
        self.cur_importgridFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.cur_importgridFrame.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_31.addWidget(self.cur_importgridFrame)


        self.verticalLayout_12.addWidget(self.frame_46)

        self.labeltextImportGrid = QLabel(self.frameleftFlow)
        self.labeltextImportGrid.setObjectName(u"labeltextImportGrid")
        sizePolicy2.setHeightForWidth(self.labeltextImportGrid.sizePolicy().hasHeightForWidth())
        self.labeltextImportGrid.setSizePolicy(sizePolicy2)
        self.labeltextImportGrid.setMaximumSize(QSize(422, 45))
        self.labeltextImportGrid.setFont(font4)
        self.labeltextImportGrid.setStyleSheet(u"    font: bold 12pt \"Segoe UI\";\n"
"    color: Black;\n"
"\n"
"")
        self.labeltextImportGrid.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_12.addWidget(self.labeltextImportGrid)

        self.currentimportgrid_value = QLabel(self.frameleftFlow)
        self.currentimportgrid_value.setObjectName(u"currentimportgrid_value")
        sizePolicy2.setHeightForWidth(self.currentimportgrid_value.sizePolicy().hasHeightForWidth())
        self.currentimportgrid_value.setSizePolicy(sizePolicy2)
        self.currentimportgrid_value.setMaximumSize(QSize(422, 45))
        self.currentimportgrid_value.setFont(font4)
        self.currentimportgrid_value.setStyleSheet(u"    font: bold 12pt \"Segoe UI\";\n"
"    color: Black;\n"
"\n"
"")
        self.currentimportgrid_value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_12.addWidget(self.currentimportgrid_value)


        self.horizontalLayout_11.addWidget(self.frameleftFlow)

        self.rightArrowFrame = QFrame(self.flowFrame)
        self.rightArrowFrame.setObjectName(u"rightArrowFrame")
        self.rightArrowFrame.setMinimumSize(QSize(100, 40))
        self.rightArrowFrame.setMaximumSize(QSize(100, 40))
        self.rightArrowFrame.setStyleSheet(u"")
        self.rightArrowFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.rightArrowFrame.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_11.addWidget(self.rightArrowFrame)

        self.frameGrowatt = QFrame(self.flowFrame)
        self.frameGrowatt.setObjectName(u"frameGrowatt")
        self.frameGrowatt.setMinimumSize(QSize(80, 80))
        self.frameGrowatt.setMaximumSize(QSize(80, 80))
        self.frameGrowatt.setStyleSheet(u"	border: 1px solid #cddff3;\n"
"	border-radius: 8px;\n"
"	 border-image: url(:/images/images/images/growatt.png) 0 0 0 0 stretch stretch;")
        self.frameGrowatt.setFrameShape(QFrame.Shape.NoFrame)
        self.frameGrowatt.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_11.addWidget(self.frameGrowatt)

        self.leftArrowFrame = QFrame(self.flowFrame)
        self.leftArrowFrame.setObjectName(u"leftArrowFrame")
        self.leftArrowFrame.setMinimumSize(QSize(100, 40))
        self.leftArrowFrame.setMaximumSize(QSize(100, 40))
        self.leftArrowFrame.setStyleSheet(u"")
        self.leftArrowFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.leftArrowFrame.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_11.addWidget(self.leftArrowFrame)

        self.framerightFlow = QFrame(self.flowFrame)
        self.framerightFlow.setObjectName(u"framerightFlow")
        self.framerightFlow.setMinimumSize(QSize(190, 135))
        self.framerightFlow.setMaximumSize(QSize(230, 135))
        self.framerightFlow.setStyleSheet(u"\n"
"#framerightFlow{\n"
"	background-color: #f8fbff;\n"
"	border: 1px solid #cddff3;\n"
"	border-radius: 8px;\n"
"	}\n"
"")
        self.framerightFlow.setFrameShape(QFrame.Shape.NoFrame)
        self.framerightFlow.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_11 = QVBoxLayout(self.framerightFlow)
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(0, 5, 0, 5)
        self.frame_39 = QFrame(self.framerightFlow)
        self.frame_39.setObjectName(u"frame_39")
        self.frame_39.setMinimumSize(QSize(0, 0))
        self.frame_39.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_39.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_19 = QHBoxLayout(self.frame_39)
        self.horizontalLayout_19.setSpacing(0)
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.horizontalLayout_19.setContentsMargins(0, 0, 0, 0)
        self.cur_consumpFrame = QFrame(self.frame_39)
        self.cur_consumpFrame.setObjectName(u"cur_consumpFrame")
        self.cur_consumpFrame.setMinimumSize(QSize(80, 80))
        self.cur_consumpFrame.setMaximumSize(QSize(80, 80))
        self.cur_consumpFrame.setStyleSheet(u"border-image: url(:/images/images/images/036-greenhouse.png) 0 0 0 0 round round;\n"
"")
        self.cur_consumpFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.cur_consumpFrame.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_19.addWidget(self.cur_consumpFrame)


        self.verticalLayout_11.addWidget(self.frame_39)

        self.labeltextConsumptionPower = QLabel(self.framerightFlow)
        self.labeltextConsumptionPower.setObjectName(u"labeltextConsumptionPower")
        sizePolicy2.setHeightForWidth(self.labeltextConsumptionPower.sizePolicy().hasHeightForWidth())
        self.labeltextConsumptionPower.setSizePolicy(sizePolicy2)
        self.labeltextConsumptionPower.setMaximumSize(QSize(422, 45))
        self.labeltextConsumptionPower.setFont(font4)
        self.labeltextConsumptionPower.setStyleSheet(u"    font: bold 12pt \"Segoe UI\";\n"
"    color: Black;\n"
"\n"
"")
        self.labeltextConsumptionPower.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_11.addWidget(self.labeltextConsumptionPower)

        self.currentconsumppower_value = QLabel(self.framerightFlow)
        self.currentconsumppower_value.setObjectName(u"currentconsumppower_value")
        sizePolicy2.setHeightForWidth(self.currentconsumppower_value.sizePolicy().hasHeightForWidth())
        self.currentconsumppower_value.setSizePolicy(sizePolicy2)
        self.currentconsumppower_value.setMaximumSize(QSize(422, 45))
        self.currentconsumppower_value.setFont(font4)
        self.currentconsumppower_value.setStyleSheet(u"    font: bold 12pt \"Segoe UI\";\n"
"    color: Black;\n"
"\n"
"")
        self.currentconsumppower_value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_11.addWidget(self.currentconsumppower_value)


        self.horizontalLayout_11.addWidget(self.framerightFlow)


        self.verticalLayout_9.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.unusedFrame9 = QFrame(self.flowFrame)
        self.unusedFrame9.setObjectName(u"unusedFrame9")
        self.unusedFrame9.setMinimumSize(QSize(0, 0))
        self.unusedFrame9.setFrameShape(QFrame.Shape.NoFrame)
        self.unusedFrame9.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_12.addWidget(self.unusedFrame9)

        self.unusedFrame10 = QFrame(self.flowFrame)
        self.unusedFrame10.setObjectName(u"unusedFrame10")
        self.unusedFrame10.setMinimumSize(QSize(0, 0))
        self.unusedFrame10.setFrameShape(QFrame.Shape.NoFrame)
        self.unusedFrame10.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_12.addWidget(self.unusedFrame10)

        self.upArrowFrame = QFrame(self.flowFrame)
        self.upArrowFrame.setObjectName(u"upArrowFrame")
        self.upArrowFrame.setMinimumSize(QSize(40, 100))
        self.upArrowFrame.setMaximumSize(QSize(40, 100))
        self.upArrowFrame.setStyleSheet(u"")
        self.upArrowFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.upArrowFrame.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_12.addWidget(self.upArrowFrame)

        self.unusedFrame11 = QFrame(self.flowFrame)
        self.unusedFrame11.setObjectName(u"unusedFrame11")
        self.unusedFrame11.setMinimumSize(QSize(0, 0))
        self.unusedFrame11.setFrameShape(QFrame.Shape.NoFrame)
        self.unusedFrame11.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_12.addWidget(self.unusedFrame11)

        self.unusedFrame12 = QFrame(self.flowFrame)
        self.unusedFrame12.setObjectName(u"unusedFrame12")
        self.unusedFrame12.setMinimumSize(QSize(0, 0))
        self.unusedFrame12.setFrameShape(QFrame.Shape.NoFrame)
        self.unusedFrame12.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_12.addWidget(self.unusedFrame12)


        self.verticalLayout_9.addLayout(self.horizontalLayout_12)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.unusedFrame13 = QFrame(self.flowFrame)
        self.unusedFrame13.setObjectName(u"unusedFrame13")
        self.unusedFrame13.setMinimumSize(QSize(0, 0))
        self.unusedFrame13.setMaximumSize(QSize(1, 1))
        self.unusedFrame13.setFrameShape(QFrame.Shape.NoFrame)
        self.unusedFrame13.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_13.addWidget(self.unusedFrame13)

        self.unusedFrame14 = QFrame(self.flowFrame)
        self.unusedFrame14.setObjectName(u"unusedFrame14")
        self.unusedFrame14.setMinimumSize(QSize(0, 0))
        self.unusedFrame14.setFrameShape(QFrame.Shape.NoFrame)
        self.unusedFrame14.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_13.addWidget(self.unusedFrame14)

        self.framebottomFlow = QFrame(self.flowFrame)
        self.framebottomFlow.setObjectName(u"framebottomFlow")
        self.framebottomFlow.setMinimumSize(QSize(250, 150))
        self.framebottomFlow.setMaximumSize(QSize(250, 150))
        self.framebottomFlow.setStyleSheet(u"\n"
"#framebottomFlow{\n"
"	background-color: #f8fbff;\n"
"	border: 1px solid #cddff3;\n"
"	border-radius: 8px;\n"
"	}\n"
"")
        self.framebottomFlow.setFrameShape(QFrame.Shape.NoFrame)
        self.framebottomFlow.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_13 = QVBoxLayout(self.framebottomFlow)
        self.verticalLayout_13.setSpacing(0)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(0, 5, 0, 5)
        self.frame_41 = QFrame(self.framebottomFlow)
        self.frame_41.setObjectName(u"frame_41")
        self.frame_41.setMinimumSize(QSize(0, 0))
        self.frame_41.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_41.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_20 = QHBoxLayout(self.frame_41)
        self.horizontalLayout_20.setSpacing(0)
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.horizontalLayout_20.setContentsMargins(0, 0, 0, 0)
        self.cur_dischFrame = QFrame(self.frame_41)
        self.cur_dischFrame.setObjectName(u"cur_dischFrame")
        self.cur_dischFrame.setMinimumSize(QSize(80, 80))
        self.cur_dischFrame.setMaximumSize(QSize(80, 80))
        self.cur_dischFrame.setStyleSheet(u"border-image: url(:/images/images/images/019-battery.png) 0 0 0 0 round round;\n"
"")
        self.cur_dischFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.cur_dischFrame.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_20.addWidget(self.cur_dischFrame)


        self.verticalLayout_13.addWidget(self.frame_41)

        self.currentdischpower_value = QLabel(self.framebottomFlow)
        self.currentdischpower_value.setObjectName(u"currentdischpower_value")
        sizePolicy2.setHeightForWidth(self.currentdischpower_value.sizePolicy().hasHeightForWidth())
        self.currentdischpower_value.setSizePolicy(sizePolicy2)
        self.currentdischpower_value.setMaximumSize(QSize(422, 45))
        self.currentdischpower_value.setFont(font4)
        self.currentdischpower_value.setStyleSheet(u"    font: bold 12pt \"Segoe UI\";\n"
"    color: Black;\n"
"\n"
"")
        self.currentdischpower_value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_13.addWidget(self.currentdischpower_value)

        self.currentsocbat_value = QLabel(self.framebottomFlow)
        self.currentsocbat_value.setObjectName(u"currentsocbat_value")
        sizePolicy2.setHeightForWidth(self.currentsocbat_value.sizePolicy().hasHeightForWidth())
        self.currentsocbat_value.setSizePolicy(sizePolicy2)
        self.currentsocbat_value.setMaximumSize(QSize(422, 45))
        self.currentsocbat_value.setFont(font4)
        self.currentsocbat_value.setStyleSheet(u"    font: bold 12pt \"Segoe UI\";\n"
"    color: Black;\n"
"\n"
"")
        self.currentsocbat_value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_13.addWidget(self.currentsocbat_value)


        self.horizontalLayout_13.addWidget(self.framebottomFlow)

        self.unusedFrame15 = QFrame(self.flowFrame)
        self.unusedFrame15.setObjectName(u"unusedFrame15")
        self.unusedFrame15.setMinimumSize(QSize(0, 0))
        self.unusedFrame15.setFrameShape(QFrame.Shape.NoFrame)
        self.unusedFrame15.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_13.addWidget(self.unusedFrame15)

        self.unusedFrame16 = QFrame(self.flowFrame)
        self.unusedFrame16.setObjectName(u"unusedFrame16")
        self.unusedFrame16.setMinimumSize(QSize(0, 0))
        self.unusedFrame16.setMaximumSize(QSize(1, 1))
        self.unusedFrame16.setFrameShape(QFrame.Shape.NoFrame)
        self.unusedFrame16.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_13.addWidget(self.unusedFrame16)


        self.verticalLayout_9.addLayout(self.horizontalLayout_13)


        self.verticalLayout_8.addWidget(self.flowFrame)


        self.layoutpage1.addWidget(self.livestatFrame)

        self.summaryFrame = QFrame(self.page1_growattMonitoring)
        self.summaryFrame.setObjectName(u"summaryFrame")
        self.summaryFrame.setMinimumSize(QSize(0, 882))
        self.summaryFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.summaryFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_14 = QVBoxLayout(self.summaryFrame)
        self.verticalLayout_14.setSpacing(0)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.frametitleSummary = QFrame(self.summaryFrame)
        self.frametitleSummary.setObjectName(u"frametitleSummary")
        self.frametitleSummary.setMinimumSize(QSize(0, 0))
        self.frametitleSummary.setMaximumSize(QSize(16777215, 90))
        self.frametitleSummary.setFrameShape(QFrame.Shape.NoFrame)
        self.frametitleSummary.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_15 = QHBoxLayout(self.frametitleSummary)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.titleSummary = QLabel(self.frametitleSummary)
        self.titleSummary.setObjectName(u"titleSummary")
        sizePolicy2.setHeightForWidth(self.titleSummary.sizePolicy().hasHeightForWidth())
        self.titleSummary.setSizePolicy(sizePolicy2)
        self.titleSummary.setMaximumSize(QSize(422, 45))
        self.titleSummary.setFont(font6)
        self.titleSummary.setStyleSheet(u"#titleSummary{\n"
"    font: bold 14pt \"Segoe UI\";\n"
"    color: white;\n"
"    background-color: #3D8D7A;\n"
"    border-radius: 8px;\n"
"    padding: 6px 10px;\n"
"    border: 1px solid #3D8D7A;\n"
"    \n"
"    /* Tambahan pengaturan ukuran */\n"
"    min-width: 500px;    /* lebar minimum */\n"
"    max-width: 400px;    /* lebar maksimum */\n"
"    qproperty-alignment: AlignCenter; /* biar teks di tengah */\n"
"}\n"
"")
        self.titleSummary.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_15.addWidget(self.titleSummary)


        self.verticalLayout_14.addWidget(self.frametitleSummary)

        self.frameSummary = QFrame(self.summaryFrame)
        self.frameSummary.setObjectName(u"frameSummary")
        self.frameSummary.setMinimumSize(QSize(0, 0))
        self.frameSummary.setMaximumSize(QSize(1000, 16777215))
        self.frameSummary.setFrameShape(QFrame.Shape.NoFrame)
        self.frameSummary.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_16 = QVBoxLayout(self.frameSummary)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.verticalLayout_16.setContentsMargins(-1, 0, -1, 9)
        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.paneloutputFrame = QFrame(self.frameSummary)
        self.paneloutputFrame.setObjectName(u"paneloutputFrame")
        self.paneloutputFrame.setMinimumSize(QSize(0, 382))
        self.paneloutputFrame.setMaximumSize(QSize(487, 382))
        self.paneloutputFrame.setStyleSheet(u"#paneloutputFrame{\n"
"	background-color: #E9F8F0;   /* hijau mint sangat lembut */\n"
"	border: 2px solid #D8F1E3;\n"
"	border-radius: 10px;\n"
"}")
        self.paneloutputFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.paneloutputFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_20 = QVBoxLayout(self.paneloutputFrame)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.framepanel4 = QFrame(self.paneloutputFrame)
        self.framepanel4.setObjectName(u"framepanel4")
        self.framepanel4.setFrameShape(QFrame.Shape.NoFrame)
        self.framepanel4.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_19 = QVBoxLayout(self.framepanel4)
        self.verticalLayout_19.setSpacing(20)
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.verticalLayout_19.setContentsMargins(-1, 50, -1, 0)
        self.framepanel5 = QFrame(self.framepanel4)
        self.framepanel5.setObjectName(u"framepanel5")
        self.framepanel5.setMinimumSize(QSize(0, 0))
        self.framepanel5.setFrameShape(QFrame.Shape.NoFrame)
        self.framepanel5.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_21 = QHBoxLayout(self.framepanel5)
        self.horizontalLayout_21.setSpacing(0)
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.horizontalLayout_21.setContentsMargins(0, 0, 0, 0)
        self.framepanelsum = QFrame(self.framepanel5)
        self.framepanelsum.setObjectName(u"framepanelsum")
        self.framepanelsum.setMinimumSize(QSize(100, 100))
        self.framepanelsum.setMaximumSize(QSize(100, 100))
        self.framepanelsum.setStyleSheet(u" border-image: url(:/images/images/images/048-solar panel.png) 0 0 0 0 stretch stretch;")
        self.framepanelsum.setFrameShape(QFrame.Shape.NoFrame)
        self.framepanelsum.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_21.addWidget(self.framepanelsum)


        self.verticalLayout_19.addWidget(self.framepanel5)

        self.framepanel6 = QFrame(self.framepanel4)
        self.framepanel6.setObjectName(u"framepanel6")
        self.framepanel6.setMinimumSize(QSize(0, 60))
        self.framepanel6.setFrameShape(QFrame.Shape.NoFrame)
        self.framepanel6.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_73 = QHBoxLayout(self.framepanel6)
        self.horizontalLayout_73.setObjectName(u"horizontalLayout_73")
        self.frame_43 = QFrame(self.framepanel6)
        self.frame_43.setObjectName(u"frame_43")
        self.frame_43.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_43.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_73.addWidget(self.frame_43)

        self.titlepvsum = QLabel(self.framepanel6)
        self.titlepvsum.setObjectName(u"titlepvsum")
        sizePolicy2.setHeightForWidth(self.titlepvsum.sizePolicy().hasHeightForWidth())
        self.titlepvsum.setSizePolicy(sizePolicy2)
        self.titlepvsum.setMaximumSize(QSize(182, 45))
        self.titlepvsum.setFont(font4)
        self.titlepvsum.setStyleSheet(u"#titlepvsum{\n"
"font: bold 12pt \"Segoe UI\";\n"
"color: white;\n"
"background-color: #4CAF8E;   /* hijau energi */\n"
"border-radius: 8px;\n"
"padding: 6px 10px;\n"
"border: 1px solid #4CAF8E;\n"
"\n"
"min-width: 100px;\n"
"max-width: 160px;\n"
"qproperty-alignment: AlignCenter;\n"
"}\n"
"")
        self.titlepvsum.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_73.addWidget(self.titlepvsum)

        self.frame_42 = QFrame(self.framepanel6)
        self.frame_42.setObjectName(u"frame_42")
        self.frame_42.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_42.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_73.addWidget(self.frame_42)


        self.verticalLayout_19.addWidget(self.framepanel6)


        self.verticalLayout_20.addWidget(self.framepanel4)

        self.framepanel1 = QFrame(self.paneloutputFrame)
        self.framepanel1.setObjectName(u"framepanel1")
        self.framepanel1.setFrameShape(QFrame.Shape.NoFrame)
        self.framepanel1.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_22 = QHBoxLayout(self.framepanel1)
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.horizontalLayout_22.setContentsMargins(-1, -1, -1, 20)
        self.pvtoday_value = QLabel(self.framepanel1)
        self.pvtoday_value.setObjectName(u"pvtoday_value")
        sizePolicy2.setHeightForWidth(self.pvtoday_value.sizePolicy().hasHeightForWidth())
        self.pvtoday_value.setSizePolicy(sizePolicy2)
        self.pvtoday_value.setMaximumSize(QSize(422, 45))
        font7 = QFont()
        font7.setFamilies([u"Segoe UI"])
        font7.setPointSize(22)
        font7.setBold(True)
        font7.setItalic(False)
        self.pvtoday_value.setFont(font7)
        self.pvtoday_value.setStyleSheet(u"    font: bold 22pt \"Segoe UI\";\n"
"    color: Black;\n"
"\n"
"")
        self.pvtoday_value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_22.addWidget(self.pvtoday_value)

        self.framepanel2 = QFrame(self.framepanel1)
        self.framepanel2.setObjectName(u"framepanel2")
        self.framepanel2.setFrameShape(QFrame.Shape.NoFrame)
        self.framepanel2.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_17 = QVBoxLayout(self.framepanel2)
        self.verticalLayout_17.setSpacing(0)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.verticalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_17.addItem(self.verticalSpacer)

        self.labeltoday1 = QLabel(self.framepanel2)
        self.labeltoday1.setObjectName(u"labeltoday1")
        sizePolicy2.setHeightForWidth(self.labeltoday1.sizePolicy().hasHeightForWidth())
        self.labeltoday1.setSizePolicy(sizePolicy2)
        self.labeltoday1.setMaximumSize(QSize(422, 45))
        font8 = QFont()
        font8.setFamilies([u"Segoe UI"])
        font8.setPointSize(11)
        font8.setBold(True)
        font8.setItalic(False)
        self.labeltoday1.setFont(font8)
        self.labeltoday1.setStyleSheet(u"    font: bold 11pt \"Segoe UI\";\n"
"    color: Black;\n"
"\n"
"")
        self.labeltoday1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_17.addWidget(self.labeltoday1)

        self.labelkwh1 = QLabel(self.framepanel2)
        self.labelkwh1.setObjectName(u"labelkwh1")
        sizePolicy2.setHeightForWidth(self.labelkwh1.sizePolicy().hasHeightForWidth())
        self.labelkwh1.setSizePolicy(sizePolicy2)
        self.labelkwh1.setMaximumSize(QSize(422, 45))
        self.labelkwh1.setFont(font8)
        self.labelkwh1.setStyleSheet(u"    font: bold 11pt \"Segoe UI\";\n"
"    color: Black;\n"
"\n"
"")
        self.labelkwh1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_17.addWidget(self.labelkwh1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_17.addItem(self.verticalSpacer_2)


        self.horizontalLayout_22.addWidget(self.framepanel2)

        self.horizontalSpacer_2 = QSpacerItem(50, 20, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_22.addItem(self.horizontalSpacer_2)

        self.pvtotal_value = QLabel(self.framepanel1)
        self.pvtotal_value.setObjectName(u"pvtotal_value")
        sizePolicy2.setHeightForWidth(self.pvtotal_value.sizePolicy().hasHeightForWidth())
        self.pvtotal_value.setSizePolicy(sizePolicy2)
        self.pvtotal_value.setMaximumSize(QSize(422, 45))
        self.pvtotal_value.setFont(font7)
        self.pvtotal_value.setStyleSheet(u"    font: bold 22pt \"Segoe UI\";\n"
"    color: Black;\n"
"\n"
"")
        self.pvtotal_value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_22.addWidget(self.pvtotal_value)

        self.framepanel3 = QFrame(self.framepanel1)
        self.framepanel3.setObjectName(u"framepanel3")
        self.framepanel3.setFrameShape(QFrame.Shape.NoFrame)
        self.framepanel3.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_18 = QVBoxLayout(self.framepanel3)
        self.verticalLayout_18.setSpacing(0)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.verticalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_18.addItem(self.verticalSpacer_3)

        self.labeltotal1 = QLabel(self.framepanel3)
        self.labeltotal1.setObjectName(u"labeltotal1")
        sizePolicy2.setHeightForWidth(self.labeltotal1.sizePolicy().hasHeightForWidth())
        self.labeltotal1.setSizePolicy(sizePolicy2)
        self.labeltotal1.setMaximumSize(QSize(422, 45))
        self.labeltotal1.setFont(font8)
        self.labeltotal1.setStyleSheet(u"    font: bold 11pt \"Segoe UI\";\n"
"    color: Black;\n"
"\n"
"")
        self.labeltotal1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_18.addWidget(self.labeltotal1)

        self.labelkwh2 = QLabel(self.framepanel3)
        self.labelkwh2.setObjectName(u"labelkwh2")
        sizePolicy2.setHeightForWidth(self.labelkwh2.sizePolicy().hasHeightForWidth())
        self.labelkwh2.setSizePolicy(sizePolicy2)
        self.labelkwh2.setMaximumSize(QSize(422, 45))
        self.labelkwh2.setFont(font8)
        self.labelkwh2.setStyleSheet(u"    font: bold 11pt \"Segoe UI\";\n"
"    color: Black;\n"
"\n"
"")
        self.labelkwh2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_18.addWidget(self.labelkwh2)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_18.addItem(self.verticalSpacer_4)


        self.horizontalLayout_22.addWidget(self.framepanel3)


        self.verticalLayout_20.addWidget(self.framepanel1)


        self.horizontalLayout_16.addWidget(self.paneloutputFrame)

        self.loadconsumptionFrame = QFrame(self.frameSummary)
        self.loadconsumptionFrame.setObjectName(u"loadconsumptionFrame")
        self.loadconsumptionFrame.setMinimumSize(QSize(0, 382))
        self.loadconsumptionFrame.setMaximumSize(QSize(487, 382))
        self.loadconsumptionFrame.setStyleSheet(u"#loadconsumptionFrame{\n"
"	background-color: #FFF4EA;   /* oranye pastel pucat */\n"
"	border: 2px solid #F9E4D2;\n"
"	border-radius: 10px;\n"
"}")
        self.loadconsumptionFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.loadconsumptionFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_26 = QVBoxLayout(self.loadconsumptionFrame)
        self.verticalLayout_26.setObjectName(u"verticalLayout_26")
        self.frameload1 = QFrame(self.loadconsumptionFrame)
        self.frameload1.setObjectName(u"frameload1")
        self.frameload1.setFrameShape(QFrame.Shape.NoFrame)
        self.frameload1.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_22 = QVBoxLayout(self.frameload1)
        self.verticalLayout_22.setSpacing(20)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.verticalLayout_22.setContentsMargins(-1, 50, -1, 0)
        self.frameload3 = QFrame(self.frameload1)
        self.frameload3.setObjectName(u"frameload3")
        self.frameload3.setMinimumSize(QSize(447, 0))
        self.frameload3.setFrameShape(QFrame.Shape.NoFrame)
        self.frameload3.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_23 = QHBoxLayout(self.frameload3)
        self.horizontalLayout_23.setSpacing(0)
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.horizontalLayout_23.setContentsMargins(0, 0, 0, 0)
        self.frameloadsum = QFrame(self.frameload3)
        self.frameloadsum.setObjectName(u"frameloadsum")
        self.frameloadsum.setMinimumSize(QSize(100, 100))
        self.frameloadsum.setMaximumSize(QSize(100, 100))
        self.frameloadsum.setStyleSheet(u" border-image: url(:/images/images/images/050-solar panels.png) 0 0 0 0 stretch stretch;")
        self.frameloadsum.setFrameShape(QFrame.Shape.NoFrame)
        self.frameloadsum.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_23.addWidget(self.frameloadsum)


        self.verticalLayout_22.addWidget(self.frameload3)

        self.frameload4 = QFrame(self.frameload1)
        self.frameload4.setObjectName(u"frameload4")
        self.frameload4.setMinimumSize(QSize(447, 60))
        self.frameload4.setFrameShape(QFrame.Shape.NoFrame)
        self.frameload4.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_74 = QHBoxLayout(self.frameload4)
        self.horizontalLayout_74.setObjectName(u"horizontalLayout_74")
        self.frame_38 = QFrame(self.frameload4)
        self.frame_38.setObjectName(u"frame_38")
        self.frame_38.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_38.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_74.addWidget(self.frame_38)

        self.titleloadsum = QLabel(self.frameload4)
        self.titleloadsum.setObjectName(u"titleloadsum")
        sizePolicy2.setHeightForWidth(self.titleloadsum.sizePolicy().hasHeightForWidth())
        self.titleloadsum.setSizePolicy(sizePolicy2)
        self.titleloadsum.setMaximumSize(QSize(172, 45))
        self.titleloadsum.setFont(font4)
        self.titleloadsum.setStyleSheet(u"#titleloadsum{\n"
"    font: bold 12pt \"Segoe UI\";\n"
"    color: white;\n"
"    background-color: #F4A261;   /* orange lembut */\n"
"    border-radius: 8px;\n"
"    padding: 6px 10px;\n"
"    border: 1px solid #F4A261;\n"
"    \n"
"    min-width: 100px;\n"
"    max-width: 150px;\n"
"    qproperty-alignment: AlignCenter;\n"
"}\n"
"")
        self.titleloadsum.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_74.addWidget(self.titleloadsum)

        self.frame_40 = QFrame(self.frameload4)
        self.frame_40.setObjectName(u"frame_40")
        self.frame_40.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_40.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_74.addWidget(self.frame_40)


        self.verticalLayout_22.addWidget(self.frameload4)


        self.verticalLayout_26.addWidget(self.frameload1)

        self.frameload2 = QFrame(self.loadconsumptionFrame)
        self.frameload2.setObjectName(u"frameload2")
        self.frameload2.setMinimumSize(QSize(467, 0))
        self.frameload2.setFrameShape(QFrame.Shape.NoFrame)
        self.frameload2.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_24 = QHBoxLayout(self.frameload2)
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.horizontalLayout_24.setContentsMargins(-1, -1, -1, 20)
        self.loadtoday_value = QLabel(self.frameload2)
        self.loadtoday_value.setObjectName(u"loadtoday_value")
        sizePolicy2.setHeightForWidth(self.loadtoday_value.sizePolicy().hasHeightForWidth())
        self.loadtoday_value.setSizePolicy(sizePolicy2)
        self.loadtoday_value.setMaximumSize(QSize(422, 45))
        self.loadtoday_value.setFont(font7)
        self.loadtoday_value.setStyleSheet(u"    font: bold 22pt \"Segoe UI\";\n"
"    color: Black;\n"
"\n"
"")
        self.loadtoday_value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_24.addWidget(self.loadtoday_value)

        self.frameload6 = QFrame(self.frameload2)
        self.frameload6.setObjectName(u"frameload6")
        self.frameload6.setFrameShape(QFrame.Shape.NoFrame)
        self.frameload6.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_24 = QVBoxLayout(self.frameload6)
        self.verticalLayout_24.setSpacing(0)
        self.verticalLayout_24.setObjectName(u"verticalLayout_24")
        self.verticalLayout_24.setContentsMargins(0, 0, 0, 0)
        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_24.addItem(self.verticalSpacer_5)

        self.labeltoday2 = QLabel(self.frameload6)
        self.labeltoday2.setObjectName(u"labeltoday2")
        sizePolicy2.setHeightForWidth(self.labeltoday2.sizePolicy().hasHeightForWidth())
        self.labeltoday2.setSizePolicy(sizePolicy2)
        self.labeltoday2.setMaximumSize(QSize(422, 45))
        self.labeltoday2.setFont(font8)
        self.labeltoday2.setStyleSheet(u"    font: bold 11pt \"Segoe UI\";\n"
"    color: Black;\n"
"\n"
"")
        self.labeltoday2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_24.addWidget(self.labeltoday2)

        self.labelkwh3 = QLabel(self.frameload6)
        self.labelkwh3.setObjectName(u"labelkwh3")
        sizePolicy2.setHeightForWidth(self.labelkwh3.sizePolicy().hasHeightForWidth())
        self.labelkwh3.setSizePolicy(sizePolicy2)
        self.labelkwh3.setMaximumSize(QSize(422, 45))
        self.labelkwh3.setFont(font8)
        self.labelkwh3.setStyleSheet(u"    font: bold 11pt \"Segoe UI\";\n"
"    color: Black;\n"
"\n"
"")
        self.labelkwh3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_24.addWidget(self.labelkwh3)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_24.addItem(self.verticalSpacer_6)


        self.horizontalLayout_24.addWidget(self.frameload6)

        self.horizontalSpacer_3 = QSpacerItem(50, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_24.addItem(self.horizontalSpacer_3)

        self.loadtotal_value = QLabel(self.frameload2)
        self.loadtotal_value.setObjectName(u"loadtotal_value")
        sizePolicy2.setHeightForWidth(self.loadtotal_value.sizePolicy().hasHeightForWidth())
        self.loadtotal_value.setSizePolicy(sizePolicy2)
        self.loadtotal_value.setMaximumSize(QSize(422, 45))
        self.loadtotal_value.setFont(font7)
        self.loadtotal_value.setStyleSheet(u"    font: bold 22pt \"Segoe UI\";\n"
"    color: Black;\n"
"\n"
"")
        self.loadtotal_value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_24.addWidget(self.loadtotal_value)

        self.frameload5 = QFrame(self.frameload2)
        self.frameload5.setObjectName(u"frameload5")
        self.frameload5.setFrameShape(QFrame.Shape.NoFrame)
        self.frameload5.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_25 = QVBoxLayout(self.frameload5)
        self.verticalLayout_25.setSpacing(0)
        self.verticalLayout_25.setObjectName(u"verticalLayout_25")
        self.verticalLayout_25.setContentsMargins(0, 0, 0, 0)
        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_25.addItem(self.verticalSpacer_7)

        self.labeltotal2 = QLabel(self.frameload5)
        self.labeltotal2.setObjectName(u"labeltotal2")
        sizePolicy2.setHeightForWidth(self.labeltotal2.sizePolicy().hasHeightForWidth())
        self.labeltotal2.setSizePolicy(sizePolicy2)
        self.labeltotal2.setMaximumSize(QSize(422, 45))
        self.labeltotal2.setFont(font8)
        self.labeltotal2.setStyleSheet(u"    font: bold 11pt \"Segoe UI\";\n"
"    color: Black;\n"
"\n"
"")
        self.labeltotal2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_25.addWidget(self.labeltotal2)

        self.labelkwh4 = QLabel(self.frameload5)
        self.labelkwh4.setObjectName(u"labelkwh4")
        sizePolicy2.setHeightForWidth(self.labelkwh4.sizePolicy().hasHeightForWidth())
        self.labelkwh4.setSizePolicy(sizePolicy2)
        self.labelkwh4.setMaximumSize(QSize(422, 45))
        self.labelkwh4.setFont(font8)
        self.labelkwh4.setStyleSheet(u"    font: bold 11pt \"Segoe UI\";\n"
"    color: Black;\n"
"\n"
"")
        self.labelkwh4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_25.addWidget(self.labelkwh4)

        self.verticalSpacer_8 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_25.addItem(self.verticalSpacer_8)


        self.horizontalLayout_24.addWidget(self.frameload5)


        self.verticalLayout_26.addWidget(self.frameload2)


        self.horizontalLayout_16.addWidget(self.loadconsumptionFrame)


        self.verticalLayout_16.addLayout(self.horizontalLayout_16)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.chargingFrame = QFrame(self.frameSummary)
        self.chargingFrame.setObjectName(u"chargingFrame")
        self.chargingFrame.setMinimumSize(QSize(0, 382))
        self.chargingFrame.setMaximumSize(QSize(323, 382))
        self.chargingFrame.setStyleSheet(u"#chargingFrame{\n"
"	background-color: #F2ECF9;   /* ungu lembut banget */\n"
"	border: 2px solid #E3DAF1;\n"
"	border-radius: 10px;\n"
"}")
        self.chargingFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.chargingFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_31 = QVBoxLayout(self.chargingFrame)
        self.verticalLayout_31.setObjectName(u"verticalLayout_31")
        self.framecharging1 = QFrame(self.chargingFrame)
        self.framecharging1.setObjectName(u"framecharging1")
        self.framecharging1.setFrameShape(QFrame.Shape.NoFrame)
        self.framecharging1.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_27 = QVBoxLayout(self.framecharging1)
        self.verticalLayout_27.setSpacing(20)
        self.verticalLayout_27.setObjectName(u"verticalLayout_27")
        self.verticalLayout_27.setContentsMargins(-1, 50, -1, 0)
        self.framecharging3 = QFrame(self.framecharging1)
        self.framecharging3.setObjectName(u"framecharging3")
        self.framecharging3.setMinimumSize(QSize(0, 0))
        self.framecharging3.setFrameShape(QFrame.Shape.NoFrame)
        self.framecharging3.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_25 = QHBoxLayout(self.framecharging3)
        self.horizontalLayout_25.setSpacing(0)
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.horizontalLayout_25.setContentsMargins(0, 0, 0, 0)
        self.framechargingsum = QFrame(self.framecharging3)
        self.framechargingsum.setObjectName(u"framechargingsum")
        self.framechargingsum.setMinimumSize(QSize(100, 100))
        self.framechargingsum.setMaximumSize(QSize(100, 100))
        self.framechargingsum.setStyleSheet(u" border-image: url(:/images/images/images/049-solar energy.png) 0 0 0 0 stretch stretch;")
        self.framechargingsum.setFrameShape(QFrame.Shape.NoFrame)
        self.framechargingsum.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_25.addWidget(self.framechargingsum)


        self.verticalLayout_27.addWidget(self.framecharging3)

        self.framecharging2 = QFrame(self.framecharging1)
        self.framecharging2.setObjectName(u"framecharging2")
        self.framecharging2.setMinimumSize(QSize(0, 60))
        self.framecharging2.setFrameShape(QFrame.Shape.NoFrame)
        self.framecharging2.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_75 = QHBoxLayout(self.framecharging2)
        self.horizontalLayout_75.setObjectName(u"horizontalLayout_75")
        self.frame_44 = QFrame(self.framecharging2)
        self.frame_44.setObjectName(u"frame_44")
        self.frame_44.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_44.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_75.addWidget(self.frame_44)

        self.titlechargingsum = QLabel(self.framecharging2)
        self.titlechargingsum.setObjectName(u"titlechargingsum")
        sizePolicy2.setHeightForWidth(self.titlechargingsum.sizePolicy().hasHeightForWidth())
        self.titlechargingsum.setSizePolicy(sizePolicy2)
        self.titlechargingsum.setMaximumSize(QSize(172, 45))
        self.titlechargingsum.setFont(font4)
        self.titlechargingsum.setStyleSheet(u"#titlechargingsum{\n"
"font: bold 12pt \"Segoe UI\";\n"
"color: white;\n"
"background-color: #8E7AB5;   /* ungu battery */\n"
"border-radius: 8px;\n"
"padding: 6px 10px;\n"
"border: 1px solid #8E7AB5;\n"
"\n"
"min-width: 100px;\n"
"max-width: 150px;\n"
"qproperty-alignment: AlignCenter;\n"
"\n"
"}\n"
"")
        self.titlechargingsum.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_75.addWidget(self.titlechargingsum)

        self.frame_45 = QFrame(self.framecharging2)
        self.frame_45.setObjectName(u"frame_45")
        self.frame_45.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_45.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_75.addWidget(self.frame_45)


        self.verticalLayout_27.addWidget(self.framecharging2)


        self.verticalLayout_31.addWidget(self.framecharging1)

        self.framecharging4 = QFrame(self.chargingFrame)
        self.framecharging4.setObjectName(u"framecharging4")
        self.framecharging4.setFrameShape(QFrame.Shape.NoFrame)
        self.framecharging4.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_26 = QHBoxLayout(self.framecharging4)
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.horizontalLayout_26.setContentsMargins(-1, -1, -1, 20)
        self.chargingtoday_value = QLabel(self.framecharging4)
        self.chargingtoday_value.setObjectName(u"chargingtoday_value")
        sizePolicy2.setHeightForWidth(self.chargingtoday_value.sizePolicy().hasHeightForWidth())
        self.chargingtoday_value.setSizePolicy(sizePolicy2)
        self.chargingtoday_value.setMaximumSize(QSize(422, 45))
        self.chargingtoday_value.setFont(font7)
        self.chargingtoday_value.setStyleSheet(u"    font: bold 22pt \"Segoe UI\";\n"
"    color: Black;\n"
"\n"
"")
        self.chargingtoday_value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_26.addWidget(self.chargingtoday_value)

        self.framecharging5 = QFrame(self.framecharging4)
        self.framecharging5.setObjectName(u"framecharging5")
        self.framecharging5.setFrameShape(QFrame.Shape.NoFrame)
        self.framecharging5.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_29 = QVBoxLayout(self.framecharging5)
        self.verticalLayout_29.setSpacing(0)
        self.verticalLayout_29.setObjectName(u"verticalLayout_29")
        self.verticalLayout_29.setContentsMargins(0, 0, 0, 0)
        self.verticalSpacer_9 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_29.addItem(self.verticalSpacer_9)

        self.labeltoday3 = QLabel(self.framecharging5)
        self.labeltoday3.setObjectName(u"labeltoday3")
        sizePolicy2.setHeightForWidth(self.labeltoday3.sizePolicy().hasHeightForWidth())
        self.labeltoday3.setSizePolicy(sizePolicy2)
        self.labeltoday3.setMaximumSize(QSize(422, 45))
        self.labeltoday3.setFont(font8)
        self.labeltoday3.setStyleSheet(u"    font: bold 11pt \"Segoe UI\";\n"
"    color: Black;\n"
"\n"
"")
        self.labeltoday3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_29.addWidget(self.labeltoday3)

        self.labelkwh5 = QLabel(self.framecharging5)
        self.labelkwh5.setObjectName(u"labelkwh5")
        sizePolicy2.setHeightForWidth(self.labelkwh5.sizePolicy().hasHeightForWidth())
        self.labelkwh5.setSizePolicy(sizePolicy2)
        self.labelkwh5.setMaximumSize(QSize(422, 45))
        self.labelkwh5.setFont(font8)
        self.labelkwh5.setStyleSheet(u"    font: bold 11pt \"Segoe UI\";\n"
"    color: Black;\n"
"\n"
"")
        self.labelkwh5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_29.addWidget(self.labelkwh5)

        self.verticalSpacer_10 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_29.addItem(self.verticalSpacer_10)


        self.horizontalLayout_26.addWidget(self.framecharging5)

        self.horizontalSpacer_4 = QSpacerItem(15, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_26.addItem(self.horizontalSpacer_4)

        self.chargingtotal_value = QLabel(self.framecharging4)
        self.chargingtotal_value.setObjectName(u"chargingtotal_value")
        sizePolicy2.setHeightForWidth(self.chargingtotal_value.sizePolicy().hasHeightForWidth())
        self.chargingtotal_value.setSizePolicy(sizePolicy2)
        self.chargingtotal_value.setMaximumSize(QSize(422, 45))
        self.chargingtotal_value.setFont(font7)
        self.chargingtotal_value.setStyleSheet(u"    font: bold 22pt \"Segoe UI\";\n"
"    color: Black;\n"
"\n"
"")
        self.chargingtotal_value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_26.addWidget(self.chargingtotal_value)

        self.frame_16 = QFrame(self.framecharging4)
        self.frame_16.setObjectName(u"frame_16")
        self.frame_16.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_16.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_30 = QVBoxLayout(self.frame_16)
        self.verticalLayout_30.setSpacing(0)
        self.verticalLayout_30.setObjectName(u"verticalLayout_30")
        self.verticalLayout_30.setContentsMargins(0, 0, 0, 0)
        self.verticalSpacer_11 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_30.addItem(self.verticalSpacer_11)

        self.labeltotal3 = QLabel(self.frame_16)
        self.labeltotal3.setObjectName(u"labeltotal3")
        sizePolicy2.setHeightForWidth(self.labeltotal3.sizePolicy().hasHeightForWidth())
        self.labeltotal3.setSizePolicy(sizePolicy2)
        self.labeltotal3.setMaximumSize(QSize(422, 45))
        self.labeltotal3.setFont(font8)
        self.labeltotal3.setStyleSheet(u"    font: bold 11pt \"Segoe UI\";\n"
"    color: Black;\n"
"\n"
"")
        self.labeltotal3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_30.addWidget(self.labeltotal3)

        self.labelkwh6 = QLabel(self.frame_16)
        self.labelkwh6.setObjectName(u"labelkwh6")
        sizePolicy2.setHeightForWidth(self.labelkwh6.sizePolicy().hasHeightForWidth())
        self.labelkwh6.setSizePolicy(sizePolicy2)
        self.labelkwh6.setMaximumSize(QSize(422, 45))
        self.labelkwh6.setFont(font8)
        self.labelkwh6.setStyleSheet(u"    font: bold 11pt \"Segoe UI\";\n"
"    color: Black;\n"
"\n"
"")
        self.labelkwh6.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_30.addWidget(self.labelkwh6)

        self.verticalSpacer_12 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_30.addItem(self.verticalSpacer_12)


        self.horizontalLayout_26.addWidget(self.frame_16)


        self.verticalLayout_31.addWidget(self.framecharging4)


        self.horizontalLayout_17.addWidget(self.chargingFrame)

        self.dischargingFrame = QFrame(self.frameSummary)
        self.dischargingFrame.setObjectName(u"dischargingFrame")
        self.dischargingFrame.setMinimumSize(QSize(0, 382))
        self.dischargingFrame.setMaximumSize(QSize(322, 382))
        self.dischargingFrame.setStyleSheet(u"#dischargingFrame{\n"
"	background-color: #ECF5FB;   /* biru pucat */\n"
"	border: 2px solid #DDEBF7;\n"
"	border-radius: 10px;\n"
"}")
        self.dischargingFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.dischargingFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_36 = QVBoxLayout(self.dischargingFrame)
        self.verticalLayout_36.setObjectName(u"verticalLayout_36")
        self.framedisch1 = QFrame(self.dischargingFrame)
        self.framedisch1.setObjectName(u"framedisch1")
        self.framedisch1.setFrameShape(QFrame.Shape.NoFrame)
        self.framedisch1.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_32 = QVBoxLayout(self.framedisch1)
        self.verticalLayout_32.setSpacing(20)
        self.verticalLayout_32.setObjectName(u"verticalLayout_32")
        self.verticalLayout_32.setContentsMargins(-1, 50, -1, 0)
        self.framedisch3 = QFrame(self.framedisch1)
        self.framedisch3.setObjectName(u"framedisch3")
        self.framedisch3.setMinimumSize(QSize(0, 0))
        self.framedisch3.setFrameShape(QFrame.Shape.NoFrame)
        self.framedisch3.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_27 = QHBoxLayout(self.framedisch3)
        self.horizontalLayout_27.setSpacing(0)
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.horizontalLayout_27.setContentsMargins(0, 0, 0, 0)
        self.framedischargingsum = QFrame(self.framedisch3)
        self.framedischargingsum.setObjectName(u"framedischargingsum")
        self.framedischargingsum.setMinimumSize(QSize(100, 100))
        self.framedischargingsum.setMaximumSize(QSize(100, 100))
        self.framedischargingsum.setStyleSheet(u" border-image: url(:/images/images/images/017-charging station.png) 0 0 0 0 stretch stretch;")
        self.framedischargingsum.setFrameShape(QFrame.Shape.NoFrame)
        self.framedischargingsum.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_27.addWidget(self.framedischargingsum)


        self.verticalLayout_32.addWidget(self.framedisch3)

        self.framedisch2 = QFrame(self.framedisch1)
        self.framedisch2.setObjectName(u"framedisch2")
        self.framedisch2.setMinimumSize(QSize(0, 60))
        self.framedisch2.setFrameShape(QFrame.Shape.NoFrame)
        self.framedisch2.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_76 = QHBoxLayout(self.framedisch2)
        self.horizontalLayout_76.setObjectName(u"horizontalLayout_76")
        self.frame_47 = QFrame(self.framedisch2)
        self.frame_47.setObjectName(u"frame_47")
        self.frame_47.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_47.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_76.addWidget(self.frame_47)

        self.titledischargingsum = QLabel(self.framedisch2)
        self.titledischargingsum.setObjectName(u"titledischargingsum")
        sizePolicy2.setHeightForWidth(self.titledischargingsum.sizePolicy().hasHeightForWidth())
        self.titledischargingsum.setSizePolicy(sizePolicy2)
        self.titledischargingsum.setMaximumSize(QSize(172, 45))
        self.titledischargingsum.setFont(font4)
        self.titledischargingsum.setStyleSheet(u"#titledischargingsum{\n"
"font: bold 12pt \"Segoe UI\";\n"
"color: white;\n"
"background-color: #4A90D9;   /* biru energi */\n"
"border-radius: 8px;\n"
"padding: 6px 10px;\n"
"border: 1px solid #4A90D9;\n"
"\n"
"min-width: 100px;\n"
"max-width: 150px;\n"
"qproperty-alignment: AlignCenter;\n"
"}\n"
"")
        self.titledischargingsum.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_76.addWidget(self.titledischargingsum)

        self.frame_48 = QFrame(self.framedisch2)
        self.frame_48.setObjectName(u"frame_48")
        self.frame_48.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_48.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_76.addWidget(self.frame_48)


        self.verticalLayout_32.addWidget(self.framedisch2)


        self.verticalLayout_36.addWidget(self.framedisch1)

        self.framedisch4 = QFrame(self.dischargingFrame)
        self.framedisch4.setObjectName(u"framedisch4")
        self.framedisch4.setFrameShape(QFrame.Shape.NoFrame)
        self.framedisch4.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_28 = QHBoxLayout(self.framedisch4)
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.horizontalLayout_28.setContentsMargins(-1, -1, -1, 20)
        self.dischargingtoday_value = QLabel(self.framedisch4)
        self.dischargingtoday_value.setObjectName(u"dischargingtoday_value")
        sizePolicy2.setHeightForWidth(self.dischargingtoday_value.sizePolicy().hasHeightForWidth())
        self.dischargingtoday_value.setSizePolicy(sizePolicy2)
        self.dischargingtoday_value.setMaximumSize(QSize(422, 45))
        self.dischargingtoday_value.setFont(font7)
        self.dischargingtoday_value.setStyleSheet(u"    font: bold 22pt \"Segoe UI\";\n"
"    color: Black;\n"
"\n"
"")
        self.dischargingtoday_value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_28.addWidget(self.dischargingtoday_value)

        self.framedisch5 = QFrame(self.framedisch4)
        self.framedisch5.setObjectName(u"framedisch5")
        self.framedisch5.setFrameShape(QFrame.Shape.NoFrame)
        self.framedisch5.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_34 = QVBoxLayout(self.framedisch5)
        self.verticalLayout_34.setSpacing(0)
        self.verticalLayout_34.setObjectName(u"verticalLayout_34")
        self.verticalLayout_34.setContentsMargins(0, 0, 0, 0)
        self.verticalSpacer_13 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_34.addItem(self.verticalSpacer_13)

        self.labeltoday4 = QLabel(self.framedisch5)
        self.labeltoday4.setObjectName(u"labeltoday4")
        sizePolicy2.setHeightForWidth(self.labeltoday4.sizePolicy().hasHeightForWidth())
        self.labeltoday4.setSizePolicy(sizePolicy2)
        self.labeltoday4.setMaximumSize(QSize(422, 45))
        self.labeltoday4.setFont(font8)
        self.labeltoday4.setStyleSheet(u"    font: bold 11pt \"Segoe UI\";\n"
"    color: Black;\n"
"\n"
"")
        self.labeltoday4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_34.addWidget(self.labeltoday4)

        self.labelkwh7 = QLabel(self.framedisch5)
        self.labelkwh7.setObjectName(u"labelkwh7")
        sizePolicy2.setHeightForWidth(self.labelkwh7.sizePolicy().hasHeightForWidth())
        self.labelkwh7.setSizePolicy(sizePolicy2)
        self.labelkwh7.setMaximumSize(QSize(422, 45))
        self.labelkwh7.setFont(font8)
        self.labelkwh7.setStyleSheet(u"    font: bold 11pt \"Segoe UI\";\n"
"    color: Black;\n"
"\n"
"")
        self.labelkwh7.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_34.addWidget(self.labelkwh7)

        self.verticalSpacer_14 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_34.addItem(self.verticalSpacer_14)


        self.horizontalLayout_28.addWidget(self.framedisch5)

        self.horizontalSpacer_5 = QSpacerItem(15, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_28.addItem(self.horizontalSpacer_5)

        self.dischargingtotal_value = QLabel(self.framedisch4)
        self.dischargingtotal_value.setObjectName(u"dischargingtotal_value")
        sizePolicy2.setHeightForWidth(self.dischargingtotal_value.sizePolicy().hasHeightForWidth())
        self.dischargingtotal_value.setSizePolicy(sizePolicy2)
        self.dischargingtotal_value.setMaximumSize(QSize(422, 45))
        self.dischargingtotal_value.setFont(font7)
        self.dischargingtotal_value.setStyleSheet(u"    font: bold 22pt \"Segoe UI\";\n"
"    color: Black;\n"
"\n"
"")
        self.dischargingtotal_value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_28.addWidget(self.dischargingtotal_value)

        self.framedisch6 = QFrame(self.framedisch4)
        self.framedisch6.setObjectName(u"framedisch6")
        self.framedisch6.setFrameShape(QFrame.Shape.NoFrame)
        self.framedisch6.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_35 = QVBoxLayout(self.framedisch6)
        self.verticalLayout_35.setSpacing(0)
        self.verticalLayout_35.setObjectName(u"verticalLayout_35")
        self.verticalLayout_35.setContentsMargins(0, 0, 0, 0)
        self.verticalSpacer_15 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_35.addItem(self.verticalSpacer_15)

        self.labeltotal4 = QLabel(self.framedisch6)
        self.labeltotal4.setObjectName(u"labeltotal4")
        sizePolicy2.setHeightForWidth(self.labeltotal4.sizePolicy().hasHeightForWidth())
        self.labeltotal4.setSizePolicy(sizePolicy2)
        self.labeltotal4.setMaximumSize(QSize(422, 45))
        self.labeltotal4.setFont(font8)
        self.labeltotal4.setStyleSheet(u"    font: bold 11pt \"Segoe UI\";\n"
"    color: Black;\n"
"\n"
"")
        self.labeltotal4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_35.addWidget(self.labeltotal4)

        self.labelkwh8 = QLabel(self.framedisch6)
        self.labelkwh8.setObjectName(u"labelkwh8")
        sizePolicy2.setHeightForWidth(self.labelkwh8.sizePolicy().hasHeightForWidth())
        self.labelkwh8.setSizePolicy(sizePolicy2)
        self.labelkwh8.setMaximumSize(QSize(422, 45))
        self.labelkwh8.setFont(font8)
        self.labelkwh8.setStyleSheet(u"    font: bold 11pt \"Segoe UI\";\n"
"    color: Black;\n"
"\n"
"")
        self.labelkwh8.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_35.addWidget(self.labelkwh8)

        self.verticalSpacer_16 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_35.addItem(self.verticalSpacer_16)


        self.horizontalLayout_28.addWidget(self.framedisch6)


        self.verticalLayout_36.addWidget(self.framedisch4)


        self.horizontalLayout_17.addWidget(self.dischargingFrame)

        self.importgridFrame = QFrame(self.frameSummary)
        self.importgridFrame.setObjectName(u"importgridFrame")
        self.importgridFrame.setMinimumSize(QSize(0, 382))
        self.importgridFrame.setMaximumSize(QSize(323, 382))
        self.importgridFrame.setStyleSheet(u"#importgridFrame{\n"
"	background-color: #FEFAEC;   /* kuning muda banget */\n"
"	border: 2px solid #F7F1D3;\n"
"	border-radius: 10px;\n"
"}")
        self.importgridFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.importgridFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_41 = QVBoxLayout(self.importgridFrame)
        self.verticalLayout_41.setObjectName(u"verticalLayout_41")
        self.frameimport1 = QFrame(self.importgridFrame)
        self.frameimport1.setObjectName(u"frameimport1")
        self.frameimport1.setMinimumSize(QSize(303, 0))
        self.frameimport1.setFrameShape(QFrame.Shape.NoFrame)
        self.frameimport1.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_37 = QVBoxLayout(self.frameimport1)
        self.verticalLayout_37.setSpacing(20)
        self.verticalLayout_37.setObjectName(u"verticalLayout_37")
        self.verticalLayout_37.setContentsMargins(-1, 50, -1, 0)
        self.frameimport3 = QFrame(self.frameimport1)
        self.frameimport3.setObjectName(u"frameimport3")
        self.frameimport3.setMinimumSize(QSize(0, 0))
        self.frameimport3.setFrameShape(QFrame.Shape.NoFrame)
        self.frameimport3.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_29 = QHBoxLayout(self.frameimport3)
        self.horizontalLayout_29.setSpacing(0)
        self.horizontalLayout_29.setObjectName(u"horizontalLayout_29")
        self.horizontalLayout_29.setContentsMargins(0, 0, 0, 0)
        self.frameimportsum = QFrame(self.frameimport3)
        self.frameimportsum.setObjectName(u"frameimportsum")
        self.frameimportsum.setMinimumSize(QSize(100, 100))
        self.frameimportsum.setMaximumSize(QSize(100, 100))
        self.frameimportsum.setStyleSheet(u" border-image: url(:/images/images/images/034-electric tower.png) 0 0 0 0 stretch stretch;")
        self.frameimportsum.setFrameShape(QFrame.Shape.NoFrame)
        self.frameimportsum.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_29.addWidget(self.frameimportsum)


        self.verticalLayout_37.addWidget(self.frameimport3)

        self.frameimport2 = QFrame(self.frameimport1)
        self.frameimport2.setObjectName(u"frameimport2")
        self.frameimport2.setMinimumSize(QSize(0, 60))
        self.frameimport2.setFrameShape(QFrame.Shape.NoFrame)
        self.frameimport2.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_77 = QHBoxLayout(self.frameimport2)
        self.horizontalLayout_77.setObjectName(u"horizontalLayout_77")
        self.frame_49 = QFrame(self.frameimport2)
        self.frame_49.setObjectName(u"frame_49")
        self.frame_49.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_49.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_77.addWidget(self.frame_49)

        self.titleimportsum = QLabel(self.frameimport2)
        self.titleimportsum.setObjectName(u"titleimportsum")
        sizePolicy2.setHeightForWidth(self.titleimportsum.sizePolicy().hasHeightForWidth())
        self.titleimportsum.setSizePolicy(sizePolicy2)
        self.titleimportsum.setMaximumSize(QSize(172, 45))
        self.titleimportsum.setFont(font4)
        self.titleimportsum.setStyleSheet(u"#titleimportsum{\n"
"font: bold 12pt \"Segoe UI\";\n"
"color: white;\n"
"background-color: #9C8F5E;   /* kuning olive netral */\n"
"border-radius: 8px;\n"
"padding: 6px 10px;\n"
"border: 1px solid #9C8F5E;\n"
"\n"
"min-width: 100px;\n"
"max-width: 150px;\n"
"qproperty-alignment: AlignCenter;\n"
"\n"
"}\n"
"")
        self.titleimportsum.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_77.addWidget(self.titleimportsum)

        self.frame_50 = QFrame(self.frameimport2)
        self.frame_50.setObjectName(u"frame_50")
        self.frame_50.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_50.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_77.addWidget(self.frame_50)


        self.verticalLayout_37.addWidget(self.frameimport2)


        self.verticalLayout_41.addWidget(self.frameimport1)

        self.frameimport4 = QFrame(self.importgridFrame)
        self.frameimport4.setObjectName(u"frameimport4")
        self.frameimport4.setMinimumSize(QSize(303, 0))
        self.frameimport4.setFrameShape(QFrame.Shape.NoFrame)
        self.frameimport4.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_30 = QHBoxLayout(self.frameimport4)
        self.horizontalLayout_30.setObjectName(u"horizontalLayout_30")
        self.horizontalLayout_30.setContentsMargins(-1, -1, -1, 20)
        self.imporgridttoday_value = QLabel(self.frameimport4)
        self.imporgridttoday_value.setObjectName(u"imporgridttoday_value")
        sizePolicy2.setHeightForWidth(self.imporgridttoday_value.sizePolicy().hasHeightForWidth())
        self.imporgridttoday_value.setSizePolicy(sizePolicy2)
        self.imporgridttoday_value.setMaximumSize(QSize(422, 45))
        self.imporgridttoday_value.setFont(font7)
        self.imporgridttoday_value.setStyleSheet(u"    font: bold 22pt \"Segoe UI\";\n"
"    color: Black;\n"
"\n"
"")
        self.imporgridttoday_value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_30.addWidget(self.imporgridttoday_value)

        self.frameimport5 = QFrame(self.frameimport4)
        self.frameimport5.setObjectName(u"frameimport5")
        self.frameimport5.setFrameShape(QFrame.Shape.NoFrame)
        self.frameimport5.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_39 = QVBoxLayout(self.frameimport5)
        self.verticalLayout_39.setSpacing(0)
        self.verticalLayout_39.setObjectName(u"verticalLayout_39")
        self.verticalLayout_39.setContentsMargins(0, 0, 0, 0)
        self.verticalSpacer_17 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_39.addItem(self.verticalSpacer_17)

        self.labeltoday5 = QLabel(self.frameimport5)
        self.labeltoday5.setObjectName(u"labeltoday5")
        sizePolicy2.setHeightForWidth(self.labeltoday5.sizePolicy().hasHeightForWidth())
        self.labeltoday5.setSizePolicy(sizePolicy2)
        self.labeltoday5.setMaximumSize(QSize(422, 45))
        self.labeltoday5.setFont(font8)
        self.labeltoday5.setStyleSheet(u"    font: bold 11pt \"Segoe UI\";\n"
"    color: Black;\n"
"\n"
"")
        self.labeltoday5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_39.addWidget(self.labeltoday5)

        self.labelkwh9 = QLabel(self.frameimport5)
        self.labelkwh9.setObjectName(u"labelkwh9")
        sizePolicy2.setHeightForWidth(self.labelkwh9.sizePolicy().hasHeightForWidth())
        self.labelkwh9.setSizePolicy(sizePolicy2)
        self.labelkwh9.setMaximumSize(QSize(422, 45))
        self.labelkwh9.setFont(font8)
        self.labelkwh9.setStyleSheet(u"    font: bold 11pt \"Segoe UI\";\n"
"    color: Black;\n"
"\n"
"")
        self.labelkwh9.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_39.addWidget(self.labelkwh9)

        self.verticalSpacer_18 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_39.addItem(self.verticalSpacer_18)


        self.horizontalLayout_30.addWidget(self.frameimport5)

        self.horizontalSpacer_6 = QSpacerItem(15, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_30.addItem(self.horizontalSpacer_6)

        self.imporgridttotal_value = QLabel(self.frameimport4)
        self.imporgridttotal_value.setObjectName(u"imporgridttotal_value")
        sizePolicy2.setHeightForWidth(self.imporgridttotal_value.sizePolicy().hasHeightForWidth())
        self.imporgridttotal_value.setSizePolicy(sizePolicy2)
        self.imporgridttotal_value.setMaximumSize(QSize(422, 45))
        self.imporgridttotal_value.setFont(font7)
        self.imporgridttotal_value.setStyleSheet(u"    font: bold 22pt \"Segoe UI\";\n"
"    color: Black;\n"
"\n"
"")
        self.imporgridttotal_value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_30.addWidget(self.imporgridttotal_value)

        self.frameimport6 = QFrame(self.frameimport4)
        self.frameimport6.setObjectName(u"frameimport6")
        self.frameimport6.setFrameShape(QFrame.Shape.NoFrame)
        self.frameimport6.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_40 = QVBoxLayout(self.frameimport6)
        self.verticalLayout_40.setSpacing(0)
        self.verticalLayout_40.setObjectName(u"verticalLayout_40")
        self.verticalLayout_40.setContentsMargins(0, 0, 0, 0)
        self.verticalSpacer_19 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_40.addItem(self.verticalSpacer_19)

        self.labeltotal5 = QLabel(self.frameimport6)
        self.labeltotal5.setObjectName(u"labeltotal5")
        sizePolicy2.setHeightForWidth(self.labeltotal5.sizePolicy().hasHeightForWidth())
        self.labeltotal5.setSizePolicy(sizePolicy2)
        self.labeltotal5.setMaximumSize(QSize(422, 45))
        self.labeltotal5.setFont(font8)
        self.labeltotal5.setStyleSheet(u"    font: bold 11pt \"Segoe UI\";\n"
"    color: Black;\n"
"\n"
"")
        self.labeltotal5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_40.addWidget(self.labeltotal5)

        self.labelkwh10 = QLabel(self.frameimport6)
        self.labelkwh10.setObjectName(u"labelkwh10")
        sizePolicy2.setHeightForWidth(self.labelkwh10.sizePolicy().hasHeightForWidth())
        self.labelkwh10.setSizePolicy(sizePolicy2)
        self.labelkwh10.setMaximumSize(QSize(422, 45))
        self.labelkwh10.setFont(font8)
        self.labelkwh10.setStyleSheet(u"    font: bold 11pt \"Segoe UI\";\n"
"    color: Black;\n"
"\n"
"")
        self.labelkwh10.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_40.addWidget(self.labelkwh10)

        self.verticalSpacer_20 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_40.addItem(self.verticalSpacer_20)


        self.horizontalLayout_30.addWidget(self.frameimport6)


        self.verticalLayout_41.addWidget(self.frameimport4)


        self.horizontalLayout_17.addWidget(self.importgridFrame)


        self.verticalLayout_16.addLayout(self.horizontalLayout_17)


        self.verticalLayout_14.addWidget(self.frameSummary)


        self.layoutpage1.addWidget(self.summaryFrame)


        self.verticalLayout_7.addLayout(self.layoutpage1)


        self.horizontalLayout_7.addLayout(self.verticalLayout_7)

        self.stackedWidget.addWidget(self.page1_growattMonitoring)
        self.page2_controlRoom = QWidget()
        self.page2_controlRoom.setObjectName(u"page2_controlRoom")
        self.verticalLayout_59 = QVBoxLayout(self.page2_controlRoom)
        self.verticalLayout_59.setSpacing(6)
        self.verticalLayout_59.setObjectName(u"verticalLayout_59")
        self.verticalLayout_59.setContentsMargins(9, 9, 9, 9)
        self.titlecontrolroomFrame = QFrame(self.page2_controlRoom)
        self.titlecontrolroomFrame.setObjectName(u"titlecontrolroomFrame")
        self.titlecontrolroomFrame.setMaximumSize(QSize(16777215, 65))
        self.titlecontrolroomFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.titlecontrolroomFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_39 = QHBoxLayout(self.titlecontrolroomFrame)
        self.horizontalLayout_39.setSpacing(0)
        self.horizontalLayout_39.setObjectName(u"horizontalLayout_39")
        self.horizontalLayout_39.setContentsMargins(0, 5, -1, 0)
        self.titlecontrolroom = QLabel(self.titlecontrolroomFrame)
        self.titlecontrolroom.setObjectName(u"titlecontrolroom")
        sizePolicy2.setHeightForWidth(self.titlecontrolroom.sizePolicy().hasHeightForWidth())
        self.titlecontrolroom.setSizePolicy(sizePolicy2)
        self.titlecontrolroom.setMaximumSize(QSize(422, 45))
        self.titlecontrolroom.setFont(font6)
        self.titlecontrolroom.setStyleSheet(u"#titlecontrolroom {\n"
"    font: bold 14pt \"Segoe UI\";\n"
"    color: white;\n"
"    background-color: #5775dc;\n"
"    border-radius: 8px;\n"
"    padding: 6px 10px;\n"
"    border: 1px solid #5775dc;\n"
"    \n"
"    /* Tambahan pengaturan ukuran */\n"
"    min-width: 500px;    /* lebar minimum */\n"
"    max-width: 400px;    /* lebar maksimum */\n"
"    qproperty-alignment: AlignCenter; /* biar teks di tengah */\n"
"}\n"
"\n"
"")
        self.titlecontrolroom.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_39.addWidget(self.titlecontrolroom)


        self.verticalLayout_59.addWidget(self.titlecontrolroomFrame)

        self.controlroommainFrame = QFrame(self.page2_controlRoom)
        self.controlroommainFrame.setObjectName(u"controlroommainFrame")
        self.controlroommainFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.controlroommainFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_18 = QHBoxLayout(self.controlroommainFrame)
        self.horizontalLayout_18.setSpacing(0)
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.horizontalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.frameLamp = QFrame(self.controlroommainFrame)
        self.frameLamp.setObjectName(u"frameLamp")
        self.frameLamp.setFrameShape(QFrame.Shape.NoFrame)
        self.frameLamp.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_42 = QVBoxLayout(self.frameLamp)
        self.verticalLayout_42.setSpacing(25)
        self.verticalLayout_42.setObjectName(u"verticalLayout_42")
        self.verticalLayout_42.setContentsMargins(-1, 230, -1, 230)
        self.frameInsideLamp = QFrame(self.frameLamp)
        self.frameInsideLamp.setObjectName(u"frameInsideLamp")
        self.frameInsideLamp.setMinimumSize(QSize(0, 150))
        self.frameInsideLamp.setMaximumSize(QSize(16777215, 16777215))
        self.frameInsideLamp.setStyleSheet(u"#frameInsideLamp{\n"
"	background-color: #def0ff;        /* warna latar belakang (gelap elegan)  #c6e1f7 */\n"
"	border: 2px solid #cfe7fa;        /* ketebalan dan warna border */\n"
"	border-radius: 10px;              /* sudut melengkung */\n"
"}\n"
"")
        self.frameInsideLamp.setFrameShape(QFrame.Shape.NoFrame)
        self.frameInsideLamp.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_54 = QVBoxLayout(self.frameInsideLamp)
        self.verticalLayout_54.setSpacing(0)
        self.verticalLayout_54.setObjectName(u"verticalLayout_54")
        self.verticalLayout_54.setContentsMargins(0, 0, 0, 0)
        self.topLampFrame = QFrame(self.frameInsideLamp)
        self.topLampFrame.setObjectName(u"topLampFrame")
        self.topLampFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.topLampFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_33 = QHBoxLayout(self.topLampFrame)
        self.horizontalLayout_33.setObjectName(u"horizontalLayout_33")
        self.titleLamp = QLabel(self.topLampFrame)
        self.titleLamp.setObjectName(u"titleLamp")
        sizePolicy2.setHeightForWidth(self.titleLamp.sizePolicy().hasHeightForWidth())
        self.titleLamp.setSizePolicy(sizePolicy2)
        self.titleLamp.setMaximumSize(QSize(422, 45))
        self.titleLamp.setFont(font6)
        self.titleLamp.setStyleSheet(u"#titleLamp{\n"
"    font: bold 14pt \"Segoe UI\";\n"
"    color: white;\n"
"    background-color: #33A1E0;\n"
"    border-radius: 8px;\n"
"    padding: 6px 10px;\n"
"    border: 1px solid #33A1E0;\n"
"    \n"
"    /* Tambahan pengaturan ukuran */\n"
"    min-width: 500px;    /* lebar minimum */\n"
"    max-width: 400px;    /* lebar maksimum */\n"
"    qproperty-alignment: AlignCenter; /* biar teks di tengah */\n"
"}\n"
"")
        self.titleLamp.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_33.addWidget(self.titleLamp)


        self.verticalLayout_54.addWidget(self.topLampFrame)

        self.bottomLayout = QHBoxLayout()
        self.bottomLayout.setObjectName(u"bottomLayout")
        self.frameLamp1 = QFrame(self.frameInsideLamp)
        self.frameLamp1.setObjectName(u"frameLamp1")
        self.frameLamp1.setFrameShape(QFrame.Shape.NoFrame)
        self.frameLamp1.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_45 = QVBoxLayout(self.frameLamp1)
        self.verticalLayout_45.setObjectName(u"verticalLayout_45")
        self.frameLampInside1 = QVBoxLayout()
        self.frameLampInside1.setObjectName(u"frameLampInside1")
        self.frame_8 = QFrame(self.frameLamp1)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setMinimumSize(QSize(150, 40))
        self.frame_8.setMaximumSize(QSize(150, 40))
        self.frame_8.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_8.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_34 = QHBoxLayout(self.frame_8)
        self.horizontalLayout_34.setSpacing(0)
        self.horizontalLayout_34.setObjectName(u"horizontalLayout_34")
        self.horizontalLayout_34.setContentsMargins(0, 0, 0, 0)
        self.titlelampbtn_1 = QLabel(self.frame_8)
        self.titlelampbtn_1.setObjectName(u"titlelampbtn_1")
        sizePolicy2.setHeightForWidth(self.titlelampbtn_1.sizePolicy().hasHeightForWidth())
        self.titlelampbtn_1.setSizePolicy(sizePolicy2)
        self.titlelampbtn_1.setMaximumSize(QSize(136, 45))
        self.titlelampbtn_1.setFont(font8)
        self.titlelampbtn_1.setStyleSheet(u"#titlelampbtn_1 {\n"
"    font: bold 11pt \"Segoe UI\";\n"
"    color: white;\n"
"\n"
"    background-color: #7F9E9B;\n"
"    border: 1px solid #6E8E8B;\n"
"\n"
"\n"
"    border-radius: 8px;\n"
"    padding: 6px 12px;\n"
"    min-height: 26px;\n"
"    line-height: 18px;\n"
"\n"
"    min-width: 70px;\n"
"    max-width: 110px;\n"
"    qproperty-alignment: AlignCenter;\n"
"}\n"
"")
        self.titlelampbtn_1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_34.addWidget(self.titlelampbtn_1)


        self.frameLampInside1.addWidget(self.frame_8)

        self.framebtnlamp1 = QFrame(self.frameLamp1)
        self.framebtnlamp1.setObjectName(u"framebtnlamp1")
        self.framebtnlamp1.setMinimumSize(QSize(150, 180))
        self.framebtnlamp1.setMaximumSize(QSize(150, 180))
        self.framebtnlamp1.setFrameShape(QFrame.Shape.NoFrame)
        self.framebtnlamp1.setFrameShadow(QFrame.Shadow.Raised)

        self.frameLampInside1.addWidget(self.framebtnlamp1)


        self.verticalLayout_45.addLayout(self.frameLampInside1)


        self.bottomLayout.addWidget(self.frameLamp1)

        self.frameLamp2 = QFrame(self.frameInsideLamp)
        self.frameLamp2.setObjectName(u"frameLamp2")
        self.frameLamp2.setFrameShape(QFrame.Shape.NoFrame)
        self.frameLamp2.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_46 = QVBoxLayout(self.frameLamp2)
        self.verticalLayout_46.setObjectName(u"verticalLayout_46")
        self.verticalLayout_47 = QVBoxLayout()
        self.verticalLayout_47.setObjectName(u"verticalLayout_47")
        self.frame_12 = QFrame(self.frameLamp2)
        self.frame_12.setObjectName(u"frame_12")
        self.frame_12.setMinimumSize(QSize(150, 40))
        self.frame_12.setMaximumSize(QSize(150, 40))
        self.frame_12.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_12.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_35 = QHBoxLayout(self.frame_12)
        self.horizontalLayout_35.setSpacing(0)
        self.horizontalLayout_35.setObjectName(u"horizontalLayout_35")
        self.horizontalLayout_35.setContentsMargins(0, 0, 0, 0)
        self.titlelampbtn_2 = QLabel(self.frame_12)
        self.titlelampbtn_2.setObjectName(u"titlelampbtn_2")
        sizePolicy2.setHeightForWidth(self.titlelampbtn_2.sizePolicy().hasHeightForWidth())
        self.titlelampbtn_2.setSizePolicy(sizePolicy2)
        self.titlelampbtn_2.setMaximumSize(QSize(136, 45))
        self.titlelampbtn_2.setFont(font8)
        self.titlelampbtn_2.setStyleSheet(u"#titlelampbtn_2 {\n"
"    font: bold 11pt \"Segoe UI\";\n"
"    color: white;\n"
"\n"
"    background-color: #6FAFA3;   /* sage green pastel */\n"
"    border: 1px solid #5F9F93;\n"
"\n"
"    border-radius: 8px;\n"
"    padding: 6px 12px;\n"
"    min-height: 26px;\n"
"    line-height: 18px;\n"
"\n"
"    min-width: 70px;\n"
"    max-width: 110px;\n"
"    qproperty-alignment: AlignCenter;\n"
"}\n"
"")
        self.titlelampbtn_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_35.addWidget(self.titlelampbtn_2)


        self.verticalLayout_47.addWidget(self.frame_12)

        self.framebtnlamp2 = QFrame(self.frameLamp2)
        self.framebtnlamp2.setObjectName(u"framebtnlamp2")
        self.framebtnlamp2.setMinimumSize(QSize(150, 180))
        self.framebtnlamp2.setMaximumSize(QSize(150, 180))
        self.framebtnlamp2.setFrameShape(QFrame.Shape.NoFrame)
        self.framebtnlamp2.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout_47.addWidget(self.framebtnlamp2)


        self.verticalLayout_46.addLayout(self.verticalLayout_47)


        self.bottomLayout.addWidget(self.frameLamp2)

        self.frameLamp3 = QFrame(self.frameInsideLamp)
        self.frameLamp3.setObjectName(u"frameLamp3")
        self.frameLamp3.setFrameShape(QFrame.Shape.NoFrame)
        self.frameLamp3.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_48 = QVBoxLayout(self.frameLamp3)
        self.verticalLayout_48.setObjectName(u"verticalLayout_48")
        self.frameLampInside3 = QVBoxLayout()
        self.frameLampInside3.setObjectName(u"frameLampInside3")
        self.frame_15 = QFrame(self.frameLamp3)
        self.frame_15.setObjectName(u"frame_15")
        self.frame_15.setMinimumSize(QSize(150, 40))
        self.frame_15.setMaximumSize(QSize(150, 40))
        self.frame_15.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_15.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_36 = QHBoxLayout(self.frame_15)
        self.horizontalLayout_36.setSpacing(0)
        self.horizontalLayout_36.setObjectName(u"horizontalLayout_36")
        self.horizontalLayout_36.setContentsMargins(0, 0, 0, 0)
        self.titlelampbtn_3 = QLabel(self.frame_15)
        self.titlelampbtn_3.setObjectName(u"titlelampbtn_3")
        sizePolicy2.setHeightForWidth(self.titlelampbtn_3.sizePolicy().hasHeightForWidth())
        self.titlelampbtn_3.setSizePolicy(sizePolicy2)
        self.titlelampbtn_3.setMaximumSize(QSize(136, 45))
        self.titlelampbtn_3.setFont(font8)
        self.titlelampbtn_3.setStyleSheet(u"#titlelampbtn_3 {\n"
"    font: bold 11pt \"Segoe UI\";\n"
"    color: white;\n"
"\n"
"    background-color: #7F9E9B;\n"
"    border: 1px solid #6E8E8B;\n"
"\n"
"\n"
"    border-radius: 8px;\n"
"    padding: 6px 12px;\n"
"    min-height: 26px;\n"
"    line-height: 18px;\n"
"\n"
"    min-width: 70px;\n"
"    max-width: 110px;\n"
"    qproperty-alignment: AlignCenter;\n"
"}\n"
"")
        self.titlelampbtn_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_36.addWidget(self.titlelampbtn_3)


        self.frameLampInside3.addWidget(self.frame_15)

        self.framebtnlamp3 = QFrame(self.frameLamp3)
        self.framebtnlamp3.setObjectName(u"framebtnlamp3")
        self.framebtnlamp3.setMinimumSize(QSize(150, 180))
        self.framebtnlamp3.setMaximumSize(QSize(150, 180))
        self.framebtnlamp3.setFrameShape(QFrame.Shape.NoFrame)
        self.framebtnlamp3.setFrameShadow(QFrame.Shadow.Raised)

        self.frameLampInside3.addWidget(self.framebtnlamp3)


        self.verticalLayout_48.addLayout(self.frameLampInside3)


        self.bottomLayout.addWidget(self.frameLamp3)

        self.frameLamp4 = QFrame(self.frameInsideLamp)
        self.frameLamp4.setObjectName(u"frameLamp4")
        self.frameLamp4.setFrameShape(QFrame.Shape.NoFrame)
        self.frameLamp4.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_50 = QVBoxLayout(self.frameLamp4)
        self.verticalLayout_50.setObjectName(u"verticalLayout_50")
        self.frameLampInside4 = QVBoxLayout()
        self.frameLampInside4.setObjectName(u"frameLampInside4")
        self.frame_19 = QFrame(self.frameLamp4)
        self.frame_19.setObjectName(u"frame_19")
        self.frame_19.setMinimumSize(QSize(150, 40))
        self.frame_19.setMaximumSize(QSize(150, 40))
        self.frame_19.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_19.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_37 = QHBoxLayout(self.frame_19)
        self.horizontalLayout_37.setSpacing(0)
        self.horizontalLayout_37.setObjectName(u"horizontalLayout_37")
        self.horizontalLayout_37.setContentsMargins(0, 0, 0, 0)
        self.titlelampbtn_4 = QLabel(self.frame_19)
        self.titlelampbtn_4.setObjectName(u"titlelampbtn_4")
        sizePolicy2.setHeightForWidth(self.titlelampbtn_4.sizePolicy().hasHeightForWidth())
        self.titlelampbtn_4.setSizePolicy(sizePolicy2)
        self.titlelampbtn_4.setMaximumSize(QSize(136, 45))
        self.titlelampbtn_4.setFont(font8)
        self.titlelampbtn_4.setStyleSheet(u"#titlelampbtn_4 {\n"
"    font: bold 11pt \"Segoe UI\";\n"
"    color: white;\n"
"\n"
"    background-color: #6FAFA3;   /* sage green pastel */\n"
"    border: 1px solid #5F9F93;\n"
"\n"
"    border-radius: 8px;\n"
"    padding: 6px 12px;\n"
"    min-height: 26px;\n"
"    line-height: 18px;\n"
"\n"
"    min-width: 70px;\n"
"    max-width: 110px;\n"
"    qproperty-alignment: AlignCenter;\n"
"}\n"
"")
        self.titlelampbtn_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_37.addWidget(self.titlelampbtn_4)


        self.frameLampInside4.addWidget(self.frame_19)

        self.framebtnlamp4 = QFrame(self.frameLamp4)
        self.framebtnlamp4.setObjectName(u"framebtnlamp4")
        self.framebtnlamp4.setMinimumSize(QSize(150, 180))
        self.framebtnlamp4.setMaximumSize(QSize(150, 180))
        self.framebtnlamp4.setFrameShape(QFrame.Shape.NoFrame)
        self.framebtnlamp4.setFrameShadow(QFrame.Shadow.Raised)

        self.frameLampInside4.addWidget(self.framebtnlamp4)


        self.verticalLayout_50.addLayout(self.frameLampInside4)


        self.bottomLayout.addWidget(self.frameLamp4)

        self.frameLamp5 = QFrame(self.frameInsideLamp)
        self.frameLamp5.setObjectName(u"frameLamp5")
        self.frameLamp5.setStyleSheet(u"")
        self.frameLamp5.setFrameShape(QFrame.Shape.NoFrame)
        self.frameLamp5.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_52 = QVBoxLayout(self.frameLamp5)
        self.verticalLayout_52.setObjectName(u"verticalLayout_52")
        self.frameLampInside5 = QVBoxLayout()
        self.frameLampInside5.setObjectName(u"frameLampInside5")
        self.frame_22 = QFrame(self.frameLamp5)
        self.frame_22.setObjectName(u"frame_22")
        self.frame_22.setMinimumSize(QSize(150, 40))
        self.frame_22.setMaximumSize(QSize(150, 40))
        self.frame_22.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_22.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_38 = QHBoxLayout(self.frame_22)
        self.horizontalLayout_38.setSpacing(0)
        self.horizontalLayout_38.setObjectName(u"horizontalLayout_38")
        self.horizontalLayout_38.setContentsMargins(0, 0, 0, 0)
        self.titlelampbtn_5 = QLabel(self.frame_22)
        self.titlelampbtn_5.setObjectName(u"titlelampbtn_5")
        sizePolicy2.setHeightForWidth(self.titlelampbtn_5.sizePolicy().hasHeightForWidth())
        self.titlelampbtn_5.setSizePolicy(sizePolicy2)
        self.titlelampbtn_5.setMaximumSize(QSize(136, 45))
        self.titlelampbtn_5.setFont(font8)
        self.titlelampbtn_5.setStyleSheet(u"#titlelampbtn_5 {\n"
"    font: bold 11pt \"Segoe UI\";\n"
"    color: white;\n"
"\n"
"    background-color: #7F9E9B;\n"
"    border: 1px solid #6E8E8B;\n"
"\n"
"\n"
"    border-radius: 8px;\n"
"    padding: 6px 12px;\n"
"    min-height: 26px;\n"
"    line-height: 18px;\n"
"\n"
"    min-width: 70px;\n"
"    max-width: 110px;\n"
"    qproperty-alignment: AlignCenter;\n"
"}\n"
"")
        self.titlelampbtn_5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_38.addWidget(self.titlelampbtn_5)


        self.frameLampInside5.addWidget(self.frame_22)

        self.framebtnlamp5 = QFrame(self.frameLamp5)
        self.framebtnlamp5.setObjectName(u"framebtnlamp5")
        self.framebtnlamp5.setMinimumSize(QSize(150, 180))
        self.framebtnlamp5.setMaximumSize(QSize(150, 180))
        self.framebtnlamp5.setFrameShape(QFrame.Shape.NoFrame)
        self.framebtnlamp5.setFrameShadow(QFrame.Shadow.Raised)

        self.frameLampInside5.addWidget(self.framebtnlamp5)


        self.verticalLayout_52.addLayout(self.frameLampInside5)


        self.bottomLayout.addWidget(self.frameLamp5)


        self.verticalLayout_54.addLayout(self.bottomLayout)


        self.verticalLayout_42.addWidget(self.frameInsideLamp)

        self.horizontalLayout_84 = QHBoxLayout()
        self.horizontalLayout_84.setObjectName(u"horizontalLayout_84")
        self.frame_53 = QFrame(self.frameLamp)
        self.frame_53.setObjectName(u"frame_53")
        self.frame_53.setMinimumSize(QSize(0, 0))
        self.frame_53.setMaximumSize(QSize(16777215, 23))
        self.frame_53.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_53.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_84.addWidget(self.frame_53)

        self.statusmcuA = QLabel(self.frameLamp)
        self.statusmcuA.setObjectName(u"statusmcuA")
        sizePolicy2.setHeightForWidth(self.statusmcuA.sizePolicy().hasHeightForWidth())
        self.statusmcuA.setSizePolicy(sizePolicy2)
        self.statusmcuA.setMinimumSize(QSize(114, 23))
        self.statusmcuA.setMaximumSize(QSize(114, 23))
        self.statusmcuA.setFont(font2)
        self.statusmcuA.setStyleSheet(u"QLabel#statusmcuA{\n"
"    font: bold 10pt \"Segoe UI\";\n"
"    color: white;\n"
"\n"
"    background-color: #CBD5E1;   /* default (abu netral) */\n"
"    border: 1px solid #94A3B8;\n"
"    border-radius: 4px;\n"
"\n"
"    padding: 2px 6px;\n"
"    min-height: 17px;\n"
"    max-width: 100px;\n"
"\n"
"    qproperty-alignment: AlignCenter;\n"
"}\n"
"\n"
"/* ===== AC ON ===== */\n"
"QLabel#statusmcuA[state=\"on\"] {\n"
"    background-color: #6FCF97;   /* hijau pastel tapi jelas */\n"
"    border-color: #27AE60;\n"
"}\n"
"\n"
"/* ===== AC OFF ===== */\n"
"QLabel#statusmcuA[state=\"off\"] {\n"
"    background-color: #EB5757;   /* merah pastel tegas */\n"
"    border-color: #C0392B;\n"
"}\n"
"")
        self.statusmcuA.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_84.addWidget(self.statusmcuA)

        self.frame_55 = QFrame(self.frameLamp)
        self.frame_55.setObjectName(u"frame_55")
        self.frame_55.setMaximumSize(QSize(16777215, 23))
        self.frame_55.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_55.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_84.addWidget(self.frame_55)


        self.verticalLayout_42.addLayout(self.horizontalLayout_84)


        self.horizontalLayout_18.addWidget(self.frameLamp)

        self.frameAC = QFrame(self.controlroommainFrame)
        self.frameAC.setObjectName(u"frameAC")
        self.frameAC.setFrameShape(QFrame.Shape.NoFrame)
        self.frameAC.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_43 = QVBoxLayout(self.frameAC)
        self.verticalLayout_43.setSpacing(25)
        self.verticalLayout_43.setObjectName(u"verticalLayout_43")
        self.verticalLayout_43.setContentsMargins(-1, 230, -1, 230)
        self.frameInsideAC = QFrame(self.frameAC)
        self.frameInsideAC.setObjectName(u"frameInsideAC")
        self.frameInsideAC.setMinimumSize(QSize(150, 150))
        self.frameInsideAC.setStyleSheet(u"#frameInsideAC{\n"
"	background-color: #def0ff;        /* warna latar belakang (gelap elegan)  #c6e1f7 */\n"
"	border: 2px solid #cfe7fa;        /* ketebalan dan warna border */\n"
"	border-radius: 10px;              /* sudut melengkung */\n"
"}\n"
"")
        self.frameInsideAC.setFrameShape(QFrame.Shape.NoFrame)
        self.frameInsideAC.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_57 = QVBoxLayout(self.frameInsideAC)
        self.verticalLayout_57.setSpacing(0)
        self.verticalLayout_57.setObjectName(u"verticalLayout_57")
        self.verticalLayout_57.setContentsMargins(0, 0, 0, 35)
        self.topFrameAC = QFrame(self.frameInsideAC)
        self.topFrameAC.setObjectName(u"topFrameAC")
        self.topFrameAC.setMinimumSize(QSize(0, 0))
        self.topFrameAC.setFrameShape(QFrame.Shape.NoFrame)
        self.topFrameAC.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_40 = QHBoxLayout(self.topFrameAC)
        self.horizontalLayout_40.setObjectName(u"horizontalLayout_40")
        self.horizontalLayout_40.setContentsMargins(-1, 25, -1, -1)
        self.titleAC = QLabel(self.topFrameAC)
        self.titleAC.setObjectName(u"titleAC")
        sizePolicy2.setHeightForWidth(self.titleAC.sizePolicy().hasHeightForWidth())
        self.titleAC.setSizePolicy(sizePolicy2)
        self.titleAC.setMaximumSize(QSize(422, 45))
        self.titleAC.setFont(font6)
        self.titleAC.setStyleSheet(u"#titleAC{\n"
"    font: bold 14pt \"Segoe UI\";\n"
"    color: white;\n"
"    background-color: #33A1E0;\n"
"    border-radius: 8px;\n"
"    padding: 6px 10px;\n"
"    border: 1px solid #33A1E0;\n"
"    \n"
"    /* Tambahan pengaturan ukuran */\n"
"    min-width: 500px;    /* lebar minimum */\n"
"    max-width: 400px;    /* lebar maksimum */\n"
"    qproperty-alignment: AlignCenter; /* biar teks di tengah */\n"
"}\n"
"")
        self.titleAC.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_40.addWidget(self.titleAC)


        self.verticalLayout_57.addWidget(self.topFrameAC)

        self.midACframe = QFrame(self.frameInsideAC)
        self.midACframe.setObjectName(u"midACframe")
        self.midACframe.setFrameShape(QFrame.Shape.NoFrame)
        self.midACframe.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_55 = QVBoxLayout(self.midACframe)
        self.verticalLayout_55.setSpacing(0)
        self.verticalLayout_55.setObjectName(u"verticalLayout_55")
        self.verticalLayout_55.setContentsMargins(-1, 0, -1, 9)
        self.framebuttonoutsideAC = QFrame(self.midACframe)
        self.framebuttonoutsideAC.setObjectName(u"framebuttonoutsideAC")
        self.framebuttonoutsideAC.setFrameShape(QFrame.Shape.NoFrame)
        self.framebuttonoutsideAC.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_43 = QHBoxLayout(self.framebuttonoutsideAC)
        self.horizontalLayout_43.setSpacing(0)
        self.horizontalLayout_43.setObjectName(u"horizontalLayout_43")
        self.horizontalLayout_43.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(self.framebuttonoutsideAC)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.NoFrame)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_43.addWidget(self.frame)

        self.frameButtonOnOffAC = QFrame(self.framebuttonoutsideAC)
        self.frameButtonOnOffAC.setObjectName(u"frameButtonOnOffAC")
        self.frameButtonOnOffAC.setMinimumSize(QSize(160, 60))
        self.frameButtonOnOffAC.setMaximumSize(QSize(160, 60))
        self.frameButtonOnOffAC.setFrameShape(QFrame.Shape.NoFrame)
        self.frameButtonOnOffAC.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_43.addWidget(self.frameButtonOnOffAC)

        self.frame_2 = QFrame(self.framebuttonoutsideAC)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_43.addWidget(self.frame_2)


        self.verticalLayout_55.addWidget(self.framebuttonoutsideAC)

        self.frameNoteStatusAC = QFrame(self.midACframe)
        self.frameNoteStatusAC.setObjectName(u"frameNoteStatusAC")
        self.frameNoteStatusAC.setMinimumSize(QSize(82, 17))
        self.frameNoteStatusAC.setMaximumSize(QSize(16777215, 60))
        self.frameNoteStatusAC.setFrameShape(QFrame.Shape.NoFrame)
        self.frameNoteStatusAC.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_42 = QHBoxLayout(self.frameNoteStatusAC)
        self.horizontalLayout_42.setObjectName(u"horizontalLayout_42")
        self.horizontalLayout_42.setContentsMargins(0, 0, 0, 0)
        self.statusAC = QLabel(self.frameNoteStatusAC)
        self.statusAC.setObjectName(u"statusAC")
        sizePolicy2.setHeightForWidth(self.statusAC.sizePolicy().hasHeightForWidth())
        self.statusAC.setSizePolicy(sizePolicy2)
        self.statusAC.setMinimumSize(QSize(0, 23))
        self.statusAC.setMaximumSize(QSize(114, 17))
        self.statusAC.setFont(font2)
        self.statusAC.setStyleSheet(u"QLabel#statusAC {\n"
"    font: bold 10pt \"Segoe UI\";\n"
"    color: white;\n"
"\n"
"    background-color: #CBD5E1;   /* default (abu netral) */\n"
"    border: 1px solid #94A3B8;\n"
"    border-radius: 4px;\n"
"\n"
"    padding: 2px 6px;\n"
"    min-height: 17px;\n"
"    max-width: 100px;\n"
"\n"
"    qproperty-alignment: AlignCenter;\n"
"}\n"
"\n"
"/* ===== AC ON ===== */\n"
"QLabel#statusAC[state=\"on\"] {\n"
"    background-color: #6FCF97;   /* hijau pastel tapi jelas */\n"
"    border-color: #27AE60;\n"
"}\n"
"\n"
"/* ===== AC OFF ===== */\n"
"QLabel#statusAC[state=\"off\"] {\n"
"    background-color: #EB5757;   /* merah pastel tegas */\n"
"    border-color: #C0392B;\n"
"}\n"
"")
        self.statusAC.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_42.addWidget(self.statusAC)


        self.verticalLayout_55.addWidget(self.frameNoteStatusAC)


        self.verticalLayout_57.addWidget(self.midACframe)

        self.bottomACframe = QFrame(self.frameInsideAC)
        self.bottomACframe.setObjectName(u"bottomACframe")
        self.bottomACframe.setFrameShape(QFrame.Shape.NoFrame)
        self.bottomACframe.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_41 = QHBoxLayout(self.bottomACframe)
        self.horizontalLayout_41.setSpacing(19)
        self.horizontalLayout_41.setObjectName(u"horizontalLayout_41")
        self.unusedACframe2 = QFrame(self.bottomACframe)
        self.unusedACframe2.setObjectName(u"unusedACframe2")
        self.unusedACframe2.setFrameShape(QFrame.Shape.NoFrame)
        self.unusedACframe2.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_41.addWidget(self.unusedACframe2)

        self.verticalLayout_56 = QVBoxLayout()
        self.verticalLayout_56.setSpacing(10)
        self.verticalLayout_56.setObjectName(u"verticalLayout_56")
        self.btn_temp_up = QPushButton(self.bottomACframe)
        self.btn_temp_up.setObjectName(u"btn_temp_up")
        self.btn_temp_up.setMinimumSize(QSize(150, 50))
        self.btn_temp_up.setMaximumSize(QSize(150, 50))
        self.btn_temp_up.setStyleSheet(u"QPushButton {\n"
"    background-color: #637AB9;        /* biru keunguan elegan */\n"
"    border: 2px solid #5066A4;        /* sedikit lebih gelap untuk kontras */\n"
"    border-radius: 8px;\n"
"    color: white;                     /* teks putih biar jelas */\n"
"    font: 12pt \"Segoe UI\";\n"
"    font-weight: bold;\n"
"    padding: 6px 14px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #6F87C5;        /* sedikit lebih terang saat hover */\n"
"    border: 2px solid #4E61A0;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #5569A8;        /* sedikit lebih gelap saat ditekan */\n"
"    border: 2px solid #45568E;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    background-color: #A8B4DA;        /* versi redup */\n"
"    color: #E8EBF7;\n"
"    border: 2px solid #96A4C8;\n"
"}\n"
"")

        self.verticalLayout_56.addWidget(self.btn_temp_up)

        self.btn_temp_down = QPushButton(self.bottomACframe)
        self.btn_temp_down.setObjectName(u"btn_temp_down")
        self.btn_temp_down.setMinimumSize(QSize(150, 50))
        self.btn_temp_down.setMaximumSize(QSize(150, 50))
        self.btn_temp_down.setStyleSheet(u"QPushButton {\n"
"    background-color: #637AB9;        /* biru keunguan elegan */\n"
"    border: 2px solid #5066A4;        /* sedikit lebih gelap untuk kontras */\n"
"    border-radius: 8px;\n"
"    color: white;                     /* teks putih biar jelas */\n"
"    font: 12pt \"Segoe UI\";\n"
"    font-weight: bold;\n"
"    padding: 6px 14px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #6F87C5;        /* sedikit lebih terang saat hover */\n"
"    border: 2px solid #4E61A0;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #5569A8;        /* sedikit lebih gelap saat ditekan */\n"
"    border: 2px solid #45568E;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    background-color: #A8B4DA;        /* versi redup */\n"
"    color: #E8EBF7;\n"
"    border: 2px solid #96A4C8;\n"
"}\n"
"")

        self.verticalLayout_56.addWidget(self.btn_temp_down)


        self.horizontalLayout_41.addLayout(self.verticalLayout_56)

        self.verticalLayout_58 = QVBoxLayout()
        self.verticalLayout_58.setSpacing(10)
        self.verticalLayout_58.setObjectName(u"verticalLayout_58")
        self.btn_cool_ac = QPushButton(self.bottomACframe)
        self.btn_cool_ac.setObjectName(u"btn_cool_ac")
        self.btn_cool_ac.setMinimumSize(QSize(150, 50))
        self.btn_cool_ac.setMaximumSize(QSize(150, 50))
        self.btn_cool_ac.setStyleSheet(u"QPushButton {\n"
"    background-color: #77CDFF;       /* biru muda utama */\n"
"    border: 2px solid #5BB8E8;       /* sedikit lebih gelap buat kontras */\n"
"    border-radius: 8px;\n"
"    color: white;                    /* teks putih agar jelas */\n"
"    font: 12pt \"Segoe UI\";\n"
"    font-weight: bold;\n"
"    padding: 6px 14px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #8BD7FF;       /* sedikit lebih terang saat hover */\n"
"    border: 2px solid #52AEE0;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #63C0F2;       /* sedikit lebih gelap saat ditekan */\n"
"    border: 2px solid #4AA3D6;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    background-color: #BDE8FF;       /* versi redup */\n"
"    color: #E6F6FF;\n"
"    border: 2px solid #A3DBF5;\n"
"}\n"
"")

        self.verticalLayout_58.addWidget(self.btn_cool_ac)

        self.btn_fan_ac = QPushButton(self.bottomACframe)
        self.btn_fan_ac.setObjectName(u"btn_fan_ac")
        self.btn_fan_ac.setMinimumSize(QSize(150, 50))
        self.btn_fan_ac.setMaximumSize(QSize(150, 50))
        self.btn_fan_ac.setStyleSheet(u"QPushButton {\n"
"    background-color: #58B368;       /* hijau lembut tapi hidup */\n"
"    border: 2px solid #4A9A59;\n"
"    border-radius: 8px;\n"
"    color: white;\n"
"    font: 12pt \"Segoe UI\";\n"
"    font-weight: bold;\n"
"    padding: 6px 14px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #68C179;\n"
"    border: 2px solid #3E874D;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: #4C9957;\n"
"    border: 2px solid #3A7A44;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    background-color: #A7D9B0;\n"
"    color: #EAF6EC;\n"
"    border: 2px solid #8BC59A;\n"
"}\n"
"")

        self.verticalLayout_58.addWidget(self.btn_fan_ac)


        self.horizontalLayout_41.addLayout(self.verticalLayout_58)

        self.unusedACframe1 = QFrame(self.bottomACframe)
        self.unusedACframe1.setObjectName(u"unusedACframe1")
        self.unusedACframe1.setFrameShape(QFrame.Shape.NoFrame)
        self.unusedACframe1.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_41.addWidget(self.unusedACframe1)


        self.verticalLayout_57.addWidget(self.bottomACframe)


        self.verticalLayout_43.addWidget(self.frameInsideAC)

        self.horizontalLayout_86 = QHBoxLayout()
        self.horizontalLayout_86.setObjectName(u"horizontalLayout_86")
        self.frame_56 = QFrame(self.frameAC)
        self.frame_56.setObjectName(u"frame_56")
        self.frame_56.setMinimumSize(QSize(0, 0))
        self.frame_56.setMaximumSize(QSize(16777215, 23))
        self.frame_56.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_56.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_86.addWidget(self.frame_56)

        self.statusmcuB = QLabel(self.frameAC)
        self.statusmcuB.setObjectName(u"statusmcuB")
        sizePolicy2.setHeightForWidth(self.statusmcuB.sizePolicy().hasHeightForWidth())
        self.statusmcuB.setSizePolicy(sizePolicy2)
        self.statusmcuB.setMinimumSize(QSize(114, 23))
        self.statusmcuB.setMaximumSize(QSize(114, 23))
        self.statusmcuB.setFont(font2)
        self.statusmcuB.setStyleSheet(u"QLabel#statusmcuB{\n"
"    font: bold 10pt \"Segoe UI\";\n"
"    color: white;\n"
"\n"
"    background-color: #CBD5E1;   /* default (abu netral) */\n"
"    border: 1px solid #94A3B8;\n"
"    border-radius: 4px;\n"
"\n"
"    padding: 2px 6px;\n"
"    min-height: 17px;\n"
"    max-width: 100px;\n"
"\n"
"    qproperty-alignment: AlignCenter;\n"
"}\n"
"\n"
"/* ===== AC ON ===== */\n"
"QLabel#statusmcuB[state=\"on\"] {\n"
"    background-color: #6FCF97;   /* hijau pastel tapi jelas */\n"
"    border-color: #27AE60;\n"
"}\n"
"\n"
"/* ===== AC OFF ===== */\n"
"QLabel#statusmcuB[state=\"off\"] {\n"
"    background-color: #EB5757;   /* merah pastel tegas */\n"
"    border-color: #C0392B;\n"
"}\n"
"")
        self.statusmcuB.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_86.addWidget(self.statusmcuB)

        self.frame_63 = QFrame(self.frameAC)
        self.frame_63.setObjectName(u"frame_63")
        self.frame_63.setMaximumSize(QSize(16777215, 23))
        self.frame_63.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_63.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_86.addWidget(self.frame_63)


        self.verticalLayout_43.addLayout(self.horizontalLayout_86)


        self.horizontalLayout_18.addWidget(self.frameAC)


        self.verticalLayout_59.addWidget(self.controlroommainFrame)

        self.stackedWidget.addWidget(self.page2_controlRoom)
        self.page3_monitoringSensor = QWidget()
        self.page3_monitoringSensor.setObjectName(u"page3_monitoringSensor")
        self.verticalLayout_44 = QVBoxLayout(self.page3_monitoringSensor)
        self.verticalLayout_44.setObjectName(u"verticalLayout_44")
        self.titlemonitoringsensorFrame = QFrame(self.page3_monitoringSensor)
        self.titlemonitoringsensorFrame.setObjectName(u"titlemonitoringsensorFrame")
        self.titlemonitoringsensorFrame.setMaximumSize(QSize(16777215, 65))
        self.titlemonitoringsensorFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.titlemonitoringsensorFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_44 = QHBoxLayout(self.titlemonitoringsensorFrame)
        self.horizontalLayout_44.setSpacing(0)
        self.horizontalLayout_44.setObjectName(u"horizontalLayout_44")
        self.horizontalLayout_44.setContentsMargins(0, 5, -1, 0)
        self.titlemonitoring = QLabel(self.titlemonitoringsensorFrame)
        self.titlemonitoring.setObjectName(u"titlemonitoring")
        sizePolicy2.setHeightForWidth(self.titlemonitoring.sizePolicy().hasHeightForWidth())
        self.titlemonitoring.setSizePolicy(sizePolicy2)
        self.titlemonitoring.setMaximumSize(QSize(422, 45))
        self.titlemonitoring.setFont(font6)
        self.titlemonitoring.setStyleSheet(u"#titlemonitoring {\n"
"    font: bold 14pt \"Segoe UI\";\n"
"    color: white;\n"
"    background-color: #5775dc;\n"
"    border-radius: 8px;\n"
"    padding: 6px 10px;\n"
"    border: 1px solid #5775dc;\n"
"    \n"
"    /* Tambahan pengaturan ukuran */\n"
"    min-width: 500px;    /* lebar minimum */\n"
"    max-width: 400px;    /* lebar maksimum */\n"
"    qproperty-alignment: AlignCenter; /* biar teks di tengah */\n"
"}\n"
"\n"
"")
        self.titlemonitoring.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_44.addWidget(self.titlemonitoring)


        self.verticalLayout_44.addWidget(self.titlemonitoringsensorFrame)

        self.frame_3 = QFrame(self.page3_monitoringSensor)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_32 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_32.setSpacing(8)
        self.horizontalLayout_32.setObjectName(u"horizontalLayout_32")
        self.horizontalLayout_32.setContentsMargins(0, 0, 0, 0)
        self.frameIndoor = QFrame(self.frame_3)
        self.frameIndoor.setObjectName(u"frameIndoor")
        self.frameIndoor.setMaximumSize(QSize(16777215, 600))
        self.frameIndoor.setStyleSheet(u"#frameIndoor {\n"
"    background-color: #EDF6FC;   /* biru sangat pucat */\n"
"\n"
"    border: 1.5px solid transparent;\n"
"    border-radius: 12px;\n"
"\n"
"    /*border-image: url(:/images/images/images/bg9.png) 12 12 12 12 stretch stretch;*/\n"
"}\n"
"")
        self.frameIndoor.setFrameShape(QFrame.Shape.NoFrame)
        self.frameIndoor.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_49 = QVBoxLayout(self.frameIndoor)
        self.verticalLayout_49.setObjectName(u"verticalLayout_49")
        self.verticalLayout_49.setContentsMargins(50, 50, 50, 50)
        self.frame_7 = QFrame(self.frameIndoor)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setMaximumSize(QSize(16777215, 538))
        self.frame_7.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_7.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_51 = QVBoxLayout(self.frame_7)
        self.verticalLayout_51.setObjectName(u"verticalLayout_51")
        self.verticalLayout_51.setContentsMargins(0, 0, 0, 0)
        self.IndoorTitleFrame = QFrame(self.frame_7)
        self.IndoorTitleFrame.setObjectName(u"IndoorTitleFrame")
        self.IndoorTitleFrame.setMaximumSize(QSize(16777215, 100))
        self.IndoorTitleFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.IndoorTitleFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_83 = QHBoxLayout(self.IndoorTitleFrame)
        self.horizontalLayout_83.setObjectName(u"horizontalLayout_83")
        self.frame_10 = QFrame(self.IndoorTitleFrame)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_10.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_83.addWidget(self.frame_10)

        self.titleIndoor = QLabel(self.IndoorTitleFrame)
        self.titleIndoor.setObjectName(u"titleIndoor")
        sizePolicy2.setHeightForWidth(self.titleIndoor.sizePolicy().hasHeightForWidth())
        self.titleIndoor.setSizePolicy(sizePolicy2)
        self.titleIndoor.setMinimumSize(QSize(522, 40))
        self.titleIndoor.setMaximumSize(QSize(422, 45))
        self.titleIndoor.setFont(font6)
        self.titleIndoor.setStyleSheet(u"#titleIndoor{\n"
"    font: bold 14pt \"Segoe UI\";\n"
"    color: white;\n"
"    background-color: #33A1E0;\n"
"    border-radius: 8px;\n"
"    padding: 6px 10px;\n"
"    border: 1px solid #33A1E0;\n"
"    \n"
"    /* Tambahan pengaturan ukuran */\n"
"    min-width: 500px;    /* lebar minimum */\n"
"    max-width: 400px;    /* lebar maksimum */\n"
"    qproperty-alignment: AlignCenter; /* biar teks di tengah */\n"
"}\n"
"")
        self.titleIndoor.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_83.addWidget(self.titleIndoor)

        self.frame_51 = QFrame(self.IndoorTitleFrame)
        self.frame_51.setObjectName(u"frame_51")
        self.frame_51.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_51.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_83.addWidget(self.frame_51)


        self.verticalLayout_51.addWidget(self.IndoorTitleFrame)

        self.verticalSpacer_21 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_51.addItem(self.verticalSpacer_21)

        self.frame_5 = QFrame(self.frame_7)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_45 = QHBoxLayout(self.frame_5)
        self.horizontalLayout_45.setSpacing(10)
        self.horizontalLayout_45.setObjectName(u"horizontalLayout_45")
        self.horizontalLayout_45.setContentsMargins(0, 0, 0, 0)
        self.frameTempIndoor = QFrame(self.frame_5)
        self.frameTempIndoor.setObjectName(u"frameTempIndoor")
        self.frameTempIndoor.setMinimumSize(QSize(0, 374))
        self.frameTempIndoor.setMaximumSize(QSize(16777215, 374))
        self.frameTempIndoor.setStyleSheet(u"#frameTempIndoor{\n"
"    background-color: #FFF3E6;   /* cream orange muda */\n"
"    border: 2px solid #FFD6B0;   /* peach soft */\n"
"    border-radius: 10px\n"
"}\n"
"")
        self.frameTempIndoor.setFrameShape(QFrame.Shape.NoFrame)
        self.frameTempIndoor.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_53 = QVBoxLayout(self.frameTempIndoor)
        self.verticalLayout_53.setSpacing(0)
        self.verticalLayout_53.setObjectName(u"verticalLayout_53")
        self.verticalLayout_53.setContentsMargins(0, 0, 0, 0)
        self.frame_11 = QFrame(self.frameTempIndoor)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setMinimumSize(QSize(0, 100))
        self.frame_11.setMaximumSize(QSize(16777215, 100))
        self.frame_11.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_11.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_47 = QHBoxLayout(self.frame_11)
        self.horizontalLayout_47.setObjectName(u"horizontalLayout_47")
        self.titleSuhuIndoor = QLabel(self.frame_11)
        self.titleSuhuIndoor.setObjectName(u"titleSuhuIndoor")
        sizePolicy2.setHeightForWidth(self.titleSuhuIndoor.sizePolicy().hasHeightForWidth())
        self.titleSuhuIndoor.setSizePolicy(sizePolicy2)
        self.titleSuhuIndoor.setMaximumSize(QSize(322, 45))
        self.titleSuhuIndoor.setFont(font6)
        self.titleSuhuIndoor.setStyleSheet(u"#titleSuhuIndoor{\n"
"    font: bold 14pt \"Segoe UI\";\n"
"    color: white;\n"
"    background-color: #F4A261;   /* orange lembut */\n"
"    border-radius: 8px;\n"
"    padding: 6px 10px;\n"
"    border: 1px solid #F4A261;\n"
"    \n"
"    min-width: 200px;\n"
"    max-width: 300px;\n"
"    qproperty-alignment: AlignCenter;\n"
"}\n"
"")
        self.titleSuhuIndoor.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_47.addWidget(self.titleSuhuIndoor)


        self.verticalLayout_53.addWidget(self.frame_11)

        self.frame_13 = QFrame(self.frameTempIndoor)
        self.frame_13.setObjectName(u"frame_13")
        self.frame_13.setMinimumSize(QSize(0, 270))
        self.frame_13.setMaximumSize(QSize(16777215, 270))
        self.frame_13.setStyleSheet(u"tempIndoor_value")
        self.frame_13.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_13.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_46 = QHBoxLayout(self.frame_13)
        self.horizontalLayout_46.setObjectName(u"horizontalLayout_46")
        self.tempIndoor_value = QLabel(self.frame_13)
        self.tempIndoor_value.setObjectName(u"tempIndoor_value")
        sizePolicy2.setHeightForWidth(self.tempIndoor_value.sizePolicy().hasHeightForWidth())
        self.tempIndoor_value.setSizePolicy(sizePolicy2)
        self.tempIndoor_value.setMaximumSize(QSize(16777215, 9999999))
        font9 = QFont()
        font9.setFamilies([u"Segoe UI"])
        font9.setPointSize(34)
        font9.setBold(True)
        font9.setItalic(False)
        self.tempIndoor_value.setFont(font9)
        self.tempIndoor_value.setStyleSheet(u"#tempIndoor_value{\n"
"    font: bold 34pt \"Segoe UI\";\n"
"    color: black;\n"
"}\n"
"")
        self.tempIndoor_value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_46.addWidget(self.tempIndoor_value)


        self.verticalLayout_53.addWidget(self.frame_13)


        self.horizontalLayout_45.addWidget(self.frameTempIndoor)

        self.frameHumidIndoor = QFrame(self.frame_5)
        self.frameHumidIndoor.setObjectName(u"frameHumidIndoor")
        self.frameHumidIndoor.setMinimumSize(QSize(0, 374))
        self.frameHumidIndoor.setMaximumSize(QSize(16777215, 374))
        self.frameHumidIndoor.setStyleSheet(u"#frameHumidIndoor{\n"
"background-color: #EAF7F4;   /* hijau sangat muda */\n"
"border: 2px solid #CDE6E0;   /* hijau abu soft */\n"
"border-radius: 10px;\n"
"}\n"
"")
        self.frameHumidIndoor.setFrameShape(QFrame.Shape.NoFrame)
        self.frameHumidIndoor.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_60 = QVBoxLayout(self.frameHumidIndoor)
        self.verticalLayout_60.setSpacing(0)
        self.verticalLayout_60.setObjectName(u"verticalLayout_60")
        self.verticalLayout_60.setContentsMargins(0, 0, 0, 0)
        self.frame_17 = QFrame(self.frameHumidIndoor)
        self.frame_17.setObjectName(u"frame_17")
        self.frame_17.setMinimumSize(QSize(0, 100))
        self.frame_17.setMaximumSize(QSize(16777215, 100))
        self.frame_17.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_17.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_48 = QHBoxLayout(self.frame_17)
        self.horizontalLayout_48.setObjectName(u"horizontalLayout_48")
        self.titleHumidIndoor = QLabel(self.frame_17)
        self.titleHumidIndoor.setObjectName(u"titleHumidIndoor")
        sizePolicy2.setHeightForWidth(self.titleHumidIndoor.sizePolicy().hasHeightForWidth())
        self.titleHumidIndoor.setSizePolicy(sizePolicy2)
        self.titleHumidIndoor.setMaximumSize(QSize(322, 45))
        self.titleHumidIndoor.setFont(font6)
        self.titleHumidIndoor.setStyleSheet(u"#titleHumidIndoor{\n"
"font: bold 14pt \"Segoe UI\";\n"
"color: white;\n"
"background-color: #5FB3A2;   /* hijau soft */\n"
"border-radius: 8px;\n"
"padding: 6px 10px;\n"
"border: 1px solid #5FB3A2;\n"
"\n"
"min-width: 200px;\n"
"max-width: 300px;\n"
"qproperty-alignment: AlignCenter;\n"
"}\n"
"")
        self.titleHumidIndoor.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_48.addWidget(self.titleHumidIndoor)


        self.verticalLayout_60.addWidget(self.frame_17)

        self.frame_14 = QFrame(self.frameHumidIndoor)
        self.frame_14.setObjectName(u"frame_14")
        self.frame_14.setMinimumSize(QSize(0, 270))
        self.frame_14.setMaximumSize(QSize(16777215, 270))
        self.frame_14.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_14.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_49 = QHBoxLayout(self.frame_14)
        self.horizontalLayout_49.setObjectName(u"horizontalLayout_49")
        self.humidIndoor_value = QLabel(self.frame_14)
        self.humidIndoor_value.setObjectName(u"humidIndoor_value")
        sizePolicy2.setHeightForWidth(self.humidIndoor_value.sizePolicy().hasHeightForWidth())
        self.humidIndoor_value.setSizePolicy(sizePolicy2)
        self.humidIndoor_value.setMaximumSize(QSize(16777215, 9999999))
        self.humidIndoor_value.setFont(font9)
        self.humidIndoor_value.setStyleSheet(u"#humidIndoor_value{\n"
"    font: bold 34pt \"Segoe UI\";\n"
"    color: black;\n"
"}\n"
"")
        self.humidIndoor_value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_49.addWidget(self.humidIndoor_value)


        self.verticalLayout_60.addWidget(self.frame_14)


        self.horizontalLayout_45.addWidget(self.frameHumidIndoor)


        self.verticalLayout_51.addWidget(self.frame_5)


        self.verticalLayout_49.addWidget(self.frame_7)


        self.horizontalLayout_32.addWidget(self.frameIndoor)

        self.frameOutdoor = QFrame(self.frame_3)
        self.frameOutdoor.setObjectName(u"frameOutdoor")
        self.frameOutdoor.setMinimumSize(QSize(0, 0))
        self.frameOutdoor.setMaximumSize(QSize(16777215, 700))
        self.frameOutdoor.setStyleSheet(u"#frameOutdoor {\n"
"    background-color: #EDF6FC;   /* biru sangat pucat */\n"
"    border: 1.5px solid #D9E9F6; /* garis tipis, hampir menyatu */\n"
"    border-radius: 12px;\n"
"}\n"
"")
        self.frameOutdoor.setFrameShape(QFrame.Shape.NoFrame)
        self.frameOutdoor.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.frameOutdoor)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_72 = QHBoxLayout()
        self.horizontalLayout_72.setObjectName(u"horizontalLayout_72")
        self.frame_35 = QFrame(self.frameOutdoor)
        self.frame_35.setObjectName(u"frame_35")
        self.frame_35.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_35.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_72.addWidget(self.frame_35)

        self.titleOutdoor = QLabel(self.frameOutdoor)
        self.titleOutdoor.setObjectName(u"titleOutdoor")
        sizePolicy2.setHeightForWidth(self.titleOutdoor.sizePolicy().hasHeightForWidth())
        self.titleOutdoor.setSizePolicy(sizePolicy2)
        self.titleOutdoor.setMinimumSize(QSize(522, 45))
        self.titleOutdoor.setMaximumSize(QSize(422, 45))
        self.titleOutdoor.setFont(font6)
        self.titleOutdoor.setStyleSheet(u"#titleOutdoor{\n"
"    font: bold 14pt \"Segoe UI\";\n"
"    color: white;\n"
"    background-color: #33A1E0;\n"
"    border-radius: 8px;\n"
"    padding: 6px 10px;\n"
"    border: 1px solid #33A1E0;\n"
"    \n"
"    /* Tambahan pengaturan ukuran */\n"
"    min-width: 500px;    /* lebar minimum */\n"
"    max-width: 400px;    /* lebar maksimum */\n"
"    qproperty-alignment: AlignCenter; /* biar teks di tengah */\n"
"}\n"
"")
        self.titleOutdoor.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_72.addWidget(self.titleOutdoor)

        self.frame_37 = QFrame(self.frameOutdoor)
        self.frame_37.setObjectName(u"frame_37")
        self.frame_37.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_37.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_72.addWidget(self.frame_37)


        self.verticalLayout.addLayout(self.horizontalLayout_72)

        self.horizontalLayout_69 = QHBoxLayout()
        self.horizontalLayout_69.setObjectName(u"horizontalLayout_69")
        self.frameTempWeather = QFrame(self.frameOutdoor)
        self.frameTempWeather.setObjectName(u"frameTempWeather")
        self.frameTempWeather.setMinimumSize(QSize(260, 150))
        self.frameTempWeather.setMaximumSize(QSize(260, 150))
        self.frameTempWeather.setStyleSheet(u"#frameTempWeather{\n"
"    background-color: #FFF3E6;   /* cream orange muda */\n"
"    border: 2px solid #FFD6B0;   /* peach soft */\n"
"    border-radius: 10px\n"
"}\n"
"")
        self.frameTempWeather.setFrameShape(QFrame.Shape.NoFrame)
        self.frameTempWeather.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_62 = QVBoxLayout(self.frameTempWeather)
        self.verticalLayout_62.setSpacing(0)
        self.verticalLayout_62.setObjectName(u"verticalLayout_62")
        self.verticalLayout_62.setContentsMargins(0, 0, 0, 0)
        self.frame_4 = QFrame(self.frameTempWeather)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setStyleSheet(u"#frameHumidIndoor{\n"
"	background-color: #def0ff;        /* warna latar belakang (gelap elegan)  #c6e1f7 */\n"
"	border: 2px solid #cfe7fa;        /* ketebalan dan warna border */\n"
"	border-radius: 10px;              /* sudut melengkung */\n"
"}\n"
"")
        self.frame_4.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_50 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_50.setObjectName(u"horizontalLayout_50")
        self.titletempW = QLabel(self.frame_4)
        self.titletempW.setObjectName(u"titletempW")
        sizePolicy2.setHeightForWidth(self.titletempW.sizePolicy().hasHeightForWidth())
        self.titletempW.setSizePolicy(sizePolicy2)
        self.titletempW.setMaximumSize(QSize(322, 45))
        self.titletempW.setFont(font6)
        self.titletempW.setStyleSheet(u"#titletempW{\n"
"    font: bold 14pt \"Segoe UI\";\n"
"    color: white;\n"
"    background-color: #F4A261;   /* orange lembut */\n"
"    border-radius: 8px;\n"
"    padding: 6px 10px;\n"
"    border: 1px solid #F4A261;\n"
"    \n"
"    min-width: 200px;\n"
"    max-width: 300px;\n"
"    qproperty-alignment: AlignCenter;\n"
"}\n"
"")
        self.titletempW.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_50.addWidget(self.titletempW)


        self.verticalLayout_62.addWidget(self.frame_4)

        self.frame_9 = QFrame(self.frameTempWeather)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setStyleSheet(u"#frameHumidIndoor{\n"
"	background-color: #def0ff;        /* warna latar belakang (gelap elegan)  #c6e1f7 */\n"
"	border: 2px solid #cfe7fa;        /* ketebalan dan warna border */\n"
"	border-radius: 10px;              /* sudut melengkung */\n"
"}\n"
"")
        self.frame_9.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_9.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_51 = QHBoxLayout(self.frame_9)
        self.horizontalLayout_51.setObjectName(u"horizontalLayout_51")
        self.tempW_value = QLabel(self.frame_9)
        self.tempW_value.setObjectName(u"tempW_value")
        sizePolicy2.setHeightForWidth(self.tempW_value.sizePolicy().hasHeightForWidth())
        self.tempW_value.setSizePolicy(sizePolicy2)
        self.tempW_value.setMaximumSize(QSize(16777215, 9999999))
        font10 = QFont()
        font10.setFamilies([u"Segoe UI"])
        font10.setPointSize(16)
        font10.setBold(True)
        font10.setItalic(False)
        self.tempW_value.setFont(font10)
        self.tempW_value.setStyleSheet(u"#tempW_value{\n"
"    font: bold 16pt \"Segoe UI\";\n"
"    color: black;\n"
"}\n"
"")
        self.tempW_value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_51.addWidget(self.tempW_value)


        self.verticalLayout_62.addWidget(self.frame_9)


        self.horizontalLayout_69.addWidget(self.frameTempWeather)

        self.frameHumidWeather = QFrame(self.frameOutdoor)
        self.frameHumidWeather.setObjectName(u"frameHumidWeather")
        self.frameHumidWeather.setMinimumSize(QSize(260, 150))
        self.frameHumidWeather.setMaximumSize(QSize(260, 150))
        self.frameHumidWeather.setStyleSheet(u"#frameHumidWeather{\n"
"background-color: #EAF7F4;   /* hijau sangat muda */\n"
"border: 2px solid #CDE6E0;   /* hijau abu soft */\n"
"border-radius: 10px;\n"
"}")
        self.frameHumidWeather.setFrameShape(QFrame.Shape.NoFrame)
        self.frameHumidWeather.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_63 = QVBoxLayout(self.frameHumidWeather)
        self.verticalLayout_63.setSpacing(0)
        self.verticalLayout_63.setObjectName(u"verticalLayout_63")
        self.verticalLayout_63.setContentsMargins(0, 0, 0, 0)
        self.frame_6 = QFrame(self.frameHumidWeather)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setStyleSheet(u"#frameHumidIndoor{\n"
"	background-color: #def0ff;        /* warna latar belakang (gelap elegan)  #c6e1f7 */\n"
"	border: 2px solid #cfe7fa;        /* ketebalan dan warna border */\n"
"	border-radius: 10px;              /* sudut melengkung */\n"
"}\n"
"")
        self.frame_6.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_52 = QHBoxLayout(self.frame_6)
        self.horizontalLayout_52.setObjectName(u"horizontalLayout_52")
        self.titlehumidw = QLabel(self.frame_6)
        self.titlehumidw.setObjectName(u"titlehumidw")
        sizePolicy2.setHeightForWidth(self.titlehumidw.sizePolicy().hasHeightForWidth())
        self.titlehumidw.setSizePolicy(sizePolicy2)
        self.titlehumidw.setMaximumSize(QSize(322, 45))
        self.titlehumidw.setFont(font6)
        self.titlehumidw.setStyleSheet(u"\n"
"#titlehumidw{\n"
"font: bold 14pt \"Segoe UI\";\n"
"color: white;\n"
"background-color: #5FB3A2;   /* hijau soft */\n"
"border-radius: 8px;\n"
"padding: 6px 10px;\n"
"border: 1px solid #5FB3A2;\n"
"\n"
"min-width: 200px;\n"
"max-width: 300px;\n"
"qproperty-alignment: AlignCenter;\n"
"}")
        self.titlehumidw.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_52.addWidget(self.titlehumidw)


        self.verticalLayout_63.addWidget(self.frame_6)

        self.frame_18 = QFrame(self.frameHumidWeather)
        self.frame_18.setObjectName(u"frame_18")
        self.frame_18.setStyleSheet(u"#frameHumidIndoor{\n"
"	background-color: #def0ff;        /* warna latar belakang (gelap elegan)  #c6e1f7 */\n"
"	border: 2px solid #cfe7fa;        /* ketebalan dan warna border */\n"
"	border-radius: 10px;              /* sudut melengkung */\n"
"}\n"
"")
        self.frame_18.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_18.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_53 = QHBoxLayout(self.frame_18)
        self.horizontalLayout_53.setObjectName(u"horizontalLayout_53")
        self.humidW_value = QLabel(self.frame_18)
        self.humidW_value.setObjectName(u"humidW_value")
        sizePolicy2.setHeightForWidth(self.humidW_value.sizePolicy().hasHeightForWidth())
        self.humidW_value.setSizePolicy(sizePolicy2)
        self.humidW_value.setMaximumSize(QSize(16777215, 9999999))
        self.humidW_value.setFont(font10)
        self.humidW_value.setStyleSheet(u"#humidW_value{\n"
"    font: bold 16pt \"Segoe UI\";\n"
"    color: black;\n"
"}\n"
"")
        self.humidW_value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_53.addWidget(self.humidW_value)


        self.verticalLayout_63.addWidget(self.frame_18)


        self.horizontalLayout_69.addWidget(self.frameHumidWeather)

        self.framePressWeather = QFrame(self.frameOutdoor)
        self.framePressWeather.setObjectName(u"framePressWeather")
        self.framePressWeather.setMinimumSize(QSize(260, 150))
        self.framePressWeather.setMaximumSize(QSize(260, 150))
        self.framePressWeather.setStyleSheet(u"#framePressWeather{\n"
"background-color: #EEF2F7;\n"
"border: 2px solid #D5DEE8;\n"
"border-radius: 10px;\n"
"\n"
"}")
        self.framePressWeather.setFrameShape(QFrame.Shape.NoFrame)
        self.framePressWeather.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_64 = QVBoxLayout(self.framePressWeather)
        self.verticalLayout_64.setSpacing(0)
        self.verticalLayout_64.setObjectName(u"verticalLayout_64")
        self.verticalLayout_64.setContentsMargins(0, 0, 0, 0)
        self.frame_20 = QFrame(self.framePressWeather)
        self.frame_20.setObjectName(u"frame_20")
        self.frame_20.setStyleSheet(u"#frameHumidIndoor{\n"
"	background-color: #def0ff;        /* warna latar belakang (gelap elegan)  #c6e1f7 */\n"
"	border: 2px solid #cfe7fa;        /* ketebalan dan warna border */\n"
"	border-radius: 10px;              /* sudut melengkung */\n"
"}\n"
"")
        self.frame_20.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_20.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_55 = QHBoxLayout(self.frame_20)
        self.horizontalLayout_55.setObjectName(u"horizontalLayout_55")
        self.titlePressW = QLabel(self.frame_20)
        self.titlePressW.setObjectName(u"titlePressW")
        sizePolicy2.setHeightForWidth(self.titlePressW.sizePolicy().hasHeightForWidth())
        self.titlePressW.setSizePolicy(sizePolicy2)
        self.titlePressW.setMaximumSize(QSize(322, 45))
        self.titlePressW.setFont(font6)
        self.titlePressW.setStyleSheet(u"\n"
"#titlePressW{\n"
"font: bold 14pt \"Segoe UI\";\n"
"color: white;\n"
"background-color: #6B7C93;   /* steel blue */\n"
"border: 1px solid #6B7C93;\n"
"border-radius: 8px;\n"
"padding: 6px 10px;\n"
"\n"
"\n"
"min-width: 200px;\n"
"max-width: 300px;\n"
"qproperty-alignment: AlignCenter;\n"
"\n"
"}")
        self.titlePressW.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_55.addWidget(self.titlePressW)


        self.verticalLayout_64.addWidget(self.frame_20)

        self.frame_21 = QFrame(self.framePressWeather)
        self.frame_21.setObjectName(u"frame_21")
        self.frame_21.setStyleSheet(u"#frameHumidIndoor{\n"
"	background-color: #def0ff;        /* warna latar belakang (gelap elegan)  #c6e1f7 */\n"
"	border: 2px solid #cfe7fa;        /* ketebalan dan warna border */\n"
"	border-radius: 10px;              /* sudut melengkung */\n"
"}\n"
"")
        self.frame_21.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_21.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_56 = QHBoxLayout(self.frame_21)
        self.horizontalLayout_56.setObjectName(u"horizontalLayout_56")
        self.pressureW_value = QLabel(self.frame_21)
        self.pressureW_value.setObjectName(u"pressureW_value")
        sizePolicy2.setHeightForWidth(self.pressureW_value.sizePolicy().hasHeightForWidth())
        self.pressureW_value.setSizePolicy(sizePolicy2)
        self.pressureW_value.setMaximumSize(QSize(16777215, 9999999))
        self.pressureW_value.setFont(font10)
        self.pressureW_value.setStyleSheet(u"#pressureW_value{\n"
"    font: bold 16pt \"Segoe UI\";\n"
"    color: black;\n"
"}\n"
"")
        self.pressureW_value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_56.addWidget(self.pressureW_value)


        self.verticalLayout_64.addWidget(self.frame_21)


        self.horizontalLayout_69.addWidget(self.framePressWeather)


        self.verticalLayout.addLayout(self.horizontalLayout_69)

        self.horizontalLayout_70 = QHBoxLayout()
        self.horizontalLayout_70.setObjectName(u"horizontalLayout_70")
        self.frameWinspdWeather = QFrame(self.frameOutdoor)
        self.frameWinspdWeather.setObjectName(u"frameWinspdWeather")
        self.frameWinspdWeather.setMinimumSize(QSize(260, 150))
        self.frameWinspdWeather.setMaximumSize(QSize(260, 150))
        self.frameWinspdWeather.setStyleSheet(u"#frameWinspdWeather{\n"
"background-color: #E8F2FA;   /* biru muda lembut */\n"
"border: 2px solid #C9DFF1;   /* biru abu soft */\n"
"border-radius: 10px;\n"
"}")
        self.frameWinspdWeather.setFrameShape(QFrame.Shape.NoFrame)
        self.frameWinspdWeather.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_65 = QVBoxLayout(self.frameWinspdWeather)
        self.verticalLayout_65.setSpacing(0)
        self.verticalLayout_65.setObjectName(u"verticalLayout_65")
        self.verticalLayout_65.setContentsMargins(0, 0, 0, 0)
        self.frame_23 = QFrame(self.frameWinspdWeather)
        self.frame_23.setObjectName(u"frame_23")
        self.frame_23.setStyleSheet(u"#frameHumidIndoor{\n"
"	background-color: #def0ff;        /* warna latar belakang (gelap elegan)  #c6e1f7 */\n"
"	border: 2px solid #cfe7fa;        /* ketebalan dan warna border */\n"
"	border-radius: 10px;              /* sudut melengkung */\n"
"}\n"
"")
        self.frame_23.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_23.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_57 = QHBoxLayout(self.frame_23)
        self.horizontalLayout_57.setObjectName(u"horizontalLayout_57")
        self.titlewinspdW = QLabel(self.frame_23)
        self.titlewinspdW.setObjectName(u"titlewinspdW")
        sizePolicy2.setHeightForWidth(self.titlewinspdW.sizePolicy().hasHeightForWidth())
        self.titlewinspdW.setSizePolicy(sizePolicy2)
        self.titlewinspdW.setMaximumSize(QSize(322, 45))
        self.titlewinspdW.setFont(font6)
        self.titlewinspdW.setStyleSheet(u"\n"
"#titlewinspdW{\n"
"font: bold 14pt \"Segoe UI\";\n"
"color: white;\n"
"background-color: #5DA9E9;   /* biru utama */\n"
"border-radius: 8px;\n"
"padding: 6px 10px;\n"
"border: 1px solid #5DA9E9;\n"
"\n"
"min-width: 200px;\n"
"max-width: 300px;\n"
"qproperty-alignment: AlignCenter;\n"
"}")
        self.titlewinspdW.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_57.addWidget(self.titlewinspdW)


        self.verticalLayout_65.addWidget(self.frame_23)

        self.frame_24 = QFrame(self.frameWinspdWeather)
        self.frame_24.setObjectName(u"frame_24")
        self.frame_24.setStyleSheet(u"#frameHumidIndoor{\n"
"	background-color: #def0ff;        /* warna latar belakang (gelap elegan)  #c6e1f7 */\n"
"	border: 2px solid #cfe7fa;        /* ketebalan dan warna border */\n"
"	border-radius: 10px;              /* sudut melengkung */\n"
"}\n"
"")
        self.frame_24.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_24.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_58 = QHBoxLayout(self.frame_24)
        self.horizontalLayout_58.setObjectName(u"horizontalLayout_58")
        self.windspdW_value = QLabel(self.frame_24)
        self.windspdW_value.setObjectName(u"windspdW_value")
        sizePolicy2.setHeightForWidth(self.windspdW_value.sizePolicy().hasHeightForWidth())
        self.windspdW_value.setSizePolicy(sizePolicy2)
        self.windspdW_value.setMaximumSize(QSize(16777215, 9999999))
        self.windspdW_value.setFont(font10)
        self.windspdW_value.setStyleSheet(u"#windspdW_value{\n"
"    font: bold 16pt \"Segoe UI\";\n"
"    color: black;\n"
"}\n"
"")
        self.windspdW_value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_58.addWidget(self.windspdW_value)


        self.verticalLayout_65.addWidget(self.frame_24)


        self.horizontalLayout_70.addWidget(self.frameWinspdWeather)

        self.frameWindspdavgWeather = QFrame(self.frameOutdoor)
        self.frameWindspdavgWeather.setObjectName(u"frameWindspdavgWeather")
        self.frameWindspdavgWeather.setMinimumSize(QSize(260, 150))
        self.frameWindspdavgWeather.setMaximumSize(QSize(260, 150))
        self.frameWindspdavgWeather.setStyleSheet(u"#frameWindspdavgWeather{\n"
"background-color: #E8F2FA;   /* biru muda lembut */\n"
"border: 2px solid #C9DFF1;   /* biru abu soft */\n"
"border-radius: 10px;\n"
"}")
        self.frameWindspdavgWeather.setFrameShape(QFrame.Shape.NoFrame)
        self.frameWindspdavgWeather.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_66 = QVBoxLayout(self.frameWindspdavgWeather)
        self.verticalLayout_66.setSpacing(0)
        self.verticalLayout_66.setObjectName(u"verticalLayout_66")
        self.verticalLayout_66.setContentsMargins(0, 0, 0, 0)
        self.frame_25 = QFrame(self.frameWindspdavgWeather)
        self.frame_25.setObjectName(u"frame_25")
        self.frame_25.setStyleSheet(u"#frameHumidIndoor{\n"
"	background-color: #def0ff;        /* warna latar belakang (gelap elegan)  #c6e1f7 */\n"
"	border: 2px solid #cfe7fa;        /* ketebalan dan warna border */\n"
"	border-radius: 10px;              /* sudut melengkung */\n"
"}\n"
"")
        self.frame_25.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_25.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_59 = QHBoxLayout(self.frame_25)
        self.horizontalLayout_59.setObjectName(u"horizontalLayout_59")
        self.titlesinspdavgW = QLabel(self.frame_25)
        self.titlesinspdavgW.setObjectName(u"titlesinspdavgW")
        sizePolicy2.setHeightForWidth(self.titlesinspdavgW.sizePolicy().hasHeightForWidth())
        self.titlesinspdavgW.setSizePolicy(sizePolicy2)
        self.titlesinspdavgW.setMaximumSize(QSize(322, 45))
        self.titlesinspdavgW.setFont(font6)
        self.titlesinspdavgW.setStyleSheet(u"\n"
"#titlesinspdavgW{\n"
"font: bold 14pt \"Segoe UI\";\n"
"color: white;\n"
"background-color: #5DA9E9;   /* biru utama */\n"
"border-radius: 8px;\n"
"padding: 6px 10px;\n"
"border: 1px solid #5DA9E9;\n"
"\n"
"min-width: 200px;\n"
"max-width: 300px;\n"
"qproperty-alignment: AlignCenter;\n"
"}")
        self.titlesinspdavgW.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_59.addWidget(self.titlesinspdavgW)


        self.verticalLayout_66.addWidget(self.frame_25)

        self.frame_26 = QFrame(self.frameWindspdavgWeather)
        self.frame_26.setObjectName(u"frame_26")
        self.frame_26.setStyleSheet(u"#frameHumidIndoor{\n"
"	background-color: #def0ff;        /* warna latar belakang (gelap elegan)  #c6e1f7 */\n"
"	border: 2px solid #cfe7fa;        /* ketebalan dan warna border */\n"
"	border-radius: 10px;              /* sudut melengkung */\n"
"}\n"
"")
        self.frame_26.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_26.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_60 = QHBoxLayout(self.frame_26)
        self.horizontalLayout_60.setObjectName(u"horizontalLayout_60")
        self.windspdavgW_value = QLabel(self.frame_26)
        self.windspdavgW_value.setObjectName(u"windspdavgW_value")
        sizePolicy2.setHeightForWidth(self.windspdavgW_value.sizePolicy().hasHeightForWidth())
        self.windspdavgW_value.setSizePolicy(sizePolicy2)
        self.windspdavgW_value.setMaximumSize(QSize(16777215, 9999999))
        self.windspdavgW_value.setFont(font10)
        self.windspdavgW_value.setStyleSheet(u"#windspdavgW_value{\n"
"    font: bold 16pt \"Segoe UI\";\n"
"    color: black;\n"
"}\n"
"")
        self.windspdavgW_value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_60.addWidget(self.windspdavgW_value)


        self.verticalLayout_66.addWidget(self.frame_26)


        self.horizontalLayout_70.addWidget(self.frameWindspdavgWeather)

        self.frameWindspddirWeather = QFrame(self.frameOutdoor)
        self.frameWindspddirWeather.setObjectName(u"frameWindspddirWeather")
        self.frameWindspddirWeather.setMinimumSize(QSize(260, 150))
        self.frameWindspddirWeather.setMaximumSize(QSize(260, 150))
        self.frameWindspddirWeather.setStyleSheet(u"#frameWindspddirWeather{\n"
"background-color: #E8F2FA;   /* biru muda lembut */\n"
"border: 2px solid #C9DFF1;   /* biru abu soft */\n"
"border-radius: 10px;\n"
"}")
        self.frameWindspddirWeather.setFrameShape(QFrame.Shape.NoFrame)
        self.frameWindspddirWeather.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_67 = QVBoxLayout(self.frameWindspddirWeather)
        self.verticalLayout_67.setSpacing(0)
        self.verticalLayout_67.setObjectName(u"verticalLayout_67")
        self.verticalLayout_67.setContentsMargins(0, 0, 0, 0)
        self.frame_27 = QFrame(self.frameWindspddirWeather)
        self.frame_27.setObjectName(u"frame_27")
        self.frame_27.setStyleSheet(u"#frameHumidIndoor{\n"
"	background-color: #def0ff;        /* warna latar belakang (gelap elegan)  #c6e1f7 */\n"
"	border: 2px solid #cfe7fa;        /* ketebalan dan warna border */\n"
"	border-radius: 10px;              /* sudut melengkung */\n"
"}\n"
"")
        self.frame_27.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_27.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_61 = QHBoxLayout(self.frame_27)
        self.horizontalLayout_61.setObjectName(u"horizontalLayout_61")
        self.titlewindspddirW = QLabel(self.frame_27)
        self.titlewindspddirW.setObjectName(u"titlewindspddirW")
        sizePolicy2.setHeightForWidth(self.titlewindspddirW.sizePolicy().hasHeightForWidth())
        self.titlewindspddirW.setSizePolicy(sizePolicy2)
        self.titlewindspddirW.setMaximumSize(QSize(322, 45))
        self.titlewindspddirW.setFont(font6)
        self.titlewindspddirW.setStyleSheet(u"\n"
"#titlewindspddirW{\n"
"font: bold 14pt \"Segoe UI\";\n"
"color: white;\n"
"background-color: #5DA9E9;   /* biru utama */\n"
"border-radius: 8px;\n"
"padding: 6px 10px;\n"
"border: 1px solid #5DA9E9;\n"
"\n"
"min-width: 200px;\n"
"max-width: 300px;\n"
"qproperty-alignment: AlignCenter;\n"
"}")
        self.titlewindspddirW.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_61.addWidget(self.titlewindspddirW)


        self.verticalLayout_67.addWidget(self.frame_27)

        self.frame_28 = QFrame(self.frameWindspddirWeather)
        self.frame_28.setObjectName(u"frame_28")
        self.frame_28.setStyleSheet(u"#frameHumidIndoor{\n"
"	background-color: #def0ff;        /* warna latar belakang (gelap elegan)  #c6e1f7 */\n"
"	border: 2px solid #cfe7fa;        /* ketebalan dan warna border */\n"
"	border-radius: 10px;              /* sudut melengkung */\n"
"}\n"
"")
        self.frame_28.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_28.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_62 = QHBoxLayout(self.frame_28)
        self.horizontalLayout_62.setObjectName(u"horizontalLayout_62")
        self.windspddirW_value = QLabel(self.frame_28)
        self.windspddirW_value.setObjectName(u"windspddirW_value")
        sizePolicy2.setHeightForWidth(self.windspddirW_value.sizePolicy().hasHeightForWidth())
        self.windspddirW_value.setSizePolicy(sizePolicy2)
        self.windspddirW_value.setMaximumSize(QSize(16777215, 9999999))
        self.windspddirW_value.setFont(font10)
        self.windspddirW_value.setStyleSheet(u"#windspddirW_value{\n"
"    font: bold 16pt \"Segoe UI\";\n"
"    color: black;\n"
"}\n"
"")
        self.windspddirW_value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_62.addWidget(self.windspddirW_value)


        self.verticalLayout_67.addWidget(self.frame_28)


        self.horizontalLayout_70.addWidget(self.frameWindspddirWeather)


        self.verticalLayout.addLayout(self.horizontalLayout_70)

        self.horizontalLayout_71 = QHBoxLayout()
        self.horizontalLayout_71.setObjectName(u"horizontalLayout_71")
        self.frameTotalrainWeather = QFrame(self.frameOutdoor)
        self.frameTotalrainWeather.setObjectName(u"frameTotalrainWeather")
        self.frameTotalrainWeather.setMinimumSize(QSize(260, 150))
        self.frameTotalrainWeather.setMaximumSize(QSize(260, 150))
        self.frameTotalrainWeather.setStyleSheet(u"#frameTotalrainWeather{\n"
"background-color: #EAF7F4;   /* hijau sangat muda */\n"
"border: 2px solid #CDE6E0;   /* hijau abu soft */\n"
"border-radius: 10px;\n"
"\n"
"}")
        self.frameTotalrainWeather.setFrameShape(QFrame.Shape.NoFrame)
        self.frameTotalrainWeather.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_68 = QVBoxLayout(self.frameTotalrainWeather)
        self.verticalLayout_68.setSpacing(0)
        self.verticalLayout_68.setObjectName(u"verticalLayout_68")
        self.verticalLayout_68.setContentsMargins(0, 0, 0, 0)
        self.frame_29 = QFrame(self.frameTotalrainWeather)
        self.frame_29.setObjectName(u"frame_29")
        self.frame_29.setStyleSheet(u"#frameHumidIndoor{\n"
"	background-color: #def0ff;        /* warna latar belakang (gelap elegan)  #c6e1f7 */\n"
"	border: 2px solid #cfe7fa;        /* ketebalan dan warna border */\n"
"	border-radius: 10px;              /* sudut melengkung */\n"
"}\n"
"")
        self.frame_29.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_29.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_63 = QHBoxLayout(self.frame_29)
        self.horizontalLayout_63.setObjectName(u"horizontalLayout_63")
        self.titletotalrainW = QLabel(self.frame_29)
        self.titletotalrainW.setObjectName(u"titletotalrainW")
        sizePolicy2.setHeightForWidth(self.titletotalrainW.sizePolicy().hasHeightForWidth())
        self.titletotalrainW.setSizePolicy(sizePolicy2)
        self.titletotalrainW.setMaximumSize(QSize(322, 45))
        self.titletotalrainW.setFont(font6)
        self.titletotalrainW.setStyleSheet(u"\n"
"#titletotalrainW{\n"
"font: bold 14pt \"Segoe UI\";\n"
"color: white;\n"
"background-color: #5FB3A2;   /* hijau soft */\n"
"border-radius: 8px;\n"
"padding: 6px 10px;\n"
"border: 1px solid #5FB3A2;\n"
"\n"
"min-width: 200px;\n"
"max-width: 300px;\n"
"qproperty-alignment: AlignCenter;\n"
"}")
        self.titletotalrainW.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_63.addWidget(self.titletotalrainW)


        self.verticalLayout_68.addWidget(self.frame_29)

        self.frame_30 = QFrame(self.frameTotalrainWeather)
        self.frame_30.setObjectName(u"frame_30")
        self.frame_30.setStyleSheet(u"#frameHumidIndoor{\n"
"	background-color: #def0ff;        /* warna latar belakang (gelap elegan)  #c6e1f7 */\n"
"	border: 2px solid #cfe7fa;        /* ketebalan dan warna border */\n"
"	border-radius: 10px;              /* sudut melengkung */\n"
"}\n"
"")
        self.frame_30.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_30.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_64 = QHBoxLayout(self.frame_30)
        self.horizontalLayout_64.setObjectName(u"horizontalLayout_64")
        self.totalrainW_value = QLabel(self.frame_30)
        self.totalrainW_value.setObjectName(u"totalrainW_value")
        sizePolicy2.setHeightForWidth(self.totalrainW_value.sizePolicy().hasHeightForWidth())
        self.totalrainW_value.setSizePolicy(sizePolicy2)
        self.totalrainW_value.setMaximumSize(QSize(16777215, 9999999))
        self.totalrainW_value.setFont(font10)
        self.totalrainW_value.setStyleSheet(u"#totalrainW_value{\n"
"    font: bold 16pt \"Segoe UI\";\n"
"    color: black;\n"
"}\n"
"")
        self.totalrainW_value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_64.addWidget(self.totalrainW_value)


        self.verticalLayout_68.addWidget(self.frame_30)


        self.horizontalLayout_71.addWidget(self.frameTotalrainWeather)

        self.frameRainrateWeather = QFrame(self.frameOutdoor)
        self.frameRainrateWeather.setObjectName(u"frameRainrateWeather")
        self.frameRainrateWeather.setMinimumSize(QSize(260, 150))
        self.frameRainrateWeather.setMaximumSize(QSize(260, 150))
        self.frameRainrateWeather.setStyleSheet(u"#frameRainrateWeather{\n"
"background-color: #EAF7F4;   /* hijau sangat muda */\n"
"border: 2px solid #CDE6E0;   /* hijau abu soft */\n"
"border-radius: 10px;\n"
"\n"
"}")
        self.frameRainrateWeather.setFrameShape(QFrame.Shape.NoFrame)
        self.frameRainrateWeather.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_69 = QVBoxLayout(self.frameRainrateWeather)
        self.verticalLayout_69.setSpacing(0)
        self.verticalLayout_69.setObjectName(u"verticalLayout_69")
        self.verticalLayout_69.setContentsMargins(0, 0, 0, 0)
        self.frame_31 = QFrame(self.frameRainrateWeather)
        self.frame_31.setObjectName(u"frame_31")
        self.frame_31.setStyleSheet(u"#frameHumidIndoor{\n"
"	background-color: #def0ff;        /* warna latar belakang (gelap elegan)  #c6e1f7 */\n"
"	border: 2px solid #cfe7fa;        /* ketebalan dan warna border */\n"
"	border-radius: 10px;              /* sudut melengkung */\n"
"}\n"
"")
        self.frame_31.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_31.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_65 = QHBoxLayout(self.frame_31)
        self.horizontalLayout_65.setObjectName(u"horizontalLayout_65")
        self.titleRainrateW = QLabel(self.frame_31)
        self.titleRainrateW.setObjectName(u"titleRainrateW")
        sizePolicy2.setHeightForWidth(self.titleRainrateW.sizePolicy().hasHeightForWidth())
        self.titleRainrateW.setSizePolicy(sizePolicy2)
        self.titleRainrateW.setMaximumSize(QSize(322, 45))
        self.titleRainrateW.setFont(font6)
        self.titleRainrateW.setStyleSheet(u"\n"
"#titleRainrateW{\n"
"font: bold 14pt \"Segoe UI\";\n"
"color: white;\n"
"background-color: #5FB3A2;   /* hijau soft */\n"
"border-radius: 8px;\n"
"padding: 6px 10px;\n"
"border: 1px solid #5FB3A2;\n"
"\n"
"min-width: 200px;\n"
"max-width: 300px;\n"
"qproperty-alignment: AlignCenter;\n"
"}")
        self.titleRainrateW.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_65.addWidget(self.titleRainrateW)


        self.verticalLayout_69.addWidget(self.frame_31)

        self.frame_32 = QFrame(self.frameRainrateWeather)
        self.frame_32.setObjectName(u"frame_32")
        self.frame_32.setStyleSheet(u"#frameHumidIndoor{\n"
"	background-color: #def0ff;        /* warna latar belakang (gelap elegan)  #c6e1f7 */\n"
"	border: 2px solid #cfe7fa;        /* ketebalan dan warna border */\n"
"	border-radius: 10px;              /* sudut melengkung */\n"
"}\n"
"")
        self.frame_32.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_32.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_66 = QHBoxLayout(self.frame_32)
        self.horizontalLayout_66.setObjectName(u"horizontalLayout_66")
        self.rainrateW_value = QLabel(self.frame_32)
        self.rainrateW_value.setObjectName(u"rainrateW_value")
        sizePolicy2.setHeightForWidth(self.rainrateW_value.sizePolicy().hasHeightForWidth())
        self.rainrateW_value.setSizePolicy(sizePolicy2)
        self.rainrateW_value.setMaximumSize(QSize(16777215, 9999999))
        self.rainrateW_value.setFont(font10)
        self.rainrateW_value.setStyleSheet(u"#rainrateW_value{\n"
"    font: bold 16pt \"Segoe UI\";\n"
"    color: black;\n"
"}\n"
"")
        self.rainrateW_value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_66.addWidget(self.rainrateW_value)


        self.verticalLayout_69.addWidget(self.frame_32)


        self.horizontalLayout_71.addWidget(self.frameRainrateWeather)

        self.frameHeatindexWeather = QFrame(self.frameOutdoor)
        self.frameHeatindexWeather.setObjectName(u"frameHeatindexWeather")
        self.frameHeatindexWeather.setMinimumSize(QSize(260, 150))
        self.frameHeatindexWeather.setMaximumSize(QSize(260, 150))
        self.frameHeatindexWeather.setStyleSheet(u"#frameHeatindexWeather{\n"
"    background-color: #FFECEE;   /* merah pastel sangat muda */\n"
"    border: 2px solid #F7C5CB;   /* pink-merah soft */\n"
"    border-radius: 10px;\n"
"}\n"
"")
        self.frameHeatindexWeather.setFrameShape(QFrame.Shape.NoFrame)
        self.frameHeatindexWeather.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_70 = QVBoxLayout(self.frameHeatindexWeather)
        self.verticalLayout_70.setSpacing(0)
        self.verticalLayout_70.setObjectName(u"verticalLayout_70")
        self.verticalLayout_70.setContentsMargins(0, 0, 0, 0)
        self.frame_33 = QFrame(self.frameHeatindexWeather)
        self.frame_33.setObjectName(u"frame_33")
        self.frame_33.setStyleSheet(u"#frameHumidIndoor{\n"
"	background-color: #def0ff;        /* warna latar belakang (gelap elegan)  #c6e1f7 */\n"
"	border: 2px solid #cfe7fa;        /* ketebalan dan warna border */\n"
"	border-radius: 10px;              /* sudut melengkung */\n"
"}\n"
"")
        self.frame_33.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_33.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_67 = QHBoxLayout(self.frame_33)
        self.horizontalLayout_67.setObjectName(u"horizontalLayout_67")
        self.titleheatindexW = QLabel(self.frame_33)
        self.titleheatindexW.setObjectName(u"titleheatindexW")
        sizePolicy2.setHeightForWidth(self.titleheatindexW.sizePolicy().hasHeightForWidth())
        self.titleheatindexW.setSizePolicy(sizePolicy2)
        self.titleheatindexW.setMaximumSize(QSize(322, 45))
        self.titleheatindexW.setFont(font6)
        self.titleheatindexW.setStyleSheet(u"#titleheatindexW{\n"
"    font: bold 14pt \"Segoe UI\";\n"
"    color: white;\n"
"    background-color: #E96A6A;   /* merah coral pastel */\n"
"    border-radius: 8px;\n"
"    padding: 6px 10px;\n"
"    border: 1px solid #E96A6A;\n"
"    \n"
"    min-width: 200px;\n"
"    max-width: 300px;\n"
"    qproperty-alignment: AlignCenter;\n"
"}\n"
"")
        self.titleheatindexW.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_67.addWidget(self.titleheatindexW)


        self.verticalLayout_70.addWidget(self.frame_33)

        self.frame_34 = QFrame(self.frameHeatindexWeather)
        self.frame_34.setObjectName(u"frame_34")
        self.frame_34.setStyleSheet(u"#frameHumidIndoor{\n"
"	background-color: #def0ff;        /* warna latar belakang (gelap elegan)  #c6e1f7 */\n"
"	border: 2px solid #cfe7fa;        /* ketebalan dan warna border */\n"
"	border-radius: 10px;              /* sudut melengkung */\n"
"}\n"
"")
        self.frame_34.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_34.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_68 = QHBoxLayout(self.frame_34)
        self.horizontalLayout_68.setObjectName(u"horizontalLayout_68")
        self.heatindexW_value = QLabel(self.frame_34)
        self.heatindexW_value.setObjectName(u"heatindexW_value")
        sizePolicy2.setHeightForWidth(self.heatindexW_value.sizePolicy().hasHeightForWidth())
        self.heatindexW_value.setSizePolicy(sizePolicy2)
        self.heatindexW_value.setMaximumSize(QSize(16777215, 9999999))
        self.heatindexW_value.setFont(font10)
        self.heatindexW_value.setStyleSheet(u"#heatindexW_value{\n"
"    font: bold 16pt \"Segoe UI\";\n"
"    color: black;\n"
"}\n"
"")
        self.heatindexW_value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_68.addWidget(self.heatindexW_value)


        self.verticalLayout_70.addWidget(self.frame_34)


        self.horizontalLayout_71.addWidget(self.frameHeatindexWeather)


        self.verticalLayout.addLayout(self.horizontalLayout_71)


        self.horizontalLayout_32.addWidget(self.frameOutdoor)


        self.verticalLayout_44.addWidget(self.frame_3)

        self.stackedWidget.addWidget(self.page3_monitoringSensor)
        self.page4_smartsocket = QWidget()
        self.page4_smartsocket.setObjectName(u"page4_smartsocket")
        self.verticalLayout_77 = QVBoxLayout(self.page4_smartsocket)
        self.verticalLayout_77.setObjectName(u"verticalLayout_77")
        self.frameSmartsocket = QFrame(self.page4_smartsocket)
        self.frameSmartsocket.setObjectName(u"frameSmartsocket")
        self.frameSmartsocket.setMaximumSize(QSize(16777215, 65))
        self.frameSmartsocket.setFrameShape(QFrame.Shape.NoFrame)
        self.frameSmartsocket.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_87 = QHBoxLayout(self.frameSmartsocket)
        self.horizontalLayout_87.setObjectName(u"horizontalLayout_87")
        self.titleSmartsocket = QLabel(self.frameSmartsocket)
        self.titleSmartsocket.setObjectName(u"titleSmartsocket")
        sizePolicy2.setHeightForWidth(self.titleSmartsocket.sizePolicy().hasHeightForWidth())
        self.titleSmartsocket.setSizePolicy(sizePolicy2)
        self.titleSmartsocket.setMaximumSize(QSize(422, 45))
        self.titleSmartsocket.setFont(font6)
        self.titleSmartsocket.setStyleSheet(u"#titleSmartsocket {\n"
"    font: bold 14pt \"Segoe UI\";\n"
"    color: white;\n"
"    background-color: #5775dc;\n"
"    border-radius: 8px;\n"
"    padding: 6px 10px;\n"
"    border: 1px solid #5775dc;\n"
"    \n"
"    /* Tambahan pengaturan ukuran */\n"
"    min-width: 500px;    /* lebar minimum */\n"
"    max-width: 400px;    /* lebar maksimum */\n"
"    qproperty-alignment: AlignCenter; /* biar teks di tengah */\n"
"}\n"
"")
        self.titleSmartsocket.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_87.addWidget(self.titleSmartsocket)


        self.verticalLayout_77.addWidget(self.frameSmartsocket)

        self.framecontentSmartsocket = QFrame(self.page4_smartsocket)
        self.framecontentSmartsocket.setObjectName(u"framecontentSmartsocket")
        self.framecontentSmartsocket.setFrameShape(QFrame.Shape.NoFrame)
        self.framecontentSmartsocket.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_111 = QHBoxLayout(self.framecontentSmartsocket)
        self.horizontalLayout_111.setSpacing(70)
        self.horizontalLayout_111.setObjectName(u"horizontalLayout_111")
        self.horizontalLayout_111.setContentsMargins(20, -1, 20, -1)
        self.framesocket1 = QFrame(self.framecontentSmartsocket)
        self.framesocket1.setObjectName(u"framesocket1")
        self.framesocket1.setMinimumSize(QSize(0, 700))
        self.framesocket1.setMaximumSize(QSize(16777215, 700))
        self.framesocket1.setStyleSheet(u"#framesocket1{\n"
"	background-color: #eee3fa;   /* ungu lembut banget */\n"
"	border: 2px solid #E3DAF1;\n"
"	border-radius: 10px;\n"
"}")
        self.framesocket1.setFrameShape(QFrame.Shape.NoFrame)
        self.framesocket1.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_72 = QVBoxLayout(self.framesocket1)
        self.verticalLayout_72.setObjectName(u"verticalLayout_72")
        self.frametitlesocket1 = QFrame(self.framesocket1)
        self.frametitlesocket1.setObjectName(u"frametitlesocket1")
        self.frametitlesocket1.setMinimumSize(QSize(0, 0))
        self.frametitlesocket1.setMaximumSize(QSize(16777215, 50))
        self.frametitlesocket1.setFrameShape(QFrame.Shape.NoFrame)
        self.frametitlesocket1.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_54 = QHBoxLayout(self.frametitlesocket1)
        self.horizontalLayout_54.setSpacing(0)
        self.horizontalLayout_54.setObjectName(u"horizontalLayout_54")
        self.horizontalLayout_54.setContentsMargins(0, 0, 0, 0)
        self.frame_61 = QFrame(self.frametitlesocket1)
        self.frame_61.setObjectName(u"frame_61")
        self.frame_61.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_61.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_54.addWidget(self.frame_61)

        self.titlesmart1 = QLabel(self.frametitlesocket1)
        self.titlesmart1.setObjectName(u"titlesmart1")
        sizePolicy2.setHeightForWidth(self.titlesmart1.sizePolicy().hasHeightForWidth())
        self.titlesmart1.setSizePolicy(sizePolicy2)
        self.titlesmart1.setMinimumSize(QSize(96, 40))
        self.titlesmart1.setMaximumSize(QSize(136, 45))
        self.titlesmart1.setFont(font4)
        self.titlesmart1.setStyleSheet(u"#titlesmart1{\n"
"font: bold 12pt \"Segoe UI\";\n"
"color: white;\n"
"background-color: #8E7AB5;   /* ungu battery */\n"
"    border: 1px solid #6E8E8B;\n"
"\n"
"\n"
"    border-radius: 8px;\n"
"    padding: 6px 12px;\n"
"    min-height: 26px;\n"
"    line-height: 18px;\n"
"\n"
"    min-width: 70px;\n"
"    max-width: 110px;\n"
"    qproperty-alignment: AlignCenter;\n"
"}\n"
"\n"
"")
        self.titlesmart1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_54.addWidget(self.titlesmart1)

        self.frame_67 = QFrame(self.frametitlesocket1)
        self.frame_67.setObjectName(u"frame_67")
        self.frame_67.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_67.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_54.addWidget(self.frame_67)


        self.verticalLayout_72.addWidget(self.frametitlesocket1)

        self.framestatussocket1 = QFrame(self.framesocket1)
        self.framestatussocket1.setObjectName(u"framestatussocket1")
        self.framestatussocket1.setMinimumSize(QSize(0, 40))
        self.framestatussocket1.setMaximumSize(QSize(16777215, 23))
        self.framestatussocket1.setFrameShape(QFrame.Shape.NoFrame)
        self.framestatussocket1.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_88 = QHBoxLayout(self.framestatussocket1)
        self.horizontalLayout_88.setSpacing(0)
        self.horizontalLayout_88.setObjectName(u"horizontalLayout_88")
        self.horizontalLayout_88.setContentsMargins(0, 0, 0, 0)
        self.frame_68 = QFrame(self.framestatussocket1)
        self.frame_68.setObjectName(u"frame_68")
        self.frame_68.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_68.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_88.addWidget(self.frame_68)

        self.statussocket1 = QLabel(self.framestatussocket1)
        self.statussocket1.setObjectName(u"statussocket1")
        sizePolicy2.setHeightForWidth(self.statussocket1.sizePolicy().hasHeightForWidth())
        self.statussocket1.setSizePolicy(sizePolicy2)
        self.statussocket1.setMinimumSize(QSize(155, 23))
        self.statussocket1.setMaximumSize(QSize(114, 23))
        self.statussocket1.setFont(font2)
        self.statussocket1.setStyleSheet(u"QLabel#statussocket1{\n"
"    font: bold 10pt \"Segoe UI\";\n"
"    color: white;\n"
"\n"
"    background-color: #CBD5E1;   /* default (abu netral) */\n"
"    border: 1px solid #94A3B8;\n"
"    border-radius: 4px;\n"
"\n"
"    padding: 2px 6px;\n"
"    min-height: 17px;\n"
"    max-width: 100px;\n"
"\n"
"    qproperty-alignment: AlignCenter;\n"
"}\n"
"\n"
"/* ===== AC ON ===== */\n"
"QLabel#statussocket1[state=\"on\"] {\n"
"    background-color: #6FCF97;   /* hijau pastel tapi jelas */\n"
"    border-color: #27AE60;\n"
"}\n"
"\n"
"/* ===== AC OFF ===== */\n"
"QLabel#statussocket1[state=\"off\"] {\n"
"    background-color: #EB5757;   /* merah pastel tegas */\n"
"    border-color: #C0392B;\n"
"}\n"
"")
        self.statussocket1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_88.addWidget(self.statussocket1)

        self.frame_69 = QFrame(self.framestatussocket1)
        self.frame_69.setObjectName(u"frame_69")
        self.frame_69.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_69.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_88.addWidget(self.frame_69)


        self.verticalLayout_72.addWidget(self.framestatussocket1)

        self.framesensor1value = QFrame(self.framesocket1)
        self.framesensor1value.setObjectName(u"framesensor1value")
        self.framesensor1value.setStyleSheet(u"QFrame#framesensor1value {\n"
"	background-color: #F2ECF9;   /* ungu lembut banget */\n"
"	border: 1px solid #E3DAF1;\n"
"	border-radius: 10px;\n"
"}\n"
"\n"
"QFrame#framesensor1value QLabel {\n"
"    font: bold 10pt \"Segoe UI\";\n"
"    color: #380082;\n"
"}")
        self.framesensor1value.setFrameShape(QFrame.Shape.StyledPanel)
        self.framesensor1value.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_sensor1 = QVBoxLayout(self.framesensor1value)
        self.verticalLayout_sensor1.setSpacing(4)
        self.verticalLayout_sensor1.setObjectName(u"verticalLayout_sensor1")
        self.verticalLayout_sensor1.setContentsMargins(10, 8, 10, 8)
        self.label_energy_monitoring_title = QLabel(self.framesensor1value)
        self.label_energy_monitoring_title.setObjectName(u"label_energy_monitoring_title")
        self.label_energy_monitoring_title.setMaximumSize(QSize(16777215, 30))
        self.label_energy_monitoring_title.setFont(font2)
        self.label_energy_monitoring_title.setStyleSheet(u"#label_energy_monitoring_title {\n"
"    font: bold 10pt \"Segoe UI\";\n"
"    color: white;\n"
"    background-color: #bd95f0;        /* ungu soft */\n"
"    border-radius: 8px;\n"
"    padding: 6px 10px;\n"
"    border: 1px solid #9B7BCB;       /* border ungu gelap tapi harmonis */\n"
"    min-height: 9px;\n"
"    qproperty-alignment: AlignCenter;\n"
"}")
        self.label_energy_monitoring_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_sensor1.addWidget(self.label_energy_monitoring_title)

        self.verticalLayout_sensor_values = QVBoxLayout()
        self.verticalLayout_sensor_values.setSpacing(2)
        self.verticalLayout_sensor_values.setObjectName(u"verticalLayout_sensor_values")
        self.label_voltage1 = QLabel(self.framesensor1value)
        self.label_voltage1.setObjectName(u"label_voltage1")
        self.label_voltage1.setFont(font2)
        self.label_voltage1.setStyleSheet(u"")

        self.verticalLayout_sensor_values.addWidget(self.label_voltage1)

        self.label_current1 = QLabel(self.framesensor1value)
        self.label_current1.setObjectName(u"label_current1")
        self.label_current1.setFont(font2)
        self.label_current1.setStyleSheet(u"")
        self.label_current1.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout_sensor_values.addWidget(self.label_current1)

        self.label_power1 = QLabel(self.framesensor1value)
        self.label_power1.setObjectName(u"label_power1")
        self.label_power1.setFont(font2)
        self.label_power1.setStyleSheet(u"")

        self.verticalLayout_sensor_values.addWidget(self.label_power1)

        self.label_energy1 = QLabel(self.framesensor1value)
        self.label_energy1.setObjectName(u"label_energy1")
        self.label_energy1.setFont(font2)
        self.label_energy1.setStyleSheet(u"")

        self.verticalLayout_sensor_values.addWidget(self.label_energy1)

        self.label_frequency1 = QLabel(self.framesensor1value)
        self.label_frequency1.setObjectName(u"label_frequency1")
        self.label_frequency1.setFont(font2)
        self.label_frequency1.setStyleSheet(u"")

        self.verticalLayout_sensor_values.addWidget(self.label_frequency1)

        self.label_powerfactor1 = QLabel(self.framesensor1value)
        self.label_powerfactor1.setObjectName(u"label_powerfactor1")
        self.label_powerfactor1.setFont(font2)
        self.label_powerfactor1.setStyleSheet(u"")

        self.verticalLayout_sensor_values.addWidget(self.label_powerfactor1)


        self.verticalLayout_sensor1.addLayout(self.verticalLayout_sensor_values)


        self.verticalLayout_72.addWidget(self.framesensor1value)

        self.frameswitch1 = QFrame(self.framesocket1)
        self.frameswitch1.setObjectName(u"frameswitch1")
        self.frameswitch1.setStyleSheet(u"#frameswitch1{\n"
"	background-color: #F2ECF9;   /* ungu lembut banget */\n"
"	border: 1px solid #E3DAF1;\n"
"	border-radius: 10px;\n"
"}")
        self.frameswitch1.setFrameShape(QFrame.Shape.StyledPanel)
        self.frameswitch1.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_61 = QVBoxLayout(self.frameswitch1)
        self.verticalLayout_61.setSpacing(6)
        self.verticalLayout_61.setObjectName(u"verticalLayout_61")
        self.verticalLayout_61.setContentsMargins(8, 8, 8, 8)
        self.frame_73 = QFrame(self.frameswitch1)
        self.frame_73.setObjectName(u"frame_73")
        self.frame_73.setMinimumSize(QSize(0, 20))
        self.frame_73.setMaximumSize(QSize(16777215, 30))
        self.frame_73.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_73.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_89 = QHBoxLayout(self.frame_73)
        self.horizontalLayout_89.setSpacing(0)
        self.horizontalLayout_89.setObjectName(u"horizontalLayout_89")
        self.horizontalLayout_89.setContentsMargins(0, 0, 0, 0)
        self.frame_74 = QFrame(self.frame_73)
        self.frame_74.setObjectName(u"frame_74")
        self.frame_74.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_74.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_89.addWidget(self.frame_74)

        self.label_switch_status_title = QLabel(self.frame_73)
        self.label_switch_status_title.setObjectName(u"label_switch_status_title")
        self.label_switch_status_title.setFont(font2)
        self.label_switch_status_title.setStyleSheet(u"QLabel#label_switch_status_title{\n"
"	font: bold 10pt \"Segoe UI\";\n"
"	color: white;\n"
"	background-color: #bd95f0;    /* ungu battery */\n"
"	border: 1px solid #9B7BCB; \n"
"\n"
"\n"
"    border-radius: 6px;\n"
"    padding: 6px 12px;\n"
"    min-height: 10px;\n"
"    line-height: 5px;\n"
"    qproperty-alignment: AlignCenter;\n"
"}\n"
"\n"
"")

        self.horizontalLayout_89.addWidget(self.label_switch_status_title)

        self.frame_75 = QFrame(self.frame_73)
        self.frame_75.setObjectName(u"frame_75")
        self.frame_75.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_75.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_89.addWidget(self.frame_75)


        self.verticalLayout_61.addWidget(self.frame_73)

        self.frame_70 = QFrame(self.frameswitch1)
        self.frame_70.setObjectName(u"frame_70")
        self.frame_70.setMinimumSize(QSize(0, 0))
        self.frame_70.setMaximumSize(QSize(16777215, 30))
        self.frame_70.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_70.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_90 = QHBoxLayout(self.frame_70)
        self.horizontalLayout_90.setSpacing(0)
        self.horizontalLayout_90.setObjectName(u"horizontalLayout_90")
        self.horizontalLayout_90.setContentsMargins(0, 0, 0, 0)
        self.frame_71 = QFrame(self.frame_70)
        self.frame_71.setObjectName(u"frame_71")
        self.frame_71.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_71.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_90.addWidget(self.frame_71)

        self.label_switch_status_value1 = QLabel(self.frame_70)
        self.label_switch_status_value1.setObjectName(u"label_switch_status_value1")
        self.label_switch_status_value1.setMinimumSize(QSize(0, 30))
        self.label_switch_status_value1.setMaximumSize(QSize(100, 30))
        font11 = QFont()
        font11.setFamilies([u"Segoe UI"])
        font11.setPointSize(9)
        font11.setBold(True)
        font11.setItalic(False)
        self.label_switch_status_value1.setFont(font11)
        self.label_switch_status_value1.setStyleSheet(u"QLabel#label_switch_status_value1{\n"
"    color: white;\n"
"    background-color: #EB5757;\n"
"    border: 1px solid #C0392B;\n"
"    border-radius: 4px;\n"
"    padding: 4px 8px;\n"
"    qproperty-alignment: AlignCenter;\n"
"font: bold 9pt \"Segoe UI\";\n"
"}\n"
"QLabel#label_switch_status_value1[state=\"on\"] {\n"
"    background-color: #6FCF97;\n"
"    border-color: #27AE60;\n"
"}")
        self.label_switch_status_value1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_90.addWidget(self.label_switch_status_value1)

        self.frame_72 = QFrame(self.frame_70)
        self.frame_72.setObjectName(u"frame_72")
        self.frame_72.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_72.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_90.addWidget(self.frame_72)


        self.verticalLayout_61.addWidget(self.frame_70)

        self.frame_switch_button_container = QFrame(self.frameswitch1)
        self.frame_switch_button_container.setObjectName(u"frame_switch_button_container")
        self.frame_switch_button_container.setMinimumSize(QSize(0, 35))
        self.frame_switch_button_container.setFrameShape(QFrame.Shape.NoFrame)

        self.verticalLayout_61.addWidget(self.frame_switch_button_container)


        self.verticalLayout_72.addWidget(self.frameswitch1)

        self.framestatustimer1 = QFrame(self.framesocket1)
        self.framestatustimer1.setObjectName(u"framestatustimer1")
        self.framestatustimer1.setMinimumSize(QSize(0, 24))
        self.framestatustimer1.setMaximumSize(QSize(16777215, 24))
        self.framestatustimer1.setStyleSheet(u"")
        self.framestatustimer1.setFrameShape(QFrame.Shape.NoFrame)
        self.framestatustimer1.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_timer1 = QHBoxLayout(self.framestatustimer1)
        self.horizontalLayout_timer1.setObjectName(u"horizontalLayout_timer1")
        self.horizontalLayout_timer1.setContentsMargins(0, 0, 0, 0)
        self.label_timer_title = QLabel(self.framestatustimer1)
        self.label_timer_title.setObjectName(u"label_timer_title")
        self.label_timer_title.setFont(font2)
        self.label_timer_title.setStyleSheet(u"    font: bold 10pt \"Segoe UI\";\n"
"    color: #380082;\n"
"")

        self.horizontalLayout_timer1.addWidget(self.label_timer_title)

        self.label_timer_status1 = QLabel(self.framestatustimer1)
        self.label_timer_status1.setObjectName(u"label_timer_status1")
        self.label_timer_status1.setFont(font2)
        self.label_timer_status1.setStyleSheet(u"    font: bold 10pt \"Segoe UI\";\n"
"    color: #380082;\n"
"")

        self.horizontalLayout_timer1.addWidget(self.label_timer_status1)


        self.verticalLayout_72.addWidget(self.framestatustimer1)

        self.framestatusscheduling1 = QFrame(self.framesocket1)
        self.framestatusscheduling1.setObjectName(u"framestatusscheduling1")
        self.framestatusscheduling1.setMinimumSize(QSize(0, 24))
        self.framestatusscheduling1.setMaximumSize(QSize(16777215, 24))
        self.framestatusscheduling1.setFrameShape(QFrame.Shape.NoFrame)
        self.framestatusscheduling1.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_scheduling1 = QHBoxLayout(self.framestatusscheduling1)
        self.horizontalLayout_scheduling1.setObjectName(u"horizontalLayout_scheduling1")
        self.horizontalLayout_scheduling1.setContentsMargins(0, 0, 0, 0)
        self.label_scheduling_title = QLabel(self.framestatusscheduling1)
        self.label_scheduling_title.setObjectName(u"label_scheduling_title")
        self.label_scheduling_title.setFont(font2)
        self.label_scheduling_title.setStyleSheet(u"    font: bold 10pt \"Segoe UI\";\n"
"    color: #380082;\n"
"")

        self.horizontalLayout_scheduling1.addWidget(self.label_scheduling_title)

        self.label_scheduling_status1 = QLabel(self.framestatusscheduling1)
        self.label_scheduling_status1.setObjectName(u"label_scheduling_status1")
        self.label_scheduling_status1.setFont(font2)
        self.label_scheduling_status1.setStyleSheet(u"    font: bold 10pt \"Segoe UI\";\n"
"    color: #380082;\n"
"")

        self.horizontalLayout_scheduling1.addWidget(self.label_scheduling_status1)


        self.verticalLayout_72.addWidget(self.framestatusscheduling1)

        self.framebuttonaction1 = QFrame(self.framesocket1)
        self.framebuttonaction1.setObjectName(u"framebuttonaction1")
        self.framebuttonaction1.setMinimumSize(QSize(0, 35))
        self.framebuttonaction1.setMaximumSize(QSize(16777215, 35))
        self.framebuttonaction1.setFrameShape(QFrame.Shape.NoFrame)
        self.framebuttonaction1.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_action1 = QHBoxLayout(self.framebuttonaction1)
        self.horizontalLayout_action1.setObjectName(u"horizontalLayout_action1")
        self.horizontalLayout_action1.setContentsMargins(0, 0, 0, 0)
        self.btn_action_socket1 = QPushButton(self.framebuttonaction1)
        self.btn_action_socket1.setObjectName(u"btn_action_socket1")
        self.btn_action_socket1.setMinimumSize(QSize(0, 35))
        self.btn_action_socket1.setFont(font2)
        self.btn_action_socket1.setStyleSheet(u"QPushButton#btn_action_socket1 {\n"
"    background-color: #ab6dfc;      /* warna utama */\n"
"    color: white;\n"
"    font: bold 10pt \"Segoe UI\";     /* teks bold */\n"
"    border: none;\n"
"    border-radius: 6px;\n"
"    padding: 6px 12px;\n"
"}\n"
"\n"
"/* Hover: sedikit lebih terang */\n"
"QPushButton#btn_action_socket1:hover {\n"
"    background-color: #c085fc;      /* ungu terang lebih soft */\n"
"}\n"
"\n"
"/* Pressed: sedikit lebih gelap */\n"
"QPushButton#btn_action_socket1:pressed {\n"
"    background-color: #914de6;      /* ungu gelap */\n"
"}")

        self.horizontalLayout_action1.addWidget(self.btn_action_socket1)


        self.verticalLayout_72.addWidget(self.framebuttonaction1)


        self.horizontalLayout_111.addWidget(self.framesocket1)

        self.framesocket2 = QFrame(self.framecontentSmartsocket)
        self.framesocket2.setObjectName(u"framesocket2")
        self.framesocket2.setMinimumSize(QSize(0, 700))
        self.framesocket2.setMaximumSize(QSize(16777215, 700))
        self.framesocket2.setStyleSheet(u"#framesocket2{\n"
"	background-color: #ECF5FB;   /* biru pucat */\n"
"	border: 2px solid #DDEBF7;\n"
"	border-radius: 10px;\n"
"}")
        self.framesocket2.setFrameShape(QFrame.Shape.NoFrame)
        self.framesocket2.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_75 = QVBoxLayout(self.framesocket2)
        self.verticalLayout_75.setObjectName(u"verticalLayout_75")
        self.frametitlesocket2 = QFrame(self.framesocket2)
        self.frametitlesocket2.setObjectName(u"frametitlesocket2")
        self.frametitlesocket2.setMinimumSize(QSize(0, 0))
        self.frametitlesocket2.setMaximumSize(QSize(16777215, 50))
        self.frametitlesocket2.setFrameShape(QFrame.Shape.NoFrame)
        self.frametitlesocket2.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_95 = QHBoxLayout(self.frametitlesocket2)
        self.horizontalLayout_95.setSpacing(0)
        self.horizontalLayout_95.setObjectName(u"horizontalLayout_95")
        self.horizontalLayout_95.setContentsMargins(0, 0, 0, 0)
        self.frame_86 = QFrame(self.frametitlesocket2)
        self.frame_86.setObjectName(u"frame_86")
        self.frame_86.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_86.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_95.addWidget(self.frame_86)

        self.titlesmart2 = QLabel(self.frametitlesocket2)
        self.titlesmart2.setObjectName(u"titlesmart2")
        sizePolicy2.setHeightForWidth(self.titlesmart2.sizePolicy().hasHeightForWidth())
        self.titlesmart2.setSizePolicy(sizePolicy2)
        self.titlesmart2.setMinimumSize(QSize(96, 40))
        self.titlesmart2.setMaximumSize(QSize(136, 45))
        self.titlesmart2.setFont(font4)
        self.titlesmart2.setStyleSheet(u"#titlesmart2{\n"
"    font: bold 12pt \"Segoe UI\";\n"
"	color: white;\n"
"	background-color: #64B5F6;    /* biru medium */\n"
"	border: 1px solid #42A5F5;\n"
"\n"
"\n"
"    border-radius: 8px;\n"
"    padding: 6px 12px;\n"
"    min-height: 26px;\n"
"    line-height: 18px;\n"
"\n"
"    min-width: 70px;\n"
"    max-width: 110px;\n"
"    qproperty-alignment: AlignCenter;\n"
"}\n"
"\n"
"")
        self.titlesmart2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_95.addWidget(self.titlesmart2)

        self.frame_87 = QFrame(self.frametitlesocket2)
        self.frame_87.setObjectName(u"frame_87")
        self.frame_87.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_87.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_95.addWidget(self.frame_87)


        self.verticalLayout_75.addWidget(self.frametitlesocket2)

        self.framestatussocket2 = QFrame(self.framesocket2)
        self.framestatussocket2.setObjectName(u"framestatussocket2")
        self.framestatussocket2.setMinimumSize(QSize(0, 40))
        self.framestatussocket2.setMaximumSize(QSize(16777215, 23))
        self.framestatussocket2.setFrameShape(QFrame.Shape.NoFrame)
        self.framestatussocket2.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_96 = QHBoxLayout(self.framestatussocket2)
        self.horizontalLayout_96.setSpacing(0)
        self.horizontalLayout_96.setObjectName(u"horizontalLayout_96")
        self.horizontalLayout_96.setContentsMargins(0, 0, 0, 0)
        self.frame_88 = QFrame(self.framestatussocket2)
        self.frame_88.setObjectName(u"frame_88")
        self.frame_88.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_88.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_96.addWidget(self.frame_88)

        self.statussocket2 = QLabel(self.framestatussocket2)
        self.statussocket2.setObjectName(u"statussocket2")
        sizePolicy2.setHeightForWidth(self.statussocket2.sizePolicy().hasHeightForWidth())
        self.statussocket2.setSizePolicy(sizePolicy2)
        self.statussocket2.setMinimumSize(QSize(155, 23))
        self.statussocket2.setMaximumSize(QSize(114, 23))
        self.statussocket2.setFont(font2)
        self.statussocket2.setStyleSheet(u"QLabel#statussocket2{\n"
"    font: bold 10pt \"Segoe UI\";\n"
"    color: white;\n"
"\n"
"    background-color: #CBD5E1;   /* default (abu netral) */\n"
"    border: 1px solid #94A3B8;\n"
"    border-radius: 4px;\n"
"\n"
"    padding: 2px 6px;\n"
"    min-height: 17px;\n"
"    max-width: 100px;\n"
"\n"
"    qproperty-alignment: AlignCenter;\n"
"}\n"
"\n"
"/* ===== AC ON ===== */\n"
"QLabel#statussocket2[state=\"on\"] {\n"
"    background-color: #6FCF97;   /* hijau pastel tapi jelas */\n"
"    border-color: #27AE60;\n"
"}\n"
"\n"
"/* ===== AC OFF ===== */\n"
"QLabel#statussocket2[state=\"off\"] {\n"
"    background-color: #EB5757;   /* merah pastel tegas */\n"
"    border-color: #C0392B;\n"
"}\n"
"")
        self.statussocket2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_96.addWidget(self.statussocket2)

        self.frame_89 = QFrame(self.framestatussocket2)
        self.frame_89.setObjectName(u"frame_89")
        self.frame_89.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_89.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_96.addWidget(self.frame_89)


        self.verticalLayout_75.addWidget(self.framestatussocket2)

        self.framesensor2value = QFrame(self.framesocket2)
        self.framesensor2value.setObjectName(u"framesensor2value")
        self.framesensor2value.setStyleSheet(u"QFrame#framesensor2value {\n"
"	background-color: #F0F7FC;   /* biru sangat pucat */\n"
"	border: 1px solid #E1EEF9;\n"
"	border-radius: 10px;\n"
"}\n"
"\n"
"QFrame#framesensor2value QLabel {\n"
"    font: bold 10pt \"Segoe UI\";\n"
"    color: #1565C0;\n"
"}")
        self.framesensor2value.setFrameShape(QFrame.Shape.StyledPanel)
        self.framesensor2value.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_sensor2 = QVBoxLayout(self.framesensor2value)
        self.verticalLayout_sensor2.setSpacing(4)
        self.verticalLayout_sensor2.setObjectName(u"verticalLayout_sensor2")
        self.verticalLayout_sensor2.setContentsMargins(10, 8, 10, 8)
        self.label_energy_monitoring_title_2 = QLabel(self.framesensor2value)
        self.label_energy_monitoring_title_2.setObjectName(u"label_energy_monitoring_title_2")
        self.label_energy_monitoring_title_2.setMaximumSize(QSize(16777215, 30))
        self.label_energy_monitoring_title_2.setFont(font2)
        self.label_energy_monitoring_title_2.setStyleSheet(u"#label_energy_monitoring_title_2 {\n"
"    font: bold 10pt \"Segoe UI\";\n"
"    color: white;\n"
"   background-color: #64B5F6;   /* biru medium */\n"
"    border-radius: 8px;\n"
"    padding: 6px 10px;\n"
"    border: 1px solid #42A5F5;       /* border biru */\n"
"    min-height: 9px;\n"
"    qproperty-alignment: AlignCenter;\n"
"}")
        self.label_energy_monitoring_title_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_sensor2.addWidget(self.label_energy_monitoring_title_2)

        self.verticalLayout_sensor_values_2 = QVBoxLayout()
        self.verticalLayout_sensor_values_2.setSpacing(2)
        self.verticalLayout_sensor_values_2.setObjectName(u"verticalLayout_sensor_values_2")
        self.label_voltage2 = QLabel(self.framesensor2value)
        self.label_voltage2.setObjectName(u"label_voltage2")
        self.label_voltage2.setFont(font2)
        self.label_voltage2.setStyleSheet(u"")

        self.verticalLayout_sensor_values_2.addWidget(self.label_voltage2)

        self.label_current2 = QLabel(self.framesensor2value)
        self.label_current2.setObjectName(u"label_current2")
        self.label_current2.setFont(font2)
        self.label_current2.setStyleSheet(u"")
        self.label_current2.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout_sensor_values_2.addWidget(self.label_current2)

        self.label_power2 = QLabel(self.framesensor2value)
        self.label_power2.setObjectName(u"label_power2")
        self.label_power2.setFont(font2)
        self.label_power2.setStyleSheet(u"")

        self.verticalLayout_sensor_values_2.addWidget(self.label_power2)

        self.label_energy2 = QLabel(self.framesensor2value)
        self.label_energy2.setObjectName(u"label_energy2")
        self.label_energy2.setFont(font2)
        self.label_energy2.setStyleSheet(u"")

        self.verticalLayout_sensor_values_2.addWidget(self.label_energy2)

        self.label_frequency2 = QLabel(self.framesensor2value)
        self.label_frequency2.setObjectName(u"label_frequency2")
        self.label_frequency2.setFont(font2)
        self.label_frequency2.setStyleSheet(u"")

        self.verticalLayout_sensor_values_2.addWidget(self.label_frequency2)

        self.label_powerfactor2 = QLabel(self.framesensor2value)
        self.label_powerfactor2.setObjectName(u"label_powerfactor2")
        self.label_powerfactor2.setFont(font2)
        self.label_powerfactor2.setStyleSheet(u"")

        self.verticalLayout_sensor_values_2.addWidget(self.label_powerfactor2)


        self.verticalLayout_sensor2.addLayout(self.verticalLayout_sensor_values_2)


        self.verticalLayout_75.addWidget(self.framesensor2value)

        self.frameswitch2 = QFrame(self.framesocket2)
        self.frameswitch2.setObjectName(u"frameswitch2")
        self.frameswitch2.setStyleSheet(u"#frameswitch2{\n"
"	background-color: #F0F7FC;   /* biru sangat pucat */\n"
"	border: 1px solid #E1EEF9;\n"
"	border-radius: 10px;\n"
"}")
        self.frameswitch2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frameswitch2.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_78 = QVBoxLayout(self.frameswitch2)
        self.verticalLayout_78.setSpacing(6)
        self.verticalLayout_78.setObjectName(u"verticalLayout_78")
        self.verticalLayout_78.setContentsMargins(8, 8, 8, 8)
        self.frame_90 = QFrame(self.frameswitch2)
        self.frame_90.setObjectName(u"frame_90")
        self.frame_90.setMinimumSize(QSize(0, 20))
        self.frame_90.setMaximumSize(QSize(16777215, 30))
        self.frame_90.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_90.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_97 = QHBoxLayout(self.frame_90)
        self.horizontalLayout_97.setSpacing(0)
        self.horizontalLayout_97.setObjectName(u"horizontalLayout_97")
        self.horizontalLayout_97.setContentsMargins(0, 0, 0, 0)
        self.frame_91 = QFrame(self.frame_90)
        self.frame_91.setObjectName(u"frame_91")
        self.frame_91.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_91.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_97.addWidget(self.frame_91)

        self.label_switch_status_title_2 = QLabel(self.frame_90)
        self.label_switch_status_title_2.setObjectName(u"label_switch_status_title_2")
        self.label_switch_status_title_2.setFont(font2)
        self.label_switch_status_title_2.setStyleSheet(u"QLabel#label_switch_status_title_2{\n"
"	font: bold 10pt \"Segoe UI\";\n"
"	color: white;\n"
"	background-color: #64B5F6;    /* biru medium */\n"
"	border: 1px solid #42A5F5;\n"
"\n"
"\n"
"    border-radius: 6px;\n"
"    padding: 6px 12px;\n"
"    min-height: 10px;\n"
"    line-height: 5px;\n"
"    qproperty-alignment: AlignCenter;\n"
"}\n"
"\n"
"")

        self.horizontalLayout_97.addWidget(self.label_switch_status_title_2)

        self.frame_92 = QFrame(self.frame_90)
        self.frame_92.setObjectName(u"frame_92")
        self.frame_92.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_92.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_97.addWidget(self.frame_92)


        self.verticalLayout_78.addWidget(self.frame_90)

        self.frame_93 = QFrame(self.frameswitch2)
        self.frame_93.setObjectName(u"frame_93")
        self.frame_93.setMinimumSize(QSize(0, 0))
        self.frame_93.setMaximumSize(QSize(16777215, 30))
        self.frame_93.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_93.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_98 = QHBoxLayout(self.frame_93)
        self.horizontalLayout_98.setSpacing(0)
        self.horizontalLayout_98.setObjectName(u"horizontalLayout_98")
        self.horizontalLayout_98.setContentsMargins(0, 0, 0, 0)
        self.frame_94 = QFrame(self.frame_93)
        self.frame_94.setObjectName(u"frame_94")
        self.frame_94.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_94.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_98.addWidget(self.frame_94)

        self.label_switch_status_value2 = QLabel(self.frame_93)
        self.label_switch_status_value2.setObjectName(u"label_switch_status_value2")
        self.label_switch_status_value2.setMinimumSize(QSize(0, 30))
        self.label_switch_status_value2.setMaximumSize(QSize(100, 30))
        self.label_switch_status_value2.setFont(font11)
        self.label_switch_status_value2.setStyleSheet(u"QLabel#label_switch_status_value2{\n"
"    color: white;\n"
"    background-color: #EB5757;\n"
"    border: 1px solid #C0392B;\n"
"    border-radius: 4px;\n"
"    padding: 4px 8px;\n"
"    qproperty-alignment: AlignCenter;\n"
"font: bold 9pt \"Segoe UI\";\n"
"}\n"
"QLabel#label_switch_status_value2[state=\"on\"] {\n"
"    background-color: #6FCF97;\n"
"    border-color: #27AE60;\n"
"}")
        self.label_switch_status_value2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_98.addWidget(self.label_switch_status_value2)

        self.frame_95 = QFrame(self.frame_93)
        self.frame_95.setObjectName(u"frame_95")
        self.frame_95.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_95.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_98.addWidget(self.frame_95)


        self.verticalLayout_78.addWidget(self.frame_93)

        self.frame_switch_button_container_2 = QFrame(self.frameswitch2)
        self.frame_switch_button_container_2.setObjectName(u"frame_switch_button_container_2")
        self.frame_switch_button_container_2.setMinimumSize(QSize(0, 35))
        self.frame_switch_button_container_2.setFrameShape(QFrame.Shape.NoFrame)

        self.verticalLayout_78.addWidget(self.frame_switch_button_container_2)


        self.verticalLayout_75.addWidget(self.frameswitch2)

        self.framestatustimer2 = QFrame(self.framesocket2)
        self.framestatustimer2.setObjectName(u"framestatustimer2")
        self.framestatustimer2.setMinimumSize(QSize(0, 24))
        self.framestatustimer2.setMaximumSize(QSize(16777215, 24))
        self.framestatustimer2.setStyleSheet(u"")
        self.framestatustimer2.setFrameShape(QFrame.Shape.NoFrame)
        self.framestatustimer2.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_timer2 = QHBoxLayout(self.framestatustimer2)
        self.horizontalLayout_timer2.setObjectName(u"horizontalLayout_timer2")
        self.horizontalLayout_timer2.setContentsMargins(0, 0, 0, 0)
        self.label_timer_title_2 = QLabel(self.framestatustimer2)
        self.label_timer_title_2.setObjectName(u"label_timer_title_2")
        self.label_timer_title_2.setFont(font2)
        self.label_timer_title_2.setStyleSheet(u"    font: bold 10pt \"Segoe UI\";\n"
"    color: #1565C0;\n"
"")

        self.horizontalLayout_timer2.addWidget(self.label_timer_title_2)

        self.label_timer_status2 = QLabel(self.framestatustimer2)
        self.label_timer_status2.setObjectName(u"label_timer_status2")
        self.label_timer_status2.setFont(font2)
        self.label_timer_status2.setStyleSheet(u"    font: bold 10pt \"Segoe UI\";\n"
"    color: #1565C0;\n"
"")

        self.horizontalLayout_timer2.addWidget(self.label_timer_status2)


        self.verticalLayout_75.addWidget(self.framestatustimer2)

        self.framestatusscheduling2 = QFrame(self.framesocket2)
        self.framestatusscheduling2.setObjectName(u"framestatusscheduling2")
        self.framestatusscheduling2.setMinimumSize(QSize(0, 24))
        self.framestatusscheduling2.setMaximumSize(QSize(16777215, 24))
        self.framestatusscheduling2.setFrameShape(QFrame.Shape.NoFrame)
        self.framestatusscheduling2.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_scheduling2 = QHBoxLayout(self.framestatusscheduling2)
        self.horizontalLayout_scheduling2.setObjectName(u"horizontalLayout_scheduling2")
        self.horizontalLayout_scheduling2.setContentsMargins(0, 0, 0, 0)
        self.label_scheduling_title_2 = QLabel(self.framestatusscheduling2)
        self.label_scheduling_title_2.setObjectName(u"label_scheduling_title_2")
        self.label_scheduling_title_2.setFont(font2)
        self.label_scheduling_title_2.setStyleSheet(u"    font: bold 10pt \"Segoe UI\";\n"
"    color: #1565C0;\n"
"")

        self.horizontalLayout_scheduling2.addWidget(self.label_scheduling_title_2)

        self.label_scheduling_status2 = QLabel(self.framestatusscheduling2)
        self.label_scheduling_status2.setObjectName(u"label_scheduling_status2")
        self.label_scheduling_status2.setFont(font2)
        self.label_scheduling_status2.setStyleSheet(u"    font: bold 10pt \"Segoe UI\";\n"
"    color: #1565C0;\n"
"")

        self.horizontalLayout_scheduling2.addWidget(self.label_scheduling_status2)


        self.verticalLayout_75.addWidget(self.framestatusscheduling2)

        self.framebuttonaction2 = QFrame(self.framesocket2)
        self.framebuttonaction2.setObjectName(u"framebuttonaction2")
        self.framebuttonaction2.setMinimumSize(QSize(0, 35))
        self.framebuttonaction2.setMaximumSize(QSize(16777215, 35))
        self.framebuttonaction2.setFrameShape(QFrame.Shape.NoFrame)
        self.framebuttonaction2.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_action2 = QHBoxLayout(self.framebuttonaction2)
        self.horizontalLayout_action2.setObjectName(u"horizontalLayout_action2")
        self.horizontalLayout_action2.setContentsMargins(0, 0, 0, 0)
        self.btn_action_socket2 = QPushButton(self.framebuttonaction2)
        self.btn_action_socket2.setObjectName(u"btn_action_socket2")
        self.btn_action_socket2.setMinimumSize(QSize(0, 35))
        self.btn_action_socket2.setFont(font2)
        self.btn_action_socket2.setStyleSheet(u"QPushButton#btn_action_socket2 {\n"
"    background-color: #42A5F5;      /* biru medium */\n"
"    color: white;\n"
"    font: bold 10pt \"Segoe UI\";     /* teks bold */\n"
"    border: none;\n"
"    border-radius: 6px;\n"
"    padding: 6px 12px;\n"
"}\n"
"\n"
"/* Hover: sedikit lebih terang */\n"
"QPushButton#btn_action_socket2:hover {\n"
"    background-color: #64B5F6;      /* biru terang */\n"
"}\n"
"\n"
"/* Pressed: sedikit lebih gelap */\n"
"QPushButton#btn_action_socket2:pressed {\n"
"    background-color: #1976D2;      /* biru gelap */\n"
"}")

        self.horizontalLayout_action2.addWidget(self.btn_action_socket2)


        self.verticalLayout_75.addWidget(self.framebuttonaction2)


        self.horizontalLayout_111.addWidget(self.framesocket2)

        self.framesocket3 = QFrame(self.framecontentSmartsocket)
        self.framesocket3.setObjectName(u"framesocket3")
        self.framesocket3.setMinimumSize(QSize(0, 700))
        self.framesocket3.setMaximumSize(QSize(16777215, 700))
        self.framesocket3.setStyleSheet(u"#framesocket3{\n"
"	background-color: #eee3fa;   /* ungu lembut banget */\n"
"	border: 2px solid #E3DAF1;\n"
"	border-radius: 10px;\n"
"}")
        self.framesocket3.setFrameShape(QFrame.Shape.NoFrame)
        self.framesocket3.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_79 = QVBoxLayout(self.framesocket3)
        self.verticalLayout_79.setObjectName(u"verticalLayout_79")
        self.frametitlesocket3 = QFrame(self.framesocket3)
        self.frametitlesocket3.setObjectName(u"frametitlesocket3")
        self.frametitlesocket3.setMinimumSize(QSize(0, 0))
        self.frametitlesocket3.setMaximumSize(QSize(16777215, 50))
        self.frametitlesocket3.setFrameShape(QFrame.Shape.NoFrame)
        self.frametitlesocket3.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_99 = QHBoxLayout(self.frametitlesocket3)
        self.horizontalLayout_99.setSpacing(0)
        self.horizontalLayout_99.setObjectName(u"horizontalLayout_99")
        self.horizontalLayout_99.setContentsMargins(0, 0, 0, 0)
        self.frame_96 = QFrame(self.frametitlesocket3)
        self.frame_96.setObjectName(u"frame_96")
        self.frame_96.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_96.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_99.addWidget(self.frame_96)

        self.titlesmart3 = QLabel(self.frametitlesocket3)
        self.titlesmart3.setObjectName(u"titlesmart3")
        sizePolicy2.setHeightForWidth(self.titlesmart3.sizePolicy().hasHeightForWidth())
        self.titlesmart3.setSizePolicy(sizePolicy2)
        self.titlesmart3.setMinimumSize(QSize(96, 40))
        self.titlesmart3.setMaximumSize(QSize(136, 45))
        self.titlesmart3.setFont(font4)
        self.titlesmart3.setStyleSheet(u"#titlesmart3{\n"
"font: bold 12pt \"Segoe UI\";\n"
"color: white;\n"
"background-color: #8E7AB5;   /* ungu battery */\n"
"    border: 1px solid #6E8E8B;\n"
"\n"
"\n"
"    border-radius: 8px;\n"
"    padding: 6px 12px;\n"
"    min-height: 26px;\n"
"    line-height: 18px;\n"
"\n"
"    min-width: 70px;\n"
"    max-width: 110px;\n"
"    qproperty-alignment: AlignCenter;\n"
"}\n"
"\n"
"")
        self.titlesmart3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_99.addWidget(self.titlesmart3)

        self.frame_97 = QFrame(self.frametitlesocket3)
        self.frame_97.setObjectName(u"frame_97")
        self.frame_97.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_97.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_99.addWidget(self.frame_97)


        self.verticalLayout_79.addWidget(self.frametitlesocket3)

        self.framestatussocket3 = QFrame(self.framesocket3)
        self.framestatussocket3.setObjectName(u"framestatussocket3")
        self.framestatussocket3.setMinimumSize(QSize(0, 40))
        self.framestatussocket3.setMaximumSize(QSize(16777215, 23))
        self.framestatussocket3.setFrameShape(QFrame.Shape.NoFrame)
        self.framestatussocket3.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_100 = QHBoxLayout(self.framestatussocket3)
        self.horizontalLayout_100.setSpacing(0)
        self.horizontalLayout_100.setObjectName(u"horizontalLayout_100")
        self.horizontalLayout_100.setContentsMargins(0, 0, 0, 0)
        self.frame_98 = QFrame(self.framestatussocket3)
        self.frame_98.setObjectName(u"frame_98")
        self.frame_98.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_98.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_100.addWidget(self.frame_98)

        self.statussocket3 = QLabel(self.framestatussocket3)
        self.statussocket3.setObjectName(u"statussocket3")
        sizePolicy2.setHeightForWidth(self.statussocket3.sizePolicy().hasHeightForWidth())
        self.statussocket3.setSizePolicy(sizePolicy2)
        self.statussocket3.setMinimumSize(QSize(155, 23))
        self.statussocket3.setMaximumSize(QSize(114, 23))
        self.statussocket3.setFont(font2)
        self.statussocket3.setStyleSheet(u"QLabel#statussocket3{\n"
"    font: bold 10pt \"Segoe UI\";\n"
"    color: white;\n"
"\n"
"    background-color: #CBD5E1;   /* default (abu netral) */\n"
"    border: 1px solid #94A3B8;\n"
"    border-radius: 4px;\n"
"\n"
"    padding: 2px 6px;\n"
"    min-height: 17px;\n"
"    max-width: 100px;\n"
"\n"
"    qproperty-alignment: AlignCenter;\n"
"}\n"
"\n"
"/* ===== AC ON ===== */\n"
"QLabel#statussocket3[state=\"on\"] {\n"
"    background-color: #6FCF97;   /* hijau pastel tapi jelas */\n"
"    border-color: #27AE60;\n"
"}\n"
"\n"
"/* ===== AC OFF ===== */\n"
"QLabel#statussocket3[state=\"off\"] {\n"
"    background-color: #EB5757;   /* merah pastel tegas */\n"
"    border-color: #C0392B;\n"
"}\n"
"")
        self.statussocket3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_100.addWidget(self.statussocket3)

        self.frame_99 = QFrame(self.framestatussocket3)
        self.frame_99.setObjectName(u"frame_99")
        self.frame_99.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_99.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_100.addWidget(self.frame_99)


        self.verticalLayout_79.addWidget(self.framestatussocket3)

        self.framesensor3value = QFrame(self.framesocket3)
        self.framesensor3value.setObjectName(u"framesensor3value")
        self.framesensor3value.setStyleSheet(u"QFrame#framesensor3value {\n"
"	background-color: #F2ECF9;   /* ungu lembut banget */\n"
"	border: 1px solid #E3DAF1;\n"
"	border-radius: 10px;\n"
"}\n"
"\n"
"QFrame#framesensor3value QLabel {\n"
"    font: bold 10pt \"Segoe UI\";\n"
"    color: #380082;\n"
"}")
        self.framesensor3value.setFrameShape(QFrame.Shape.StyledPanel)
        self.framesensor3value.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_sensor3 = QVBoxLayout(self.framesensor3value)
        self.verticalLayout_sensor3.setSpacing(4)
        self.verticalLayout_sensor3.setObjectName(u"verticalLayout_sensor3")
        self.verticalLayout_sensor3.setContentsMargins(10, 8, 10, 8)
        self.label_energy_monitoring_title_3 = QLabel(self.framesensor3value)
        self.label_energy_monitoring_title_3.setObjectName(u"label_energy_monitoring_title_3")
        self.label_energy_monitoring_title_3.setMaximumSize(QSize(16777215, 30))
        self.label_energy_monitoring_title_3.setFont(font2)
        self.label_energy_monitoring_title_3.setStyleSheet(u"#label_energy_monitoring_title_3{\n"
"    font: bold 10pt \"Segoe UI\";\n"
"    color: white;\n"
"    background-color: #bd95f0;        /* ungu soft */\n"
"    border-radius: 8px;\n"
"    padding: 6px 10px;\n"
"    border: 1px solid #9B7BCB;       /* border ungu gelap tapi harmonis */\n"
"    min-height: 9px;\n"
"    qproperty-alignment: AlignCenter;\n"
"}")
        self.label_energy_monitoring_title_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_sensor3.addWidget(self.label_energy_monitoring_title_3)

        self.verticalLayout_sensor_values_3 = QVBoxLayout()
        self.verticalLayout_sensor_values_3.setSpacing(2)
        self.verticalLayout_sensor_values_3.setObjectName(u"verticalLayout_sensor_values_3")
        self.label_voltage3 = QLabel(self.framesensor3value)
        self.label_voltage3.setObjectName(u"label_voltage3")
        self.label_voltage3.setFont(font2)
        self.label_voltage3.setStyleSheet(u"")

        self.verticalLayout_sensor_values_3.addWidget(self.label_voltage3)

        self.label_current3 = QLabel(self.framesensor3value)
        self.label_current3.setObjectName(u"label_current3")
        self.label_current3.setFont(font2)
        self.label_current3.setStyleSheet(u"")
        self.label_current3.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout_sensor_values_3.addWidget(self.label_current3)

        self.label_power3 = QLabel(self.framesensor3value)
        self.label_power3.setObjectName(u"label_power3")
        self.label_power3.setFont(font2)
        self.label_power3.setStyleSheet(u"")

        self.verticalLayout_sensor_values_3.addWidget(self.label_power3)

        self.label_energy3 = QLabel(self.framesensor3value)
        self.label_energy3.setObjectName(u"label_energy3")
        self.label_energy3.setFont(font2)
        self.label_energy3.setStyleSheet(u"")

        self.verticalLayout_sensor_values_3.addWidget(self.label_energy3)

        self.label_frequency3 = QLabel(self.framesensor3value)
        self.label_frequency3.setObjectName(u"label_frequency3")
        self.label_frequency3.setFont(font2)
        self.label_frequency3.setStyleSheet(u"")

        self.verticalLayout_sensor_values_3.addWidget(self.label_frequency3)

        self.label_powerfactor3 = QLabel(self.framesensor3value)
        self.label_powerfactor3.setObjectName(u"label_powerfactor3")
        self.label_powerfactor3.setFont(font2)
        self.label_powerfactor3.setStyleSheet(u"")

        self.verticalLayout_sensor_values_3.addWidget(self.label_powerfactor3)


        self.verticalLayout_sensor3.addLayout(self.verticalLayout_sensor_values_3)


        self.verticalLayout_79.addWidget(self.framesensor3value)

        self.frameswitch3 = QFrame(self.framesocket3)
        self.frameswitch3.setObjectName(u"frameswitch3")
        self.frameswitch3.setStyleSheet(u"#frameswitch3{\n"
"	background-color: #F2ECF9;   /* ungu lembut banget */\n"
"	border: 1px solid #E3DAF1;\n"
"	border-radius: 10px;\n"
"}")
        self.frameswitch3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frameswitch3.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_80 = QVBoxLayout(self.frameswitch3)
        self.verticalLayout_80.setSpacing(6)
        self.verticalLayout_80.setObjectName(u"verticalLayout_80")
        self.verticalLayout_80.setContentsMargins(8, 8, 8, 8)
        self.frame_100 = QFrame(self.frameswitch3)
        self.frame_100.setObjectName(u"frame_100")
        self.frame_100.setMinimumSize(QSize(0, 20))
        self.frame_100.setMaximumSize(QSize(16777215, 30))
        self.frame_100.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_100.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_101 = QHBoxLayout(self.frame_100)
        self.horizontalLayout_101.setSpacing(0)
        self.horizontalLayout_101.setObjectName(u"horizontalLayout_101")
        self.horizontalLayout_101.setContentsMargins(0, 0, 0, 0)
        self.frame_101 = QFrame(self.frame_100)
        self.frame_101.setObjectName(u"frame_101")
        self.frame_101.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_101.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_101.addWidget(self.frame_101)

        self.label_switch_status_title_3 = QLabel(self.frame_100)
        self.label_switch_status_title_3.setObjectName(u"label_switch_status_title_3")
        self.label_switch_status_title_3.setFont(font2)
        self.label_switch_status_title_3.setStyleSheet(u"QLabel#label_switch_status_title_3{\n"
"	font: bold 10pt \"Segoe UI\";\n"
"	color: white;\n"
"	background-color: #bd95f0;    /* ungu battery */\n"
"	border: 1px solid #9B7BCB; \n"
"\n"
"\n"
"    border-radius: 6px;\n"
"    padding: 6px 12px;\n"
"    min-height: 10px;\n"
"    line-height: 5px;\n"
"    qproperty-alignment: AlignCenter;\n"
"}\n"
"\n"
"")

        self.horizontalLayout_101.addWidget(self.label_switch_status_title_3)

        self.frame_102 = QFrame(self.frame_100)
        self.frame_102.setObjectName(u"frame_102")
        self.frame_102.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_102.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_101.addWidget(self.frame_102)


        self.verticalLayout_80.addWidget(self.frame_100)

        self.frame_103 = QFrame(self.frameswitch3)
        self.frame_103.setObjectName(u"frame_103")
        self.frame_103.setMinimumSize(QSize(0, 0))
        self.frame_103.setMaximumSize(QSize(16777215, 30))
        self.frame_103.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_103.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_102 = QHBoxLayout(self.frame_103)
        self.horizontalLayout_102.setSpacing(0)
        self.horizontalLayout_102.setObjectName(u"horizontalLayout_102")
        self.horizontalLayout_102.setContentsMargins(0, 0, 0, 0)
        self.frame_104 = QFrame(self.frame_103)
        self.frame_104.setObjectName(u"frame_104")
        self.frame_104.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_104.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_102.addWidget(self.frame_104)

        self.label_switch_status_value3 = QLabel(self.frame_103)
        self.label_switch_status_value3.setObjectName(u"label_switch_status_value3")
        self.label_switch_status_value3.setMinimumSize(QSize(0, 30))
        self.label_switch_status_value3.setMaximumSize(QSize(100, 30))
        self.label_switch_status_value3.setFont(font11)
        self.label_switch_status_value3.setStyleSheet(u"QLabel#label_switch_status_value3{\n"
"    color: white;\n"
"    background-color: #EB5757;\n"
"    border: 1px solid #C0392B;\n"
"    border-radius: 4px;\n"
"    padding: 4px 8px;\n"
"    qproperty-alignment: AlignCenter;\n"
"font: bold 9pt \"Segoe UI\";\n"
"}\n"
"QLabel#label_switch_status_value3[state=\"on\"] {\n"
"    background-color: #6FCF97;\n"
"    border-color: #27AE60;\n"
"}")
        self.label_switch_status_value3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_102.addWidget(self.label_switch_status_value3)

        self.frame_105 = QFrame(self.frame_103)
        self.frame_105.setObjectName(u"frame_105")
        self.frame_105.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_105.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_102.addWidget(self.frame_105)


        self.verticalLayout_80.addWidget(self.frame_103)

        self.frame_switch_button_container_3 = QFrame(self.frameswitch3)
        self.frame_switch_button_container_3.setObjectName(u"frame_switch_button_container_3")
        self.frame_switch_button_container_3.setMinimumSize(QSize(0, 35))
        self.frame_switch_button_container_3.setFrameShape(QFrame.Shape.NoFrame)

        self.verticalLayout_80.addWidget(self.frame_switch_button_container_3)


        self.verticalLayout_79.addWidget(self.frameswitch3)

        self.framestatustimer3 = QFrame(self.framesocket3)
        self.framestatustimer3.setObjectName(u"framestatustimer3")
        self.framestatustimer3.setMinimumSize(QSize(0, 24))
        self.framestatustimer3.setMaximumSize(QSize(16777215, 24))
        self.framestatustimer3.setStyleSheet(u"")
        self.framestatustimer3.setFrameShape(QFrame.Shape.NoFrame)
        self.framestatustimer3.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_timer3 = QHBoxLayout(self.framestatustimer3)
        self.horizontalLayout_timer3.setObjectName(u"horizontalLayout_timer3")
        self.horizontalLayout_timer3.setContentsMargins(0, 0, 0, 0)
        self.label_timer_title_3 = QLabel(self.framestatustimer3)
        self.label_timer_title_3.setObjectName(u"label_timer_title_3")
        self.label_timer_title_3.setFont(font2)
        self.label_timer_title_3.setStyleSheet(u"    font: bold 10pt \"Segoe UI\";\n"
"    color: #380082;\n"
"")

        self.horizontalLayout_timer3.addWidget(self.label_timer_title_3)

        self.label_timer_status3 = QLabel(self.framestatustimer3)
        self.label_timer_status3.setObjectName(u"label_timer_status3")
        self.label_timer_status3.setFont(font2)
        self.label_timer_status3.setStyleSheet(u"    font: bold 10pt \"Segoe UI\";\n"
"    color: #380082;\n"
"")

        self.horizontalLayout_timer3.addWidget(self.label_timer_status3)


        self.verticalLayout_79.addWidget(self.framestatustimer3)

        self.framestatusscheduling3 = QFrame(self.framesocket3)
        self.framestatusscheduling3.setObjectName(u"framestatusscheduling3")
        self.framestatusscheduling3.setMinimumSize(QSize(0, 24))
        self.framestatusscheduling3.setMaximumSize(QSize(16777215, 24))
        self.framestatusscheduling3.setFrameShape(QFrame.Shape.NoFrame)
        self.framestatusscheduling3.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_scheduling3 = QHBoxLayout(self.framestatusscheduling3)
        self.horizontalLayout_scheduling3.setObjectName(u"horizontalLayout_scheduling3")
        self.horizontalLayout_scheduling3.setContentsMargins(0, 0, 0, 0)
        self.label_scheduling_title_3 = QLabel(self.framestatusscheduling3)
        self.label_scheduling_title_3.setObjectName(u"label_scheduling_title_3")
        self.label_scheduling_title_3.setFont(font2)
        self.label_scheduling_title_3.setStyleSheet(u"    font: bold 10pt \"Segoe UI\";\n"
"    color: #380082;\n"
"")

        self.horizontalLayout_scheduling3.addWidget(self.label_scheduling_title_3)

        self.label_scheduling_status3 = QLabel(self.framestatusscheduling3)
        self.label_scheduling_status3.setObjectName(u"label_scheduling_status3")
        self.label_scheduling_status3.setFont(font2)
        self.label_scheduling_status3.setStyleSheet(u"    font: bold 10pt \"Segoe UI\";\n"
"    color: #380082;\n"
"")

        self.horizontalLayout_scheduling3.addWidget(self.label_scheduling_status3)


        self.verticalLayout_79.addWidget(self.framestatusscheduling3)

        self.framebuttonaction3 = QFrame(self.framesocket3)
        self.framebuttonaction3.setObjectName(u"framebuttonaction3")
        self.framebuttonaction3.setMinimumSize(QSize(0, 35))
        self.framebuttonaction3.setMaximumSize(QSize(16777215, 35))
        self.framebuttonaction3.setFrameShape(QFrame.Shape.NoFrame)
        self.framebuttonaction3.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_action3 = QHBoxLayout(self.framebuttonaction3)
        self.horizontalLayout_action3.setObjectName(u"horizontalLayout_action3")
        self.horizontalLayout_action3.setContentsMargins(0, 0, 0, 0)
        self.btn_action_socket3 = QPushButton(self.framebuttonaction3)
        self.btn_action_socket3.setObjectName(u"btn_action_socket3")
        self.btn_action_socket3.setMinimumSize(QSize(0, 35))
        self.btn_action_socket3.setFont(font2)
        self.btn_action_socket3.setStyleSheet(u"QPushButton#btn_action_socket3 {\n"
"    background-color: #ab6dfc;      /* warna utama */\n"
"    color: white;\n"
"    font: bold 10pt \"Segoe UI\";     /* teks bold */\n"
"    border: none;\n"
"    border-radius: 6px;\n"
"    padding: 6px 12px;\n"
"}\n"
"\n"
"/* Hover: sedikit lebih terang */\n"
"QPushButton#btn_action_socket3:hover {\n"
"    background-color: #c085fc;      /* ungu terang lebih soft */\n"
"}\n"
"\n"
"/* Pressed: sedikit lebih gelap */\n"
"QPushButton#btn_action_socket3:pressed {\n"
"    background-color: #914de6;      /* ungu gelap */\n"
"}")

        self.horizontalLayout_action3.addWidget(self.btn_action_socket3)


        self.verticalLayout_79.addWidget(self.framebuttonaction3)


        self.horizontalLayout_111.addWidget(self.framesocket3)

        self.framesocket4 = QFrame(self.framecontentSmartsocket)
        self.framesocket4.setObjectName(u"framesocket4")
        self.framesocket4.setMinimumSize(QSize(0, 700))
        self.framesocket4.setMaximumSize(QSize(16777215, 700))
        self.framesocket4.setStyleSheet(u"#framesocket4{\n"
"	background-color: #ECF5FB;   /* biru pucat */\n"
"	border: 2px solid #DDEBF7;\n"
"	border-radius: 10px;\n"
"}")
        self.framesocket4.setFrameShape(QFrame.Shape.NoFrame)
        self.framesocket4.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_81 = QVBoxLayout(self.framesocket4)
        self.verticalLayout_81.setObjectName(u"verticalLayout_81")
        self.frametitlesocket4 = QFrame(self.framesocket4)
        self.frametitlesocket4.setObjectName(u"frametitlesocket4")
        self.frametitlesocket4.setMinimumSize(QSize(0, 0))
        self.frametitlesocket4.setMaximumSize(QSize(16777215, 50))
        self.frametitlesocket4.setFrameShape(QFrame.Shape.NoFrame)
        self.frametitlesocket4.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_103 = QHBoxLayout(self.frametitlesocket4)
        self.horizontalLayout_103.setSpacing(0)
        self.horizontalLayout_103.setObjectName(u"horizontalLayout_103")
        self.horizontalLayout_103.setContentsMargins(0, 0, 0, 0)
        self.frame_106 = QFrame(self.frametitlesocket4)
        self.frame_106.setObjectName(u"frame_106")
        self.frame_106.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_106.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_103.addWidget(self.frame_106)

        self.titlesmart4 = QLabel(self.frametitlesocket4)
        self.titlesmart4.setObjectName(u"titlesmart4")
        sizePolicy2.setHeightForWidth(self.titlesmart4.sizePolicy().hasHeightForWidth())
        self.titlesmart4.setSizePolicy(sizePolicy2)
        self.titlesmart4.setMinimumSize(QSize(96, 40))
        self.titlesmart4.setMaximumSize(QSize(136, 45))
        self.titlesmart4.setFont(font4)
        self.titlesmart4.setStyleSheet(u"#titlesmart4{\n"
"font: bold 12pt \"Segoe UI\";\n"
"color: white;\n"
"background-color: #64B5F6;   /* biru medium */\n"
"    border: 1px solid #42A5F5;\n"
"\n"
"\n"
"    border-radius: 8px;\n"
"    padding: 6px 12px;\n"
"    min-height: 26px;\n"
"    line-height: 18px;\n"
"\n"
"    min-width: 70px;\n"
"    max-width: 110px;\n"
"    qproperty-alignment: AlignCenter;\n"
"}\n"
"\n"
"")
        self.titlesmart4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_103.addWidget(self.titlesmart4)

        self.frame_107 = QFrame(self.frametitlesocket4)
        self.frame_107.setObjectName(u"frame_107")
        self.frame_107.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_107.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_103.addWidget(self.frame_107)


        self.verticalLayout_81.addWidget(self.frametitlesocket4)

        self.framestatussocket4 = QFrame(self.framesocket4)
        self.framestatussocket4.setObjectName(u"framestatussocket4")
        self.framestatussocket4.setMinimumSize(QSize(0, 40))
        self.framestatussocket4.setMaximumSize(QSize(16777215, 23))
        self.framestatussocket4.setFrameShape(QFrame.Shape.NoFrame)
        self.framestatussocket4.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_104 = QHBoxLayout(self.framestatussocket4)
        self.horizontalLayout_104.setSpacing(0)
        self.horizontalLayout_104.setObjectName(u"horizontalLayout_104")
        self.horizontalLayout_104.setContentsMargins(0, 0, 0, 0)
        self.frame_108 = QFrame(self.framestatussocket4)
        self.frame_108.setObjectName(u"frame_108")
        self.frame_108.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_108.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_104.addWidget(self.frame_108)

        self.statussocket4 = QLabel(self.framestatussocket4)
        self.statussocket4.setObjectName(u"statussocket4")
        sizePolicy2.setHeightForWidth(self.statussocket4.sizePolicy().hasHeightForWidth())
        self.statussocket4.setSizePolicy(sizePolicy2)
        self.statussocket4.setMinimumSize(QSize(155, 23))
        self.statussocket4.setMaximumSize(QSize(114, 23))
        self.statussocket4.setFont(font2)
        self.statussocket4.setStyleSheet(u"QLabel#statussocket4{\n"
"    font: bold 10pt \"Segoe UI\";\n"
"    color: white;\n"
"\n"
"    background-color: #CBD5E1;   /* default (abu netral) */\n"
"    border: 1px solid #94A3B8;\n"
"    border-radius: 4px;\n"
"\n"
"    padding: 2px 6px;\n"
"    min-height: 17px;\n"
"    max-width: 100px;\n"
"\n"
"    qproperty-alignment: AlignCenter;\n"
"}\n"
"\n"
"/* ===== AC ON ===== */\n"
"QLabel#statussocket4[state=\"on\"] {\n"
"    background-color: #6FCF97;   /* hijau pastel tapi jelas */\n"
"    border-color: #27AE60;\n"
"}\n"
"\n"
"/* ===== AC OFF ===== */\n"
"QLabel#statussocket4[state=\"off\"] {\n"
"    background-color: #EB5757;   /* merah pastel tegas */\n"
"    border-color: #C0392B;\n"
"}\n"
"")
        self.statussocket4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_104.addWidget(self.statussocket4)

        self.frame_109 = QFrame(self.framestatussocket4)
        self.frame_109.setObjectName(u"frame_109")
        self.frame_109.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_109.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_104.addWidget(self.frame_109)


        self.verticalLayout_81.addWidget(self.framestatussocket4)

        self.framesensor4value = QFrame(self.framesocket4)
        self.framesensor4value.setObjectName(u"framesensor4value")
        self.framesensor4value.setStyleSheet(u"QFrame#framesensor4value {\n"
"	background-color: #F0F7FC;   /* biru sangat pucat */\n"
"	border: 1px solid #E1EEF9;\n"
"	border-radius: 10px;\n"
"}\n"
"\n"
"QFrame#framesensor4value QLabel {\n"
"    font: bold 10pt \"Segoe UI\";\n"
"    color: #1565C0;\n"
"}")
        self.framesensor4value.setFrameShape(QFrame.Shape.StyledPanel)
        self.framesensor4value.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_sensor4 = QVBoxLayout(self.framesensor4value)
        self.verticalLayout_sensor4.setSpacing(4)
        self.verticalLayout_sensor4.setObjectName(u"verticalLayout_sensor4")
        self.verticalLayout_sensor4.setContentsMargins(10, 8, 10, 8)
        self.label_energy_monitoring_title_4 = QLabel(self.framesensor4value)
        self.label_energy_monitoring_title_4.setObjectName(u"label_energy_monitoring_title_4")
        self.label_energy_monitoring_title_4.setMaximumSize(QSize(16777215, 30))
        self.label_energy_monitoring_title_4.setFont(font2)
        self.label_energy_monitoring_title_4.setStyleSheet(u"#label_energy_monitoring_title_4 {\n"
"    font: bold 10pt \"Segoe UI\";\n"
"    color: white;\n"
"   background-color: #64B5F6;   /* biru medium */\n"
"    border-radius: 8px;\n"
"    padding: 6px 10px;\n"
"    border: 1px solid #42A5F5;       /* border biru */\n"
"    min-height: 9px;\n"
"    qproperty-alignment: AlignCenter;\n"
"}")
        self.label_energy_monitoring_title_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_sensor4.addWidget(self.label_energy_monitoring_title_4)

        self.verticalLayout_sensor_values_4 = QVBoxLayout()
        self.verticalLayout_sensor_values_4.setSpacing(2)
        self.verticalLayout_sensor_values_4.setObjectName(u"verticalLayout_sensor_values_4")
        self.label_voltage4 = QLabel(self.framesensor4value)
        self.label_voltage4.setObjectName(u"label_voltage4")
        self.label_voltage4.setFont(font2)
        self.label_voltage4.setStyleSheet(u"")

        self.verticalLayout_sensor_values_4.addWidget(self.label_voltage4)

        self.label_current4 = QLabel(self.framesensor4value)
        self.label_current4.setObjectName(u"label_current4")
        self.label_current4.setFont(font2)
        self.label_current4.setStyleSheet(u"")
        self.label_current4.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout_sensor_values_4.addWidget(self.label_current4)

        self.label_power4 = QLabel(self.framesensor4value)
        self.label_power4.setObjectName(u"label_power4")
        self.label_power4.setFont(font2)
        self.label_power4.setStyleSheet(u"")

        self.verticalLayout_sensor_values_4.addWidget(self.label_power4)

        self.label_energy4 = QLabel(self.framesensor4value)
        self.label_energy4.setObjectName(u"label_energy4")
        self.label_energy4.setFont(font2)
        self.label_energy4.setStyleSheet(u"")

        self.verticalLayout_sensor_values_4.addWidget(self.label_energy4)

        self.label_frequency4 = QLabel(self.framesensor4value)
        self.label_frequency4.setObjectName(u"label_frequency4")
        self.label_frequency4.setFont(font2)
        self.label_frequency4.setStyleSheet(u"")

        self.verticalLayout_sensor_values_4.addWidget(self.label_frequency4)

        self.label_powerfactor4 = QLabel(self.framesensor4value)
        self.label_powerfactor4.setObjectName(u"label_powerfactor4")
        self.label_powerfactor4.setFont(font2)
        self.label_powerfactor4.setStyleSheet(u"")

        self.verticalLayout_sensor_values_4.addWidget(self.label_powerfactor4)


        self.verticalLayout_sensor4.addLayout(self.verticalLayout_sensor_values_4)


        self.verticalLayout_81.addWidget(self.framesensor4value)

        self.frameswitch4 = QFrame(self.framesocket4)
        self.frameswitch4.setObjectName(u"frameswitch4")
        self.frameswitch4.setStyleSheet(u"#frameswitch4{\n"
"	background-color: #F0F7FC;   /* biru sangat pucat */\n"
"	border: 1px solid #E1EEF9;\n"
"	border-radius: 10px;\n"
"}")
        self.frameswitch4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frameswitch4.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_82 = QVBoxLayout(self.frameswitch4)
        self.verticalLayout_82.setSpacing(6)
        self.verticalLayout_82.setObjectName(u"verticalLayout_82")
        self.verticalLayout_82.setContentsMargins(8, 8, 8, 8)
        self.frame_110 = QFrame(self.frameswitch4)
        self.frame_110.setObjectName(u"frame_110")
        self.frame_110.setMinimumSize(QSize(0, 20))
        self.frame_110.setMaximumSize(QSize(16777215, 30))
        self.frame_110.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_110.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_105 = QHBoxLayout(self.frame_110)
        self.horizontalLayout_105.setSpacing(0)
        self.horizontalLayout_105.setObjectName(u"horizontalLayout_105")
        self.horizontalLayout_105.setContentsMargins(0, 0, 0, 0)
        self.frame_111 = QFrame(self.frame_110)
        self.frame_111.setObjectName(u"frame_111")
        self.frame_111.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_111.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_105.addWidget(self.frame_111)

        self.label_switch_status_title_4 = QLabel(self.frame_110)
        self.label_switch_status_title_4.setObjectName(u"label_switch_status_title_4")
        self.label_switch_status_title_4.setFont(font2)
        self.label_switch_status_title_4.setStyleSheet(u"QLabel#label_switch_status_title_4{\n"
"	font: bold 10pt \"Segoe UI\";\n"
"	color: white;\n"
"	background-color: #64B5F6;    /* biru medium */\n"
"	border: 1px solid #42A5F5;\n"
"\n"
"\n"
"    border-radius: 6px;\n"
"    padding: 6px 12px;\n"
"    min-height: 10px;\n"
"    line-height: 5px;\n"
"    qproperty-alignment: AlignCenter;\n"
"}\n"
"\n"
"")

        self.horizontalLayout_105.addWidget(self.label_switch_status_title_4)

        self.frame_112 = QFrame(self.frame_110)
        self.frame_112.setObjectName(u"frame_112")
        self.frame_112.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_112.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_105.addWidget(self.frame_112)


        self.verticalLayout_82.addWidget(self.frame_110)

        self.frame_113 = QFrame(self.frameswitch4)
        self.frame_113.setObjectName(u"frame_113")
        self.frame_113.setMinimumSize(QSize(0, 0))
        self.frame_113.setMaximumSize(QSize(16777215, 30))
        self.frame_113.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_113.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_106 = QHBoxLayout(self.frame_113)
        self.horizontalLayout_106.setSpacing(0)
        self.horizontalLayout_106.setObjectName(u"horizontalLayout_106")
        self.horizontalLayout_106.setContentsMargins(0, 0, 0, 0)
        self.frame_114 = QFrame(self.frame_113)
        self.frame_114.setObjectName(u"frame_114")
        self.frame_114.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_114.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_106.addWidget(self.frame_114)

        self.label_switch_status_value4 = QLabel(self.frame_113)
        self.label_switch_status_value4.setObjectName(u"label_switch_status_value4")
        self.label_switch_status_value4.setMinimumSize(QSize(0, 30))
        self.label_switch_status_value4.setMaximumSize(QSize(100, 30))
        self.label_switch_status_value4.setFont(font11)
        self.label_switch_status_value4.setStyleSheet(u"QLabel#label_switch_status_value4{\n"
"    color: white;\n"
"    background-color: #EB5757;\n"
"    border: 1px solid #C0392B;\n"
"    border-radius: 4px;\n"
"    padding: 4px 8px;\n"
"    qproperty-alignment: AlignCenter;\n"
"font: bold 9pt \"Segoe UI\";\n"
"}\n"
"QLabel#label_switch_status_value4[state=\"on\"] {\n"
"    background-color: #6FCF97;\n"
"    border-color: #27AE60;\n"
"}")
        self.label_switch_status_value4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_106.addWidget(self.label_switch_status_value4)

        self.frame_115 = QFrame(self.frame_113)
        self.frame_115.setObjectName(u"frame_115")
        self.frame_115.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_115.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_106.addWidget(self.frame_115)


        self.verticalLayout_82.addWidget(self.frame_113)

        self.frame_switch_button_container_4 = QFrame(self.frameswitch4)
        self.frame_switch_button_container_4.setObjectName(u"frame_switch_button_container_4")
        self.frame_switch_button_container_4.setMinimumSize(QSize(0, 35))
        self.frame_switch_button_container_4.setFrameShape(QFrame.Shape.NoFrame)

        self.verticalLayout_82.addWidget(self.frame_switch_button_container_4)


        self.verticalLayout_81.addWidget(self.frameswitch4)

        self.framestatustimer4 = QFrame(self.framesocket4)
        self.framestatustimer4.setObjectName(u"framestatustimer4")
        self.framestatustimer4.setMinimumSize(QSize(0, 24))
        self.framestatustimer4.setMaximumSize(QSize(16777215, 24))
        self.framestatustimer4.setStyleSheet(u"")
        self.framestatustimer4.setFrameShape(QFrame.Shape.NoFrame)
        self.framestatustimer4.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_timer4 = QHBoxLayout(self.framestatustimer4)
        self.horizontalLayout_timer4.setObjectName(u"horizontalLayout_timer4")
        self.horizontalLayout_timer4.setContentsMargins(0, 0, 0, 0)
        self.label_timer_title_4 = QLabel(self.framestatustimer4)
        self.label_timer_title_4.setObjectName(u"label_timer_title_4")
        self.label_timer_title_4.setFont(font2)
        self.label_timer_title_4.setStyleSheet(u"    font: bold 10pt \"Segoe UI\";\n"
"    color: #1565C0;\n"
"")

        self.horizontalLayout_timer4.addWidget(self.label_timer_title_4)

        self.label_timer_status4 = QLabel(self.framestatustimer4)
        self.label_timer_status4.setObjectName(u"label_timer_status4")
        self.label_timer_status4.setFont(font2)
        self.label_timer_status4.setStyleSheet(u"    font: bold 10pt \"Segoe UI\";\n"
"    color: #1565C0;\n"
"")

        self.horizontalLayout_timer4.addWidget(self.label_timer_status4)


        self.verticalLayout_81.addWidget(self.framestatustimer4)

        self.framestatusscheduling4 = QFrame(self.framesocket4)
        self.framestatusscheduling4.setObjectName(u"framestatusscheduling4")
        self.framestatusscheduling4.setMinimumSize(QSize(0, 24))
        self.framestatusscheduling4.setMaximumSize(QSize(16777215, 24))
        self.framestatusscheduling4.setFrameShape(QFrame.Shape.NoFrame)
        self.framestatusscheduling4.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_scheduling4 = QHBoxLayout(self.framestatusscheduling4)
        self.horizontalLayout_scheduling4.setObjectName(u"horizontalLayout_scheduling4")
        self.horizontalLayout_scheduling4.setContentsMargins(0, 0, 0, 0)
        self.label_scheduling_title_4 = QLabel(self.framestatusscheduling4)
        self.label_scheduling_title_4.setObjectName(u"label_scheduling_title_4")
        self.label_scheduling_title_4.setFont(font2)
        self.label_scheduling_title_4.setStyleSheet(u"    font: bold 10pt \"Segoe UI\";\n"
"    color: #1565C0;\n"
"")

        self.horizontalLayout_scheduling4.addWidget(self.label_scheduling_title_4)

        self.label_scheduling_status4 = QLabel(self.framestatusscheduling4)
        self.label_scheduling_status4.setObjectName(u"label_scheduling_status4")
        self.label_scheduling_status4.setFont(font2)
        self.label_scheduling_status4.setStyleSheet(u"    font: bold 10pt \"Segoe UI\";\n"
"    color: #1565C0;\n"
"")

        self.horizontalLayout_scheduling4.addWidget(self.label_scheduling_status4)


        self.verticalLayout_81.addWidget(self.framestatusscheduling4)

        self.framebuttonaction4 = QFrame(self.framesocket4)
        self.framebuttonaction4.setObjectName(u"framebuttonaction4")
        self.framebuttonaction4.setMinimumSize(QSize(0, 35))
        self.framebuttonaction4.setMaximumSize(QSize(16777215, 35))
        self.framebuttonaction4.setFrameShape(QFrame.Shape.NoFrame)
        self.framebuttonaction4.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_action4 = QHBoxLayout(self.framebuttonaction4)
        self.horizontalLayout_action4.setObjectName(u"horizontalLayout_action4")
        self.horizontalLayout_action4.setContentsMargins(0, 0, 0, 0)
        self.btn_action_socket4 = QPushButton(self.framebuttonaction4)
        self.btn_action_socket4.setObjectName(u"btn_action_socket4")
        self.btn_action_socket4.setMinimumSize(QSize(0, 35))
        self.btn_action_socket4.setFont(font2)
        self.btn_action_socket4.setStyleSheet(u"QPushButton#btn_action_socket4 {\n"
"    background-color: #42A5F5;      /* biru medium */\n"
"    color: white;\n"
"    font: bold 10pt \"Segoe UI\";     /* teks bold */\n"
"    border: none;\n"
"    border-radius: 6px;\n"
"    padding: 6px 12px;\n"
"}\n"
"\n"
"/* Hover: sedikit lebih terang */\n"
"QPushButton#btn_action_socket4:hover {\n"
"    background-color: #64B5F6;      /* biru terang */\n"
"}\n"
"\n"
"/* Pressed: sedikit lebih gelap */\n"
"QPushButton#btn_action_socket4:pressed {\n"
"    background-color: #1976D2;      /* biru gelap */\n"
"}")

        self.horizontalLayout_action4.addWidget(self.btn_action_socket4)


        self.verticalLayout_81.addWidget(self.framebuttonaction4)


        self.horizontalLayout_111.addWidget(self.framesocket4)

        self.framesocket5 = QFrame(self.framecontentSmartsocket)
        self.framesocket5.setObjectName(u"framesocket5")
        self.framesocket5.setMinimumSize(QSize(0, 700))
        self.framesocket5.setMaximumSize(QSize(16777215, 700))
        self.framesocket5.setStyleSheet(u"#framesocket5{\n"
"	background-color: #eee3fa;   /* ungu lembut banget */\n"
"	border: 2px solid #E3DAF1;\n"
"	border-radius: 10px;\n"
"}")
        self.framesocket5.setFrameShape(QFrame.Shape.NoFrame)
        self.framesocket5.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_83 = QVBoxLayout(self.framesocket5)
        self.verticalLayout_83.setObjectName(u"verticalLayout_83")
        self.frametitlesocket5 = QFrame(self.framesocket5)
        self.frametitlesocket5.setObjectName(u"frametitlesocket5")
        self.frametitlesocket5.setMinimumSize(QSize(0, 0))
        self.frametitlesocket5.setMaximumSize(QSize(16777215, 50))
        self.frametitlesocket5.setFrameShape(QFrame.Shape.NoFrame)
        self.frametitlesocket5.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_107 = QHBoxLayout(self.frametitlesocket5)
        self.horizontalLayout_107.setSpacing(0)
        self.horizontalLayout_107.setObjectName(u"horizontalLayout_107")
        self.horizontalLayout_107.setContentsMargins(0, 0, 0, 0)
        self.frame_116 = QFrame(self.frametitlesocket5)
        self.frame_116.setObjectName(u"frame_116")
        self.frame_116.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_116.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_107.addWidget(self.frame_116)

        self.titlesmart5 = QLabel(self.frametitlesocket5)
        self.titlesmart5.setObjectName(u"titlesmart5")
        sizePolicy2.setHeightForWidth(self.titlesmart5.sizePolicy().hasHeightForWidth())
        self.titlesmart5.setSizePolicy(sizePolicy2)
        self.titlesmart5.setMinimumSize(QSize(96, 40))
        self.titlesmart5.setMaximumSize(QSize(136, 45))
        self.titlesmart5.setFont(font4)
        self.titlesmart5.setStyleSheet(u"#titlesmart5{\n"
"font: bold 12pt \"Segoe UI\";\n"
"color: white;\n"
"background-color: #8E7AB5;   /* ungu battery */\n"
"    border: 1px solid #6E8E8B;\n"
"\n"
"\n"
"    border-radius: 8px;\n"
"    padding: 6px 12px;\n"
"    min-height: 26px;\n"
"    line-height: 18px;\n"
"\n"
"    min-width: 70px;\n"
"    max-width: 110px;\n"
"    qproperty-alignment: AlignCenter;\n"
"}\n"
"\n"
"")
        self.titlesmart5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_107.addWidget(self.titlesmart5)

        self.frame_117 = QFrame(self.frametitlesocket5)
        self.frame_117.setObjectName(u"frame_117")
        self.frame_117.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_117.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_107.addWidget(self.frame_117)


        self.verticalLayout_83.addWidget(self.frametitlesocket5)

        self.framestatussocket5 = QFrame(self.framesocket5)
        self.framestatussocket5.setObjectName(u"framestatussocket5")
        self.framestatussocket5.setMinimumSize(QSize(0, 40))
        self.framestatussocket5.setMaximumSize(QSize(16777215, 23))
        self.framestatussocket5.setFrameShape(QFrame.Shape.NoFrame)
        self.framestatussocket5.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_108 = QHBoxLayout(self.framestatussocket5)
        self.horizontalLayout_108.setSpacing(0)
        self.horizontalLayout_108.setObjectName(u"horizontalLayout_108")
        self.horizontalLayout_108.setContentsMargins(0, 0, 0, 0)
        self.frame_118 = QFrame(self.framestatussocket5)
        self.frame_118.setObjectName(u"frame_118")
        self.frame_118.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_118.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_108.addWidget(self.frame_118)

        self.statussocket5 = QLabel(self.framestatussocket5)
        self.statussocket5.setObjectName(u"statussocket5")
        sizePolicy2.setHeightForWidth(self.statussocket5.sizePolicy().hasHeightForWidth())
        self.statussocket5.setSizePolicy(sizePolicy2)
        self.statussocket5.setMinimumSize(QSize(155, 23))
        self.statussocket5.setMaximumSize(QSize(114, 23))
        self.statussocket5.setFont(font2)
        self.statussocket5.setStyleSheet(u"QLabel#statussocket5{\n"
"    font: bold 10pt \"Segoe UI\";\n"
"    color: white;\n"
"\n"
"    background-color: #CBD5E1;   /* default (abu netral) */\n"
"    border: 1px solid #94A3B8;\n"
"    border-radius: 4px;\n"
"\n"
"    padding: 2px 6px;\n"
"    min-height: 17px;\n"
"    max-width: 100px;\n"
"\n"
"    qproperty-alignment: AlignCenter;\n"
"}\n"
"\n"
"/* ===== AC ON ===== */\n"
"QLabel#statussocket5[state=\"on\"] {\n"
"    background-color: #6FCF97;   /* hijau pastel tapi jelas */\n"
"    border-color: #27AE60;\n"
"}\n"
"\n"
"/* ===== AC OFF ===== */\n"
"QLabel#statussocket5[state=\"off\"] {\n"
"    background-color: #EB5757;   /* merah pastel tegas */\n"
"    border-color: #C0392B;\n"
"}\n"
"")
        self.statussocket5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_108.addWidget(self.statussocket5)

        self.frame_119 = QFrame(self.framestatussocket5)
        self.frame_119.setObjectName(u"frame_119")
        self.frame_119.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_119.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_108.addWidget(self.frame_119)


        self.verticalLayout_83.addWidget(self.framestatussocket5)

        self.framesensor5value = QFrame(self.framesocket5)
        self.framesensor5value.setObjectName(u"framesensor5value")
        self.framesensor5value.setStyleSheet(u"QFrame#framesensor5value {\n"
"	background-color: #F2ECF9;   /* ungu lembut banget */\n"
"	border: 1px solid #E3DAF1;\n"
"	border-radius: 10px;\n"
"}\n"
"\n"
"QFrame#framesensor5value QLabel {\n"
"    font: bold 10pt \"Segoe UI\";\n"
"    color: #380082;\n"
"}")
        self.framesensor5value.setFrameShape(QFrame.Shape.StyledPanel)
        self.framesensor5value.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_sensor5 = QVBoxLayout(self.framesensor5value)
        self.verticalLayout_sensor5.setSpacing(4)
        self.verticalLayout_sensor5.setObjectName(u"verticalLayout_sensor5")
        self.verticalLayout_sensor5.setContentsMargins(10, 8, 10, 8)
        self.label_energy_monitoring_title_5 = QLabel(self.framesensor5value)
        self.label_energy_monitoring_title_5.setObjectName(u"label_energy_monitoring_title_5")
        self.label_energy_monitoring_title_5.setMaximumSize(QSize(16777215, 30))
        self.label_energy_monitoring_title_5.setFont(font2)
        self.label_energy_monitoring_title_5.setStyleSheet(u"#label_energy_monitoring_title_5{\n"
"    font: bold 10pt \"Segoe UI\";\n"
"    color: white;\n"
"    background-color: #bd95f0;        /* ungu soft */\n"
"    border-radius: 8px;\n"
"    padding: 6px 10px;\n"
"    border: 1px solid #9B7BCB;       /* border ungu gelap tapi harmonis */\n"
"    min-height: 9px;\n"
"    qproperty-alignment: AlignCenter;\n"
"}")
        self.label_energy_monitoring_title_5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_sensor5.addWidget(self.label_energy_monitoring_title_5)

        self.verticalLayout_sensor_values_5 = QVBoxLayout()
        self.verticalLayout_sensor_values_5.setSpacing(2)
        self.verticalLayout_sensor_values_5.setObjectName(u"verticalLayout_sensor_values_5")
        self.label_voltage5 = QLabel(self.framesensor5value)
        self.label_voltage5.setObjectName(u"label_voltage5")
        self.label_voltage5.setFont(font2)
        self.label_voltage5.setStyleSheet(u"")

        self.verticalLayout_sensor_values_5.addWidget(self.label_voltage5)

        self.label_current5 = QLabel(self.framesensor5value)
        self.label_current5.setObjectName(u"label_current5")
        self.label_current5.setFont(font2)
        self.label_current5.setStyleSheet(u"")
        self.label_current5.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout_sensor_values_5.addWidget(self.label_current5)

        self.label_power5 = QLabel(self.framesensor5value)
        self.label_power5.setObjectName(u"label_power5")
        self.label_power5.setFont(font2)
        self.label_power5.setStyleSheet(u"")

        self.verticalLayout_sensor_values_5.addWidget(self.label_power5)

        self.label_energy5 = QLabel(self.framesensor5value)
        self.label_energy5.setObjectName(u"label_energy5")
        self.label_energy5.setFont(font2)
        self.label_energy5.setStyleSheet(u"")

        self.verticalLayout_sensor_values_5.addWidget(self.label_energy5)

        self.label_frequency5 = QLabel(self.framesensor5value)
        self.label_frequency5.setObjectName(u"label_frequency5")
        self.label_frequency5.setFont(font2)
        self.label_frequency5.setStyleSheet(u"")

        self.verticalLayout_sensor_values_5.addWidget(self.label_frequency5)

        self.label_powerfactor5 = QLabel(self.framesensor5value)
        self.label_powerfactor5.setObjectName(u"label_powerfactor5")
        self.label_powerfactor5.setFont(font2)
        self.label_powerfactor5.setStyleSheet(u"")

        self.verticalLayout_sensor_values_5.addWidget(self.label_powerfactor5)


        self.verticalLayout_sensor5.addLayout(self.verticalLayout_sensor_values_5)


        self.verticalLayout_83.addWidget(self.framesensor5value)

        self.frameswitch5 = QFrame(self.framesocket5)
        self.frameswitch5.setObjectName(u"frameswitch5")
        self.frameswitch5.setStyleSheet(u"#frameswitch5{\n"
"	background-color: #F2ECF9;   /* ungu lembut banget */\n"
"	border: 1px solid #E3DAF1;\n"
"	border-radius: 10px;\n"
"}")
        self.frameswitch5.setFrameShape(QFrame.Shape.StyledPanel)
        self.frameswitch5.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_84 = QVBoxLayout(self.frameswitch5)
        self.verticalLayout_84.setSpacing(6)
        self.verticalLayout_84.setObjectName(u"verticalLayout_84")
        self.verticalLayout_84.setContentsMargins(8, 8, 8, 8)
        self.frame_120 = QFrame(self.frameswitch5)
        self.frame_120.setObjectName(u"frame_120")
        self.frame_120.setMinimumSize(QSize(0, 20))
        self.frame_120.setMaximumSize(QSize(16777215, 30))
        self.frame_120.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_120.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_109 = QHBoxLayout(self.frame_120)
        self.horizontalLayout_109.setSpacing(0)
        self.horizontalLayout_109.setObjectName(u"horizontalLayout_109")
        self.horizontalLayout_109.setContentsMargins(0, 0, 0, 0)
        self.frame_121 = QFrame(self.frame_120)
        self.frame_121.setObjectName(u"frame_121")
        self.frame_121.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_121.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_109.addWidget(self.frame_121)

        self.label_switch_status_title_5 = QLabel(self.frame_120)
        self.label_switch_status_title_5.setObjectName(u"label_switch_status_title_5")
        self.label_switch_status_title_5.setFont(font2)
        self.label_switch_status_title_5.setStyleSheet(u"QLabel#label_switch_status_title_5{\n"
"	font: bold 10pt \"Segoe UI\";\n"
"	color: white;\n"
"	background-color: #bd95f0;    /* ungu battery */\n"
"	border: 1px solid #9B7BCB; \n"
"\n"
"\n"
"    border-radius: 6px;\n"
"    padding: 6px 12px;\n"
"    min-height: 10px;\n"
"    line-height: 5px;\n"
"    qproperty-alignment: AlignCenter;\n"
"}\n"
"\n"
"")

        self.horizontalLayout_109.addWidget(self.label_switch_status_title_5)

        self.frame_122 = QFrame(self.frame_120)
        self.frame_122.setObjectName(u"frame_122")
        self.frame_122.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_122.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_109.addWidget(self.frame_122)


        self.verticalLayout_84.addWidget(self.frame_120)

        self.frame_123 = QFrame(self.frameswitch5)
        self.frame_123.setObjectName(u"frame_123")
        self.frame_123.setMinimumSize(QSize(0, 0))
        self.frame_123.setMaximumSize(QSize(16777215, 30))
        self.frame_123.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_123.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_110 = QHBoxLayout(self.frame_123)
        self.horizontalLayout_110.setSpacing(0)
        self.horizontalLayout_110.setObjectName(u"horizontalLayout_110")
        self.horizontalLayout_110.setContentsMargins(0, 0, 0, 0)
        self.frame_124 = QFrame(self.frame_123)
        self.frame_124.setObjectName(u"frame_124")
        self.frame_124.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_124.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_110.addWidget(self.frame_124)

        self.label_switch_status_value5 = QLabel(self.frame_123)
        self.label_switch_status_value5.setObjectName(u"label_switch_status_value5")
        self.label_switch_status_value5.setMinimumSize(QSize(0, 30))
        self.label_switch_status_value5.setMaximumSize(QSize(100, 30))
        self.label_switch_status_value5.setFont(font11)
        self.label_switch_status_value5.setStyleSheet(u"QLabel#label_switch_status_value5{\n"
"    color: white;\n"
"    background-color: #EB5757;\n"
"    border: 1px solid #C0392B;\n"
"    border-radius: 4px;\n"
"    padding: 4px 8px;\n"
"    qproperty-alignment: AlignCenter;\n"
"font: bold 9pt \"Segoe UI\";\n"
"}\n"
"QLabel#label_switch_status_value5[state=\"on\"] {\n"
"    background-color: #6FCF97;\n"
"    border-color: #27AE60;\n"
"}")
        self.label_switch_status_value5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_110.addWidget(self.label_switch_status_value5)

        self.frame_125 = QFrame(self.frame_123)
        self.frame_125.setObjectName(u"frame_125")
        self.frame_125.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_125.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_110.addWidget(self.frame_125)


        self.verticalLayout_84.addWidget(self.frame_123)

        self.frame_switch_button_container_5 = QFrame(self.frameswitch5)
        self.frame_switch_button_container_5.setObjectName(u"frame_switch_button_container_5")
        self.frame_switch_button_container_5.setMinimumSize(QSize(0, 35))
        self.frame_switch_button_container_5.setFrameShape(QFrame.Shape.NoFrame)

        self.verticalLayout_84.addWidget(self.frame_switch_button_container_5)


        self.verticalLayout_83.addWidget(self.frameswitch5)

        self.framestatustimer5 = QFrame(self.framesocket5)
        self.framestatustimer5.setObjectName(u"framestatustimer5")
        self.framestatustimer5.setMinimumSize(QSize(0, 24))
        self.framestatustimer5.setMaximumSize(QSize(16777215, 24))
        self.framestatustimer5.setStyleSheet(u"")
        self.framestatustimer5.setFrameShape(QFrame.Shape.NoFrame)
        self.framestatustimer5.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_timer5 = QHBoxLayout(self.framestatustimer5)
        self.horizontalLayout_timer5.setObjectName(u"horizontalLayout_timer5")
        self.horizontalLayout_timer5.setContentsMargins(0, 0, 0, 0)
        self.label_timer_title_5 = QLabel(self.framestatustimer5)
        self.label_timer_title_5.setObjectName(u"label_timer_title_5")
        self.label_timer_title_5.setFont(font2)
        self.label_timer_title_5.setStyleSheet(u"    font: bold 10pt \"Segoe UI\";\n"
"    color: #380082;\n"
"")

        self.horizontalLayout_timer5.addWidget(self.label_timer_title_5)

        self.label_timer_status5 = QLabel(self.framestatustimer5)
        self.label_timer_status5.setObjectName(u"label_timer_status5")
        self.label_timer_status5.setFont(font2)
        self.label_timer_status5.setStyleSheet(u"    font: bold 10pt \"Segoe UI\";\n"
"    color: #380082;\n"
"")

        self.horizontalLayout_timer5.addWidget(self.label_timer_status5)


        self.verticalLayout_83.addWidget(self.framestatustimer5)

        self.framestatusscheduling5 = QFrame(self.framesocket5)
        self.framestatusscheduling5.setObjectName(u"framestatusscheduling5")
        self.framestatusscheduling5.setMinimumSize(QSize(0, 24))
        self.framestatusscheduling5.setMaximumSize(QSize(16777215, 24))
        self.framestatusscheduling5.setFrameShape(QFrame.Shape.NoFrame)
        self.framestatusscheduling5.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_scheduling5 = QHBoxLayout(self.framestatusscheduling5)
        self.horizontalLayout_scheduling5.setObjectName(u"horizontalLayout_scheduling5")
        self.horizontalLayout_scheduling5.setContentsMargins(0, 0, 0, 0)
        self.label_scheduling_title_5 = QLabel(self.framestatusscheduling5)
        self.label_scheduling_title_5.setObjectName(u"label_scheduling_title_5")
        self.label_scheduling_title_5.setFont(font2)
        self.label_scheduling_title_5.setStyleSheet(u"    font: bold 10pt \"Segoe UI\";\n"
"    color: #380082;\n"
"")

        self.horizontalLayout_scheduling5.addWidget(self.label_scheduling_title_5)

        self.label_scheduling_status5 = QLabel(self.framestatusscheduling5)
        self.label_scheduling_status5.setObjectName(u"label_scheduling_status5")
        self.label_scheduling_status5.setFont(font2)
        self.label_scheduling_status5.setStyleSheet(u"    font: bold 10pt \"Segoe UI\";\n"
"    color: #380082;\n"
"")

        self.horizontalLayout_scheduling5.addWidget(self.label_scheduling_status5)


        self.verticalLayout_83.addWidget(self.framestatusscheduling5)

        self.framebuttonaction5 = QFrame(self.framesocket5)
        self.framebuttonaction5.setObjectName(u"framebuttonaction5")
        self.framebuttonaction5.setMinimumSize(QSize(0, 35))
        self.framebuttonaction5.setMaximumSize(QSize(16777215, 35))
        self.framebuttonaction5.setFrameShape(QFrame.Shape.NoFrame)
        self.framebuttonaction5.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_action5 = QHBoxLayout(self.framebuttonaction5)
        self.horizontalLayout_action5.setObjectName(u"horizontalLayout_action5")
        self.horizontalLayout_action5.setContentsMargins(0, 0, 0, 0)
        self.btn_action_socket5 = QPushButton(self.framebuttonaction5)
        self.btn_action_socket5.setObjectName(u"btn_action_socket5")
        self.btn_action_socket5.setMinimumSize(QSize(0, 35))
        self.btn_action_socket5.setFont(font2)
        self.btn_action_socket5.setStyleSheet(u"QPushButton#btn_action_socket5 {\n"
"    background-color: #ab6dfc;      /* warna utama */\n"
"    color: white;\n"
"    font: bold 10pt \"Segoe UI\";     /* teks bold */\n"
"    border: none;\n"
"    border-radius: 6px;\n"
"    padding: 6px 12px;\n"
"}\n"
"\n"
"/* Hover: sedikit lebih terang */\n"
"QPushButton#btn_action_socket5:hover {\n"
"    background-color: #c085fc;      /* ungu terang lebih soft */\n"
"}\n"
"\n"
"/* Pressed: sedikit lebih gelap */\n"
"QPushButton#btn_action_socket5:pressed {\n"
"    background-color: #914de6;      /* ungu gelap */\n"
"}")

        self.horizontalLayout_action5.addWidget(self.btn_action_socket5)


        self.verticalLayout_83.addWidget(self.framebuttonaction5)


        self.horizontalLayout_111.addWidget(self.framesocket5)


        self.verticalLayout_77.addWidget(self.framecontentSmartsocket)

        self.stackedWidget.addWidget(self.page4_smartsocket)
        self.page5_settings = QWidget()
        self.page5_settings.setObjectName(u"page5_settings")
        self.verticalLayout_21 = QVBoxLayout(self.page5_settings)
        self.verticalLayout_21.setSpacing(6)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.verticalLayout_21.setContentsMargins(9, 9, 9, 9)
        self.framesettings = QFrame(self.page5_settings)
        self.framesettings.setObjectName(u"framesettings")
        self.framesettings.setMaximumSize(QSize(16777215, 65))
        self.framesettings.setFrameShape(QFrame.Shape.NoFrame)
        self.framesettings.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_79 = QHBoxLayout(self.framesettings)
        self.horizontalLayout_79.setObjectName(u"horizontalLayout_79")
        self.titleSettings = QLabel(self.framesettings)
        self.titleSettings.setObjectName(u"titleSettings")
        sizePolicy2.setHeightForWidth(self.titleSettings.sizePolicy().hasHeightForWidth())
        self.titleSettings.setSizePolicy(sizePolicy2)
        self.titleSettings.setMaximumSize(QSize(422, 45))
        self.titleSettings.setFont(font6)
        self.titleSettings.setStyleSheet(u"#titleSettings {\n"
"    font: bold 14pt \"Segoe UI\";\n"
"    color: white;\n"
"    background-color: #5775dc;\n"
"    border-radius: 8px;\n"
"    padding: 6px 10px;\n"
"    border: 1px solid #5775dc;\n"
"    \n"
"    /* Tambahan pengaturan ukuran */\n"
"    min-width: 500px;    /* lebar minimum */\n"
"    max-width: 400px;    /* lebar maksimum */\n"
"    qproperty-alignment: AlignCenter; /* biar teks di tengah */\n"
"}\n"
"")
        self.titleSettings.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_79.addWidget(self.titleSettings)


        self.verticalLayout_21.addWidget(self.framesettings)

        self.framecontentsettings = QFrame(self.page5_settings)
        self.framecontentsettings.setObjectName(u"framecontentsettings")
        self.framecontentsettings.setFrameShape(QFrame.Shape.NoFrame)
        self.framecontentsettings.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_78 = QHBoxLayout(self.framecontentsettings)
        self.horizontalLayout_78.setObjectName(u"horizontalLayout_78")
        self.settingsandlogFrame = QFrame(self.framecontentsettings)
        self.settingsandlogFrame.setObjectName(u"settingsandlogFrame")
        self.settingsandlogFrame.setStyleSheet(u"")
        self.settingsandlogFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.settingsandlogFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_23 = QVBoxLayout(self.settingsandlogFrame)
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.settingsFrame = QFrame(self.settingsandlogFrame)
        self.settingsFrame.setObjectName(u"settingsFrame")
        self.settingsFrame.setMinimumSize(QSize(0, 421))
        self.settingsFrame.setMaximumSize(QSize(16777215, 421))
        self.settingsFrame.setStyleSheet(u"#settingsFrame {\n"
"    background-color: #EEF4FB;   /* biru abu lembut */\n"
"    border: 2px solid #D6E2F1;\n"
"    border-radius: 10px;\n"
"}\n"
"")
        self.settingsFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.settingsFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_28 = QVBoxLayout(self.settingsFrame)
        self.verticalLayout_28.setObjectName(u"verticalLayout_28")
        self.verticalLayout_28.setContentsMargins(10, 10, 10, 10)
        self.frame_57 = QFrame(self.settingsFrame)
        self.frame_57.setObjectName(u"frame_57")
        self.frame_57.setMaximumSize(QSize(16777215, 100))
        self.frame_57.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_57.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_80 = QHBoxLayout(self.frame_57)
        self.horizontalLayout_80.setObjectName(u"horizontalLayout_80")
        self.frame_58 = QFrame(self.frame_57)
        self.frame_58.setObjectName(u"frame_58")
        self.frame_58.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_58.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_80.addWidget(self.frame_58)

        self.titleProfile = QLabel(self.frame_57)
        self.titleProfile.setObjectName(u"titleProfile")
        sizePolicy2.setHeightForWidth(self.titleProfile.sizePolicy().hasHeightForWidth())
        self.titleProfile.setSizePolicy(sizePolicy2)
        self.titleProfile.setMaximumSize(QSize(172, 45))
        self.titleProfile.setFont(font4)
        self.titleProfile.setStyleSheet(u"#titleProfile{\n"
"font: bold 12pt \"Segoe UI\";\n"
"color: white;\n"
"background-color: #4A90D9;   /* biru energi */\n"
"border-radius: 8px;\n"
"padding: 6px 10px;\n"
"border: 1px solid #4A90D9;\n"
"\n"
"min-width: 100px;\n"
"max-width: 150px;\n"
"qproperty-alignment: AlignCenter;\n"
"}\n"
"")
        self.titleProfile.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_80.addWidget(self.titleProfile)

        self.frame_59 = QFrame(self.frame_57)
        self.frame_59.setObjectName(u"frame_59")
        self.frame_59.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_59.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_80.addWidget(self.frame_59)


        self.verticalLayout_28.addWidget(self.frame_57)

        self.frame_60 = QFrame(self.settingsFrame)
        self.frame_60.setObjectName(u"frame_60")
        self.frame_60.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_60.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_33 = QVBoxLayout(self.frame_60)
        self.verticalLayout_33.setSpacing(15)
        self.verticalLayout_33.setObjectName(u"verticalLayout_33")
        self.verticalLayout_33.setContentsMargins(20, 30, 20, 30)
        self.horizontalLayout_81 = QHBoxLayout()
        self.horizontalLayout_81.setObjectName(u"horizontalLayout_81")
        self.labelUsername = QLabel(self.frame_60)
        self.labelUsername.setObjectName(u"labelUsername")
        self.labelUsername.setMinimumSize(QSize(120, 40))
        self.labelUsername.setMaximumSize(QSize(16777215, 40))
        self.labelUsername.setFont(font4)
        self.labelUsername.setStyleSheet(u"QLabel#labelUsername {\n"
"    font: bold 12pt \"Segoe UI\";\n"
"background-color: #4DB6AC;  /* hijau pastel */\n"
"border: 1px solid #4DB6AC;\n"
"color: white;\n"
"    border-radius: 8px;\n"
"    padding: 6px 10px;\n"
"    border: 1px solid #33A1E0;\n"
"    	qproperty-alignment: AlignCenter;\n"
"}\n"
"\n"
"")

        self.horizontalLayout_81.addWidget(self.labelUsername)

        self.inputUsername = QLineEdit(self.frame_60)
        self.inputUsername.setObjectName(u"inputUsername")
        self.inputUsername.setEnabled(False)
        self.inputUsername.setMaximumSize(QSize(16777215, 50))
        self.inputUsername.setStyleSheet(u"QLineEdit#inputUsername {\n"
"    background-color: rgba(240, 243, 247, 0.9); /* soft background */\n"
"    color: rgb(40, 40, 40); /* teks gelap, jelas terbaca */\n"
"    font-size: 13pt; /* ukuran font */\n"
"    font-weight: 500; /* sedikit bold supaya lebih jelas */\n"
"    border: 2px solid rgb(210, 220, 230);\n"
"    border-radius: 8px;\n"
"    padding: 6px;\n"
"}")

        self.horizontalLayout_81.addWidget(self.inputUsername)


        self.verticalLayout_33.addLayout(self.horizontalLayout_81)

        self.horizontalLayout_82 = QHBoxLayout()
        self.horizontalLayout_82.setObjectName(u"horizontalLayout_82")
        self.labelEmail = QLabel(self.frame_60)
        self.labelEmail.setObjectName(u"labelEmail")
        self.labelEmail.setMinimumSize(QSize(120, 40))
        self.labelEmail.setMaximumSize(QSize(16777215, 40))
        self.labelEmail.setFont(font4)
        self.labelEmail.setStyleSheet(u"QLabel#labelEmail {\n"
"    font: bold 12pt \"Segoe UI\";\n"
"background-color: #4DB6AC;  /* hijau pastel */\n"
"border: 1px solid #4DB6AC;\n"
"color: white;\n"
"    border-radius: 8px;\n"
"    padding: 6px 10px;\n"
"    border: 1px solid #33A1E0;\n"
"    qproperty-alignment: AlignCenter;\n"
"}\n"
"")

        self.horizontalLayout_82.addWidget(self.labelEmail)

        self.inputEmail = QLineEdit(self.frame_60)
        self.inputEmail.setObjectName(u"inputEmail")
        self.inputEmail.setEnabled(False)
        self.inputEmail.setMaximumSize(QSize(16777215, 50))
        self.inputEmail.setStyleSheet(u"QLineEdit#inputEmail {\n"
"    background-color: rgba(240, 243, 247, 0.9); /* soft background */\n"
"    color: rgb(40, 40, 40); /* teks gelap, jelas terbaca */\n"
"    font-size: 13pt; /* ukuran font */\n"
"    font-weight: 500; /* sedikit bold supaya lebih jelas */\n"
"    border: 2px solid rgb(210, 220, 230);\n"
"    border-radius: 8px;\n"
"    padding: 6px;\n"
"}")

        self.horizontalLayout_82.addWidget(self.inputEmail)


        self.verticalLayout_33.addLayout(self.horizontalLayout_82)

        self.horizontalLayout_831 = QHBoxLayout()
        self.horizontalLayout_831.setObjectName(u"horizontalLayout_831")
        self.btnUpdatePassword = QPushButton(self.frame_60)
        self.btnUpdatePassword.setObjectName(u"btnUpdatePassword")
        self.btnUpdatePassword.setMinimumSize(QSize(150, 45))
        self.btnUpdatePassword.setMaximumSize(QSize(160, 45))
        self.btnUpdatePassword.setFont(font8)
        self.btnUpdatePassword.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btnUpdatePassword.setStyleSheet(u"QPushButton#btnUpdatePassword {\n"
"    background-color: #4A90D9;\n"
"    border: 2px solid #4A90D9;\n"
"    border-radius: 8px;\n"
"    color: white;\n"
"    font: bold 11pt \"Segoe UI\";\n"
"    padding: 6px 14px;\n"
"}\n"
"\n"
"QPushButton#btnUpdatePassword:hover {\n"
"    background-color: #5BA0E9;\n"
"}\n"
"\n"
"QPushButton#btnUpdatePassword:pressed {\n"
"    background-color: #3A7BC4;\n"
"}\n"
"\n"
"QPushButton#btnUpdatePassword:disabled {\n"
"    background-color: #B5D9F0;\n"
"    color: #F2FAF7;\n"
"    border: 2px solid #9BC9E8;\n"
"}")

        self.horizontalLayout_831.addWidget(self.btnUpdatePassword)

        self.btnAdminpanel = QPushButton(self.frame_60)
        self.btnAdminpanel.setObjectName(u"btnAdminpanel")
        self.btnAdminpanel.setMinimumSize(QSize(150, 45))
        self.btnAdminpanel.setMaximumSize(QSize(100, 45))
        self.btnAdminpanel.setFont(font8)
        self.btnAdminpanel.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btnAdminpanel.setStyleSheet(u"QPushButton#btnAdminpanel {\n"
"    background-color: #8E44AD;  /* ungu utama */\n"
"    border: 2px solid #8E44AD;\n"
"    border-radius: 8px;\n"
"    color: white;\n"
"    font: bold 11pt \"Segoe UI\";\n"
"    padding: 6px 14px;\n"
"}\n"
"\n"
"QPushButton#btnAdminpanel:hover {\n"
"    background-color: #9B59B6;  /* ungu lebih terang saat hover */\n"
"}\n"
"\n"
"QPushButton#btnAdminpanel:pressed {\n"
"    background-color: #6C3483;  /* ungu lebih gelap saat ditekan */\n"
"}\n"
"\n"
"QPushButton#btnAdminpanel:disabled {\n"
"    background-color: #D2B4DE;  /* ungu pastel saat disabled */\n"
"    color: #F2EAF8;\n"
"    border: 2px solid #B39DD9;\n"
"}")

        self.horizontalLayout_831.addWidget(self.btnAdminpanel)

        self.btnLogout = QPushButton(self.frame_60)
        self.btnLogout.setObjectName(u"btnLogout")
        self.btnLogout.setMinimumSize(QSize(100, 45))
        self.btnLogout.setMaximumSize(QSize(100, 45))
        self.btnLogout.setFont(font8)
        self.btnLogout.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btnLogout.setStyleSheet(u"QPushButton#btnLogout {\n"
"    background-color: #E74C3C;\n"
"    border: 2px solid #E74C3C;\n"
"    border-radius: 8px;\n"
"    color: white;\n"
"    font: bold 11pt \"Segoe UI\";\n"
"    padding: 6px 14px;\n"
"}\n"
"\n"
"QPushButton#btnLogout:hover {\n"
"    background-color: #F75C4C;\n"
"}\n"
"\n"
"QPushButton#btnLogout:pressed {\n"
"    background-color: #C0392B;\n"
"}\n"
"\n"
"QPushButton#btnLogout:disabled {\n"
"    background-color: #F5B7B1;\n"
"    color: #FDF2F2;\n"
"    border: 2px solid #F1948A;\n"
"}")

        self.horizontalLayout_831.addWidget(self.btnLogout)


        self.verticalLayout_33.addLayout(self.horizontalLayout_831)


        self.verticalLayout_28.addWidget(self.frame_60)


        self.verticalLayout_23.addWidget(self.settingsFrame)

        self.logFrame = QFrame(self.settingsandlogFrame)
        self.logFrame.setObjectName(u"logFrame")
        self.logFrame.setStyleSheet(u"#logFrame {\n"
"    background-color: #EEF4FB;   /* biru abu lembut */\n"
"    border: 2px solid #D6E2F1;\n"
"    border-radius: 10px;\n"
"}\n"
"")
        self.logFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.logFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_71 = QVBoxLayout(self.logFrame)
        self.verticalLayout_71.setObjectName(u"verticalLayout_71")
        self.frame_64 = QFrame(self.logFrame)
        self.frame_64.setObjectName(u"frame_64")
        self.frame_64.setMaximumSize(QSize(16777215, 100))
        self.frame_64.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_64.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_85 = QHBoxLayout(self.frame_64)
        self.horizontalLayout_85.setObjectName(u"horizontalLayout_85")
        self.frame_65 = QFrame(self.frame_64)
        self.frame_65.setObjectName(u"frame_65")
        self.frame_65.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_65.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_85.addWidget(self.frame_65)

        self.titlelog = QLabel(self.frame_64)
        self.titlelog.setObjectName(u"titlelog")
        sizePolicy2.setHeightForWidth(self.titlelog.sizePolicy().hasHeightForWidth())
        self.titlelog.setSizePolicy(sizePolicy2)
        self.titlelog.setMaximumSize(QSize(172, 45))
        self.titlelog.setFont(font4)
        self.titlelog.setStyleSheet(u"#titlelog{\n"
"    font: bold 12pt \"Segoe UI\";\n"
"    color: white;\n"
"    background-color: #9B8EC7;   /* ungu pastel lembut */\n"
"    border-radius: 8px;\n"
"    padding: 6px 10px;\n"
"    border: 1px solid #9B8EC7;\n"
"    \n"
"    min-width: 100px;\n"
"    max-width: 150px;\n"
"    qproperty-alignment: AlignCenter;\n"
"}\n"
"")
        self.titlelog.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_85.addWidget(self.titlelog)

        self.frame_66 = QFrame(self.frame_64)
        self.frame_66.setObjectName(u"frame_66")
        self.frame_66.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_66.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_85.addWidget(self.frame_66)


        self.verticalLayout_71.addWidget(self.frame_64)

        self.frame_62 = QFrame(self.logFrame)
        self.frame_62.setObjectName(u"frame_62")
        self.frame_62.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_62.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_38 = QVBoxLayout(self.frame_62)
        self.verticalLayout_38.setObjectName(u"verticalLayout_38")
        self.logPlainEdit = QPlainTextEdit(self.frame_62)
        self.logPlainEdit.setObjectName(u"logPlainEdit")
        self.logPlainEdit.setStyleSheet(u"QPlainTextEdit#logPlainEdit {\n"
"    background-color: #FAFCFF;          /* lebih terang dari frame */\n"
"    color: #1F2933;                     /* teks lebih kontras */\n"
"    border: 2px solid #D6E2F1;           /* tetap senada frame */\n"
"    border-radius: 20px;\n"
"    padding: 6px;\n"
"    font: 10.5pt \"Consolas\";\n"
"    selection-background-color: #4A90D9;\n"
"    selection-color: white;\n"
"}\n"
"\n"
"QPlainTextEdit#logPlainEdit:focus {\n"
"    border: 2px solid #4A90D9;\n"
"    background-color: #FFFFFF;          /* fokus = paling terang */\n"
"}\n"
"\n"
"QPlainTextEdit#logPlainEdit:read-only {\n"
"    background-color: #F7FAFE;          /* read-only tapi tetap terang */\n"
"}\n"
"\n"
"/* ===== Scrollbar ===== */\n"
"\n"
"QScrollBar:vertical {\n"
"    background: #EEF4FB;                /* frame color */\n"
"    width: 10px;\n"
"    margin: 2px;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical {\n"
"    background: #BFD2EA;                /* lebih kontras */\n"
"    min-h"
                        "eight: 20px;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical:hover {\n"
"    background: #4A90D9;\n"
"}\n"
"\n"
"QScrollBar::add-line:vertical,\n"
"QScrollBar::sub-line:vertical {\n"
"    height: 0px;\n"
"}\n"
"")

        self.verticalLayout_38.addWidget(self.logPlainEdit)


        self.verticalLayout_71.addWidget(self.frame_62)


        self.verticalLayout_23.addWidget(self.logFrame)


        self.horizontalLayout_78.addWidget(self.settingsandlogFrame)

        self.framekosong = QFrame(self.framecontentsettings)
        self.framekosong.setObjectName(u"framekosong")
        self.framekosong.setMinimumSize(QSize(936, 0))
        self.framekosong.setMaximumSize(QSize(936, 16777215))
        self.framekosong.setFrameShape(QFrame.Shape.NoFrame)
        self.framekosong.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_78.addWidget(self.framekosong)


        self.verticalLayout_21.addWidget(self.framecontentsettings)

        self.stackedWidget.addWidget(self.page5_settings)

        self.verticalLayout_15.addWidget(self.stackedWidget)


        self.horizontalLayout_4.addWidget(self.pagesContainer)


        self.verticalLayout_6.addWidget(self.content)

        self.bottomBar = QFrame(self.contentBottom)
        self.bottomBar.setObjectName(u"bottomBar")
        self.bottomBar.setMinimumSize(QSize(0, 22))
        self.bottomBar.setMaximumSize(QSize(16777215, 22))
        self.bottomBar.setFrameShape(QFrame.Shape.NoFrame)
        self.bottomBar.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.bottomBar)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.creditsLabel = QLabel(self.bottomBar)
        self.creditsLabel.setObjectName(u"creditsLabel")
        self.creditsLabel.setMaximumSize(QSize(16777215, 16))
        font12 = QFont()
        font12.setFamilies([u"Segoe UI"])
        font12.setBold(False)
        font12.setItalic(False)
        self.creditsLabel.setFont(font12)
        self.creditsLabel.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.creditsLabel)

        self.version = QLabel(self.bottomBar)
        self.version.setObjectName(u"version")
        self.version.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.version)

        self.frame_size_grip = QFrame(self.bottomBar)
        self.frame_size_grip.setObjectName(u"frame_size_grip")
        self.frame_size_grip.setMinimumSize(QSize(20, 0))
        self.frame_size_grip.setMaximumSize(QSize(20, 16777215))
        self.frame_size_grip.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_size_grip.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_5.addWidget(self.frame_size_grip)


        self.verticalLayout_6.addWidget(self.bottomBar)


        self.verticalLayout_3.addWidget(self.contentBottom)


        self.appLayout.addWidget(self.contentBox)


        self.verticalLayout_76.addWidget(self.bgApp)

        MainWindow.setCentralWidget(self.styleSheet)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.titleLeftApp.setText(QCoreApplication.translate("MainWindow", u"EcoLab", None))
        self.titleLeftDescription.setText(QCoreApplication.translate("MainWindow", u"Dashboard", None))
        self.toggleButton.setText(QCoreApplication.translate("MainWindow", u"Hide", None))
        self.btn_growatt.setText(QCoreApplication.translate("MainWindow", u"EcoLab Power Monitoring", None))
        self.btn_controlroom.setText(QCoreApplication.translate("MainWindow", u"Control Room", None))
        self.btn_monitoringsensor.setText(QCoreApplication.translate("MainWindow", u"Environment Monitoring", None))
        self.btn_smartsocket.setText(QCoreApplication.translate("MainWindow", u"Smart Socket", None))
        self.btn_setting.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.btn_exit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.clockInfo.setText(QCoreApplication.translate("MainWindow", u"Friday, 22 August 2025 | 18:22:25", None))
        self.titleRightInfo.setText(QCoreApplication.translate("MainWindow", u"Dashboard EcoLab", None))
#if QT_CONFIG(tooltip)
        self.minimizeAppBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Minimize", None))
#endif // QT_CONFIG(tooltip)
        self.minimizeAppBtn.setText("")
#if QT_CONFIG(tooltip)
        self.maximizeRestoreAppBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Maximize", None))
#endif // QT_CONFIG(tooltip)
        self.maximizeRestoreAppBtn.setText("")
#if QT_CONFIG(tooltip)
        self.closeAppBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Close", None))
#endif // QT_CONFIG(tooltip)
        self.closeAppBtn.setText("")
        self.titleGrowattpage1.setText(QCoreApplication.translate("MainWindow", u"EcoLab Power Monitoring", None))
        self.titleFlow.setText(QCoreApplication.translate("MainWindow", u"Current Power", None))
        self.currentpvpower_value.setText(QCoreApplication.translate("MainWindow", u"PV Power: 0W", None))
        self.labeltextImportGrid.setText(QCoreApplication.translate("MainWindow", u"Import from Grid:", None))
        self.currentimportgrid_value.setText(QCoreApplication.translate("MainWindow", u"0W", None))
        self.labeltextConsumptionPower.setText(QCoreApplication.translate("MainWindow", u"Consumption Power:", None))
        self.currentconsumppower_value.setText(QCoreApplication.translate("MainWindow", u"0W/0VA", None))
        self.currentdischpower_value.setText(QCoreApplication.translate("MainWindow", u"Charging Power\uff1a0W", None))
        self.currentsocbat_value.setText(QCoreApplication.translate("MainWindow", u"SoC Battery\uff1a0%", None))
        self.titleSummary.setText(QCoreApplication.translate("MainWindow", u"Energy Summary", None))
        self.titlepvsum.setText(QCoreApplication.translate("MainWindow", u"Photovoltaic Output", None))
        self.pvtoday_value.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.labeltoday1.setText(QCoreApplication.translate("MainWindow", u"Today", None))
        self.labelkwh1.setText(QCoreApplication.translate("MainWindow", u"kWh", None))
        self.pvtotal_value.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.labeltotal1.setText(QCoreApplication.translate("MainWindow", u"Total", None))
        self.labelkwh2.setText(QCoreApplication.translate("MainWindow", u"kWh", None))
        self.titleloadsum.setText(QCoreApplication.translate("MainWindow", u"Load Consumption", None))
        self.loadtoday_value.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.labeltoday2.setText(QCoreApplication.translate("MainWindow", u"Today", None))
        self.labelkwh3.setText(QCoreApplication.translate("MainWindow", u"kWh", None))
        self.loadtotal_value.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.labeltotal2.setText(QCoreApplication.translate("MainWindow", u"Total", None))
        self.labelkwh4.setText(QCoreApplication.translate("MainWindow", u"kWh", None))
        self.titlechargingsum.setText(QCoreApplication.translate("MainWindow", u"Charging", None))
        self.chargingtoday_value.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.labeltoday3.setText(QCoreApplication.translate("MainWindow", u"Today", None))
        self.labelkwh5.setText(QCoreApplication.translate("MainWindow", u"kWh", None))
        self.chargingtotal_value.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.labeltotal3.setText(QCoreApplication.translate("MainWindow", u"Total", None))
        self.labelkwh6.setText(QCoreApplication.translate("MainWindow", u"kWh", None))
        self.titledischargingsum.setText(QCoreApplication.translate("MainWindow", u"Discharging", None))
        self.dischargingtoday_value.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.labeltoday4.setText(QCoreApplication.translate("MainWindow", u"Today", None))
        self.labelkwh7.setText(QCoreApplication.translate("MainWindow", u"kWh", None))
        self.dischargingtotal_value.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.labeltotal4.setText(QCoreApplication.translate("MainWindow", u"Total", None))
        self.labelkwh8.setText(QCoreApplication.translate("MainWindow", u"kWh", None))
        self.titleimportsum.setText(QCoreApplication.translate("MainWindow", u"Imported from Grid", None))
        self.imporgridttoday_value.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.labeltoday5.setText(QCoreApplication.translate("MainWindow", u"Today", None))
        self.labelkwh9.setText(QCoreApplication.translate("MainWindow", u"kWh", None))
        self.imporgridttotal_value.setText(QCoreApplication.translate("MainWindow", u"0.0", None))
        self.labeltotal5.setText(QCoreApplication.translate("MainWindow", u"Total", None))
        self.labelkwh10.setText(QCoreApplication.translate("MainWindow", u"kWh", None))
        self.titlecontrolroom.setText(QCoreApplication.translate("MainWindow", u"Control Room", None))
        self.titleLamp.setText(QCoreApplication.translate("MainWindow", u"Lamp Control", None))
        self.titlelampbtn_1.setText(QCoreApplication.translate("MainWindow", u"Lampu 1", None))
        self.titlelampbtn_2.setText(QCoreApplication.translate("MainWindow", u"Lampu 2", None))
        self.titlelampbtn_3.setText(QCoreApplication.translate("MainWindow", u"Lampu 3", None))
        self.titlelampbtn_4.setText(QCoreApplication.translate("MainWindow", u"Lampu 4", None))
        self.titlelampbtn_5.setText(QCoreApplication.translate("MainWindow", u"Lampu 5", None))
        self.statusmcuA.setText(QCoreApplication.translate("MainWindow", u"MCU A: Online", None))
        self.titleAC.setText(QCoreApplication.translate("MainWindow", u"AC Control", None))
        self.statusAC.setText(QCoreApplication.translate("MainWindow", u"Status AC: ON", None))
        self.btn_temp_up.setText(QCoreApplication.translate("MainWindow", u"Temp +", None))
        self.btn_temp_down.setText(QCoreApplication.translate("MainWindow", u"Temp -", None))
        self.btn_cool_ac.setText(QCoreApplication.translate("MainWindow", u"COOL", None))
        self.btn_fan_ac.setText(QCoreApplication.translate("MainWindow", u"FAN", None))
        self.statusmcuB.setText(QCoreApplication.translate("MainWindow", u"MCU B: Online", None))
        self.titlemonitoring.setText(QCoreApplication.translate("MainWindow", u"Sensor Monitoring: Indoor & Weather Station", None))
        self.titleIndoor.setText(QCoreApplication.translate("MainWindow", u"Indoor Conditions", None))
        self.titleSuhuIndoor.setText(QCoreApplication.translate("MainWindow", u"Temperature", None))
        self.tempIndoor_value.setText(QCoreApplication.translate("MainWindow", u"0.0\u00b0C", None))
        self.titleHumidIndoor.setText(QCoreApplication.translate("MainWindow", u"Humidity", None))
        self.humidIndoor_value.setText(QCoreApplication.translate("MainWindow", u"0%", None))
        self.titleOutdoor.setText(QCoreApplication.translate("MainWindow", u"Outdoor Conditions", None))
        self.titletempW.setText(QCoreApplication.translate("MainWindow", u"Temperature", None))
        self.tempW_value.setText(QCoreApplication.translate("MainWindow", u"0.0\u00b0C", None))
        self.titlehumidw.setText(QCoreApplication.translate("MainWindow", u"Humidity", None))
        self.humidW_value.setText(QCoreApplication.translate("MainWindow", u"0%", None))
        self.titlePressW.setText(QCoreApplication.translate("MainWindow", u"Pressure", None))
        self.pressureW_value.setText(QCoreApplication.translate("MainWindow", u"0.0 hPa", None))
        self.titlewinspdW.setText(QCoreApplication.translate("MainWindow", u"Wind Speed", None))
        self.windspdW_value.setText(QCoreApplication.translate("MainWindow", u"0.0 m/s", None))
        self.titlesinspdavgW.setText(QCoreApplication.translate("MainWindow", u"Wind Speed Average", None))
        self.windspdavgW_value.setText(QCoreApplication.translate("MainWindow", u"0.0 m/s", None))
        self.titlewindspddirW.setText(QCoreApplication.translate("MainWindow", u"Wind Speed Direction", None))
        self.windspddirW_value.setText(QCoreApplication.translate("MainWindow", u"0\u00b0C", None))
        self.titletotalrainW.setText(QCoreApplication.translate("MainWindow", u"Total Rainfall", None))
        self.totalrainW_value.setText(QCoreApplication.translate("MainWindow", u"0.0 mm", None))
        self.titleRainrateW.setText(QCoreApplication.translate("MainWindow", u"Rainfall Rate", None))
        self.rainrateW_value.setText(QCoreApplication.translate("MainWindow", u"0.0 mm", None))
        self.titleheatindexW.setText(QCoreApplication.translate("MainWindow", u"Heat Index", None))
        self.heatindexW_value.setText(QCoreApplication.translate("MainWindow", u"0.0\u00b0C", None))
        self.titleSmartsocket.setText(QCoreApplication.translate("MainWindow", u"Smart Socket", None))
        self.titlesmart1.setText(QCoreApplication.translate("MainWindow", u"Smart Socket 1", None))
        self.statussocket1.setText(QCoreApplication.translate("MainWindow", u"Status Device: Offline", None))
        self.label_energy_monitoring_title.setText(QCoreApplication.translate("MainWindow", u"Energy Monitoring", None))
        self.label_voltage1.setText(QCoreApplication.translate("MainWindow", u"Voltage: -- V", None))
        self.label_current1.setText(QCoreApplication.translate("MainWindow", u"Current: -- A", None))
        self.label_power1.setText(QCoreApplication.translate("MainWindow", u"Power: -- W", None))
        self.label_energy1.setText(QCoreApplication.translate("MainWindow", u"Energy: -- kWh", None))
        self.label_frequency1.setText(QCoreApplication.translate("MainWindow", u"Frequency: -- Hz", None))
        self.label_powerfactor1.setText(QCoreApplication.translate("MainWindow", u"Power Factor: --", None))
        self.label_switch_status_title.setText(QCoreApplication.translate("MainWindow", u"Status Switch", None))
        self.label_switch_status_value1.setText(QCoreApplication.translate("MainWindow", u"OFF", None))
        self.label_timer_title.setText(QCoreApplication.translate("MainWindow", u"Timer:", None))
        self.label_timer_status1.setText(QCoreApplication.translate("MainWindow", u"No Timer", None))
        self.label_scheduling_title.setText(QCoreApplication.translate("MainWindow", u"Scheduling:", None))
        self.label_scheduling_status1.setText(QCoreApplication.translate("MainWindow", u"No Schedule", None))
        self.btn_action_socket1.setText(QCoreApplication.translate("MainWindow", u"Action", None))
        self.titlesmart2.setText(QCoreApplication.translate("MainWindow", u"Smart Socket 2", None))
        self.statussocket2.setText(QCoreApplication.translate("MainWindow", u"Status Device: Offline", None))
        self.label_energy_monitoring_title_2.setText(QCoreApplication.translate("MainWindow", u"Energy Monitoring", None))
        self.label_voltage2.setText(QCoreApplication.translate("MainWindow", u"Voltage: -- V", None))
        self.label_current2.setText(QCoreApplication.translate("MainWindow", u"Current: -- A", None))
        self.label_power2.setText(QCoreApplication.translate("MainWindow", u"Power: -- W", None))
        self.label_energy2.setText(QCoreApplication.translate("MainWindow", u"Energy: -- kWh", None))
        self.label_frequency2.setText(QCoreApplication.translate("MainWindow", u"Frequency: -- Hz", None))
        self.label_powerfactor2.setText(QCoreApplication.translate("MainWindow", u"Power Factor: --", None))
        self.label_switch_status_title_2.setText(QCoreApplication.translate("MainWindow", u"Status Switch", None))
        self.label_switch_status_value2.setText(QCoreApplication.translate("MainWindow", u"OFF", None))
        self.label_timer_title_2.setText(QCoreApplication.translate("MainWindow", u"Timer:", None))
        self.label_timer_status2.setText(QCoreApplication.translate("MainWindow", u"No Timer", None))
        self.label_scheduling_title_2.setText(QCoreApplication.translate("MainWindow", u"Scheduling:", None))
        self.label_scheduling_status2.setText(QCoreApplication.translate("MainWindow", u"No Schedule", None))
        self.btn_action_socket2.setText(QCoreApplication.translate("MainWindow", u"Action", None))
        self.titlesmart3.setText(QCoreApplication.translate("MainWindow", u"Smart Socket 3", None))
        self.statussocket3.setText(QCoreApplication.translate("MainWindow", u"Status Device: Offline", None))
        self.label_energy_monitoring_title_3.setText(QCoreApplication.translate("MainWindow", u"Energy Monitoring", None))
        self.label_voltage3.setText(QCoreApplication.translate("MainWindow", u"Voltage: -- V", None))
        self.label_current3.setText(QCoreApplication.translate("MainWindow", u"Current: -- A", None))
        self.label_power3.setText(QCoreApplication.translate("MainWindow", u"Power: -- W", None))
        self.label_energy3.setText(QCoreApplication.translate("MainWindow", u"Energy: -- kWh", None))
        self.label_frequency3.setText(QCoreApplication.translate("MainWindow", u"Frequency: -- Hz", None))
        self.label_powerfactor3.setText(QCoreApplication.translate("MainWindow", u"Power Factor: --", None))
        self.label_switch_status_title_3.setText(QCoreApplication.translate("MainWindow", u"Status Switch", None))
        self.label_switch_status_value3.setText(QCoreApplication.translate("MainWindow", u"OFF", None))
        self.label_timer_title_3.setText(QCoreApplication.translate("MainWindow", u"Timer:", None))
        self.label_timer_status3.setText(QCoreApplication.translate("MainWindow", u"No Timer", None))
        self.label_scheduling_title_3.setText(QCoreApplication.translate("MainWindow", u"Scheduling:", None))
        self.label_scheduling_status3.setText(QCoreApplication.translate("MainWindow", u"No Schedule", None))
        self.btn_action_socket3.setText(QCoreApplication.translate("MainWindow", u"Action", None))
        self.titlesmart4.setText(QCoreApplication.translate("MainWindow", u"Smart Socket 4", None))
        self.statussocket4.setText(QCoreApplication.translate("MainWindow", u"Status Device: Offline", None))
        self.label_energy_monitoring_title_4.setText(QCoreApplication.translate("MainWindow", u"Energy Monitoring", None))
        self.label_voltage4.setText(QCoreApplication.translate("MainWindow", u"Voltage: -- V", None))
        self.label_current4.setText(QCoreApplication.translate("MainWindow", u"Current: -- A", None))
        self.label_power4.setText(QCoreApplication.translate("MainWindow", u"Power: -- W", None))
        self.label_energy4.setText(QCoreApplication.translate("MainWindow", u"Energy: -- kWh", None))
        self.label_frequency4.setText(QCoreApplication.translate("MainWindow", u"Frequency: -- Hz", None))
        self.label_powerfactor4.setText(QCoreApplication.translate("MainWindow", u"Power Factor: --", None))
        self.label_switch_status_title_4.setText(QCoreApplication.translate("MainWindow", u"Status Switch", None))
        self.label_switch_status_value4.setText(QCoreApplication.translate("MainWindow", u"OFF", None))
        self.label_timer_title_4.setText(QCoreApplication.translate("MainWindow", u"Timer:", None))
        self.label_timer_status4.setText(QCoreApplication.translate("MainWindow", u"No Timer", None))
        self.label_scheduling_title_4.setText(QCoreApplication.translate("MainWindow", u"Scheduling:", None))
        self.label_scheduling_status4.setText(QCoreApplication.translate("MainWindow", u"No Schedule", None))
        self.btn_action_socket4.setText(QCoreApplication.translate("MainWindow", u"Action", None))
        self.titlesmart5.setText(QCoreApplication.translate("MainWindow", u"Smart Socket 5", None))
        self.statussocket5.setText(QCoreApplication.translate("MainWindow", u"Status Device: Offline", None))
        self.label_energy_monitoring_title_5.setText(QCoreApplication.translate("MainWindow", u"Energy Monitoring", None))
        self.label_voltage5.setText(QCoreApplication.translate("MainWindow", u"Voltage: -- V", None))
        self.label_current5.setText(QCoreApplication.translate("MainWindow", u"Current: -- A", None))
        self.label_power5.setText(QCoreApplication.translate("MainWindow", u"Power: -- W", None))
        self.label_energy5.setText(QCoreApplication.translate("MainWindow", u"Energy: -- kWh", None))
        self.label_frequency5.setText(QCoreApplication.translate("MainWindow", u"Frequency: -- Hz", None))
        self.label_powerfactor5.setText(QCoreApplication.translate("MainWindow", u"Power Factor: --", None))
        self.label_switch_status_title_5.setText(QCoreApplication.translate("MainWindow", u"Status Switch", None))
        self.label_switch_status_value5.setText(QCoreApplication.translate("MainWindow", u"OFF", None))
        self.label_timer_title_5.setText(QCoreApplication.translate("MainWindow", u"Timer:", None))
        self.label_timer_status5.setText(QCoreApplication.translate("MainWindow", u"No Timer", None))
        self.label_scheduling_title_5.setText(QCoreApplication.translate("MainWindow", u"Scheduling:", None))
        self.label_scheduling_status5.setText(QCoreApplication.translate("MainWindow", u"No Schedule", None))
        self.btn_action_socket5.setText(QCoreApplication.translate("MainWindow", u"Action", None))
        self.titleSettings.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.titleProfile.setText(QCoreApplication.translate("MainWindow", u"User Profile", None))
        self.labelUsername.setText(QCoreApplication.translate("MainWindow", u"Username", None))
        self.inputUsername.setText("")
        self.labelEmail.setText(QCoreApplication.translate("MainWindow", u"Email", None))
        self.btnUpdatePassword.setText(QCoreApplication.translate("MainWindow", u"Update Password", None))
        self.btnAdminpanel.setText(QCoreApplication.translate("MainWindow", u"Admin Panel", None))
        self.btnLogout.setText(QCoreApplication.translate("MainWindow", u"Logout", None))
        self.titlelog.setText(QCoreApplication.translate("MainWindow", u"Log Activity", None))
        self.creditsLabel.setText(QCoreApplication.translate("MainWindow", u"By: SKAR, IP, EcoLab DTEDI", None))
        self.version.setText(QCoreApplication.translate("MainWindow", u"v1.0", None))
    # retranslateUi

