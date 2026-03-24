# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'adminpanelEZGgDC.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QHeaderView,
    QLabel, QMainWindow, QPushButton, QSizePolicy,
    QSpacerItem, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1920, 1094)
        self.styleSheet = QWidget(MainWindow)
        self.styleSheet.setObjectName(u"styleSheet")
        self.styleSheet.setMinimumSize(QSize(1920, 1080))
        self.styleSheet.setMaximumSize(QSize(1920, 1080))
        self.styleSheet.setStyleSheet(u"\n"
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
"#contentTop {	\n"
"	background-color: #002B5B;\n"
"	border: 1px solid #003F7D;\n"
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
""
                        "\n"
"/* ================= TABLE ================= */\n"
"QTableWidget {\n"
"    background-color: #FFFFFF;\n"
"    alternate-background-color: #F4FAFF;\n"
"    gridline-color: #D6EAF8;\n"
"\n"
"    border: 1px solid #005C99;   /* border biru */\n"
"    border-radius: 10px;         /* rounded utama */\n"
"\n"
"    color: #002B5B;\n"
"    font-size: 11pt;\n"
"    font-weight: 600;\n"
"\n"
"    selection-background-color: #005C99;\n"
"    selection-color: #FFFFFF;\n"
"}\n"
"\n"
"/* ================= ITEM ================= */\n"
"QTableWidget::item {\n"
"    border-bottom: 1px solid #E1F2FB;\n"
"    padding: 8px;\n"
"    font-weight: 600;\n"
"}\n"
"\n"
"QTableWidget::item:hover {\n"
"    background-color: #E8F4FC;\n"
"}\n"
"\n"
"QTableWidget::item:selected {\n"
"    background-color: #005C99;\n"
"    color: #FFFFFF;\n"
"}\n"
"\n"
"/* ================= HEADER (BIAR NYATU & ROUNDED LOOK) ================= */\n"
"QHeaderView {\n"
"    background-color: #003F7D;   /* base header */\n"
"    border-top-left-radius: 10px"
                        ";\n"
"    border-top-right-radius: 10px;\n"
"}\n"
"\n"
"QHeaderView::section {\n"
"    background-color: transparent; /* ikut parent biar nyatu */\n"
"    color: #FFFFFF;\n"
"    padding: 10px 8px;\n"
"    border: none;\n"
"    font-weight: bold;\n"
"    font-size: 11pt;\n"
"}\n"
"\n"
"/* ================= COMBOBOX (ROLE DROPDOWN) ================= */\n"
"QTableWidget QComboBox {\n"
"    background-color: #FFFFFF;\n"
"    border: 1px solid #005C99;\n"
"    border-radius: 5px;\n"
"    padding: 4px 8px;\n"
"    font-weight: 600;\n"
"    font-size: 10pt;\n"
"    color: #002B5B;\n"
"}\n"
"\n"
"QTableWidget QComboBox:hover {\n"
"    background-color: #E8F4FC;\n"
"    border: 1px solid #003F7D;\n"
"}\n"
"\n"
"QTableWidget QComboBox::drop-down {\n"
"    border: none;\n"
"    width: 20px;\n"
"}\n"
"\n"
"QTableWidget QComboBox::down-arrow {\n"
"    image: url(none);\n"
"    border: 2px solid #005C99;\n"
"    width: 8px;\n"
"    height: 8px;\n"
"    background-color: #005C99;\n"
"}\n"
"\n"
"QTableWidget QComboBox QAbstr"
                        "actItemView {\n"
"    background-color: #FFFFFF;\n"
"    border: 1px solid #005C99;\n"
"    selection-background-color: #005C99;\n"
"    selection-color: #FFFFFF;\n"
"    padding: 4px;\n"
"}\n"
"\n"
"/* ================= CORNER ================= */\n"
"QTableCornerButton::section {\n"
"    background-color: #003F7D;\n"
"    border: none;\n"
"}\n"
"\n"
"/* ================= SCROLLBAR VERTICAL ================= */\n"
"QTableWidget QScrollBar:vertical {\n"
"    background: transparent;\n"
"    width: 12px;\n"
"    margin: 4px 2px 4px 2px;\n"
"}\n"
"\n"
"QTableWidget QScrollBar::handle:vertical {\n"
"    background: #005C99;\n"
"    border-radius: 5px;\n"
"    min-height: 20px;\n"
"}\n"
"\n"
"QTableWidget QScrollBar::handle:vertical:hover {\n"
"    background: #003F7D;\n"
"}\n"
"\n"
"QTableWidget QScrollBar::handle:vertical:pressed {\n"
"    background: #002B5B;\n"
"}\n"
"\n"
"QScrollBar::add-line:vertical,\n"
"QScrollBar::sub-line:vertical {\n"
"    height: 0px;\n"
"}\n"
"\n"
"/* ================= SCROLLBAR HORIZ"
                        "ONTAL ================= */\n"
"QTableWidget QScrollBar:horizontal {\n"
"    background: transparent;\n"
"    height: 10px;\n"
"    margin: 2px;\n"
"}\n"
"\n"
"QTableWidget QScrollBar::handle:horizontal {\n"
"    background: #005C99;\n"
"    border-radius: 5px;\n"
"    min-width: 20px;\n"
"}\n"
"\n"
"QTableWidget QScrollBar::handle:horizontal:hover {\n"
"    background: #003F7D;\n"
"}\n"
"\n"
"QTableWidget QScrollBar::handle:horizontal:pressed {\n"
"    background: #002B5B;\n"
"}\n"
"\n"
"QScrollBar::add-line:horizontal,\n"
"QScrollBar::sub-line:horizontal {\n"
"    width: 0px;\n"
"}\n"
"\n"
"#infoaccountFrame QFrame {\n"
"    background-color: #EDF6FC;   /* biru sangat pucat */\n"
"    border: 2px solid #D9E9F6; /* garis tipis, hampir menyatu */\n"
"    border-radius: 12px;\n"
"    margin: 4px;\n"
"    padding: 8px 0;\n"
"}\n"
"\n"
"#infoaccountFrame QLabel {\n"
"    border: none;              /* hapus border default */\n"
"    background: transparent;    /* pastikan tidak ada background */\n"
"    color: #0b3"
                        "d91;            /* warna font */\n"
"    font-weight: bold;\n"
"    font-size: 36px;\n"
"}\n"
"\n"
"\n"
"")
        self.verticalLayout_4 = QVBoxLayout(self.styleSheet)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.bgApp = QFrame(self.styleSheet)
        self.bgApp.setObjectName(u"bgApp")
        self.bgApp.setStyleSheet(u"#topLogoadmin {\n"
"	background-color: #003F7D;\n"
"	background-image: url(:/images/images/images/logoecolab.png);\n"
"	background-position: centered;\n"
"	background-repeat: no-repeat;\n"
"}")
        self.bgApp.setFrameShape(QFrame.Shape.NoFrame)
        self.bgApp.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.bgApp)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.contentTop = QFrame(self.bgApp)
        self.contentTop.setObjectName(u"contentTop")
        self.contentTop.setMaximumSize(QSize(16777215, 50))
        self.contentTop.setFrameShape(QFrame.Shape.NoFrame)
        self.contentTop.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.contentTop)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 10, 0)
        self.topLogoadmin = QFrame(self.contentTop)
        self.topLogoadmin.setObjectName(u"topLogoadmin")
        self.topLogoadmin.setMinimumSize(QSize(50, 50))
        self.topLogoadmin.setMaximumSize(QSize(50, 50))
        self.topLogoadmin.setFrameShape(QFrame.Shape.NoFrame)
        self.topLogoadmin.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_4.addWidget(self.topLogoadmin)

        self.leftBox = QFrame(self.contentTop)
        self.leftBox.setObjectName(u"leftBox")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.leftBox.sizePolicy().hasHeightForWidth())
        self.leftBox.setSizePolicy(sizePolicy)
        self.leftBox.setFrameShape(QFrame.Shape.NoFrame)
        self.leftBox.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.leftBox)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.clockInfo = QLabel(self.leftBox)
        self.clockInfo.setObjectName(u"clockInfo")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.clockInfo.sizePolicy().hasHeightForWidth())
        self.clockInfo.setSizePolicy(sizePolicy1)
        self.clockInfo.setMaximumSize(QSize(16777215, 45))
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        self.clockInfo.setFont(font)
        self.clockInfo.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.clockInfo)

        self.titleRightInfo = QLabel(self.leftBox)
        self.titleRightInfo.setObjectName(u"titleRightInfo")
        sizePolicy1.setHeightForWidth(self.titleRightInfo.sizePolicy().hasHeightForWidth())
        self.titleRightInfo.setSizePolicy(sizePolicy1)
        self.titleRightInfo.setMaximumSize(QSize(16777215, 45))
        font1 = QFont()
        font1.setFamilies([u"Segoe UI"])
        font1.setPointSize(12)
        font1.setBold(True)
        font1.setItalic(False)
        self.titleRightInfo.setFont(font1)
        self.titleRightInfo.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.titleRightInfo)

        self.horizontalSpacer = QSpacerItem(80, 20, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.horizontalLayout_4.addWidget(self.leftBox)

        self.rightButtons = QFrame(self.contentTop)
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
        font2 = QFont()
        font2.setFamilies([u"Segoe UI"])
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        font2.setStyleStrategy(QFont.PreferDefault)
        self.maximizeRestoreAppBtn.setFont(font2)
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


        self.horizontalLayout_4.addWidget(self.rightButtons)


        self.verticalLayout.addWidget(self.contentTop)

        self.contentBottom = QFrame(self.bgApp)
        self.contentBottom.setObjectName(u"contentBottom")
        self.contentBottom.setFrameShape(QFrame.Shape.NoFrame)
        self.contentBottom.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.contentBottom)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.titleFrame = QFrame(self.contentBottom)
        self.titleFrame.setObjectName(u"titleFrame")
        self.titleFrame.setMinimumSize(QSize(0, 150))
        self.titleFrame.setMaximumSize(QSize(16777215, 200))
        self.titleFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.titleFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.titleFrame)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(30, 20, 30, -1)
        self.insidetitleFrame = QFrame(self.titleFrame)
        self.insidetitleFrame.setObjectName(u"insidetitleFrame")
        self.insidetitleFrame.setMinimumSize(QSize(0, 150))
        self.insidetitleFrame.setMaximumSize(QSize(16777215, 200))
        self.insidetitleFrame.setStyleSheet(u"#insidetitleFrame {\n"
"    background-color: #EDF6FC;   /* biru sangat pucat */\n"
"    border: 1.5px solid #D9E9F6; /* garis tipis, hampir menyatu */\n"
"    border-radius: 12px;\n"
"}\n"
"")
        self.insidetitleFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.insidetitleFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.insidetitleFrame)
        self.verticalLayout_5.setSpacing(6)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(10, 10, 10, 10)
        self.setFrame = QFrame(self.insidetitleFrame)
        self.setFrame.setObjectName(u"setFrame")
        self.setFrame.setMinimumSize(QSize(0, 70))
        self.setFrame.setMaximumSize(QSize(16777215, 70))
        self.setFrame.setStyleSheet(u"#insidetitleFrame {\n"
"    background-color: #EDF6FC;   /* biru sangat pucat */\n"
"    border: 1.5px solid #D9E9F6; /* garis tipis, hampir menyatu */\n"
"    border-radius: 12px;\n"
"}\n"
"")
        self.setFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.setFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.setFrame)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(self.setFrame)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.NoFrame)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout.addWidget(self.frame)

        self.labelTitle = QLabel(self.setFrame)
        self.labelTitle.setObjectName(u"labelTitle")
        font3 = QFont()
        font3.setFamilies([u"Segoe UI"])
        font3.setPointSize(32)
        font3.setBold(True)
        font3.setItalic(False)
        self.labelTitle.setFont(font3)
        self.labelTitle.setStyleSheet(u"#labelTitle{\n"
"    font: bold 32pt \"Segoe UI\";\n"
"    color: white;\n"
"    background-color: #33A1E0;\n"
"    border-radius: 8px;\n"
"    padding: 6px 10px;\n"
"    border: 1px solid #33A1E0;\n"
"    qproperty-alignment: AlignCenter; /* biar teks di tengah */\n"
"    /* Tambahan pengaturan ukuran */\n"
"    min-width: 500px;    /* lebar minimum */\n"
"    max-width: 1000px;    /* lebar maksimum */\n"
"}\n"
"")
        self.labelTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.labelTitle)

        self.frame_2 = QFrame(self.setFrame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.frame_3 = QFrame(self.frame_2)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_5.addWidget(self.frame_3)

        self.btn_back = QPushButton(self.frame_2)
        self.btn_back.setObjectName(u"btn_back")
        self.btn_back.setMinimumSize(QSize(90, 40))
        self.btn_back.setMaximumSize(QSize(90, 40))
        font4 = QFont()
        font4.setFamilies([u"Arial"])
        font4.setPointSize(12)
        font4.setBold(True)
        self.btn_back.setFont(font4)
        self.btn_back.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    border-radius: 12px;\n"
"    background-color: rgb(65, 127, 193); /* Warna background utama */\n"
"    color: rgb(255, 255, 255); /* Warna teks */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(65, 127, 193, 150); /* Warna saat hover */\n"
"}\n"
"")

        self.horizontalLayout_5.addWidget(self.btn_back)


        self.horizontalLayout.addWidget(self.frame_2)


        self.verticalLayout_5.addWidget(self.setFrame)

        self.labelSubtitle = QLabel(self.insidetitleFrame)
        self.labelSubtitle.setObjectName(u"labelSubtitle")
        font5 = QFont()
        font5.setWeight(QFont.DemiBold)
        self.labelSubtitle.setFont(font5)
        self.labelSubtitle.setStyleSheet(u"color: #33A1E0;\n"
"    font-size: 14px;\n"
"    font-weight: 600;\n"
"\n"
"")
        self.labelSubtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_5.addWidget(self.labelSubtitle)


        self.verticalLayout_3.addWidget(self.insidetitleFrame)


        self.verticalLayout_2.addWidget(self.titleFrame)

        self.infoaccountFrame = QFrame(self.contentBottom)
        self.infoaccountFrame.setObjectName(u"infoaccountFrame")
        self.infoaccountFrame.setMinimumSize(QSize(0, 150))
        self.infoaccountFrame.setMaximumSize(QSize(16777215, 140))
        self.infoaccountFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.infoaccountFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayoutInfo = QHBoxLayout(self.infoaccountFrame)
        self.horizontalLayoutInfo.setObjectName(u"horizontalLayoutInfo")
        self.horizontalLayoutInfo.setContentsMargins(30, -1, 30, -1)
        self.frameAccounts = QFrame(self.infoaccountFrame)
        self.frameAccounts.setObjectName(u"frameAccounts")
        self.frameAccounts.setStyleSheet(u"")
        self.frameAccounts.setFrameShape(QFrame.Shape.NoFrame)
        self.verticalLayoutAccounts = QVBoxLayout(self.frameAccounts)
        self.verticalLayoutAccounts.setSpacing(0)
        self.verticalLayoutAccounts.setObjectName(u"verticalLayoutAccounts")
        self.verticalLayoutAccounts.setContentsMargins(20, 0, 0, 0)
        self.labelAccountsCount = QLabel(self.frameAccounts)
        self.labelAccountsCount.setObjectName(u"labelAccountsCount")
        font6 = QFont()
        font6.setBold(True)
        self.labelAccountsCount.setFont(font6)
        self.labelAccountsCount.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayoutAccounts.addWidget(self.labelAccountsCount)

        self.labelAccountsText = QLabel(self.frameAccounts)
        self.labelAccountsText.setObjectName(u"labelAccountsText")
        self.labelAccountsText.setStyleSheet(u"    font-size: 14px;\n"
"    font-weight: 600;\n"
"	color: none;  \n"
"")
        self.labelAccountsText.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayoutAccounts.addWidget(self.labelAccountsText)


        self.horizontalLayoutInfo.addWidget(self.frameAccounts)

        self.framePending = QFrame(self.infoaccountFrame)
        self.framePending.setObjectName(u"framePending")
        self.framePending.setFrameShape(QFrame.Shape.NoFrame)
        self.verticalLayoutPending = QVBoxLayout(self.framePending)
        self.verticalLayoutPending.setSpacing(0)
        self.verticalLayoutPending.setObjectName(u"verticalLayoutPending")
        self.verticalLayoutPending.setContentsMargins(20, 0, 0, 0)
        self.labelPendingCount = QLabel(self.framePending)
        self.labelPendingCount.setObjectName(u"labelPendingCount")
        self.labelPendingCount.setFont(font6)
        self.labelPendingCount.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayoutPending.addWidget(self.labelPendingCount)

        self.labelPendingText = QLabel(self.framePending)
        self.labelPendingText.setObjectName(u"labelPendingText")
        self.labelPendingText.setStyleSheet(u"    font-size: 14px;\n"
"    font-weight: 600;\n"
"	color: none;  \n"
"")
        self.labelPendingText.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayoutPending.addWidget(self.labelPendingText)


        self.horizontalLayoutInfo.addWidget(self.framePending)

        self.frameActive = QFrame(self.infoaccountFrame)
        self.frameActive.setObjectName(u"frameActive")
        self.frameActive.setFrameShape(QFrame.Shape.NoFrame)
        self.verticalLayoutActive = QVBoxLayout(self.frameActive)
        self.verticalLayoutActive.setSpacing(0)
        self.verticalLayoutActive.setObjectName(u"verticalLayoutActive")
        self.verticalLayoutActive.setContentsMargins(20, 0, 0, 0)
        self.labelActiveCount = QLabel(self.frameActive)
        self.labelActiveCount.setObjectName(u"labelActiveCount")
        self.labelActiveCount.setFont(font6)
        self.labelActiveCount.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayoutActive.addWidget(self.labelActiveCount)

        self.labelActiveText = QLabel(self.frameActive)
        self.labelActiveText.setObjectName(u"labelActiveText")
        self.labelActiveText.setStyleSheet(u"    font-size: 14px;\n"
"    font-weight: 600;\n"
"	color: none;  \n"
"")
        self.labelActiveText.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayoutActive.addWidget(self.labelActiveText)


        self.horizontalLayoutInfo.addWidget(self.frameActive)

        self.frameBlocked = QFrame(self.infoaccountFrame)
        self.frameBlocked.setObjectName(u"frameBlocked")
        self.frameBlocked.setFrameShape(QFrame.Shape.NoFrame)
        self.verticalLayoutBlocked = QVBoxLayout(self.frameBlocked)
        self.verticalLayoutBlocked.setSpacing(0)
        self.verticalLayoutBlocked.setObjectName(u"verticalLayoutBlocked")
        self.verticalLayoutBlocked.setContentsMargins(20, 0, 0, 0)
        self.labelBlockedCount = QLabel(self.frameBlocked)
        self.labelBlockedCount.setObjectName(u"labelBlockedCount")
        self.labelBlockedCount.setFont(font6)
        self.labelBlockedCount.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayoutBlocked.addWidget(self.labelBlockedCount)

        self.labelBlockedText = QLabel(self.frameBlocked)
        self.labelBlockedText.setObjectName(u"labelBlockedText")
        self.labelBlockedText.setStyleSheet(u"    font-size: 14px;\n"
"    font-weight: 600;\n"
"	color: none;  \n"
"")
        self.labelBlockedText.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayoutBlocked.addWidget(self.labelBlockedText)


        self.horizontalLayoutInfo.addWidget(self.frameBlocked)

        self.frameAdmins = QFrame(self.infoaccountFrame)
        self.frameAdmins.setObjectName(u"frameAdmins")
        self.frameAdmins.setFrameShape(QFrame.Shape.NoFrame)
        self.verticalLayoutAdmins = QVBoxLayout(self.frameAdmins)
        self.verticalLayoutAdmins.setSpacing(0)
        self.verticalLayoutAdmins.setObjectName(u"verticalLayoutAdmins")
        self.verticalLayoutAdmins.setContentsMargins(20, 0, 0, 0)
        self.labelAdminsCount = QLabel(self.frameAdmins)
        self.labelAdminsCount.setObjectName(u"labelAdminsCount")
        self.labelAdminsCount.setFont(font6)
        self.labelAdminsCount.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayoutAdmins.addWidget(self.labelAdminsCount)

        self.labelAdminsText = QLabel(self.frameAdmins)
        self.labelAdminsText.setObjectName(u"labelAdminsText")
        self.labelAdminsText.setStyleSheet(u"    font-size: 14px;\n"
"    font-weight: 600;\n"
"	color: none;  \n"
"")
        self.labelAdminsText.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayoutAdmins.addWidget(self.labelAdminsText)


        self.horizontalLayoutInfo.addWidget(self.frameAdmins)


        self.verticalLayout_2.addWidget(self.infoaccountFrame)

        self.table_frame = QFrame(self.contentBottom)
        self.table_frame.setObjectName(u"table_frame")
        self.table_frame.setMinimumSize(QSize(1366, 596))
        self.table_frame.setMaximumSize(QSize(16777215, 16777215))
        self.table_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.table_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.table_frame)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(30, 20, 30, 20)
        self.tabeldata = QTableWidget(self.table_frame)
        if (self.tabeldata.columnCount() < 7):
            self.tabeldata.setColumnCount(7)
        font7 = QFont()
        font7.setFamilies([u"Arial"])
        font7.setPointSize(11)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setFont(font7);
        self.tabeldata.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setFont(font7);
        self.tabeldata.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        __qtablewidgetitem2.setFont(font7);
        self.tabeldata.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        __qtablewidgetitem3.setFont(font7);
        self.tabeldata.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        __qtablewidgetitem4.setFont(font7);
        self.tabeldata.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        __qtablewidgetitem5.setFont(font7);
        self.tabeldata.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        __qtablewidgetitem6.setFont(font7);
        self.tabeldata.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        self.tabeldata.setObjectName(u"tabeldata")
        self.tabeldata.setMinimumSize(QSize(0, 0))
        self.tabeldata.setMaximumSize(QSize(16777215, 16777215))
        self.tabeldata.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.tabeldata.setShowGrid(False)
        self.tabeldata.setGridStyle(Qt.PenStyle.NoPen)
        self.tabeldata.horizontalHeader().setCascadingSectionResizes(False)
        self.tabeldata.horizontalHeader().setMinimumSectionSize(50)
        self.tabeldata.horizontalHeader().setDefaultSectionSize(190)
        self.tabeldata.horizontalHeader().setStretchLastSection(True)
        self.tabeldata.verticalHeader().setVisible(False)

        self.horizontalLayout_6.addWidget(self.tabeldata)


        self.verticalLayout_2.addWidget(self.table_frame)


        self.verticalLayout.addWidget(self.contentBottom)


        self.verticalLayout_4.addWidget(self.bgApp)

        MainWindow.setCentralWidget(self.styleSheet)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.clockInfo.setText(QCoreApplication.translate("MainWindow", u"Friday, 22 August 2025 | 18:22:25", None))
        self.titleRightInfo.setText(QCoreApplication.translate("MainWindow", u"Dashboard EcoLab - Admin Editorial", None))
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
        self.labelTitle.setText(QCoreApplication.translate("MainWindow", u"User Management Desk", None))
        self.btn_back.setText(QCoreApplication.translate("MainWindow", u"Back", None))
        self.labelSubtitle.setText(QCoreApplication.translate("MainWindow", u"Review every account in one surface, confirm role changes deliberately, and use guarded actions for password and deletion flows.", None))
        self.labelAccountsCount.setText(QCoreApplication.translate("MainWindow", u"6", None))
        self.labelAccountsText.setText(QCoreApplication.translate("MainWindow", u"ACCOUNTS", None))
        self.labelPendingCount.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.labelPendingText.setText(QCoreApplication.translate("MainWindow", u"PENDING", None))
        self.labelActiveCount.setText(QCoreApplication.translate("MainWindow", u"4", None))
        self.labelActiveText.setText(QCoreApplication.translate("MainWindow", u"ACTIVE", None))
        self.labelBlockedCount.setText(QCoreApplication.translate("MainWindow", u"2", None))
        self.labelBlockedText.setText(QCoreApplication.translate("MainWindow", u"BLOCKED", None))
        self.labelAdminsCount.setText(QCoreApplication.translate("MainWindow", u"2", None))
        self.labelAdminsText.setText(QCoreApplication.translate("MainWindow", u"ADMINS", None))
        ___qtablewidgetitem = self.tabeldata.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"No", None));
        ___qtablewidgetitem1 = self.tabeldata.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Username", None));
        ___qtablewidgetitem2 = self.tabeldata.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Email", None));
        ___qtablewidgetitem3 = self.tabeldata.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Role ", None));
        ___qtablewidgetitem4 = self.tabeldata.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Status", None));
        ___qtablewidgetitem5 = self.tabeldata.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"Created", None));
        ___qtablewidgetitem6 = self.tabeldata.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"Action", None));
    # retranslateUi

