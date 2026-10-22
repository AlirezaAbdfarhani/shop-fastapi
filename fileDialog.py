import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog


class FileOpenDialog(QWidget):

    def __init__(self):
        super().__init__()
        self.left = 100
        self.top = 100
        self.width = 700
        self.height = 500
        self.initUI()
    
    def initUI(self):
        self.setGeometry(self.left, self.top, self.width, self.height)
        
    
    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog    
        fileName , _ = QFileDialog.getOpenFileName(self,caption="find picture"
                                                       , directory=""
                                                       , filter= "All Files (*);; png (*.png);; jpg (*.jpg)"
                                                       )
        if fileName:
            return fileName
        else:
            return None    
          
    
    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"Open Files", "","Text Files (*.txt);;All Files (*)", options=options)
        if files:
            print(files)
    
    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"Save File","","Text Files (*.txt)", options=options)
        if fileName:
            return fileName
        else:
            return None  

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileOpenDialog()
    ex.show()
    sys.exit(app.exec_())