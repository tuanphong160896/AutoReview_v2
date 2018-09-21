#################################################

#packing to exe command: pyinstaller -F  AutoReview_main.py

#################################################

import os
import sys
import glob
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QLineEdit, QMessageBox, QLabel, QFileDialog
from win32api import GetSystemMetrics
import AutoReview_Script as AutoReview_Script
import AutoReview_Spec as AutoReview_Spec
import AutoReview_Summ as AutoReview_Summ

#################################################


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Auto Review Tool'
        self.setWindowIcon(QtGui.QIcon('github.ico'))
        self.MonitorWidth = GetSystemMetrics(0)
        self.MonitorHeight = GetSystemMetrics(1)
        self.left = int(self.MonitorWidth/100)
        self.top = int(self.MonitorWidth/100)
        self.width = int(self.MonitorWidth / 3.1)
        self.height = int(self.MonitorWidth / 5.5)
        self.initUI()

 #################################################

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.unit_size = int((self.MonitorWidth)/250)

        #create Menu
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        editMenu = mainMenu.addMenu('Edit')
        viewMenu = mainMenu.addMenu('View')
        searchMenu = mainMenu.addMenu('Search')
        toolsMenu = mainMenu.addMenu('Tools')
        helpMenu = mainMenu.addMenu('Help')

        # Create label
        instruction_text = "1. Click on the Browse directory button.\n\n" + \
                           "2. Choose the directory which contains 01_, 02_, 03_, 04_ folders.\n\n" + \
                           "3. Click on any Review button: Test Script, Test Spec or Test Summary."
 
        self.label = QLabel(instruction_text, self)
        self.label.setFont(QtGui.QFont('MS San Serif', 9))
        self.label.move((self.unit_size)*4,(self.unit_size)*6)
        self.label.setAlignment(Qt.AlignLeft)
        self.label.adjustSize()

        #insert PYTHON logo
        self.github = QLabel(self)
        self.github.pic = QtGui.QPixmap('Octocat.png')
        self.github.setPixmap(self.github.pic)
        self.github.adjustSize()
        self.github.move((self.unit_size)*58,(self.unit_size)*22)
        self.github.show()

        # Create textbox
        self.textbox = QLineEdit(self)
        self.textbox.move((self.unit_size)*4, (self.unit_size)*21)
        self.textbox.resize((self.unit_size)*48, (self.unit_size)*6)
        
        # Create Browse directory button
        self.button_browse = QPushButton('Browse directory', self)
        self.button_browse.move((self.unit_size)*4, (self.unit_size)*30)
        self.button_browse.resize((self.unit_size)*21, (self.unit_size)*5)
        self.button_browse.setStyleSheet("border-style: solid; border-color: #0986ED; border-width: 2px;");
        self.button_browse.clicked.connect(self.browse_root_dir)

        # Create Review Script button
        self.button_script = QPushButton('Review Test Script', self)
        self.button_script.move((self.unit_size)*31, (self.unit_size)*30)
        self.button_script.resize((self.unit_size)*21, (self.unit_size)*5)
        self.button_script.setStyleSheet("border-style: solid; border-color: #0986ED; border-width: 2px;");
        self.button_script.setEnabled(False)
        self.button_script.clicked.connect(self.Review_Test_Script)

        # Create Review Spec button
        self.button_spec = QPushButton('Review Test Spec', self)
        self.button_spec.move((self.unit_size)*4, (self.unit_size)*37)
        self.button_spec.resize((self.unit_size)*21, (self.unit_size)*5)
        self.button_spec.setStyleSheet("border-style: solid; border-color: #0986ED; border-width: 2px;");
        self.button_spec.setEnabled(False)
        self.button_spec.clicked.connect(self.Review_Test_Spec)

        # Create Review Summary button
        self.button_summ = QPushButton('Review Test Summary', self)
        self.button_summ.move((self.unit_size)*31, (self.unit_size)*37)
        self.button_summ.resize((self.unit_size)*21, (self.unit_size)*5)
        self.button_summ.setStyleSheet("border-style: solid; border-color: #0986ED; border-width: 2px;");
        self.button_summ.setEnabled(False)
        self.button_summ.clicked.connect(self.Review_Test_Summ)

        #Create open newest .txt file
        self.button_open = QPushButton('Open', self)
        self.button_open.move((self.unit_size)*54, (self.unit_size)*21)
        self.button_open.resize((self.unit_size)*21, (self.unit_size)*6)
        self.button_open.resize(55,36)
        self.button_open.setEnabled(False)
        self.button_open.clicked.connect(self.Open_latest_report)

        self.move(self.width, self.height)
        self.show() 

#################################################

    def browse_root_dir(self):
        try:
            self.input_directory = QFileDialog.getExistingDirectory(None, 'Select folder:')
            self.textbox.setText(self.input_directory)
            print(sys.argv[:])
        except Exception as e:
            messagebox.showinfo('Auto Review Tool', e)

        if (self.input_directory != ""):
            self.button_script.setEnabled(True)
            self.button_spec.setEnabled(True)
            self.button_summ.setEnabled(True)
           
#################################################

    def Review_Test_Script(self):
        if (self.input_directory == ""):
            QMessageBox.warning(self, 'Auto Review Tool', 'Plese input a directory')
        else:
            AutoReview_Script.main_Script(self.input_directory)
            self.button_open.setEnabled(True)
           
#################################################

    def Review_Test_Spec(self):
        if (self.input_directory == ""):
            QMessageBox.warning(self, 'Auto Review Tool', 'Plese input a directory')
        else:
            AutoReview_Spec.main_Spec(self.input_directory)
            self.button_open.setEnabled(True)

    def Review_Test_Summ(self):
        if (self.input_directory == ""):
            QMessageBox.warning(self, 'Auto Review Tool', 'Plese input a directory')
        else:
            if (CheckNumberofFiles(self.input_directory)):
                AutoReview_Summ.main_Summ(self.input_directory)
                self.button_open.setEnabled(True)
            else:
                QMessageBox.warning(self, 'Auto Review Tool', 'Can not continue...')

    def Open_latest_report(self):
        latest_file = max(glob.iglob('*.txt'), key=os.path.getctime)
        os.system("start notepad.exe " + latest_file)
        latest_file = ""
           
#################################################

def CheckNumberofFiles(dir):
    directory_Spec = dir + "/01_TestSpecification"
    directory_Summ = dir + "/04_TestReportSummary"
    directory_Rep = dir + "/03_TestReport"
    Spec_files_count = 0
    Summ_files_count = 0
    Rep_files_count = 0

    Spec_files_count = len(next(os.walk(directory_Spec))[2])
    Rep_files_count = len(next(os.walk(directory_Rep))[2])
    Summ_files_count = len(next(os.walk(directory_Summ))[2])

    if ((Spec_files_count == Summ_files_count) and (Summ_files_count == Rep_files_count)):
        print("The numbers of files in 3 folders (01_ , 03_ , 04_) are the same \nStart Auto Review...")
        return 1
    else:
        QMessageBox.warning(None, 'Auto Review Tool', 'The numbers of files in 3 folders are different')
        return 0

#################################################

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyle('fusion')
    ex = App()
    sys.exit(app.exec_())

