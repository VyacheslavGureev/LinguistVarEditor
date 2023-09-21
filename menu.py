from PyQt5 import QtCore, QtWidgets
import re

from PyQt5.QtWidgets import QFileDialog

from ui import Graphs_Ui


class Menu_Ui(object):
    Dial = None
    namesTermsEdits = None
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(500, 110)
        Dialog.setWindowOpacity(1.0)
        Dialog.setLayoutDirection(QtCore.Qt.LeftToRight)

        self.downloadButton = QtWidgets.QPushButton(Dialog)
        self.downloadButton.setGeometry(QtCore.QRect(410, 50, 71, 31))
        self.downloadButton.setObjectName("downloadButton")
        self.downloadButton.clicked.connect(self.onUpload)

        self.createButton = QtWidgets.QPushButton(Dialog)
        self.createButton.setGeometry(QtCore.QRect(410, 10, 71, 31))
        self.createButton.setObjectName("createButton")
        self.createButton.clicked.connect(self.onCreate)

        self.nameLinVarLabel = QtWidgets.QLabel(Dialog)
        self.nameLinVarLabel.setGeometry(QtCore.QRect(20, 10, 181, 16))
        self.nameLinVarLabel.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.nameLinVarLabel.setObjectName("nameLinVarLabel")

        self.nameLinVarEdit = QtWidgets.QLineEdit(Dialog)
        self.nameLinVarEdit.setGeometry(QtCore.QRect(200, 10, 191, 21))
        self.nameLinVarEdit.setObjectName("nameLinVarEdit")

        self.numTermsEdit = QtWidgets.QLineEdit(Dialog)
        self.numTermsEdit.setGeometry(QtCore.QRect(200, 40, 191, 21))
        self.numTermsEdit.setObjectName("numTermsEdit")
        self.numTermsEdit.editingFinished.connect(self.onEdited)

        self.namesTermsEdit1 = QtWidgets.QLineEdit(Dialog)
        self.namesTermsEdit1.setGeometry(QtCore.QRect(200, 70, 191, 21))
        self.namesTermsEdit1.setObjectName("nameTermEdit1")

        self.namesTermsLabel = QtWidgets.QLabel(Dialog)
        self.namesTermsLabel.setGeometry(QtCore.QRect(120, 70, 81, 20))
        self.namesTermsLabel.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.namesTermsLabel.setObjectName("namesTermsLabel")

        self.numTermsLabel = QtWidgets.QLabel(Dialog)
        self.numTermsLabel.setGeometry(QtCore.QRect(90, 40, 101, 20))
        self.numTermsLabel.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.numTermsLabel.setObjectName("numTermsLabel")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.Dial = Dialog

        self.graphs_window = QtWidgets.QMainWindow()
        self.graphs_ui = Graphs_Ui()
        self.graphs_ui.setupUi(self.graphs_window)


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Выбор параметров"))
        self.downloadButton.setText(_translate("Dialog", "Загрузить"))
        self.createButton.setText(_translate("Dialog", "Создать"))
        self.nameLinVarLabel.setText(_translate("Dialog", "Имя лингвистической переменной:"))
        self.namesTermsLabel.setText(_translate("Dialog", "Имена термов:"))
        self.numTermsLabel.setText(_translate("Dialog", "Количество термов:"))


    def onEdited(self):
        numt_text = self.numTermsEdit.text()
        if not(bool(re.match(r'^[0123456789]{1,}$', numt_text))):
            return
        numt = int(numt_text)
        if numt < 2 or numt > 10:
            return
        if numt == 1:
            return
        if self.namesTermsEdits != None:
            for i in range(1, len(self.namesTermsEdits)):
                self.namesTermsEdits[i].deleteLater()
            self.namesTermsEdits.clear()
        self.Dial.resize(500, 110 + (numt - 1) * 30)
        self.namesTermsEdits = [0] * numt
        self.namesTermsEdits[0] = self.namesTermsEdit1
        for i in range(1, numt):
            te = QtWidgets.QLineEdit(self.Dial)
            te.setGeometry(QtCore.QRect(200, 70 + i*30, 191, 21))
            te.setObjectName(f"nameTermEdit{i + 1}")
            te.show()
            self.namesTermsEdits[i] = te


    def onCreate(self):
        from main import init_ui, create_lin_var
        names = []
        if self.namesTermsEdits != None:
            for i in range(len(self.namesTermsEdits)):
                names.append(self.namesTermsEdits[i].text())
            lin_var = create_lin_var(name_lv= self.nameLinVarEdit.text(),
                                    n=len(self.namesTermsEdits),
                                    names_terms= names,
                                    x_max=100)
            init_ui(lin_var = lin_var,
                    n=len(self.namesTermsEdits),
                    x_max=100,
                    window=self.graphs_ui)
            self.graphs_window.show()
            self.Dial.deleteLater()


    def onUpload(self):
        path = QFileDialog.getOpenFileName()[0]
        from main import load_lin_variable, init_ui
        lin_var = load_lin_variable(path)
        if lin_var != None:
            x_max = lin_var.terms[len(lin_var.terms)].x_right[1]
            init_ui(lin_var=lin_var,
                    n=len(lin_var.terms),
                    x_max=x_max,
                    window=self.graphs_ui)
            self.graphs_window.show()
            self.Dial.deleteLater()