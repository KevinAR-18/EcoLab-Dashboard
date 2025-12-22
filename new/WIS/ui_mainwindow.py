# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindowXGeIve.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
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
from PySide6.QtWidgets import (QApplication, QDateEdit, QFrame, QGridLayout,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)
import images_rc, os

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
            
            
        font_paths = [
            "font\\ARIAL.TTF",
            "font\\MONDAPICK.TTF"
        ]
        
        absolute_font_paths = [self.resource_path(font) for font in font_paths]
        # Muat semua font
        self.font_families = self.load_custom_fonts(absolute_font_paths)
        
            
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1366, 768)
        MainWindow.setMinimumSize(QSize(1366, 768))
        MainWindow.setMaximumSize(QSize(1920, 1080))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setMinimumSize(QSize(1366, 768))
        self.centralwidget.setMaximumSize(QSize(1920, 1080))
        self.centralwidget.setStyleSheet(u"#frame_info_sensor {\n"
"    background-color: white;\n"
" 	border-radius: 5px;\n"
"}\n"
"\n"
"#frame_input{\n"
"	background-color: white;\n"
"	border-radius: 10px;\n"
"}\n"
"\n"
"QTableWidget {\n"
"    background-color: rgb(255, 255, 255); \n"
"    alternate-background-color: rgba(230, 250, 245, 1); \n"
"    color: rgb(0, 0, 0);\n"
"    font-size: 13px; \n"
"    border: 1px solid rgb(0, 103, 95); /* Garis border tabel hitam */\n"
"    gridline-color: rgb(0, 0, 0); /* Garis antar sel hitam */\n"
"    gridline-width: 1px; /* Menambah ketebalan garis antar sel */\n"
"    selection-background-color: rgba(2, 144, 133, 0.2);\n"
"    selection-color: rgb(0, 0, 0); \n"
"    border-radius: 5px; /* Membuat sudut tabel bulat */\n"
"    padding: 5px; /* Memberi jarak isi dengan tepi */\n"
"}\n"
"\n"
"QHeaderView::section {\n"
"    background-color: rgb(230, 230, 230); /* Latar belakang abu-abu muda untuk header */\n"
"    color: rgb(0, 0, 0"
                        "); /* Warna teks hitam */\n"
"    font-weight: bold; /* Membuat teks menjadi bold */\n"
"    font-size: 13px; /* Ukuran font header 13px */\n"
"    \n"
"    padding: 4px; /* Padding untuk header */\n"
"    border-radius: 1px; /* Membuat sudut header sedikit bulat */\n"
"    text-align: center; /* Teks di header rata tengah */\n"
"}\n"
"\n"
"QTableWidget::Item{\n"
"	border-bottom:1px solid rgb(0,60, 55);\n"
"	color:#000;\n"
"	padding-left:3px;\n"
"}\n"
"\n"
"QTableWidget QScrollBar:vertical {\n"
"    background: rgb(255, 255, 255); /* Latar belakang scrollbar tetap putih */\n"
"    width: 12px;\n"
"    margin: 3px;\n"
"}\n"
"\n"
"QTableWidget QScrollBar::handle:vertical {\n"
"    background: rgb(0, 0, 0); /* Warna handle scrollbar hitam */\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QTableWidget QScrollBar::handle:vertical:hover {\n"
"    background: rgb(0, 0, 0); /* Warna handle scrollbar saat hover */\n"
"}\n"
"")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.drop_shadow_frame = QFrame(self.centralwidget)
        self.drop_shadow_frame.setObjectName(u"drop_shadow_frame")
        self.drop_shadow_frame.setMinimumSize(QSize(1366, 768))
        self.drop_shadow_frame.setMaximumSize(QSize(1920, 1080))
        self.drop_shadow_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.drop_shadow_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.drop_shadow_frame.setStyleSheet("background-color: rgb(206, 225, 223);")
        self.drop_shadow_layout = QVBoxLayout(self.drop_shadow_frame)
        self.drop_shadow_layout.setSpacing(0)
        self.drop_shadow_layout.setObjectName(u"drop_shadow_layout")
        self.drop_shadow_layout.setContentsMargins(0, 0, 0, 0)
        self.top_bar_frame = QFrame(self.drop_shadow_frame)
        self.top_bar_frame.setObjectName(u"top_bar_frame")
        self.top_bar_frame.setMinimumSize(QSize(1366, 30))
        self.top_bar_frame.setMaximumSize(QSize(16777215, 35))
        self.top_bar_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.top_bar_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.top_bar_frame)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(5, 0, 0, 0)
        self.frame_date = QFrame(self.top_bar_frame)
        self.frame_date.setObjectName(u"frame_date")
        self.frame_date.setMinimumSize(QSize(0, 35))
        self.frame_date.setMaximumSize(QSize(230, 35))
        self.frame_date.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_date.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_date)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.date_label = QLabel(self.frame_date)
        self.date_label.setObjectName(u"date_label")
        self.date_label.setMinimumSize(QSize(2120, 25))
        font = QFont(self.font_families[1],12) #Mondapick
        # font = QFont()
        # font.setFamilies([u"Mondapick"])
        # font.setPointSize(12)
        self.date_label.setFont(font)
        self.date_label.setStyleSheet(u"color: rgb(2, 144, 133);\n"
"")
        self.date_label.setFrameShape(QFrame.Shape.NoFrame)

        self.verticalLayout_3.addWidget(self.date_label)


        self.horizontalLayout_3.addWidget(self.frame_date)

        self.hspacer1 = QSpacerItem(300, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.hspacer1)

        self.frame_title = QFrame(self.top_bar_frame)
        self.frame_title.setObjectName(u"frame_title")
        self.frame_title.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_title.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_title)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.smart_title = QLabel(self.frame_title)
        self.smart_title.setObjectName(u"smart_title")
        self.smart_title.setMinimumSize(QSize(80, 25))
        # font1 = QFont()
        # font1.setFamilies([u"Mondapick"])
        # font1.setPointSize(14)
        font1 = QFont(self.font_families[1],14) #Mondapick
        font1.setBold(False)
        font1.setItalic(False)
        font1.setStrikeOut(False)
        font1.setKerning(True)
        self.smart_title.setFont(font1)
        self.smart_title.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.smart_title.setStyleSheet(u"color: rgb(2, 144, 133);\n"
"")
        self.smart_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.smart_title)


        self.horizontalLayout_3.addWidget(self.frame_title)

        self.hspacer2 = QSpacerItem(400, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.hspacer2)

        self.frame_btn_control = QFrame(self.top_bar_frame)
        self.frame_btn_control.setObjectName(u"frame_btn_control")
        self.frame_btn_control.setMaximumSize(QSize(140, 16777215))
        self.frame_btn_control.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_btn_control.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_btn_control)
        self.horizontalLayout_2.setSpacing(10)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.btn_minimize = QPushButton(self.frame_btn_control)
        self.btn_minimize.setObjectName(u"btn_minimize")
        self.btn_minimize.setMinimumSize(QSize(17, 17))
        self.btn_minimize.setMaximumSize(QSize(18, 18))
        self.btn_minimize.setStyleSheet(u"QPushButton{\n"
"	background-color: rgb(255, 189, 68);\n"
"	border-radius:8px;\n"
"	border:none;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	background-color: rgba(254, 189, 68, 150);\n"
"}\n"
"\n"
"QToolTip{\n"
"	background-color: rgb(254, 189, 68);\n"
"	color: rgb(255, 255, 255);\n"
"	border:none;\n"
"	border-radius:2px;\n"
"}")

        self.horizontalLayout_2.addWidget(self.btn_minimize)

        self.btn_maximize = QPushButton(self.frame_btn_control)
        self.btn_maximize.setObjectName(u"btn_maximize")
        self.btn_maximize.setMinimumSize(QSize(17, 17))
        self.btn_maximize.setMaximumSize(QSize(18, 18))
        self.btn_maximize.setStyleSheet(u"QPushButton{\n"
"	background-color: rgb(0, 202, 78);\n"
"	border-radius:8px;\n"
"	border:none;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	background-color: rgba(0, 202, 78, 150);\n"
"}\n"
"\n"
"QToolTip{\n"
"	background-color: rgb(0, 202, 78);\n"
"	color: rgb(255, 255, 255);\n"
"	border:none;\n"
"	border-radius:2px;\n"
"}")

        self.horizontalLayout_2.addWidget(self.btn_maximize)

        self.btn_close = QPushButton(self.frame_btn_control)
        self.btn_close.setObjectName(u"btn_close")
        self.btn_close.setMinimumSize(QSize(17, 17))
        self.btn_close.setMaximumSize(QSize(18, 18))
        self.btn_close.setStyleSheet(u"QPushButton{\n"
"	background-color: rgb(255, 96, 92);\n"
"\n"
"	border-radius:8px;\n"
"	border:none;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	background-color: rgba(255, 96, 92, 150)\n"
"}\n"
"\n"
"QToolTip{\n"
"	background-color: rgb(255, 96, 92);\n"
"	color: rgb(255, 255, 255);\n"
"	border:none;\n"
"	border-radius:2px;\n"
"}\n"
"")

        self.horizontalLayout_2.addWidget(self.btn_close)


        self.horizontalLayout_3.addWidget(self.frame_btn_control)


        self.drop_shadow_layout.addWidget(self.top_bar_frame)

        self.title_bar_frame = QFrame(self.drop_shadow_frame)
        self.title_bar_frame.setObjectName(u"title_bar_frame")
        self.title_bar_frame.setMinimumSize(QSize(1336, 100))
        self.title_bar_frame.setMaximumSize(QSize(16777215, 100))
        self.title_bar_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.title_bar_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.title_bar_frame)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(35, 0, 35, 0)
        self.btn_info = QPushButton(self.title_bar_frame)
        self.btn_info.setObjectName(u"btn_info")
        self.btn_info.setMinimumSize(QSize(85, 85))
        self.btn_info.setMaximumSize(QSize(85, 85))
        self.btn_info.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    border-radius: 12px;\n"
"    background-color: rgb(2, 144, 133);\n"
"    background-image: url(':/images/button_1.png');\n"
"    background-repeat: no-repeat;\n"
"    background-position: center;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(2, 144, 133, 150);\n"
"    background-image: url(':/images/button_1_hover.png');\n"
"}\n"
"")

        self.horizontalLayout_4.addWidget(self.btn_info)

        self.horizontalSpacer = QSpacerItem(106, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.titile_label = QLabel(self.title_bar_frame)
        self.titile_label.setObjectName(u"titile_label")
        font2 = QFont(self.font_families[0],44) #Arial
        # font2.setFamilies([u"Arial"])
        # font2.setPointSize(44)
        font2.setBold(True)
        self.titile_label.setFont(font2)
        self.titile_label.setStyleSheet(u"QLabel {\n"
"    background-color: rgb(2, 144, 133);\n"
"    color: white;  /* Warna teks */\n"
"    padding-left: 10px;  /* Padding kiri */\n"
"    padding-right: 10px;  /* Padding kanan */\n"
"    border-radius: 10px;  /* Membuat sudut bulat */\n"
"\n"
"    max-height: 85px;  /* Tinggi maksimum background */\n"
"  	max-width: 2000px;\n"
"	min-width: 900px;\n"
"}\n"
"")
        self.titile_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_4.addWidget(self.titile_label)

        self.horizontalSpacer_2 = QSpacerItem(106, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_2)

        self.framedoang = QFrame(self.title_bar_frame)
        self.framedoang.setObjectName(u"framedoang")
        self.framedoang.setMinimumSize(QSize(85, 85))
        self.framedoang.setMaximumSize(QSize(85, 85))
        self.framedoang.setFrameShape(QFrame.Shape.StyledPanel)
        self.framedoang.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_4.addWidget(self.framedoang)


        self.drop_shadow_layout.addWidget(self.title_bar_frame)

        self.content_bar_frame = QFrame(self.drop_shadow_frame)
        self.content_bar_frame.setObjectName(u"content_bar_frame")
        self.content_bar_frame.setMinimumSize(QSize(1366, 2))
        self.content_bar_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.content_bar_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.content_bar_frame)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.function_frame = QFrame(self.content_bar_frame)
        self.function_frame.setObjectName(u"function_frame")
        self.function_frame.setMinimumSize(QSize(1366, 190))
        self.function_frame.setMaximumSize(QSize(16777215, 266))
        self.function_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.function_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.function_frame)
        self.horizontalLayout_5.setSpacing(30)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(50, 10, 50, 10)
        self.frame_info = QFrame(self.function_frame)
        self.frame_info.setObjectName(u"frame_info")
        self.frame_info.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_info.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frame_info)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.status_label_barang = QLabel(self.frame_info)
        self.status_label_barang.setObjectName(u"status_label_barang")
        font3 = QFont(self.font_families[0],22) #Arial
        # font3.setFamilies([u"Arial"])
        # font3.setPointSize(22)
        font3.setBold(True)
        self.status_label_barang.setFont(font3)
        self.status_label_barang.setStyleSheet(u"QLabel {\n"
"    background-color: rgb(71, 183, 92); /* Warna background baru */\n"
"    color: white;  /* Warna teks */\n"
"    padding: 2px;  /* Padding untuk memberi jarak antara teks dan border */\n"
"    border-radius: 5px;  /* Membuat sudut bulat\n"
"}")
        self.status_label_barang.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_6.addWidget(self.status_label_barang)

        self.frame_info_sensor = QFrame(self.frame_info)
        self.frame_info_sensor.setObjectName(u"frame_info_sensor")
        self.frame_info_sensor.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_info_sensor.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_info_sensor.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.verticalLayout_5 = QVBoxLayout(self.frame_info_sensor)
        self.verticalLayout_5.setSpacing(5)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(5, 5, 5, 5)
        self.label_suhu = QLabel(self.frame_info_sensor)
        self.label_suhu.setObjectName(u"label_suhu")
        font4 = QFont(self.font_families[0],14) #Arial
        # font4.setFamilies([u"Arial"])
        # font4.setPointSize(14)
        font4.setBold(True)
        self.label_suhu.setFont(font4)
        self.label_suhu.setStyleSheet(u"color: rgb(0, 103, 95);")

        self.verticalLayout_5.addWidget(self.label_suhu)

        self.label_humid = QLabel(self.frame_info_sensor)
        self.label_humid.setObjectName(u"label_humid")
        self.label_humid.setFont(font4)
        self.label_humid.setStyleSheet(u"color: rgb(0, 103, 95);")

        self.verticalLayout_5.addWidget(self.label_humid)

        self.label_light = QLabel(self.frame_info_sensor)
        self.label_light.setObjectName(u"label_light")
        self.label_light.setFont(font4)
        self.label_light.setStyleSheet(u"color: rgb(0, 103, 95);")

        self.verticalLayout_5.addWidget(self.label_light)


        self.verticalLayout_6.addWidget(self.frame_info_sensor)


        self.horizontalLayout_5.addWidget(self.frame_info)

        self.frame_input = QFrame(self.function_frame)
        self.frame_input.setObjectName(u"frame_input")
        self.frame_input.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_input.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_input.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.gridLayout_3 = QGridLayout(self.frame_input)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setHorizontalSpacing(20)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(10)
        self.gridLayout.setVerticalSpacing(15)
        self.gridLayout.setContentsMargins(10, -1, 0, -1)
        self.label_tanggal = QLabel(self.frame_input)
        self.label_tanggal.setObjectName(u"label_tanggal")
        self.label_tanggal.setFont(font4)
        self.label_tanggal.setStyleSheet(u"color: rgb(0, 60, 55);")

        self.gridLayout.addWidget(self.label_tanggal, 1, 0, 1, 1)

        self.lineEdit_namabarang = QLineEdit(self.frame_input)
        self.lineEdit_namabarang.setObjectName(u"lineEdit_namabarang")
        font5 = QFont(self.font_families[0],12) #Arial
        # font5.setFamilies([u"Arial"])
        # font5.setPointSize(12)
        font5.setBold(True)
        self.lineEdit_namabarang.setFont(font5)
        self.lineEdit_namabarang.setStyleSheet(u"QLineEdit {\n"
"    background-color: rgba(255, 255, 255, 0.8); /* Warna latar belakang putih dengan sedikit transparansi */\n"
"    color: rgb(4, 133, 123); /* Warna teks */\n"
"    border: 2px solid rgb(4, 133, 123); /* Garis batas dengan warna tema */\n"
"    border-radius: 8px; /* Membuat sudut lebih bulat */\n"
"    padding: 5px; /* Memberi jarak antara teks dan batas */\n"
"}\n"
"\n"
"/* Saat fokus */\n"
"QLineEdit:focus {\n"
"    border: 2px solid rgb(3, 160, 148); /* Warna batas saat fokus (lebih terang) */\n"
"    background-color: rgba(4, 133, 123, 0.1); /* Latar belakang yang lebih gelap saat fokus */\n"
"}\n"
"")

        self.gridLayout.addWidget(self.lineEdit_namabarang, 2, 1, 1, 1)

        self.label_namabarang = QLabel(self.frame_input)
        self.label_namabarang.setObjectName(u"label_namabarang")
        self.label_namabarang.setFont(font4)
        self.label_namabarang.setStyleSheet(u"color: rgb(0, 60, 55);")

        self.gridLayout.addWidget(self.label_namabarang, 2, 0, 1, 1)

        self.dateEdit = QDateEdit(self.frame_input)
        self.dateEdit.setObjectName(u"dateEdit")
        self.dateEdit.setFont(font5)
        self.dateEdit.setStyleSheet(u"QDateEdit {\n"
"    background-color: rgba(255, 255, 255, 0.8); /* Latar belakang putih dengan transparansi */\n"
"    color: rgb(4, 133, 123); /* Warna teks */\n"
"    border: 2px solid rgb(4, 133, 123); /* Warna garis batas */\n"
"    border-radius: 8px; /* Membuat sudut lebih bulat */\n"
"    padding: 5px; /* Jarak teks dengan batas */\n"
"}\n"
"\n"
"/* Saat fokus */\n"
"QDateEdit:focus {\n"
"    border: 2px solid rgb(3, 160, 148); /* Warna garis batas saat fokus */\n"
"    background-color: rgba(4, 133, 123, 0.1); /* Latar belakang lebih gelap saat fokus */\n"
"}\n"
"\n"
"/* Drop-down panah (button di sebelah kanan) */\n"
"QDateEdit::drop-down {\n"
"    border: none;\n"
"    background-color: rgb(4, 133, 123); /* Warna latar dropdown */\n"
"    border-radius: 4px; /* Membuat sudut dropdown bulat */\n"
"}\n"
"\n"
"/* Panah pada drop-down */\n"
"\n"
"\n"
"/* Saat hover pada drop-down */\n"
"QDateEdit::drop-down:hover {\n"
"    background-color: rgb(3, 160, 148); /* Warna latar dropdown saat hover */\n"
"}\n"
"")
        self.dateEdit.setDateTime(QDateTime(QDate(2025, 1, 1), QTime(7, 0, 0)))
        self.dateEdit.setTimeSpec(Qt.TimeSpec.LocalTime)

        self.gridLayout.addWidget(self.dateEdit, 1, 1, 1, 1)

        self.label_merek = QLabel(self.frame_input)
        self.label_merek.setObjectName(u"label_merek")
        self.label_merek.setFont(font4)
        self.label_merek.setStyleSheet(u"color: rgb(0, 60, 55);")

        self.gridLayout.addWidget(self.label_merek, 0, 0, 1, 1)

        self.lineEdit_merek = QLineEdit(self.frame_input)
        self.lineEdit_merek.setObjectName(u"lineEdit_merek")
        self.lineEdit_merek.setFont(font5)
        self.lineEdit_merek.setStyleSheet(u"QLineEdit {\n"
"    background-color: rgba(255, 255, 255, 0.8); /* Warna latar belakang putih dengan sedikit transparansi */\n"
"    color: rgb(4, 133, 123); /* Warna teks */\n"
"	\n"
"    border: 2px solid rgb(4, 133, 123); /* Garis batas dengan warna tema */\n"
"    border-radius: 8px; /* Membuat sudut lebih bulat */\n"
"    padding: 5px; /* Memberi jarak antara teks dan batas */\n"
"}\n"
"\n"
"/* Saat fokus */\n"
"QLineEdit:focus {\n"
"    border: 2px solid rgb(3, 160, 148); /* Warna batas saat fokus (lebih terang) */\n"
"    background-color: rgba(4, 133, 123, 0.1); /* Latar belakang yang lebih gelap saat fokus */\n"
"}\n"
"")

        self.gridLayout.addWidget(self.lineEdit_merek, 0, 1, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setHorizontalSpacing(10)
        self.gridLayout_2.setVerticalSpacing(15)
        self.gridLayout_2.setContentsMargins(-1, -1, 10, -1)
        self.label_jumlah = QLabel(self.frame_input)
        self.label_jumlah.setObjectName(u"label_jumlah")
        self.label_jumlah.setFont(font4)
        self.label_jumlah.setStyleSheet(u"color: rgb(0, 60, 55);")

        self.gridLayout_2.addWidget(self.label_jumlah, 0, 0, 1, 1)

        self.lineEdit_jumlah = QLineEdit(self.frame_input)
        self.lineEdit_jumlah.setObjectName(u"lineEdit_jumlah")
        self.lineEdit_jumlah.setFont(font5)
        self.lineEdit_jumlah.setStyleSheet(u"QLineEdit {\n"
"    background-color: rgba(255, 255, 255, 0.8); /* Warna latar belakang putih dengan sedikit transparansi */\n"
"    color: rgb(4, 133, 123); /* Warna teks */\n"
"    border: 2px solid rgb(4, 133, 123); /* Garis batas dengan warna tema */\n"
"    border-radius: 8px; /* Membuat sudut lebih bulat */\n"
"    padding: 5px; /* Memberi jarak antara teks dan batas */\n"
"}\n"
"\n"
"/* Saat fokus */\n"
"QLineEdit:focus {\n"
"    border: 2px solid rgb(3, 160, 148); /* Warna batas saat fokus (lebih terang) */\n"
"    background-color: rgba(4, 133, 123, 0.1); /* Latar belakang yang lebih gelap saat fokus */\n"
"}\n"
"")

        self.gridLayout_2.addWidget(self.lineEdit_jumlah, 0, 1, 1, 1)

        self.label_rak = QLabel(self.frame_input)
        self.label_rak.setObjectName(u"label_rak")
        self.label_rak.setFont(font4)
        self.label_rak.setStyleSheet(u"color: rgb(0, 60, 55);")

        self.gridLayout_2.addWidget(self.label_rak, 1, 0, 1, 1)

        self.lineEdit_rak = QLineEdit(self.frame_input)
        self.lineEdit_rak.setObjectName(u"lineEdit_rak")
        self.lineEdit_rak.setFont(font5)
        self.lineEdit_rak.setStyleSheet(u"QLineEdit {\n"
"    background-color: rgba(255, 255, 255, 0.8); /* Warna latar belakang putih dengan sedikit transparansi */\n"
"    color: rgb(4, 133, 123); /* Warna teks */\n"
"    border: 2px solid rgb(4, 133, 123); /* Garis batas dengan warna tema */\n"
"    border-radius: 8px; /* Membuat sudut lebih bulat */\n"
"    padding: 5px; /* Memberi jarak antara teks dan batas */\n"
"}\n"
"\n"
"/* Saat fokus */\n"
"QLineEdit:focus {\n"
"    border: 2px solid rgb(3, 160, 148); /* Warna batas saat fokus (lebih terang) */\n"
"    background-color: rgba(4, 133, 123, 0.1); /* Latar belakang yang lebih gelap saat fokus */\n"
"}\n"
"")

        self.gridLayout_2.addWidget(self.lineEdit_rak, 1, 1, 1, 1)

        self.label_unused = QLabel(self.frame_input)
        self.label_unused.setObjectName(u"label_unused")
        self.label_unused.setFont(font4)
        self.label_unused.setStyleSheet(u"color: rgb(0, 60, 55);")

        self.gridLayout_2.addWidget(self.label_unused, 2, 0, 1, 1)

        self.lineEdit_unused = QLineEdit(self.frame_input)
        self.lineEdit_unused.setObjectName(u"lineEdit_unused")
        self.lineEdit_unused.setFont(font5)
        self.lineEdit_unused.setStyleSheet(u"QLineEdit {\n"
"    background-color: rgb(255, 255, 255); /* Warna latar belakang putih dengan sedikit transparansi */\n"
"    color: rgb(255, 255, 255); /* Warna teks */\n"
"    border: 2px solid rgb(255, 255, 255); /* Garis batas dengan warna tema */\n"
"    border-radius: 8px; /* Membuat sudut lebih bulat */\n"
"    padding: 5px; /* Memberi jarak antara teks dan batas */\n"
"}\n"
"\n"
"")

        self.gridLayout_2.addWidget(self.lineEdit_unused, 2, 1, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 1, 1, 1)


        self.horizontalLayout_5.addWidget(self.frame_input)

        self.button_function = QFrame(self.function_frame)
        self.button_function.setObjectName(u"button_function")
        self.button_function.setFrameShape(QFrame.Shape.StyledPanel)
        self.button_function.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.button_function)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(20, 15, 20, 15)
        self.btn_add = QPushButton(self.button_function)
        self.btn_add.setObjectName(u"btn_add")
        self.btn_add.setMinimumSize(QSize(90, 40))
        self.btn_add.setFont(font5)
        self.btn_add.setStyleSheet(u"QPushButton {\n"
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

        self.verticalLayout_7.addWidget(self.btn_add)

        self.btn_remove = QPushButton(self.button_function)
        self.btn_remove.setObjectName(u"btn_remove")
        self.btn_remove.setMinimumSize(QSize(90, 40))
        self.btn_remove.setFont(font5)
        self.btn_remove.setStyleSheet(u"QPushButton{\n"
"	border:none;\n"
"	border-radius:12px;\n"
"	background-color:rgb(220, 50, 50); \n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"	background-color: rgba(220, 50, 50, 150);\n"
"}\n"
"")

        self.verticalLayout_7.addWidget(self.btn_remove)

        self.btn_download = QPushButton(self.button_function)
        self.btn_download.setObjectName(u"btn_download")
        self.btn_download.setMinimumSize(QSize(90, 40))
        self.btn_download.setFont(font5)
        self.btn_download.setStyleSheet(u"QPushButton {\n"
"    border: none;\n"
"    border-radius: 12px;\n"
"    background-color: rgb(255, 140, 0); /* Warna background utama (orange) */\n"
"    color: rgb(255, 255, 255); /* Warna teks */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(255, 140, 0, 150); /* Warna saat hover (orange dengan transparansi) */\n"
"}\n"
"")

        self.verticalLayout_7.addWidget(self.btn_download)


        self.horizontalLayout_5.addWidget(self.button_function)


        self.verticalLayout_4.addWidget(self.function_frame)

        self.table_frame = QFrame(self.content_bar_frame)
        self.table_frame.setObjectName(u"table_frame")
        self.table_frame.setMinimumSize(QSize(1366, 596))
        self.table_frame.setMaximumSize(QSize(16777215, 16777215))
        self.table_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.table_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.table_frame)
        self.horizontalLayout_6.setSpacing(30)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(30, 20, 30, 160)
        self.tabeldata = QTableWidget(self.table_frame)
        if (self.tabeldata.columnCount() < 7):
            self.tabeldata.setColumnCount(7)
        font6 = QFont(self.font_families[0],11) #Arial
        # font6.setFamilies([u"Arial"])
        # font6.setPointSize(11)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        __qtablewidgetitem.setFont(font6);
        self.tabeldata.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        __qtablewidgetitem1.setFont(font6);
        self.tabeldata.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        __qtablewidgetitem2.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        __qtablewidgetitem2.setFont(font6);
        self.tabeldata.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        __qtablewidgetitem3.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        __qtablewidgetitem3.setFont(font6);
        self.tabeldata.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        __qtablewidgetitem4.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        __qtablewidgetitem4.setFont(font6);
        self.tabeldata.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        __qtablewidgetitem5.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        __qtablewidgetitem5.setFont(font6);
        self.tabeldata.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        __qtablewidgetitem6.setTextAlignment(Qt.AlignLeading|Qt.AlignVCenter);
        __qtablewidgetitem6.setFont(font6);
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
        self.tabeldata.setStyleSheet("background-color: white;")


        self.horizontalLayout_6.addWidget(self.tabeldata)


        self.verticalLayout_4.addWidget(self.table_frame)


        self.drop_shadow_layout.addWidget(self.content_bar_frame)


        self.horizontalLayout.addWidget(self.drop_shadow_frame)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.date_label.setText(QCoreApplication.translate("MainWindow", u"18:07 - Senin, 26 Agustus 2024", None))
        self.smart_title.setText(QCoreApplication.translate("MainWindow", u"Warehouse Information System", None))
#if QT_CONFIG(tooltip)
        self.btn_minimize.setToolTip(QCoreApplication.translate("MainWindow", u"Minimize", None))
#endif // QT_CONFIG(tooltip)
        self.btn_minimize.setText("")
#if QT_CONFIG(tooltip)
        self.btn_maximize.setToolTip(QCoreApplication.translate("MainWindow", u"Maximize", None))
#endif // QT_CONFIG(tooltip)
        self.btn_maximize.setText("")
#if QT_CONFIG(tooltip)
        self.btn_close.setToolTip(QCoreApplication.translate("MainWindow", u"Close", None))
#endif // QT_CONFIG(tooltip)
        self.btn_close.setText("")
        self.btn_info.setText("")
        self.titile_label.setText(QCoreApplication.translate("MainWindow", u"SISTEM INFORMASI GUDANG", None))
        self.status_label_barang.setText(QCoreApplication.translate("MainWindow", u"Barang Masuk", None))
        self.label_suhu.setText(QCoreApplication.translate("MainWindow", u"Suhu : 30 C", None))
        self.label_humid.setText(QCoreApplication.translate("MainWindow", u"Kelembaban : 100%", None))
        self.label_light.setText(QCoreApplication.translate("MainWindow", u"Tingkat Cahaya : 100 %", None))
        self.label_tanggal.setText(QCoreApplication.translate("MainWindow", u"Tanggal Masuk", None))
        self.lineEdit_namabarang.setText("")
        self.label_namabarang.setText(QCoreApplication.translate("MainWindow", u"Nama Barang", None))
        self.label_merek.setText(QCoreApplication.translate("MainWindow", u"Merek", None))
        self.lineEdit_merek.setPlaceholderText("")
        self.label_jumlah.setText(QCoreApplication.translate("MainWindow", u"Jumlah Masuk", None))
        self.label_rak.setText(QCoreApplication.translate("MainWindow", u"Rak", None))
        self.label_unused.setText("")
        self.btn_add.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.btn_remove.setText(QCoreApplication.translate("MainWindow", u"Remove", None))
        self.btn_download.setText(QCoreApplication.translate("MainWindow", u"Download", None))
        ___qtablewidgetitem = self.tabeldata.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"No", None));
        ___qtablewidgetitem1 = self.tabeldata.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Tanggal Masuk", None));
        ___qtablewidgetitem2 = self.tabeldata.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Merek", None));
        ___qtablewidgetitem3 = self.tabeldata.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Nama Barang", None));
        ___qtablewidgetitem4 = self.tabeldata.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Jumlah Masuk", None));
        ___qtablewidgetitem5 = self.tabeldata.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"Stok", None));
        ___qtablewidgetitem6 = self.tabeldata.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"Rak", None));
    # retranslateUi

    def load_custom_fonts(self, font_paths):
        font_families = []
        for path in font_paths:
                font_id = QFontDatabase.addApplicationFont(path)
                families = QFontDatabase.applicationFontFamilies(font_id)
                if families:
                        font_families.append(families[0])  # Ambil nama keluarga font pertama
                else:
                        print(f"Font tidak ditemukan atau gagal dimuat: {path}")
        return font_families

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)
