#################################################

#packing to exe command: pyinstaller -F  AutoReview_main.py

#################################################

import os
import sys
import glob
from PyQt5.QtCore import Qt, QRect
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QToolButton, QPushButton, QLineEdit, QMessageBox, QLabel, QFileDialog
import AutoReview_Script as AutoReview_Script
# import AutoReview_Spec as AutoReview_Spec
# import AutoReview_Summ as AutoReview_Summ
from datetime import datetime
#from timeit import default_timer as timer

#################################################


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Auto Review Tool'
        self.setWindowIcon(QtGui.QIcon('github.ico'))
        self.initUI()


 #################################################


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(10, 10, 550, 330)

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
        self.label.setFont(QtGui.QFont('MS San Serif', 8))
        self.label.setAlignment(Qt.AlignLeft)
        self.label.setGeometry(QRect(25, 40, 0, 0))
        self.label.adjustSize()

        # insert PYTHON logo
        self.github = QLabel(self)
        self.github.pic = QtGui.QPixmap('Octocat.png')
        self.github.setPixmap(self.github.pic)
        self.github.setGeometry(QRect(325, 135, 0, 0))
        self.github.adjustSize()
        self.github.show()

        # Create textbox
        self.textbox = QLineEdit(self)
        self.textbox.setGeometry(QRect(25, 130, 275, 32))
        self.textbox.setText("C:/Users/tuanp/Desktop/Dem/Com_Section3_4/rba/TEST/ComServices/Com")
        
        #Create Browse directory button
        self.button_browse = QToolButton(self)
        self.button_browse.setText('...')
        self.button_browse.setGeometry(QRect(320, 130, 32, 32))
        self.button_browse.clicked.connect(self.browse_root_dir)

        # Create Review Script button
        self.button_script = QPushButton('Review Test Script', self)
        self.button_script.setGeometry(QRect(25, 190, 120, 35))
        self.button_script.clicked.connect(self.Review_Test_Script)

        # Create Review Spec button
        self.button_spec = QPushButton('Review Test Spec', self)
        self.button_spec.setGeometry(QRect(180, 190, 120, 35))
        self.button_spec.clicked.connect(self.Review_Test_Spec)

        # Create Review Summary button
        self.button_summ = QPushButton('Review Test Summ', self)
        self.button_summ.setGeometry(QRect(25, 250, 120, 35))
        self.button_summ.clicked.connect(self.Review_Test_Summ)

        #Create open newest .txt file
        self.button_open = QPushButton('Open Report', self)
        self.button_open.setGeometry(QRect(180, 250, 120, 35))
        self.button_open.setEnabled(False)
        self.button_open.clicked.connect(Open_latest_report)


        self.move(500, 200)
        self.show() 


#################################################


    def browse_root_dir(self):
        try:
            self.input_directory = QFileDialog.getExistingDirectory(None, 'Select folder:')
            self.textbox.setText(self.input_directory)

        except Exception as e:
            messagebox.showinfo('Auto Review Tool', e)

           
#################################################


    def Review_Test_Script(self):
        root_dir = self.textbox.text()
        if (root_dir == ""):
            QMessageBox.warning(self, 'Auto Review Tool', 'Plese input a directory')
        else:
            report_name = getReportName(root_dir, "Script")
            AutoReview_Script.main_Script(root_dir, report_name)
            self.button_open.setEnabled(True)
            QMessageBox.warning(self, 'Auto Review Tool', 'Review Test Script done !')
           

#################################################


    def Review_Test_Spec(self):
        root_dir = self.textbox.text()
        if (root_dir == ""):
            QMessageBox.warning(self, 'Auto Review Tool', 'Plese input a directory')
        else:
            report_name = getReportName(root_dir, "Spec")
            AutoReview_Spec.main_Spec(root_dir, report_name)
            self.button_open.setEnabled(True)
            QMessageBox.warning(self, 'Auto Review Tool', 'Review Test Spec done !')


    def Review_Test_Summ(self):
        root_dir = self.textbox.text()
        if (root_dir == ""):
            QMessageBox.warning(self, 'Auto Review Tool', 'Plese input a directory')
        else:
            if (CheckNumberofFiles(root_dir)):
                report_name = getReportName(root_dir, "Summ")
                AutoReview_Spec.main_Spec(root_dir, report_name)
                self.button_open.setEnabled(True)
                QMessageBox.warning(self, 'Auto Review Tool', 'Review Test Summ done !')

            else:
                QMessageBox.warning(self, 'Auto Review Tool', 'The tool can not continue...')


#################################################


def getReportName(roor_dir, report_type):

    #get Component name
    try:
        inverse_dir = roor_dir[::-1]
        first_slash_index = inverse_dir.index("/")
        component_name = inverse_dir[:first_slash_index]
        component_name = component_name[::-1]
    except Exception as e:
        component_name = "default"

    #get datetime
    time = str(datetime.now().strftime("%H%M%S"))

    #Report name
    report_name = "Review_" + report_type + "_" + component_name + "_" + time + ".txt"
    return report_name


#################################################


def Open_latest_report():
    latest_file = max(glob.glob('*.txt'), key=os.path.getctime)
    os.system("start notepad.exe " + latest_file)
           

#################################################


def CheckNumberofFiles(dir):
    directory_Spec = dir + "/01_TestSpecification"
    directory_Summ = dir + "/04_TestReportSummary"
    directory_Rep = dir + "/03_TestReport"
    Spec_files_count = 0
    Summ_files_count = 0
    Rep_files_count = 0

    Spec_files_count = countNumberofFiles(directory_Spec)
    Rep_files_count = countNumberofFiles(directory_Rep)
    Summ_files_count = countNumberofFiles(directory_Summ)

    if ((Spec_files_count == Summ_files_count) and (Summ_files_count == Rep_files_count)):
        print("The numbers of files in 3 folders (01_ , 03_ , 04_) are the same \nStart Auto Review...")
        return 1
    else:
        QMessageBox.warning(None, 'Auto Review Tool', 'The numbers of files in 3 folders are different')
        return 0


#################################################


def countNumberofFiles(dir):
    count = 0
    for root, dirs, files in os.walk(dir):
        for filename in files:
            if not (filename[0:2] == '~$'): #check for temporary if file is opening
                count += 1
    return count


#################################################


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyle('fusion')
    ex = App()
    sys.exit(app.exec_())

