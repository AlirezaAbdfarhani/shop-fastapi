from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_newCustomer(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 227)

        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(190, 20, 191, 191))
        self.label_4.setText("")
        self.label_4.setTextFormat(QtCore.Qt.MarkdownText)
        self.label_4.setPixmap(QtGui.QPixmap("pic/nobody.jpg"))
        self.label_4.setScaledContents(True)
        self.label_4.setObjectName("label_4")

        self.pushButton_save = QtWidgets.QPushButton(Dialog)
        self.pushButton_save.setGeometry(QtCore.QRect(0, 180, 181, 28))
        self.pushButton_save.setEnabled(False)

        self.toolButton = QtWidgets.QToolButton(Dialog)
        self.toolButton.setGeometry(QtCore.QRect(346, 181, 31, 31))

        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(5, 10, 161, 161))
        self.formLayout = QtWidgets.QFormLayout(self.widget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)

        self.label = QtWidgets.QLabel(self.widget)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)

        self.lineEdit_ID = QtWidgets.QLineEdit(self.widget)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_ID)

        self.label_2 = QtWidgets.QLabel(self.widget)
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.label_2)

        self.lineEdit_Name = QtWidgets.QLineEdit(self.widget)
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.lineEdit_Name)

        self.label_3 = QtWidgets.QLabel(self.widget)
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.SpanningRole, self.label_3)

        self.lineEdit_phone = QtWidgets.QLineEdit(self.widget)
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.lineEdit_phone)

        self.mySignals()
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton_save.setText(_translate("Dialog", "SAVE"))
        self.toolButton.setText(_translate("Dialog", "..."))
        self.label.setText(_translate("Dialog", "Id"))
        self.label_2.setText(_translate("Dialog", "Name"))
        self.label_3.setText(_translate("Dialog", "Phone"))

    def mySignals(self):
        self.lineEdit_ID.textChanged.connect(self.enableBtn)
        self.lineEdit_Name.textChanged.connect(self.enableBtn)
        self.lineEdit_phone.textChanged.connect(self.enableBtn)
        self.toolButton.clicked.connect(self.selectImage)

    def enableBtn(self):
        self.pushButton_save.setEnabled(
            self.lineEdit_ID.text().strip() != ''
            and self.lineEdit_Name.text().strip() != ''
            and self.lineEdit_phone.text().strip() != ''
        )

    def selectImage(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
            None, "Select Profile Image", "",
            "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if fileName:
            self.label_4.setPixmap(QtGui.QPixmap(fileName))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_newCustomer()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())