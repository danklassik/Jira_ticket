from jira import JIRA
import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from win32api import GetSystemMetrics
from pathlib import Path
import threading

threads = []
posA = GetSystemMetrics(0) - 560
posB = GetSystemMetrics(1) - 250
appdir = Path(__file__).cwd()

jira = JIRA('https://<you_domain>.atlassian.net', basic_auth=('<you_mail>', '<you_token>'))
iss = jira.search_issues('project=AD and assignee=currentuser() and not status=Done')
print(len(iss))
for issue in iss:
    print(str(issue.key))
    print(str(issue.fields.summary))
    print(str(issue.fields.status))
    print(str(issue.self))



class MainWindow(QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.layout  = QVBoxLayout()
        self.layout.addWidget(MyBar(self))
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.addStretch(-1)
        self.setMinimumSize(580,220)

        self.label = QLabel(self)
        pixmap = QPixmap(str(appdir) + "\\img\\message.png")
        self.label.move(0, 0)
        self.label.resize(580,220)
        self.label.setPixmap(pixmap)

        self.btnOk = QtWidgets.QPushButton(self)
        self.btnOk.move(510,15)
        self.btnOk.resize(20,20)
        self.btnOk.setFont(QtGui.QFont('SansSerif', 10))
        self.btnOk.setText("X")
        self.btnOk.clicked.connect(self.deny_click)

        self.lbl1 = QLabel(self)
        self.lbl1.move(30, 15)
        self.lbl1.resize(400, 20)
        self.lbl1.setText("У тебя есть незакрытые тикеты в Жире!")
        self.lbl1.setFont(QtGui.QFont('SansSerif', 14))
        self.lbl1.setStyleSheet("color: rgba(0, 0, 0, 1);")

        self.lbl2 = QLabel(self)
        self.lbl2.move(200, 60)
        self.lbl2.resize(300, 20)
        self.lbl2.setText("Всего открытых тикетов: " + str(len(iss))+'!')
        self.lbl2.setFont(QtGui.QFont('SansSerif', 14))
        self.lbl2.setStyleSheet("color: rgba(50, 0, 0, 1);")

        self.lbl3 = QLabel(self)
        self.lbl3.move(200, 100)
        self.lbl3.resize(300, 20)
        self.lbl3.setText("Последний тикет: " + str(iss[0].key))
        self.lbl3.setFont(QtGui.QFont('SansSerif', 12))
        self.lbl3.setStyleSheet("color: rgba(0, 0, 0, 1);")

        self.lbl4 = QLabel(self)
        self.lbl4.move(200, 120)
        self.lbl4.resize(300, 20)
        self.lbl4.setText(str(iss[0].fields.summary))
        self.lbl4.setFont(QtGui.QFont('SansSerif', 10))
        self.lbl4.setStyleSheet("color: rgba(0, 0, 0, 1);")

        self.lbl5 = QLabel(self)
        self.lbl5.move(200, 140)
        self.lbl5.resize(300, 20)
        self.lbl5.setText('<a href="'+str(iss[0].self)+'">'+str(iss[0].self)+'</a>')
        self.lbl5.setOpenExternalLinks(True)
        self.lbl5.setFont(QtGui.QFont('SansSerif', 10))
        self.lbl5.setStyleSheet("color: rgba(0, 0, 200, 1); text-decoration:underline; cursor: pointer;")


        self.setGeometry(posA, posB,400,220)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint | QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
#        self.pressing = False

    def deny_click(self):
        try:
            self.hide()
        except:
            pass



class MyBar(QWidget):

    def __init__(self, parent):
        super(MyBar, self).__init__()
        self.parent = parent
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)

        self.setLayout(self.layout)

        self.start = QPoint(0, 0)
        self.pressing = False


app = QApplication(sys.argv)
mw = MainWindow()
mw.show()

def check():
    if len(iss) != 0:
        mw.show()
    else:
        pass

t = threading.Thread(target=check)

threads.append(t)
t.start()


sys.exit(app.exec_())
