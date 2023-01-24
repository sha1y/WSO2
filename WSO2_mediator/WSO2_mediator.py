import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QCheckBox, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore
from mediator import mediator

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'WSO2-Mediator'
        self.left = 450
        self.top = 200
        self.width = 400
        self.height = 250
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.value = "0"
        # Create label
        self.label = QLabel('API Name',self)
        self.label.move(20,0)
		
        # Create textbox
        self.textbox = QLineEdit(self)
        self.textbox.move(20,25)
        self.textbox.resize(280,50)
		
        # Create checkbox
        self.checkbox = QCheckBox("OAuth",self)
        self.checkbox.move(20,80)
        self.checkbox.stateChanged.connect(self.checkedbox)

        self.label2 = QLabel('Sub Request Path',self)
        self.label2.move(20,110)
        # Create textbox
        self.textbox2 = QLineEdit(self)
        self.textbox2.move(20,135)
        self.textbox2.resize(280,40)		

        # Create a button in the window
        self.button = QPushButton('Create mappings', self)
        self.button.move(20,190)
		
		
        # connect button to function on_click
        self.button.clicked.connect(self.on_click)
        self.show()
    
    @pyqtSlot()
    def on_click(self):
        textboxValue1 = self.textbox.text()
        textboxValue2 = self.textbox2.text()
        QMessageBox.question(self, 'Mediation creation', "File created" ,QMessageBox.Ok, QMessageBox.Ok)
        self.textbox.setText("")
        m = mediator(textboxValue1,self.value,textboxValue2);
        m.create_mediator();
        m.create_content();
        if(textboxValue2 != ""):
                m.create_mappings();
        else:
                m.direct_mapping();
        m.close_file();
			
    def checkedbox(self,state):
        if state == QtCore.Qt.Checked:
                self.value = "1"
        else:
                self.value = "0";

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())