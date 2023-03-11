from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.uic import loadUi
import sys
import sqlite3
import time

class StartDB:
    def __init__(self):
        self.connect = sqlite3.connect('bank.db')
        self.connect.execute("""
            CREATE TABLE IF NOT EXISTS users(
            login VARCHAR(255),
            password VARCHAR(255),
            email VARCHAR(255),
            created VARCHAR(100)
            );
        """)
        self.connect.commit()


class SignUp(QWidget):
    def __init__(self):
        super(SignUp, self).__init__()
        loadUi('signup.ui', self)
        self.hide_error()
        self.db = StartDB()
        self.signup.clicked.connect(self.register)

    def hide_error(self):
        self.error.hide()

    def show_error(self):
        self.error.show()

    def register(self):
        login = self.login.text()
        password = self.password.text()
        email = self.email.text()
        self.show_error()
        cursor = self.db.connect.cursor()
        try:
            cursor.execute(f"INSERT INTO users VALUES ('{login}', '{password}', '{email}', '{time.ctime()}')")
            self.error.setText("Ваши данные успешно записаны")
        except sqlite3.IntegrityError as d:
            print(d.args)
            if d.args == "('UNIQUE constraint failed: users.login',)":
                self.error.setText("Данный логин занят")
            elif d.args == ('UNIQUE constraint failed: users.email',):
                self.error.setText("Данная почта занята")
            else:
                self.error.setText("Логин занят")
        self.db.connect.commit()


class Bank(QMainWindow):
    def __init__(self):
        super(Bank, self).__init__()
        loadUi('main.ui', self)
        self.hide_error()
        self.signin.clicked.connect(self.check_login)
        self.class_signup = SignUp()
        self.signup.clicked.connect(self.show_signup)

    def show_signup(self):
        self.class_signup.show()

    def hide_error(self):
        self.error.hide()

    def show_error(self):
        self.error.show()

    def check_login(self):
        login = self.login.text()
        password = self.password.text()
        if login == 'geeks' and password == 'geeks2023':
            self.show_error()
            self.error.setText("Ok")
        else:
            self.show_error()
            self.error.setText("Неправильные данные")

app = QApplication(sys.argv)
bank = Bank()
bank.show()
app.exec_()