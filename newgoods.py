from PyQt5 import QtCore, QtGui, QtWidgets
from crud.database import database


class Ui_newGoodsDialog(object):
    def setupUi(self, newGoodsDialog):
        self.dialog = newGoodsDialog

        newGoodsDialog.setObjectName("newGoodsDialog")
        newGoodsDialog.resize(267, 138)

        self.widget = QtWidgets.QWidget(newGoodsDialog)
        self.widget.setGeometry(QtCore.QRect(23, 16, 211, 101))
        self.widget.setObjectName("widget")

        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.lineEditAName = QtWidgets.QLineEdit(self.widget)
        self.lineEditAName.setObjectName("lineEditAName")
        self.gridLayout.addWidget(self.lineEditAName, 0, 1, 1, 1)

        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.lineEditAPrice = QtWidgets.QLineEdit(self.widget)
        self.lineEditAPrice.setObjectName("lineEditAPrice")
        self.gridLayout.addWidget(self.lineEditAPrice, 1, 1, 1, 1)

        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setEnabled(False)
        self.gridLayout.addWidget(self.pushButton, 2, 0, 1, 2)

        self.signals()
        self.retranslateUi(newGoodsDialog)
        QtCore.QMetaObject.connectSlotsByName(newGoodsDialog)

    def retranslateUi(self, newGoodsDialog):
        _translate = QtCore.QCoreApplication.translate
        newGoodsDialog.setWindowTitle(_translate("newGoodsDialog", "New Goods"))
        self.label.setText(_translate("newGoodsDialog", "name :"))
        self.label_2.setText(_translate("newGoodsDialog", "Price:"))
        self.pushButton.setText(_translate("newGoodsDialog", "Save"))

    def signals(self):
        self.pushButton.clicked.connect(self.additem)
        self.lineEditAName.textChanged.connect(self.checkFields)
        self.lineEditAPrice.textChanged.connect(self.checkFields)

    def checkFields(self):
        name = self.lineEditAName.text().strip()
        price = self.lineEditAPrice.text().strip()
        valid = bool(name) and price.isdigit() and int(price) > 0
        self.pushButton.setEnabled(valid)

    def additem(self):
        name = self.lineEditAName.text().strip()
        price = int(self.lineEditAPrice.text())

        try:
            db = database()
            result = db.insert_into_goods(name, price)
            if result:
                QtWidgets.QMessageBox.information(
                    self.dialog, "Saved",
                    f"'{name}' added successfully"
                )
                self.dialog.accept()
            else:
                QtWidgets.QMessageBox.warning(
                    self.dialog, "Error",
                    "Failed to add product. Check FastAPI server."
                )
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self.dialog, "Error", str(e)
            )


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    newGoodsDialog = QtWidgets.QDialog()
    ui = Ui_newGoodsDialog()
    ui.setupUi(newGoodsDialog)
    newGoodsDialog.show()
    sys.exit(app.exec_())