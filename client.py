from PyQt5.QtWidgets import QWidget, QApplication, QStyleFactory, QPushButton, QVBoxLayout, QFileDialog, QListWidget, QListWidgetItem, QLabel, QAbstractItemView
from PyQt5 import QtGui,QtCore
import sys
import PyPDF2

class DragAndDropList(QListWidget):
    itemMoved = QtCore.pyqtSignal(int, int, QListWidgetItem) # Old index, new index, item

    def __init__(self, parent=None, **args):
        super(DragAndDropList, self).__init__(parent, **args)

        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.drag_item = None
        self.drag_row = None

    def dropEvent(self, event):
        super(DragAndDropList, self).dropEvent(event)
        self.itemMoved.emit(self.drag_row, self.row(self.drag_item),self.drag_item)
        self.drag_item = None

    def startDrag(self, supportedActions):
        self.drag_item = self.currentItem()
        self.drag_row = self.row(self.drag_item)
        super(DragAndDropList, self).startDrag(supportedActions)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.lw = DragAndDropList()
        # self.lw.dragEnabled = True
        # self.lw.itemPressed.connect(lambda x: print(x.text()))
        btn = QPushButton()
        btn2 = QPushButton()
        btn.setText('Add Files')
        btn2.setText('CreatePDF')
        btn.clicked.connect(self.browse)
        btn2.clicked.connect(self.create_pdf)
        l = QVBoxLayout()
        l.addWidget(btn)
        l.addWidget(self.lw)
        l.addWidget(btn2)
        self.setLayout(l)
        self.setGeometry(750,200,500,250)
        self.setWindowTitle('PDFTools')
        self.show()
    
    def browse(self):
        file_names = QFileDialog.getOpenFileNames(self,'Select Files','.','*.pdf')
        file_names = list(file_names)[0]
        self.lw.addItems(file_names)

    def create_pdf(self):
        merger = PyPDF2.PdfFileMerger()
        for index in range(self.lw.count()):
            pdf = (self.lw.item(index).text())    
            merger.append(open(pdf, 'rb'))
            
        with open('output.pdf','wb') as file:
            merger.write(file)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("fusion"))
    main = MainWindow()
    sys.exit(app.exec_())