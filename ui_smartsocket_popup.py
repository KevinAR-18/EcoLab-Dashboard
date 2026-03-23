# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'smartsocket_popup.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFrame,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)
import resources_rc

class Ui_SmartSocketPopup(object):
    def setupUi(self, SmartSocketPopup):
        if not SmartSocketPopup.objectName():
            SmartSocketPopup.setObjectName(u"SmartSocketPopup")
        SmartSocketPopup.resize(550, 650)
        SmartSocketPopup.setMinimumSize(QSize(550, 650))
        SmartSocketPopup.setMaximumSize(QSize(550, 650))
        SmartSocketPopup.setStyleSheet(u"#SmartSocketPopup{\n"
"    background: qlineargradient(\n"
"        x1:0, y1:0, x2:0, y2:1,\n"
"        stop:0 #E1F2FB,\n"
"        stop:1 #F1F9F9\n"
"    );\n"
"border: 1px solid #B0D6E8;    /* border ungu/soft biru sesuai gradient */\n"
"    border-radius: 10px;       \n"
"}")
        SmartSocketPopup.setModal(True)
        self.verticalLayout = QVBoxLayout(SmartSocketPopup)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.topFrame = QFrame(SmartSocketPopup)
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

        self.btn_close = QPushButton(self.topFrame)
        self.btn_close.setObjectName(u"btn_close")
        self.btn_close.setMinimumSize(QSize(0, 0))
        self.btn_close.setMaximumSize(QSize(25, 25))
        self.btn_close.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_close.setStyleSheet(u"QPushButton#btn_close{\n"
"    background-color: #5A8BD8;       /* biru kalem, agak gelap dari background */\n"
"    border: none;\n"
"    border-radius: 12px;             /* rounded corners */\n"
"    color: white;\n"
"    font-weight: bold;\n"
"    font-size: 14px;\n"
"}\n"
"QPushButton#btn_close:hover {\n"
"    background-color: #4672C4;       /* biru lebih gelap saat hover */\n"
"}\n"
"QPushButton#btn_close:pressed {\n"
"    background-color: #3B5CA0;       /* biru lebih gelap saat ditekan */\n"
"}")
        icon = QIcon()
        icon.addFile(u":/icons/images/icons/icon_close.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_close.setIcon(icon)
        self.btn_close.setIconSize(QSize(20, 20))

        self.horizontalLayout_3.addWidget(self.btn_close)


        self.verticalLayout.addWidget(self.topFrame)

        self.frame = QFrame(SmartSocketPopup)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.NoFrame)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout.addWidget(self.frame_2)

        self.label_title = QLabel(self.frame)
        self.label_title.setObjectName(u"label_title")
        self.label_title.setMinimumSize(QSize(400, 55))
        self.label_title.setMaximumSize(QSize(400, 60))
        self.label_title.setStyleSheet(u"#label_title{\n"
"    font: bold 18pt \"Segoe UI\";\n"
"    color: white;\n"
"    background-color: #005C99;\n"
"    border-radius: 8px;\n"
"    padding: 10px;\n"
"    border: 1px solid #005C99;\n"
"    qproperty-alignment: AlignCenter;\n"
"}")

        self.horizontalLayout.addWidget(self.label_title)

        self.frame_3 = QFrame(self.frame)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout.addWidget(self.frame_3)


        self.verticalLayout.addWidget(self.frame)

        self.groupBox_timer = QGroupBox(SmartSocketPopup)
        self.groupBox_timer.setObjectName(u"groupBox_timer")
        self.groupBox_timer.setStyleSheet(u"QGroupBox{\n"
"    font: bold 11pt \"Segoe UI\";\n"
"    border: 2px solid #005C99;\n"
"    border-radius: 10px;\n"
"    margin-top: 10px;\n"
"    padding-top: 15px;\n"
"}")
        self.verticalLayout_timer = QVBoxLayout(self.groupBox_timer)
        self.verticalLayout_timer.setObjectName(u"verticalLayout_timer")
        self.horizontalLayout_timer_input = QHBoxLayout()
        self.horizontalLayout_timer_input.setObjectName(u"horizontalLayout_timer_input")
        self.label_timer_duration = QLabel(self.groupBox_timer)
        self.label_timer_duration.setObjectName(u"label_timer_duration")

        self.horizontalLayout_timer_input.addWidget(self.label_timer_duration)

        self.input_timer_duration = QLineEdit(self.groupBox_timer)
        self.input_timer_duration.setObjectName(u"input_timer_duration")

        self.horizontalLayout_timer_input.addWidget(self.input_timer_duration)


        self.verticalLayout_timer.addLayout(self.horizontalLayout_timer_input)

        self.horizontalLayout_timer_buttons = QHBoxLayout()
        self.horizontalLayout_timer_buttons.setObjectName(u"horizontalLayout_timer_buttons")
        self.horizontalSpacer_timer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_timer_buttons.addItem(self.horizontalSpacer_timer)

        self.btn_start_timer = QPushButton(self.groupBox_timer)
        self.btn_start_timer.setObjectName(u"btn_start_timer")
        self.btn_start_timer.setMinimumSize(QSize(120, 35))
        self.btn_start_timer.setStyleSheet(u"QPushButton#btn_start_timer{\n"
"    background-color: #005C99;\n"
"    color: white;\n"
"    border: none;\n"
"    border-radius: 6px;\n"
"    padding: 8px 16px;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QPushButton#btn_start_timer:hover {\n"
"    background-color: #004A7A;\n"
"}")

        self.horizontalLayout_timer_buttons.addWidget(self.btn_start_timer)

        self.btn_cancel_timer = QPushButton(self.groupBox_timer)
        self.btn_cancel_timer.setObjectName(u"btn_cancel_timer")
        self.btn_cancel_timer.setMinimumSize(QSize(120, 35))
        self.btn_cancel_timer.setStyleSheet(u"QPushButton#btn_cancel_timer{\n"
"    background-color: #EB5757;\n"
"    color: white;\n"
"    border: none;\n"
"    border-radius: 6px;\n"
"    padding: 8px 16px;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QPushButton#btn_cancel_timer:hover {\n"
"    background-color: #c0392B;\n"
"}")

        self.horizontalLayout_timer_buttons.addWidget(self.btn_cancel_timer)


        self.verticalLayout_timer.addLayout(self.horizontalLayout_timer_buttons)

        self.label_timer_status = QLabel(self.groupBox_timer)
        self.label_timer_status.setObjectName(u"label_timer_status")
        self.label_timer_status.setStyleSheet(u"QLabel#label_timer_status{\n"
"    color: gray;\n"
"    font-weight: bold;\n"
"    qproperty-alignment: AlignCenter;\n"
"}")

        self.verticalLayout_timer.addWidget(self.label_timer_status)


        self.verticalLayout.addWidget(self.groupBox_timer)

        self.groupBox_schedule = QGroupBox(SmartSocketPopup)
        self.groupBox_schedule.setObjectName(u"groupBox_schedule")
        self.groupBox_schedule.setStyleSheet(u"QGroupBox{\n"
"    font: bold 11pt \"Segoe UI\";\n"
"    border: 2px solid #005C99;\n"
"    border-radius: 10px;\n"
"    margin-top: 10px;\n"
"    padding-top: 15px;\n"
"}")
        self.verticalLayout_schedule = QVBoxLayout(self.groupBox_schedule)
        self.verticalLayout_schedule.setObjectName(u"verticalLayout_schedule")
        self.horizontalLayout_mode = QHBoxLayout()
        self.horizontalLayout_mode.setObjectName(u"horizontalLayout_mode")
        self.label_mode = QLabel(self.groupBox_schedule)
        self.label_mode.setObjectName(u"label_mode")

        self.horizontalLayout_mode.addWidget(self.label_mode)

        self.combo_schedule_mode = QComboBox(self.groupBox_schedule)
        self.combo_schedule_mode.addItem("")
        self.combo_schedule_mode.addItem("")
        self.combo_schedule_mode.setObjectName(u"combo_schedule_mode")
        self.combo_schedule_mode.setStyleSheet(u"QComboBox{\n"
"    padding: 5px;\n"
"    border-radius: 3px;\n"
"}")

        self.horizontalLayout_mode.addWidget(self.combo_schedule_mode)


        self.verticalLayout_schedule.addLayout(self.horizontalLayout_mode)

        self.horizontalLayout_start = QHBoxLayout()
        self.horizontalLayout_start.setObjectName(u"horizontalLayout_start")
        self.label_start = QLabel(self.groupBox_schedule)
        self.label_start.setObjectName(u"label_start")

        self.horizontalLayout_start.addWidget(self.label_start)

        self.input_schedule_start = QLineEdit(self.groupBox_schedule)
        self.input_schedule_start.setObjectName(u"input_schedule_start")

        self.horizontalLayout_start.addWidget(self.input_schedule_start)


        self.verticalLayout_schedule.addLayout(self.horizontalLayout_start)

        self.horizontalLayout_stop = QHBoxLayout()
        self.horizontalLayout_stop.setObjectName(u"horizontalLayout_stop")
        self.label_stop = QLabel(self.groupBox_schedule)
        self.label_stop.setObjectName(u"label_stop")

        self.horizontalLayout_stop.addWidget(self.label_stop)

        self.input_schedule_stop = QLineEdit(self.groupBox_schedule)
        self.input_schedule_stop.setObjectName(u"input_schedule_stop")

        self.horizontalLayout_stop.addWidget(self.input_schedule_stop)


        self.verticalLayout_schedule.addLayout(self.horizontalLayout_stop)

        self.horizontalLayout_schedule_buttons = QHBoxLayout()
        self.horizontalLayout_schedule_buttons.setObjectName(u"horizontalLayout_schedule_buttons")
        self.horizontalSpacer_schedule = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_schedule_buttons.addItem(self.horizontalSpacer_schedule)

        self.btn_set_schedule = QPushButton(self.groupBox_schedule)
        self.btn_set_schedule.setObjectName(u"btn_set_schedule")
        self.btn_set_schedule.setMinimumSize(QSize(120, 35))
        self.btn_set_schedule.setStyleSheet(u"QPushButton#btn_set_schedule{\n"
"    background-color: #FF9800;\n"
"    color: white;\n"
"    border: none;\n"
"    border-radius: 6px;\n"
"    padding: 8px 16px;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QPushButton#btn_set_schedule:hover {\n"
"    background-color: #e68900;\n"
"}")

        self.horizontalLayout_schedule_buttons.addWidget(self.btn_set_schedule)

        self.btn_clear_schedule = QPushButton(self.groupBox_schedule)
        self.btn_clear_schedule.setObjectName(u"btn_clear_schedule")
        self.btn_clear_schedule.setMinimumSize(QSize(120, 35))
        self.btn_clear_schedule.setStyleSheet(u"QPushButton#btn_clear_schedule{\n"
"    background-color: #EB5757;\n"
"    color: white;\n"
"    border: none;\n"
"    border-radius: 6px;\n"
"    padding: 8px 16px;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QPushButton#btn_clear_schedule:hover {\n"
"    background-color: #c0392B;\n"
"}")

        self.horizontalLayout_schedule_buttons.addWidget(self.btn_clear_schedule)


        self.verticalLayout_schedule.addLayout(self.horizontalLayout_schedule_buttons)

        self.label_schedule_status = QLabel(self.groupBox_schedule)
        self.label_schedule_status.setObjectName(u"label_schedule_status")
        self.label_schedule_status.setStyleSheet(u"QLabel#label_schedule_status{\n"
"    color: gray;\n"
"    font-weight: bold;\n"
"}")
        self.label_schedule_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_schedule_status.setWordWrap(True)

        self.verticalLayout_schedule.addWidget(self.label_schedule_status)


        self.verticalLayout.addWidget(self.groupBox_schedule)

        self.groupbox_datetime = QGroupBox(SmartSocketPopup)
        self.groupbox_datetime.setObjectName(u"groupbox_datetime")
        self.groupbox_datetime.setStyleSheet(u"QGroupBox{\n"
"    font: bold 11pt \"Segoe UI\";\n"
"    border: 2px solid #005C99;\n"
"    border-radius: 10px;\n"
"    margin-top: 10px;\n"
"    padding-top: 15px;\n"
"}")
        self.verticalLayout_datetime = QVBoxLayout(self.groupbox_datetime)
        self.verticalLayout_datetime.setObjectName(u"verticalLayout_datetime")
        self.label_datetime_status = QLabel(self.groupbox_datetime)
        self.label_datetime_status.setObjectName(u"label_datetime_status")
        self.label_datetime_status.setStyleSheet(u"QLabel#label_datetime_status{\n"
"    color: green;\n"
"    font-size: 10pt;\n"
"}")
        self.label_datetime_status.setWordWrap(True)

        self.verticalLayout_datetime.addWidget(self.label_datetime_status)

        self.label_datetime_info = QLabel(self.groupbox_datetime)
        self.label_datetime_info.setObjectName(u"label_datetime_info")
        self.label_datetime_info.setStyleSheet(u"QLabel#label_datetime_info{\n"
"    color: blue;\n"
"    font-size: 9pt;\n"
"    font-style: italic;\n"
"    qproperty-alignment: AlignCenter;\n"
"}")

        self.verticalLayout_datetime.addWidget(self.label_datetime_info)


        self.verticalLayout.addWidget(self.groupbox_datetime)


        self.retranslateUi(SmartSocketPopup)

        QMetaObject.connectSlotsByName(SmartSocketPopup)
    # setupUi

    def retranslateUi(self, SmartSocketPopup):
        SmartSocketPopup.setWindowTitle(QCoreApplication.translate("SmartSocketPopup", u"Smart Socket Control", None))
#if QT_CONFIG(tooltip)
        self.btn_close.setToolTip(QCoreApplication.translate("SmartSocketPopup", u"Close", None))
#endif // QT_CONFIG(tooltip)
        self.btn_close.setText("")
        self.label_title.setText(QCoreApplication.translate("SmartSocketPopup", u"\u26a1 Smart Socket # Control", None))
        self.groupBox_timer.setTitle(QCoreApplication.translate("SmartSocketPopup", u"\u23f1\ufe0f Timer", None))
        self.label_timer_duration.setText(QCoreApplication.translate("SmartSocketPopup", u"Duration (seconds):", None))
        self.input_timer_duration.setPlaceholderText(QCoreApplication.translate("SmartSocketPopup", u"60", None))
        self.btn_start_timer.setText(QCoreApplication.translate("SmartSocketPopup", u"Start Timer", None))
        self.btn_cancel_timer.setText(QCoreApplication.translate("SmartSocketPopup", u"Cancel Timer", None))
        self.label_timer_status.setText(QCoreApplication.translate("SmartSocketPopup", u"Status: INACTIVE", None))
        self.groupBox_schedule.setTitle(QCoreApplication.translate("SmartSocketPopup", u"\U0001f4c5 Schedule", None))
        self.label_mode.setText(QCoreApplication.translate("SmartSocketPopup", u"Mode:", None))
        self.combo_schedule_mode.setItemText(0, QCoreApplication.translate("SmartSocketPopup", u"Daily", None))
        self.combo_schedule_mode.setItemText(1, QCoreApplication.translate("SmartSocketPopup", u"Onetime", None))

        self.label_start.setText(QCoreApplication.translate("SmartSocketPopup", u"Start Time (ON):", None))
        self.input_schedule_start.setPlaceholderText(QCoreApplication.translate("SmartSocketPopup", u"08:00", None))
        self.label_stop.setText(QCoreApplication.translate("SmartSocketPopup", u"Stop Time (OFF):", None))
        self.input_schedule_stop.setPlaceholderText(QCoreApplication.translate("SmartSocketPopup", u"17:00", None))
        self.btn_set_schedule.setText(QCoreApplication.translate("SmartSocketPopup", u"Set Schedule", None))
        self.btn_clear_schedule.setText(QCoreApplication.translate("SmartSocketPopup", u"Clear Schedule", None))
        self.label_schedule_status.setText(QCoreApplication.translate("SmartSocketPopup", u"Status: Not Set", None))
        self.groupbox_datetime.setTitle(QCoreApplication.translate("SmartSocketPopup", u"\U0001f550 RTC DateTime (NTP Sync)", None))
        self.label_datetime_status.setText(QCoreApplication.translate("SmartSocketPopup", u"\U0001f7e2 RTC: Syncing from NTP...", None))
        self.label_datetime_info.setText(QCoreApplication.translate("SmartSocketPopup", u"\u2139\ufe0f RTC auto-synced from NTP time server", None))
    # retranslateUi

