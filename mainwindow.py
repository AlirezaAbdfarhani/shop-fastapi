from PyQt5 import QtCore, QtGui, QtWidgets
from newcus import Ui_newCustomer
from newgoods import Ui_newGoodsDialog
from openfactor import Ui_OpenFactorDialog
from crud.database import database


class Ui_MainWindow(object):
    def __init__(self):
        self.db = database()
        self.goods = self.load_goods_from_db()
        self.factordata = []
        self.customer = {'id': '1', 'name': 'alireza', 'Phone': '09383842692'}
        self.factor = {'id': 1, 'data': 2026}
        self.factorchanged = False

    def load_goods_from_db(self):
        goods = [{'id': '0', 'name': 'please selecte....', 'price': 0}]
        try:
            data = self.db.find_all_goods()
            for d in data:
                goods.append({'id': str(d[0]), 'name': d[1], 'price': d[2]})
        except Exception as e:
            print("Load goods error:", e)
        return goods

    def refresh_goods(self):
        self.goods = self.load_goods_from_db()
        self.comboBoxTollNAme.clear()
        self.fillComboBox()

    def mysignal(self):
        self.pushButtonAdd.clicked.connect(self.additem)
        self.comboBoxTollNAme.currentIndexChanged.connect(self.enabledadd)
        self.spinBoxNo.valueChanged.connect(self.enabledadd)
        self.pushButtonSave.clicked.connect(self.savefactor)
        self.actionNew_Factor.triggered.connect(self.newfactor)
        self.actionClose.triggered.connect(self.MainWindow.close)
        self.tableWidget.cellClicked.connect(self.onCellClicked)
        self.actionNew_Customer.triggered.connect(self.newCustomer)
        self.actionNew_Goods.triggered.connect(self.openNewGoods)
        self.actionOpen_Factor.triggered.connect(self.openFactor)

    def openFactor(self):
        Dialog = QtWidgets.QDialog()
        ui = Ui_OpenFactorDialog()
        ui.setupUi(Dialog)
        Dialog.exec_()

    def newCustomer(self):
        Dialog = QtWidgets.QDialog()
        ui = Ui_newCustomer()
        ui.setupUi(Dialog)
        ui.lineEdit_ID.setText('1')
        ui.lineEdit_Name.setText('name')
        ui.lineEdit_phone.setText('phone')
        ui.pushButton_save.clicked.connect(lambda: self.newCustomer2(ui, Dialog))
        Dialog.exec_()

    def newCustomer2(self, ui, Dialog):
        self.customer = {
            'id': int(ui.lineEdit_ID.text()),
            'name': ui.lineEdit_Name.text(),
            'Phone': ui.lineEdit_phone.text(),
        }
        try:
            self.db.insert_into_customers(
                username=self.customer['name'],
                password=self.customer['Phone']
            )
        except Exception as e:
            print("Save customer error:", e)

        Dialog.close()
        self.setcustomer()

    def setcustomer(self):
        self.lineEditCustomerId.setText(str(self.customer.get('id', '----')))
        self.lineEditCustomerName.setText(str(self.customer.get('name', 'New user')))
        self.lineEditCustomerPhone.setText(str(self.customer.get('Phone', '----')))

    def onCellClicked(self, row, col):
        if row < 0 or row >= len(self.factordata):
            return
        if col == 6:
            del self.factordata[row]
            self.factorchanged = True
            self.fillTable()
        elif col == 5:
            item = self.factordata[row]
            item['No'] += 1
            item['Total'] = item['No'] * item['price']
            self.factorchanged = True
            self.fillTable()

    def newfactor(self):
        if self.factorchanged:
            reply = QtWidgets.QMessageBox.question(
                self.MainWindow,
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            )
            if reply == QtWidgets.QMessageBox.No:
                return
        self.factordata = []
        self.customer = {}
        self.factor = {}
        self.factorchanged = False
        self.fillTable()
        self.setcustomer()
        self.comboBoxTollNAme.setCurrentIndex(0)
        self.spinBoxNo.setValue(0)

    def savefactor(self):
        if not self.customer or not self.factordata:
            QtWidgets.QMessageBox.warning(
                self.MainWindow, "Warning",
                "Customer or items are empty"
            )
            return

        items = []
        for item in self.factordata:
            items.append({
                'product_id': int(item['id']),
                'no': item['No'],
            })

        try:
            result = self.db.insert_into_factors(
                customer_id=int(self.customer['id']),
                items=items
            )
            if result:
                QtWidgets.QMessageBox.information(
                    self.MainWindow, "Saved",
                    "Factor saved successfully"
                )
                self.factorchanged = False
                self.pushButtonSave.setEnabled(False)
            else:
                QtWidgets.QMessageBox.warning(
                    self.MainWindow, "Error",
                    "Failed to save factor"
                )
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self.MainWindow, "Error", str(e)
            )

    def enabledadd(self):
        self.pushButtonAdd.setEnabled(
            self.comboBoxTollNAme.currentIndex() != 0
            and self.spinBoxNo.value() != 0
        )

    def additem(self):
        index = self.comboBoxTollNAme.currentIndex()
        if index <= 0:
            return

        newitem = {
            'id':    self.goods[index]['id'],
            'name':  self.comboBoxTollNAme.currentText(),
            'price': self.goods[index]['price'],
            'No':    self.spinBoxNo.value(),
        }
        newitem['Total'] = newitem['No'] * newitem['price']

        found = False
        for item in self.factordata:
            if item['id'] == newitem['id']:
                item['No'] += newitem['No']
                item['Total'] = item['No'] * item['price']
                found = True
                break
        if not found:
            self.factordata.append(newitem)

        self.comboBoxTollNAme.setCurrentIndex(0)
        self.spinBoxNo.setValue(0)
        self.factorchanged = True
        self.fillTable()

    def fillComboBox(self):
        for item in self.goods:
            self.comboBoxTollNAme.addItem(item['name'])

    def fillTable(self):
        total = 0
        tableHeader = ['id', 'name', 'No', 'price', 'Total', 'Edit', 'Delete']
        dataKeys    = ['id', 'name', 'No', 'price', 'Total']
        rowcount = len(self.factordata)
        colcount = len(tableHeader)

        self.tableWidget.setColumnCount(colcount)
        self.tableWidget.setRowCount(rowcount)

        for row in range(rowcount):
            item = QtWidgets.QTableWidgetItem()
            item.setText(str(row + 1))
            self.tableWidget.setVerticalHeaderItem(row, item)

        for col in range(colcount):
            item = QtWidgets.QTableWidgetItem()
            item.setText(tableHeader[col])
            self.tableWidget.setHorizontalHeaderItem(col, item)

        for row in range(rowcount):
            for col in range(5):
                item = QtWidgets.QTableWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                item.setFlags(QtCore.Qt.NoItemFlags)
                item.setText(str(self.factordata[row][dataKeys[col]]))
                self.tableWidget.setItem(row, col, item)

        for row in range(rowcount):
            item = QtWidgets.QTableWidgetItem()
            item.setFont(QtGui.QFont("Tahoma", weight=75))
            icon1 = QtGui.QIcon()
            icon1.addPixmap(QtGui.QPixmap("pic/Edite.png"),
                            QtGui.QIcon.Normal, QtGui.QIcon.Off)
            item.setIcon(icon1)
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            item.setText('Edite')
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(row, 5, item)

            item = QtWidgets.QTableWidgetItem()
            item.setFont(QtGui.QFont("Tahoma", weight=75))
            icon2 = QtGui.QIcon()
            icon2.addPixmap(QtGui.QPixmap("pic/delete.png"),
                            QtGui.QIcon.Normal, QtGui.QIcon.Off)
            item.setIcon(icon2)
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            item.setText('delete')
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(row, 6, item)

        for item in self.factordata:
            total += item['Total']
        self.lineEditTotal.setText(str(total))
        self.pushButtonSave.setEnabled(self.factorchanged)

    def openNewGoods(self):
        Dialog = QtWidgets.QDialog()
        ui = Ui_newGoodsDialog()
        ui.setupUi(Dialog)
        Dialog.exec_()
        self.refresh_goods()

    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        MainWindow.setMaximumSize(QtCore.QSize(800, 600))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(10)
        MainWindow.setFont(font)
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(0, 0, 791, 51))
        self.groupBox.setObjectName("groupBox")
        self.widget = QtWidgets.QWidget(self.groupBox)
        self.widget.setGeometry(QtCore.QRect(10, 20, 761, 24))
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

        self.label_2 = QtWidgets.QLabel(self.widget)
        self.horizontalLayout.addWidget(self.label_2)

        self.lineEditCustomerId = QtWidgets.QLineEdit(self.widget)
        self.lineEditCustomerId.setMaximumSize(QtCore.QSize(50, 16777215))
        self.lineEditCustomerId.setReadOnly(True)
        self.horizontalLayout.addWidget(self.lineEditCustomerId)

        spacerItem = QtWidgets.QSpacerItem(40, 20,
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)

        self.label = QtWidgets.QLabel(self.widget)
        self.horizontalLayout.addWidget(self.label)

        self.lineEditCustomerName = QtWidgets.QLineEdit(self.widget)
        self.lineEditCustomerName.setReadOnly(True)
        self.horizontalLayout.addWidget(self.lineEditCustomerName)

        self.label_3 = QtWidgets.QLabel(self.widget)
        self.horizontalLayout.addWidget(self.label_3)

        self.lineEditCustomerPhone = QtWidgets.QLineEdit(self.widget)
        self.lineEditCustomerPhone.setReadOnly(True)
        self.horizontalLayout.addWidget(self.lineEditCustomerPhone)

        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(0, 50, 791, 61))
        self.widget1 = QtWidgets.QWidget(self.groupBox_2)
        self.widget1.setGeometry(QtCore.QRect(20, 20, 751, 26))
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget1)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)

        self.label_4 = QtWidgets.QLabel(self.widget1)
        self.horizontalLayout_2.addWidget(self.label_4)

        self.comboBoxTollNAme = QtWidgets.QComboBox(self.widget1)
        self.comboBoxTollNAme.setMinimumSize(QtCore.QSize(300, 0))
        self.horizontalLayout_2.addWidget(self.comboBoxTollNAme)

        spacerItem1 = QtWidgets.QSpacerItem(20, 20,
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)

        self.label_5 = QtWidgets.QLabel(self.widget1)
        self.horizontalLayout_2.addWidget(self.label_5)

        self.spinBoxNo = QtWidgets.QSpinBox(self.widget1)
        self.horizontalLayout_2.addWidget(self.spinBoxNo)

        spacerItem2 = QtWidgets.QSpacerItem(40, 20,
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)

        self.pushButtonAdd = QtWidgets.QPushButton(self.widget1)
        self.pushButtonAdd.setMinimumSize(QtCore.QSize(150, 0))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("pic/add.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonAdd.setIcon(icon)
        self.horizontalLayout_2.addWidget(self.pushButtonAdd)
        self.pushButtonAdd.setEnabled(False)

        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(20, 120, 771, 311))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)

        self.pushButtonSave = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonSave.setGeometry(QtCore.QRect(290, 500, 171, 41))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("pic/Save.png"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonSave.setIcon(icon2)
        self.pushButtonSave.setIconSize(QtCore.QSize(22, 22))
        self.pushButtonSave.setEnabled(False)

        self.widget2 = QtWidgets.QWidget(self.centralwidget)
        self.widget2.setGeometry(QtCore.QRect(506, 440, 275, 31))
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget2)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)

        self.label_6 = QtWidgets.QLabel(self.widget2)
        f = QtGui.QFont()
        f.setPointSize(14)
        f.setBold(True)
        f.setWeight(75)
        self.label_6.setFont(f)
        self.horizontalLayout_3.addWidget(self.label_6)

        self.lineEditTotal = QtWidgets.QLineEdit(self.widget2)
        self.lineEditTotal.setFont(f)
        self.lineEditTotal.setReadOnly(True)
        self.horizontalLayout_3.addWidget(self.lineEditTotal)

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuCustomer = QtWidgets.QMenu(self.menubar)
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        self.actionNew_Factor = QtWidgets.QAction(MainWindow)
        self.actionNew_Goods = QtWidgets.QAction(MainWindow)
        self.actionOpen_Factor = QtWidgets.QAction(MainWindow)
        self.actionClose = QtWidgets.QAction(MainWindow)
        self.actionNew_Customer = QtWidgets.QAction(MainWindow)
        self.actionAll = QtWidgets.QAction(MainWindow)
        self.actionMany = QtWidgets.QAction(MainWindow)
        self.actionOne = QtWidgets.QAction(MainWindow)
        self.actionFind_Customer = QtWidgets.QAction(MainWindow)
        self.actionSave = QtWidgets.QAction(MainWindow)

        self.menuFile.addAction(self.actionNew_Factor)
        self.menuFile.addAction(self.actionNew_Goods)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionOpen_Factor)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionClose)
        self.menuCustomer.addAction(self.actionNew_Customer)
        self.menuCustomer.addAction(self.actionFind_Customer)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuCustomer.menuAction())

        self.fillComboBox()
        self.fillTable()
        self.setcustomer()
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.mysignal()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "Customer"))
        self.label_2.setText(_translate("MainWindow", "Id:"))
        self.label.setText(_translate("MainWindow", "Name:"))
        self.label_3.setText(_translate("MainWindow", "Phone:"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Tools"))
        self.label_4.setText(_translate("MainWindow", "Name:"))
        self.label_5.setText(_translate("MainWindow", "No:"))
        self.pushButtonAdd.setText(_translate("MainWindow", "Add"))
        self.pushButtonSave.setText(_translate("MainWindow", "Save"))
        self.label_6.setText(_translate("MainWindow", "Total"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuCustomer.setTitle(_translate("MainWindow", "Customer"))
        self.actionNew_Factor.setText(_translate("MainWindow", "New Factor"))
        self.actionNew_Goods.setText(_translate("MainWindow", "New Goods"))
        self.actionOpen_Factor.setText(_translate("MainWindow", "Open Factor"))
        self.actionClose.setText(_translate("MainWindow", "Close"))
        self.actionNew_Customer.setText(_translate("MainWindow", "New Customer"))
        self.actionAll.setText(_translate("MainWindow", "All"))
        self.actionMany.setText(_translate("MainWindow", "Many"))
        self.actionOne.setText(_translate("MainWindow", "One"))
        self.actionFind_Customer.setText(_translate("MainWindow", "Find Customer"))
        self.actionSave.setText(_translate("MainWindow", "Save Factor"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())