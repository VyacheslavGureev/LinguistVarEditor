import re
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from pyqtgraph import PlotWidget
import pyqtgraph as pg


class Graphs_Ui(object):
    lin_var = None
    x_max = None
    def setupUi(self, lab1):
        lab1.setObjectName("lab1")
        lab1.resize(1150, 600)
        self.centralwidget = QtWidgets.QWidget(lab1)
        self.centralwidget.setObjectName("centralwidget")

        self.plotWidget = PlotWidget(self.centralwidget)
        self.plotWidget.setGeometry(QtCore.QRect(10, 40, 581, 441))
        self.plotWidget.setObjectName("plotWidget")
        self.plotWidget.setBackground('w')
        self.plotWidget.addLegend()

        # self.horizontalSlider = QtWidgets.QSlider(self.centralwidget)
        # self.horizontalSlider.setGeometry(QtCore.QRect(30, 500, 541, 31))
        # self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        # self.horizontalSlider.setObjectName("horizontalSlider")

        self.tableView = QtWidgets.QTableWidget(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(620, 130, 190, 351))
        self.tableView.setObjectName("tableView")
        self.tableView.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)

        self.maxXLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.maxXLineEdit.setGeometry(QtCore.QRect(620, 40, 181, 21))
        self.maxXLineEdit.setObjectName("maxXLineEdit")

        self.maxValue = QtWidgets.QLabel(self.centralwidget)
        self.maxValue.setGeometry(QtCore.QRect(620, 10, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.maxValue.setFont(font)
        self.maxValue.setObjectName("maxValue")

        self.report = QtWidgets.QLabel(self.centralwidget)
        self.report.setGeometry(QtCore.QRect(821, 35, 300, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.report.setFont(font)
        self.report.setObjectName("report")

        self.saveButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveButton.setGeometry(QtCore.QRect(714, 80, 91, 31))
        self.saveButton.setObjectName("saveButton")
        self.saveButton.clicked.connect(self.save_lin_var)

        self.buildButton = QtWidgets.QPushButton(self.centralwidget)
        self.buildButton.setGeometry(QtCore.QRect(620, 80, 91, 31))
        self.buildButton.setObjectName("buildButton")
        self.buildButton.clicked.connect(self.update_terms)

        lab1.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(lab1)
        self.statusbar.setObjectName("statusbar")
        lab1.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(lab1)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 21))
        self.menubar.setObjectName("menubar")
        lab1.setMenuBar(self.menubar)

        self.retranslateUi(lab1)
        QtCore.QMetaObject.connectSlotsByName(lab1)


    def retranslateUi(self, lab1):
        _translate = QtCore.QCoreApplication.translate
        lab1.setWindowTitle(_translate("lab1", "Редактор лингвистических переменных"))
        self.maxValue.setText(_translate("lab1", "Максимальное значение"))
        self.saveButton.setText(_translate("lab1", "Сохранить"))
        self.buildButton.setText(_translate("lab1", "Построить"))
        self.report.setText(_translate("lab1", ""))


    def update_terms(self):
        self.clear()
        new_max_x = self.maxXLineEdit.text()
        if not(bool(re.match(r'(^[0123456789]{1,}$)|(^[0123456789]{1,}\.[0123456789]{1,}$)', new_max_x))):
            return
        new_max_x = float(new_max_x)
        k = round(new_max_x/self.x_max, 4)
        from main import check_requirements
        self.read_table((self.lin_var).terms, k)
        self.report.setText(check_requirements(self.lin_var))
        self.draw_lin_var(self.lin_var)
        self.fill_table(self.lin_var)
        self.maxXLineEdit.setText(str(new_max_x))
        self.x_max = new_max_x


    def draw_lin_var(self, lin_var):
        terms = lin_var.terms
        for key in terms:
            t = terms[key]
            self.draw_term(term=t, color_matrix=t.color, width=3, name=t.name)


    def clear(self):
        self.plotWidget.clear()


    def draw_term(self, term, color_matrix, width, name):
        pen = pg.mkPen(color=(color_matrix[0], color_matrix[1], color_matrix[2]), width=width)
        self.plotWidget.plot(term.x_left, term.y_left, pen=pen)
        self.plotWidget.plot(term.x_middle, term.y_middle, pen=pen)
        self.plotWidget.plot(term.x_right, term.y_right, pen=pen, name = name)


    def fill_table(self, lin_var):
        terms = lin_var.terms
        n = len(terms)
        for key in terms:
            t = terms[key]
            if key == 1:
                self.tableView.setItem(key - 1, 1, QTableWidgetItem(str(t.x_middle[1])))
                self.tableView.setItem(key - 1, 3, QTableWidgetItem(str(t.x_right[1])))
            elif key == n:
                self.tableView.setItem(key - 1, 0, QTableWidgetItem(str(t.x_middle[0])))
                self.tableView.setItem(key - 1, 2, QTableWidgetItem(str(t.x_left[0])))
            else:
                self.tableView.setItem(key - 1, 0, QTableWidgetItem(str(t.x_middle[0])))
                self.tableView.setItem(key - 1, 1, QTableWidgetItem(str(t.x_middle[1])))
                self.tableView.setItem(key - 1, 2, QTableWidgetItem(str(t.x_left[0])))
                self.tableView.setItem(key - 1, 3, QTableWidgetItem(str(t.x_right[1])))
        self.tableView.resizeColumnsToContents()


    def save_lin_var(self):
        from main import save_lin_variable
        save_lin_variable(self.lin_var)


    def read_table(self, terms, k):
        for key in terms:
            if key == 1:
                item = self.tableView.item(key - 1, 1)
                x_middle1 = round(float(item.text())*k, 2)
                (terms[key]).x_middle[1] = x_middle1
                (terms[key]).x_right[0] = x_middle1
                item = self.tableView.item(key - 1, 3)
                x_right1 = round(float(item.text())*k, 2)
                (terms[key]).x_right[1] = x_right1
            elif key == len(terms):
                item = self.tableView.item(key - 1, 0)
                x_middle0 = round(float(item.text())*k, 2)
                (terms[key]).x_middle[0] = x_middle0
                (terms[key]).x_left[1] = x_middle0
                item = self.tableView.item(key - 1, 2)
                x_left0 = round(float(item.text())*k, 2)
                (terms[key]).x_left[0] = x_left0
                x_max = round((terms[key]).x_middle[1] * k, 2)
                (terms[key]).x_middle[1] = x_max
                (terms[key]).x_right[0] = x_max
                (terms[key]).x_right[1] = x_max
            else:
                x_middle0 = round(float((self.tableView.item(key - 1, 0)).text())*k, 2)
                x_middle1 = round(float((self.tableView.item(key - 1, 1)).text())*k, 2)
                x_left0 = round(float((self.tableView.item(key - 1, 2)).text())*k, 2)
                x_right1 = round(float((self.tableView.item(key - 1, 3)).text())*k, 2)
                (terms[key]).x_middle[0] = x_middle0
                (terms[key]).x_middle[1] = x_middle1
                (terms[key]).x_left[0] = x_left0
                (terms[key]).x_right[1] = x_right1
                (terms[key]).x_left[1] = x_middle0
                (terms[key]).x_right[0] = x_middle1