import sys

from PySide6.QtWidgets import QApplication

from login_page import LoginPage


def main():
    app = QApplication(sys.argv)
    window = LoginPage()
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
