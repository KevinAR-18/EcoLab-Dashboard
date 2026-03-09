import sys
import os
import pyrebase
import requests
from datetime import datetime
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from google_auth_oauthlib.flow import InstalledAppFlow


# ===============================
# PATH FILE (IMPORTANT)
# ===============================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLIENT_SECRET = os.path.join(BASE_DIR, "client_secret.json")


# ===============================
# FIREBASE CONFIG
# ===============================

firebaseConfig = {
  "apiKey": "AIzaSyDkca9-2rrP1_wetueUq-TbX-HTCrA_sCw",
  "authDomain": "cobaloginpage.firebaseapp.com",
  "databaseURL": "https://cobaloginpage-default-rtdb.asia-southeast1.firebasedatabase.app",
  "projectId": "cobaloginpage",
  "storageBucket": "cobaloginpage.firebasestorage.app",
  "messagingSenderId": "204601095466",
  "appId": "1:204601095466:web:556f5b16bc20eccb679a53"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()


# ===============================
# GOOGLE LOGIN
# ===============================

def google_auth_login():

    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRET,
        scopes=[
            "openid",
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile"
        ]
    )

    credentials = flow.run_local_server(port=0)

    token = credentials.token

    userinfo = requests.get(
        "https://www.googleapis.com/oauth2/v1/userinfo",
        params={"access_token": token}
    ).json()

    return userinfo

def create_admin():

        email = "admin@ecolab.com"
        password = "admin123"

        user = auth.create_user_with_email_and_password(email,password)

        uid = user["localId"]

        db.child("users").child(uid).set({
            "username":"admin",
            "email":email,
            "role":"admin",
            "role_request":"admin",
            "status":"active",
            "date":datetime.now().strftime("%Y-%m-%d")
        })

# ===============================
# ADMIN PAGE
# ===============================

class AdminPage(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Admin Panel")
        self.resize(900,500)

        layout = QVBoxLayout()

        self.tabs = QTabWidget()

        self.pending_tab = QWidget()
        self.active_tab = QWidget()
        self.block_tab = QWidget()

        self.tabs.addTab(self.pending_tab,"Signup Requests")
        self.tabs.addTab(self.active_tab,"Active Users")
        self.tabs.addTab(self.block_tab,"Blocked Users")

        layout.addWidget(self.tabs)

        self.setLayout(layout)

        self.pending_table()
        self.refresh()


    def pending_table(self):

        layout = QVBoxLayout()

        self.pending = QTableWidget()
        self.pending.setColumnCount(6)

        self.pending.setHorizontalHeaderLabels([
            "Username","Email","Role Request","Date","Approve","Reject"
        ])

        layout.addWidget(self.pending)

        self.pending_tab.setLayout(layout)


    def refresh(self):

        users = db.child("users").get()

        self.pending.setRowCount(0)

        if users.each():

            for user in users.each():

                data = user.val()

                if data["status"] == "pending":

                    row = self.pending.rowCount()
                    self.pending.insertRow(row)

                    self.pending.setItem(row,0,QTableWidgetItem(data["username"]))
                    self.pending.setItem(row,1,QTableWidgetItem(data["email"]))
                    self.pending.setItem(row,2,QTableWidgetItem(data["role_request"]))
                    self.pending.setItem(row,3,QTableWidgetItem(data["date"]))

                    approve = QPushButton("Approve")
                    reject = QPushButton("Reject")

                    approve.clicked.connect(lambda _,u=user.key():self.approve(u))
                    reject.clicked.connect(lambda _,u=user.key():self.reject(u))

                    self.pending.setCellWidget(row,4,approve)
                    self.pending.setCellWidget(row,5,reject)


    def approve(self,uid):

        user = db.child("users").child(uid).get().val()

        db.child("users").child(uid).update({
            "status":"active",
            "role":user["role_request"]
        })

        self.refresh()


    def reject(self,uid):

        db.child("users").child(uid).remove()

        self.refresh()
        
    



# ===============================
# LOGIN PAGE
# ===============================

class LoginPage(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("EcoLab Login")
        self.resize(350,420)

        layout = QVBoxLayout()

        title = QLabel("EcoLab Login")
        title.setAlignment(Qt.AlignCenter)

        layout.addWidget(title)

        self.email = QLineEdit()
        self.email.setPlaceholderText("Email")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.Password)

        self.showpass = QCheckBox("Show Password")
        self.showpass.stateChanged.connect(self.toggle_pass)

        login = QPushButton("Login")
        signup = QPushButton("Sign Up")
        google = QPushButton("Sign in with Google")
        forgot = QPushButton("Forgot Password")

        login.clicked.connect(self.login)
        signup.clicked.connect(self.signup)
        google.clicked.connect(self.google_login)
        forgot.clicked.connect(self.reset_password)

        layout.addWidget(self.email)
        layout.addWidget(self.password)
        layout.addWidget(self.showpass)
        layout.addWidget(login)
        layout.addWidget(signup)
        layout.addWidget(google)
        layout.addWidget(forgot)

        self.setLayout(layout)


    def toggle_pass(self):

        if self.showpass.isChecked():
            self.password.setEchoMode(QLineEdit.Normal)
        else:
            self.password.setEchoMode(QLineEdit.Password)


    def login(self):

        email = self.email.text()
        password = self.password.text()

        try:

            user = auth.sign_in_with_email_and_password(email,password)

            uid = user["localId"]

            data = db.child("users").child(uid).get().val()

            if not data:
                QMessageBox.warning(self,"Error","User data not found")
                return

            if data["status"] == "pending":
                QMessageBox.warning(self,"Wait","Waiting admin approval")

            elif data["status"] == "blocked":
                QMessageBox.warning(self,"Blocked","Account blocked")

            elif data["role"] == "admin":
                self.admin = AdminPage()
                self.admin.show()

            else:
                QMessageBox.information(self,"Login","Login success")

        except Exception as e:
            QMessageBox.warning(self,"Login Failed",str(e))


    def signup(self):

        email = self.email.text()
        password = self.password.text()

        try:

            user = auth.create_user_with_email_and_password(email,password)

            uid = user["localId"]

            db.child("users").child(uid).set({
                "username":email.split("@")[0],
                "email":email,
                "role_request":"user",
                "role":"user",
                "status":"pending",
                "date":datetime.now().strftime("%Y-%m-%d")
            })

            QMessageBox.information(self,"Signup","Signup request sent")

        except Exception as e:
            QMessageBox.warning(self,"Signup Error",str(e))


    def google_login(self):

        try:

            userinfo = google_auth_login()

            email = userinfo["email"]
            name = userinfo["name"]
            uid = userinfo["id"]

            user = db.child("users").child(uid).get().val()

            if not user:

                db.child("users").child(uid).set({
                    "username":name,
                    "email":email,
                    "role_request":"user",
                    "role":"user",
                    "status":"pending",
                    "date":datetime.now().strftime("%Y-%m-%d")
                })

                QMessageBox.information(self,"Signup","Google signup request sent")
                return

            if user["status"] == "pending":
                QMessageBox.warning(self,"Wait","Waiting admin approval")

            elif user["status"] == "blocked":
                QMessageBox.warning(self,"Blocked","Account blocked")

            elif user["role"] == "admin":
                self.admin = AdminPage()
                self.admin.show()

            else:
                QMessageBox.information(self,"Login","Google login success")

        except Exception as e:
            QMessageBox.warning(self,"Google Login Error",str(e))


    def reset_password(self):

        email,ok = QInputDialog.getText(self,"Reset Password","Enter Email")

        if ok:

            try:
                auth.send_password_reset_email(email)
                QMessageBox.information(self,"Email Sent","Check your email")

            except Exception as e:
                QMessageBox.warning(self,"Error",str(e))


# ===============================
# MAIN
# ===============================
# create_admin()
app = QApplication(sys.argv)

window = LoginPage()
window.show()

sys.exit(app.exec())