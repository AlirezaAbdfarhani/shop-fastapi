
from PyQt5 import QtCore, QtGui, QtWidgets
from crud.database import database


class Ui_Dialog(object):
    def __init__(self):
        self.db=database()
        data=self.db.find_all_goods()
        self.data=[{'id':d[0], 'name':d[1],'price':d[2]}for d in data]

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(373, 429)
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(20, 130, 331, 281))
        self.tableWidget.setObjectName("tableWidget")
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(20, 0, 241, 121))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 1, 1, 1)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.gridLayout.addWidget(self.lineEdit_4, 4, 1, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 1, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 1, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 1, 0, 1, 1)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout.addWidget(self.lineEdit_3, 4, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        self.widget1 = QtWidgets.QWidget(Dialog)
        self.widget1.setGeometry(QtCore.QRect(270, 0, 77, 121))
        self.widget1.setObjectName("widget1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget1)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton = QtWidgets.QPushButton(self.widget1)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.pushButton_3 = QtWidgets.QPushButton(self.widget1)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout.addWidget(self.pushButton_3)
        self.pushButton_4 = QtWidgets.QPushButton(self.widget1)
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout.addWidget(self.pushButton_4)
        self.filltable()
        self.mysignals()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))

        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.setSortingEnabled(__sortingEnabled)
        self.label_3.setText(_translate("Dialog", "name:"))
        self.label_4.setText(_translate("Dialog", "To Price:"))
        self.label.setText(_translate("Dialog", "Id :"))
        self.label_2.setText(_translate("Dialog", "From Price:"))
        self.pushButton.setText(_translate("Dialog", "Search"))
        self.pushButton_3.setText(_translate("Dialog", "Delete"))
        self.pushButton_4.setText(_translate("Dialog", "Edit"))
        # item = self.tableWidget.verticalHeaderItem(0)
        # item.setText(_translate("Dialog", "1"))
        # item = self.tableWidget.verticalHeaderItem(1)
        # item.setText(_translate("Dialog", "2"))
        # item = self.tableWidget.verticalHeaderItem(2)
        # item.setText(_translate("Dialog", "3"))
        # item = self.tableWidget.verticalHeaderItem(3)
        # item.setText(_translate("Dialog", "4"))
        # item = self.tableWidget.horizontalHeaderItem(0)
        # item.setText(_translate("Dialog", "ID"))
        # item = self.tableWidget.horizontalHeaderItem(1)
        # item.setText(_translate("Dialog", "Name"))
        # item = self.tableWidget.horizontalHeaderItem(2)
        # item.setText(_translate("Dialog", "Fee"))
    def filltable(self):
        cols=['id','name','price']
        self.tableWidget.setColumnCount(3)
        mylen=len(self.data)
        self.tableWidget.setRowCount(mylen)
        for i in range(mylen):
            item=QtWidgets.QTableWidgetItem()
            item.setText(str(i+1))
            self.tableWidget.setVerticalHeaderItem(i , item)
        
        for i in range(3): 
            item=QtWidgets.QTableWidgetItem()
            item.setText(cols[i])
            self.tableWidget.setHorizontalHeaderItem(i,item)
        for i in range(mylen):
            for j in range(3):
             item=QtWidgets.QTableWidgetItem()
             item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
             item.setText(str(self.data[i][cols[j]]))
             self.tableWidget.setItem(i,j,item)
    
    def mysignals(self):
        self.pushButton.clicked.connect(self.filter)
   
    def filter(self):
        id= self.lineEdit.text()
        name=self.lineEdit_2.text()
        fp=self.lineEdit_3.text()
        tp=self.lineEdit_4.text()
        self.data=self.db.find_goods_filter(id=id , name=name , from_price=fp , to_price=tp)
        self.data=[{'id':d[0] , 'name':d[1] , 'price':d[2]} for d in self.data]
        self.filltable()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
