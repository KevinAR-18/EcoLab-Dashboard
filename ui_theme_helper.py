"""
UI Theme Helper
Memaksa light theme agar tidak terpengaruh Dark Mode Windows 11
"""


def get_light_theme_stylesheet():
    """
    Mengembalikan stylesheet untuk memaksa light theme
    Mencegah teks berubah warna karena Dark Mode Windows 11

    Windows 11 Dark Mode causes text color inversion:
    - Black text becomes white
    - White text becomes black
    - Gray text becomes inverted

    This stylesheet forces explicit colors on all widgets.
    """
    return """
    /* ========================================
       GLOBAL WIDGET STYLES - Force Light Theme
       ======================================== */

    /* ALL WIDGETS - Force default text color */
    * {
        color: #000000;
    }

    /* LABEL - Force black text (most common) */
    QLabel {
        color: #000000;
    }

    /* WHITE LABEL - Special property for white text on dark background */
    QLabel[whiteText="true"],
    QLabel[white_text="true"] {
        color: #FFFFFF !important;
    }

    /* BUTTONS - Force white text on colored buttons */
    QPushButton {
        color: #FFFFFF;
    }

    /* Black text buttons (special case) */
    QPushButton[textBlack="true"],
    QPushButton[text_black="true"] {
        color: #000000 !important;
    }

    /* LINE EDIT - Force black text on white background */
    QLineEdit {
        color: #000000;
        background-color: #FFFFFF;
    }

    QLineEdit::placeholder {
        color: #999999;
    }

    /* TEXT EDIT - Force black text on white background */
    QTextEdit {
        color: #000000;
        background-color: #FFFFFF;
    }

    /* PLAIN TEXT EDIT */
    QPlainTextEdit {
        color: #000000;
        background-color: #FFFFFF;
    }

    /* COMBO BOX - Force black text on white background */
    QComboBox {
        color: #000000;
        background-color: #FFFFFF;
    }

    QComboBox QAbstractItemView {
        color: #000000;
        background-color: #FFFFFF;
        selection-background-color: #2b6cb0;
        selection-color: #FFFFFF;
    }

    QComboBox::drop-down {
        border: 1px solid #cfd8e3;
        background-color: #FFFFFF;
    }

    /* SPIN BOX */
    QSpinBox,
    QDoubleSpinBox {
        color: #000000;
        background-color: #FFFFFF;
    }

    QSpinBox::up-button,
    QSpinBox::down-button,
    QDoubleSpinBox::up-button,
    QDoubleSpinBox::down-button {
        background-color: #F0F0F0;
        border: 1px solid #cfd8e3;
    }

    /* DATE/TIME EDIT */
    QDateEdit,
    QTimeEdit,
    QDateTimeEdit {
        color: #000000;
        background-color: #FFFFFF;
    }

    /* TABLE WIDGET - Force black text on white background */
    QTableWidget,
    QTableView {
        color: #000000;
        background-color: #FFFFFF;
        gridline-color: #D9E9F6;
        alternate-background-color: #F5F9FC;
    }

    QTableWidget::item,
    QTableView::item {
        color: #000000;
    }

    QTableWidget::item:selected,
    QTableView::item:selected {
        background-color: #2b6cb0;
        color: #FFFFFF;
    }

    QHeaderView::section {
        color: #000000;
        background-color: #E1F2FB;
        border: 1px solid #D9E9F6;
        padding: 5px;
        font-weight: bold;
    }

    /* LIST WIDGET */
    QListWidget {
        color: #000000;
        background-color: #FFFFFF;
    }

    QListWidget::item {
        color: #000000;
    }

    QListWidget::item:selected {
        background-color: #2b6cb0;
        color: #FFFFFF;
    }

    /* TREE WIDGET */
    QTreeWidget {
        color: #000000;
        background-color: #FFFFFF;
    }

    QTreeWidget::item {
        color: #000000;
    }

    QTreeWidget::item:selected {
        background-color: #2b6cb0;
        color: #FFFFFF;
    }

    /* CHECKBOX - Force black text */
    QCheckBox {
        color: #000000;
    }

    QCheckBox::indicator {
        border: 1px solid #cfd8e3;
        background-color: #FFFFFF;
        border-radius: 4px;
    }

    QCheckBox::indicator:checked {
        background-color: #2b6cb0;
        border: 1px solid #2b6cb0;
    }

    /* RADIO BUTTON - Force black text */
    QRadioButton {
        color: #000000;
    }

    QRadioButton::indicator {
        border: 1px solid #cfd8e3;
        background-color: #FFFFFF;
        border-radius: 6px;
    }

    QRadioButton::indicator:checked {
        background-color: #2b6cb0;
        border: 1px solid #2b6cb0;
    }

    /* GROUP BOX - Force black title */
    QGroupBox {
        color: #000000;
        border: 1px solid #D9E9F6;
        border-radius: 5px;
        margin-top: 10px;
        padding: 10px;
    }

    QGroupBox::title {
        color: #000000;
        subcontrol-origin: margin;
        subcontrol-position: top left;
        padding: 0 5px;
    }

    /* SLIDER */
    QSlider::groove:horizontal {
        background: #E1F2FB;
        height: 8px;
        border-radius: 4px;
    }

    QSlider::handle:horizontal {
        background: #2b6cb0;
        width: 18px;
        margin: -5px 0;
        border-radius: 9px;
    }

    /* PROGRESS BAR */
    QProgressBar {
        color: #000000;
        border: 1px solid #D9E9F6;
        border-radius: 5px;
        text-align: center;
    }

    QProgressBar::chunk {
        background-color: #2b6cb0;
    }

    /* TAB WIDGET */
    QTabWidget::pane {
        border: 1px solid #D9E9F6;
        background: #FFFFFF;
    }

    QTabBar::tab {
        color: #000000;
        background: #E1F2FB;
        border: 1px solid #D9E9F6;
        padding: 8px 16px;
        margin-right: 2px;
    }

    QTabBar::tab:selected {
        background: #FFFFFF;
        border-bottom-color: #FFFFFF;
    }

    /* SCROLL BAR */
    QScrollBar:vertical {
        background: #F0F0F0;
        width: 12px;
        border-radius: 6px;
    }

    QScrollBar::handle:vertical {
        background: #cfd8e3;
        border-radius: 6px;
        min-height: 20px;
    }

    QScrollBar::handle:vertical:hover {
        background: #b8c9d9;
    }

    QScrollBar:horizontal {
        background: #F0F0F0;
        height: 12px;
        border-radius: 6px;
    }

    QScrollBar::handle:horizontal {
        background: #cfd8e3;
        border-radius: 6px;
        min-width: 20px;
    }

    QScrollBar::handle:horizontal:hover {
        background: #b8c9d9;
    }

    /* TOOLTIP */
    QToolTip {
        color: #000000;
        background-color: #FFFFE0;
        border: 1px solid #cfd8e3;
        padding: 5px;
    }

    /* STATUS BAR */
    QStatusBar {
        color: #000000;
        background-color: #F5F9FC;
    }

    /* MENU BAR */
    QMenuBar {
        color: #000000;
        background-color: #F5F9FC;
    }

    QMenuBar::item {
        color: #000000;
        background-color: transparent;
    }

    QMenuBar::item:selected {
        background-color: #2b6cb0;
        color: #FFFFFF;
    }

    /* MENU */
    QMenu {
        color: #000000;
        background-color: #FFFFFF;
        border: 1px solid #D9E9F6;
    }

    QMenu::item {
        color: #000000;
    }

    QMenu::item:selected {
        background-color: #2b6cb0;
        color: #FFFFFF;
    }

    /* SPINER/ARROW BUTTONS */
    QSpinBox::up-button,
    QSpinBox::down-button,
    QDoubleSpinBox::up-button,
    QDoubleSpinBox::down-button,
    QDateEdit::up-button,
    QDateEdit::down-button,
    QTimeEdit::up-button,
    QTimeEdit::down-button,
    QDateTimeEdit::up-button,
    QDateTimeEdit::down-button {
        background-color: #F0F0F0;
        border: 1px solid #cfd8e3;
        width: 20px;
    }

    /* DIALOG */
    QDialog {
        color: #000000;
    }
    """


def apply_light_theme_to_widget(widget):
    """
    Apply light theme stylesheet ke widget dan semua children-nya

    Args:
        widget: QWidget object (QMainWindow, QDialog, dll)
    """
    widget.setStyleSheet(get_light_theme_stylesheet() + widget.styleSheet())


def force_label_color(label, color="#000000"):
    """
    Memaksa warna teks label tertentu

    Args:
        label: QLabel object
        color: Hex color code (default: #000000 untuk hitam)

    Usage:
        force_label_color(my_label, "#FF0000")  # Red text
        force_label_color(my_label, "#FFFFFF")  # White text
    """
    label.setStyleSheet(f"QLabel {{ color: {color} !important; }}")


def force_button_text_color(button, color="#FFFFFF"):
    """
    Memaksa warna teks button tertentu

    Args:
        button: QPushButton object
        color: Hex color code (default: #FFFFFF untuk putih)

    Usage:
        force_button_text_color(my_button, "#000000")  # Black text
    """
    original_style = button.styleSheet() or ""
    # Tambahkan atau update color property
    if "color:" in original_style:
        # Replace existing color
        import re
        new_style = re.sub(r'color:\s*#[0-9A-Fa-f]+;', f'color: {color};', original_style)
        button.setStyleSheet(new_style)
    else:
        # Append color
        button.setStyleSheet(original_style + f"QPushButton {{ color: {color} !important; }}")


def set_widget_text_color(widget, color):
    """
    Generic function untuk set warna teks widget apapun

    Args:
        widget: QWidget object
        color: Hex color code

    Usage:
        set_widget_text_color(my_label, "#000000")
        set_widget_text_color(my_button, "#FFFFFF")
    """
    widget.setStyleSheet(f"{widget.__class__.__name__} {{ color: {color} !important; }}")
