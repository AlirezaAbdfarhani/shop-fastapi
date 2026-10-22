from PyQt5 import QtCore, QtGui, QtWidgets
from crud.database import database


class Ui_OpenFactorDialog(object):
    def setupUi(self, Dialog):
        self.dialog = Dialog
        Dialog.setObjectName("OpenFactorDialog")
        Dialog.resize(750, 500)
        Dialog.setWindowTitle("Open Factor")

        self.db = database()

        self.labelList = QtWidgets.QLabel(Dialog)
        self.labelList.setGeometry(QtCore.QRect(20, 10, 200, 25))
        self.labelList.setText("Factors List:")

        self.tableFactors = QtWidgets.QTableWidget(Dialog)
        self.tableFactors.setGeometry(QtCore.QRect(20, 40, 710, 180))
        self.tableFactors.setColumnCount(5)
        self.tableFactors.setHorizontalHeaderLabels(
            ['ID', 'Customer', 'Date', 'Total', 'Items']
        )
        self.tableFactors.setSelectionBehavior(
            QtWidgets.QTableWidget.SelectRows
        )
        self.tableFactors.setEditTriggers(
            QtWidgets.QTableWidget.NoEditTriggers
        )

        self.labelDetails = QtWidgets.QLabel(Dialog)
        self.labelDetails.setGeometry(QtCore.QRect(20, 230, 200, 25))
        self.labelDetails.setText("Factor Details:")

        self.tableItems = QtWidgets.QTableWidget(Dialog)
        self.tableItems.setGeometry(QtCore.QRect(20, 260, 710, 180))
        self.tableItems.setColumnCount(4)
        self.tableItems.setHorizontalHeaderLabels(
            ['Product ID', 'Quantity', 'Unit Price', 'Sum']
        )
        self.tableItems.setEditTriggers(
            QtWidgets.QTableWidget.NoEditTriggers
        )

        self.pushButtonRefresh = QtWidgets.QPushButton(Dialog)
        self.pushButtonRefresh.setGeometry(QtCore.QRect(20, 455, 120, 32))
        self.pushButtonRefresh.setText("Refresh")

        self.pushButtonDelete = QtWidgets.QPushButton(Dialog)
        self.pushButtonDelete.setGeometry(QtCore.QRect(150, 455, 120, 32))
        self.pushButtonDelete.setText("Delete")

        self.pushButtonClose = QtWidgets.QPushButton(Dialog)
        self.pushButtonClose.setGeometry(QtCore.QRect(610, 455, 120, 32))
        self.pushButtonClose.setText("Close")

        self.pushButtonRefresh.clicked.connect(self.loadFactors)
        self.pushButtonDelete.clicked.connect(self.deleteFactor)
        self.pushButtonClose.clicked.connect(Dialog.close)
        self.tableFactors.cellClicked.connect(self.loadFactorDetails)

        self.loadFactors()

    def loadFactors(self):
        factors = self.db.find_all_factors()
        self.tableFactors.setRowCount(len(factors))

        for row, factor in enumerate(factors):
            customer_id = factor.get('customer_id')
            customer = self.db.find_customer_by_id(customer_id)
            customer_name = (
                customer.get('username', f"ID {customer_id}")
                if customer else f"ID {customer_id}"
            )

            self._setCell(row, 0, str(factor.get('id', '')))
            self._setCell(row, 1, customer_name)
            self._setCell(row, 2, str(factor.get('date', ''))[:19])
            self._setCell(row, 3, str(factor.get('total', 0)))
            self._setCell(row, 4, str(len(factor.get('items', []))))

    def _setCell(self, row, col, text):
        item = QtWidgets.QTableWidgetItem()
        item.setText(text)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableFactors.setItem(row, col, item)

    def loadFactorDetails(self, row, col):
        item = self.tableFactors.item(row, 0)
        if not item:
            return
        factor_id = int(item.text())
        factor = self.db.find_factor_by_id(factor_id)
        if not factor:
            return

        items = factor.get('items', [])
        self.tableItems.setRowCount(len(items))

        for i, it in enumerate(items):
            self._setItemCell(i, 0, str(it.get('product_id', '')))
            self._setItemCell(i, 1, str(it.get('no', 0)))
            self._setItemCell(i, 2, str(it.get('fee', 0)))
            self._setItemCell(i, 3, str(it.get('sum_fee', 0)))

    def _setItemCell(self, row, col, text):
        item = QtWidgets.QTableWidgetItem()
        item.setText(text)
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableItems.setItem(row, col, item)

    def deleteFactor(self):
        row = self.tableFactors.currentRow()
        if row < 0:
            QtWidgets.QMessageBox.warning(
                self.dialog, "Warning",
                "Please select a factor first"
            )
            return

        item = self.tableFactors.item(row, 0)
        if not item:
            return
        factor_id = int(item.text())

        reply = QtWidgets.QMessageBox.question(
            self.dialog, "Confirm Delete",
            f"Delete factor #{factor_id}?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
        )
        if reply != QtWidgets.QMessageBox.Yes:
            return

        ok = self.db.delete_factor(factor_id)
        if ok:
            QtWidgets.QMessageBox.information(
                self.dialog, "Deleted",
                f"Factor #{factor_id} deleted"
            )
            self.tableItems.setRowCount(0)
            self.loadFactors()
        else:
            QtWidgets.QMessageBox.warning(
                self.dialog, "Error",
                "Failed to delete factor"
            )


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_OpenFactorDialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())