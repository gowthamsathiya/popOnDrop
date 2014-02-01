"""
__author__ = Gowtham
__summary__ = simple GUI application to save file to dropbox as such or save as encrypted one. One more process calls main.py and run in the background to capture any file updates or addition to the dropbox which is of type ".doc" or ".txt"
__copyright__ = GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
"""

#import necessary python modules
import os,sys
from multiprocessing import Process

#import pyQt4 necessary modules
from PyQt4 import QtGui,Qt,QtCore

#import dropbox module
import dropbox

#import submodules
import Accesstoken
from upload import upload
from edecrypt_ import edecrypt_ as edecrypt
from main import popMessage


#Label class to inherit QtLabel and add own dropEvent handler
class Label(QtGui.QLabel):

    def __init__(self, title, parent):
        super(Label, self).__init__(title, parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat('text/plain'):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e): #Method To handle dropped file to upload to dropbox
        filepath = e.mimeData().text().replace("file://","")
        for url in e.mimeData().urls():
            localfilepath = url.toLocalFile()
            strfilepath = ""
            for x in localfilepath:
                strfilepath += str(x) #to convert from QString to str of python
            if encryptradiobox.isChecked():
                optstrfilepath = edecrypt('encrypt',strfilepath) #returns encrypted file path
                response = upload(client,optstrfilepath) # upload encrypted file to dropbox
            elif decryptradiobox.isChecked():
                optstrfilepath = edecrypt('decrypt',strfilepath) #returns encrypted file path
            else:
                response = upload(client,strfilepath) #uploads file to dropbox without any encryption

#start popMessage module from main.py to run in background to capture **updates/**addition/deletion to files in dropbox.
#**handles only .txt .doc files
p1 = Process(target= popMessage)
p1.start()

#accesstoken to authenticate dropbox access
access_token = Accesstoken.getaccesstoken()
client = dropbox.client.DropboxClient(access_token)

#Qt GUI generation
app = QtGui.QApplication(sys.argv)
window = QtGui.QWidget()
window.setGeometry(0, 0, 330, 200)

#additing inherited label to QWidget of the application
pic = Label("Label",window)
pic.setGeometry(0,0, 500, 200)
imagemap = QtGui.QPixmap(os.getcwd() + "/dragndrop.png") #adding image to label
pic.setPixmap(imagemap)
pic.setAcceptDrops(True) #to accept drop event over label

edecryptbuttongroup = QtGui.QButtonGroup(window)

encryptradiobox = QtGui.QRadioButton("Encrypt and \nsave",window)
encryptradiobox.setGeometry(210,50,130,50)
edecryptbuttongroup.addButton(encryptradiobox)

decryptradiobox = QtGui.QRadioButton("Decrypt",window)
decryptradiobox.setGeometry(210,110,130,50)
edecryptbuttongroup.addButton(decryptradiobox)

window.show()
sys.exit(app.exec_())