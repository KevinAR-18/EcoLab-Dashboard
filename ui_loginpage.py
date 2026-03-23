# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'loginpage.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QPushButton,
    QSizePolicy, QSpacerItem, QStackedWidget, QVBoxLayout,
    QWidget)
import resources_rc
import resources_rc
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(520, 720)
        MainWindow.setMinimumSize(QSize(520, 720))
        MainWindow.setMaximumSize(QSize(520, 720))
        self.styleSheet = QWidget(MainWindow)
        self.styleSheet.setObjectName(u"styleSheet")
        self.styleSheet.setStyleSheet(u"\n"
"\n"
"/* BACKGROUND */\n"
"\n"
"QWidget{\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"/* LOGIN CARD */\n"
"\n"
"#loginpageFrame {\n"
"    border-top: 3px solid #005C99;\n"
"\n"
"    background: qlineargradient(\n"
"        x1:0, y1:0, x2:0, y2:1,\n"
"        stop:0 #E1F2FB,\n"
"        stop:1 #F1F9F9\n"
"    );\n"
"\n"
"    background-image: url(:/images/images/images/bg5.png);\n"
"    background-repeat: no-repeat;\n"
"    background-position: top;\n"
"    border-radius:18px;\n"
"border: 1px solid #D9E9F6;\n"
"}\n"
"\n"
"/* INPUT */\n"
"\n"
"QLineEdit{\n"
"background:white;\n"
"border:1px solid #cfd8e3;\n"
"border-radius:8px;\n"
"padding:8px;\n"
"font-size:12pt;\n"
"}\n"
"\n"
"QLineEdit:focus{\n"
"border:1px solid #2b6cb0;\n"
"}\n"
"\n"
"/* BUTTON GLOBAL */\n"
"\n"
"QPushButton{\n"
"border-radius:10px;\n"
"padding:8px;\n"
"font-weight:bold;\n"
"}\n"
"\n"
"/* PRIMARY */\n"
"\n"
"#signinButton,#signupButton{\n"
"background-color:#2b6cb0;\n"
"color:white;\n"
"}\n"
"\n"
"#signinButton:hover,#signupButton:hover{\n"
"backgroun"
                        "d-color:#1e4f8a;\n"
"}\n"
"\n"
"/* GUEST */\n"
"\n"
"#guestButton{\n"
"background:#4c8ed9;\n"
"color:white;\n"
"}\n"
"\n"
"#guestButton:hover{\n"
"background:#3979c7;\n"
"}\n"
"\n"
"/* GOOGLE - IMAGE BUTTONS */\n"
"\n"
"#googleSigninButton,#googleSignupButton{\n"
"background:transparent;\n"
"border:none;\n"
"}\n"
"\n"
"#googleSigninButton:hover,#googleSignupButton:hover{\n"
"background:transparent;\n"
"opacity:0.8;\n"
"}\n"
"\n"
"/* OR LABEL */\n"
"\n"
"#orLabel{\n"
"font-size:10pt;\n"
"font-weight:bold;\n"
"color:#5b6f82;\n"
"}\n"
"\n"
"/* LINK BUTTON */\n"
"\n"
"#goto_signuppage,#goto_signinpage{\n"
"background:transparent;\n"
"color:#2b6cb0;\n"
"border:none;\n"
"font-weight:bold;\n"
"}\n"
"\n"
"#goto_signuppage:hover,#goto_signinpage:hover{\n"
"text-decoration:underline;\n"
"}\n"
"\n"
"")
        self.verticalLayout = QVBoxLayout(self.styleSheet)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(30, 30, 30, 30)
        self.loginpageFrame = QFrame(self.styleSheet)
        self.loginpageFrame.setObjectName(u"loginpageFrame")
        self.loginpageFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.loginpageFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.loginpageFrame)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.topFrame = QFrame(self.loginpageFrame)
        self.topFrame.setObjectName(u"topFrame")
        self.topFrame.setMinimumSize(QSize(0, 25))
        self.topFrame.setMaximumSize(QSize(16777215, 25))
        self.topFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.topFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.topFrame)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer = QSpacerItem(412, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.closeAppBtn = QPushButton(self.topFrame)
        self.closeAppBtn.setObjectName(u"closeAppBtn")
        self.closeAppBtn.setMinimumSize(QSize(0, 0))
        self.closeAppBtn.setMaximumSize(QSize(25, 25))
        self.closeAppBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.closeAppBtn.setStyleSheet(u"QPushButton#closeAppBtn {\n"
"    background-color: #5A8BD8;       /* biru kalem, agak gelap dari background */\n"
"    border: none;\n"
"    border-radius: 12px;             /* rounded corners */\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    font-size: 14px;\n"
"}\n"
"QPushButton#closeAppBtn:hover {\n"
"    background-color: #4672C4;       /* biru lebih gelap saat hover */\n"
"}\n"
"QPushButton#closeAppBtn:pressed {\n"
"    background-color: #3B5CA0;       /* biru lebih gelap saat ditekan */\n"
"}")
        icon = QIcon()
        icon.addFile(u":/icons/images/icons/icon_close.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.closeAppBtn.setIcon(icon)
        self.closeAppBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_3.addWidget(self.closeAppBtn)


        self.verticalLayout_2.addWidget(self.topFrame)

        self.frame = QFrame(self.loginpageFrame)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.NoFrame)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 10, 0, 10)
        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout.addWidget(self.frame_2)

        self.logoLabel = QLabel(self.frame)
        self.logoLabel.setObjectName(u"logoLabel")
        self.logoLabel.setMinimumSize(QSize(80, 80))
        self.logoLabel.setMaximumSize(QSize(60, 60))
        self.logoLabel.setPixmap(QPixmap(u":/images/images/images/logoecolabbig.png"))
        self.logoLabel.setScaledContents(True)
        self.logoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.logoLabel)

        self.frame_3 = QFrame(self.frame)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout.addWidget(self.frame_3)


        self.verticalLayout_2.addWidget(self.frame)

        self.titleLabel = QLabel(self.loginpageFrame)
        self.titleLabel.setObjectName(u"titleLabel")
        self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.titleLabel)

        self.subtitleLabel = QLabel(self.loginpageFrame)
        self.subtitleLabel.setObjectName(u"subtitleLabel")
        self.subtitleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.subtitleLabel)

        self.stackedWidget = QStackedWidget(self.loginpageFrame)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page_signin = QWidget()
        self.page_signin.setObjectName(u"page_signin")
        self.verticalLayout_3 = QVBoxLayout(self.page_signin)
        self.verticalLayout_3.setSpacing(10)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(-1, 30, -1, 30)
        self.guestButton = QPushButton(self.page_signin)
        self.guestButton.setObjectName(u"guestButton")

        self.verticalLayout_3.addWidget(self.guestButton)

        self.orLabel = QLabel(self.page_signin)
        self.orLabel.setObjectName(u"orLabel")
        self.orLabel.setMaximumSize(QSize(16777215, 20))
        self.orLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_3.addWidget(self.orLabel)

        self.emailInput = QLineEdit(self.page_signin)
        self.emailInput.setObjectName(u"emailInput")

        self.verticalLayout_3.addWidget(self.emailInput)

        self.passwordInput = QLineEdit(self.page_signin)
        self.passwordInput.setObjectName(u"passwordInput")
        self.passwordInput.setEchoMode(QLineEdit.EchoMode.Password)

        self.verticalLayout_3.addWidget(self.passwordInput)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.rememberCheck = QCheckBox(self.page_signin)
        self.rememberCheck.setObjectName(u"rememberCheck")
        self.rememberCheck.setStyleSheet(u"/* CHECKBOX TEXT */\n"
"\n"
"QCheckBox{\n"
"font-size:9pt;\n"
"color:#3c5166;\n"
"spacing:6px;\n"
"}\n"
"\n"
"/* BOX */\n"
"\n"
"QCheckBox::indicator{\n"
"width:16px;\n"
"height:16px;\n"
"border-radius:4px;\n"
"border:1px solid #9fb3c8;\n"
"background:white;\n"
"}\n"
"\n"
"/* HOVER */\n"
"\n"
"QCheckBox::indicator:hover{\n"
"border:1px solid #2b6cb0;\n"
"}\n"
"\n"
"/* CHECKED */\n"
"\n"
"QCheckBox::indicator:checked{\n"
"background-color:#2b6cb0;\n"
"border:1px solid #2b6cb0;\n"
"}\n"
"\n"
"/* DISABLED */\n"
"\n"
"QCheckBox::indicator:disabled{\n"
"background:#e5e9ef;\n"
"border:1px solid #cfd8e3;\n"
"}")

        self.horizontalLayout_2.addWidget(self.rememberCheck)

        self.showpasssigninCheck = QCheckBox(self.page_signin)
        self.showpasssigninCheck.setObjectName(u"showpasssigninCheck")
        self.showpasssigninCheck.setStyleSheet(u"/* CHECKBOX TEXT */\n"
"\n"
"QCheckBox{\n"
"font-size:9pt;\n"
"color:#3c5166;\n"
"spacing:6px;\n"
"}\n"
"\n"
"/* BOX */\n"
"\n"
"QCheckBox::indicator{\n"
"width:16px;\n"
"height:16px;\n"
"border-radius:4px;\n"
"border:1px solid #9fb3c8;\n"
"background:white;\n"
"}\n"
"\n"
"/* HOVER */\n"
"\n"
"QCheckBox::indicator:hover{\n"
"border:1px solid #2b6cb0;\n"
"}\n"
"\n"
"/* CHECKED */\n"
"\n"
"QCheckBox::indicator:checked{\n"
"background-color:#2b6cb0;\n"
"border:1px solid #2b6cb0;\n"
"}\n"
"\n"
"/* DISABLED */\n"
"\n"
"QCheckBox::indicator:disabled{\n"
"background:#e5e9ef;\n"
"border:1px solid #cfd8e3;\n"
"}")

        self.horizontalLayout_2.addWidget(self.showpasssigninCheck)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.signinButton = QPushButton(self.page_signin)
        self.signinButton.setObjectName(u"signinButton")

        self.verticalLayout_3.addWidget(self.signinButton)

        self.googleSigninButton = QPushButton(self.page_signin)
        self.googleSigninButton.setObjectName(u"googleSigninButton")
        self.googleSigninButton.setMinimumSize(QSize(0, 35))
        self.googleSigninButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon1 = QIcon()
        icon1.addFile(u":/images/images/images/signin.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.googleSigninButton.setIcon(icon1)
        self.googleSigninButton.setIconSize(QSize(300, 35))

        self.verticalLayout_3.addWidget(self.googleSigninButton)

        self.donthaveLabel = QLabel(self.page_signin)
        self.donthaveLabel.setObjectName(u"donthaveLabel")
        self.donthaveLabel.setMaximumSize(QSize(16777215, 20))
        self.donthaveLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_3.addWidget(self.donthaveLabel)

        self.goto_signuppage = QPushButton(self.page_signin)
        self.goto_signuppage.setObjectName(u"goto_signuppage")

        self.verticalLayout_3.addWidget(self.goto_signuppage)

        self.stackedWidget.addWidget(self.page_signin)
        self.page_signup = QWidget()
        self.page_signup.setObjectName(u"page_signup")
        self.verticalLayout_4 = QVBoxLayout(self.page_signup)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.usernameInput = QLineEdit(self.page_signup)
        self.usernameInput.setObjectName(u"usernameInput")

        self.verticalLayout_4.addWidget(self.usernameInput)

        self.signupEmailInput = QLineEdit(self.page_signup)
        self.signupEmailInput.setObjectName(u"signupEmailInput")

        self.verticalLayout_4.addWidget(self.signupEmailInput)

        self.signupPasswordInput = QLineEdit(self.page_signup)
        self.signupPasswordInput.setObjectName(u"signupPasswordInput")
        self.signupPasswordInput.setEchoMode(QLineEdit.EchoMode.Password)

        self.verticalLayout_4.addWidget(self.signupPasswordInput)

        self.showpasssignupCheck = QCheckBox(self.page_signup)
        self.showpasssignupCheck.setObjectName(u"showpasssignupCheck")
        self.showpasssignupCheck.setStyleSheet(u"/* CHECKBOX TEXT */\n"
"\n"
"QCheckBox{\n"
"font-size:9pt;\n"
"color:#3c5166;\n"
"spacing:6px;\n"
"}\n"
"\n"
"/* BOX */\n"
"\n"
"QCheckBox::indicator{\n"
"width:16px;\n"
"height:16px;\n"
"border-radius:4px;\n"
"border:1px solid #9fb3c8;\n"
"background:white;\n"
"}\n"
"\n"
"/* HOVER */\n"
"\n"
"QCheckBox::indicator:hover{\n"
"border:1px solid #2b6cb0;\n"
"}\n"
"\n"
"/* CHECKED */\n"
"\n"
"QCheckBox::indicator:checked{\n"
"background-color:#2b6cb0;\n"
"border:1px solid #2b6cb0;\n"
"}\n"
"\n"
"/* DISABLED */\n"
"\n"
"QCheckBox::indicator:disabled{\n"
"background:#e5e9ef;\n"
"border:1px solid #cfd8e3;\n"
"}")

        self.verticalLayout_4.addWidget(self.showpasssignupCheck)

        self.signupButton = QPushButton(self.page_signup)
        self.signupButton.setObjectName(u"signupButton")

        self.verticalLayout_4.addWidget(self.signupButton)

        self.googleSignupButton = QPushButton(self.page_signup)
        self.googleSignupButton.setObjectName(u"googleSignupButton")
        self.googleSignupButton.setMinimumSize(QSize(0, 35))
        self.googleSignupButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon2 = QIcon()
        icon2.addFile(u":/images/images/images/signup.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.googleSignupButton.setIcon(icon2)
        self.googleSignupButton.setIconSize(QSize(300, 35))

        self.verticalLayout_4.addWidget(self.googleSignupButton)

        self.goto_signinpage = QPushButton(self.page_signup)
        self.goto_signinpage.setObjectName(u"goto_signinpage")

        self.verticalLayout_4.addWidget(self.goto_signinpage)

        self.stackedWidget.addWidget(self.page_signup)

        self.verticalLayout_2.addWidget(self.stackedWidget)


        self.verticalLayout.addWidget(self.loginpageFrame)

        MainWindow.setCentralWidget(self.styleSheet)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"EcoLab Login", None))
#if QT_CONFIG(tooltip)
        self.closeAppBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Close", None))
#endif // QT_CONFIG(tooltip)
        self.closeAppBtn.setText("")
        self.titleLabel.setStyleSheet(QCoreApplication.translate("MainWindow", u"\n"
"font-size:18pt;\n"
"font-weight:bold;\n"
"color:#1f3c5a;\n"
"", None))
        self.titleLabel.setText(QCoreApplication.translate("MainWindow", u"Welcome to EcoLab Dashboard", None))
        self.subtitleLabel.setStyleSheet(QCoreApplication.translate("MainWindow", u"\n"
"font-size:11pt;\n"
"color:#4a647d;\n"
"", None))
        self.subtitleLabel.setText(QCoreApplication.translate("MainWindow", u"Energy Monitoring and Control System", None))
        self.guestButton.setText(QCoreApplication.translate("MainWindow", u"Continue as Guest", None))
        self.orLabel.setText(QCoreApplication.translate("MainWindow", u"OR SIGN IN", None))
        self.emailInput.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Email", None))
        self.passwordInput.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Password", None))
        self.rememberCheck.setText(QCoreApplication.translate("MainWindow", u"Remember me", None))
        self.showpasssigninCheck.setText(QCoreApplication.translate("MainWindow", u"Show Password", None))
        self.signinButton.setText(QCoreApplication.translate("MainWindow", u"Sign In", None))
        self.googleSigninButton.setText("")
        self.donthaveLabel.setText(QCoreApplication.translate("MainWindow", u"Don't have an account?", None))
        self.goto_signuppage.setText(QCoreApplication.translate("MainWindow", u"Create Account", None))
        self.usernameInput.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Username", None))
        self.signupEmailInput.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Email", None))
        self.signupPasswordInput.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Password", None))
        self.showpasssignupCheck.setText(QCoreApplication.translate("MainWindow", u"Show Password", None))
        self.signupButton.setText(QCoreApplication.translate("MainWindow", u"Create Account", None))
        self.googleSignupButton.setText("")
        self.goto_signinpage.setText(QCoreApplication.translate("MainWindow", u"Back to Sign In", None))
    # retranslateUi

