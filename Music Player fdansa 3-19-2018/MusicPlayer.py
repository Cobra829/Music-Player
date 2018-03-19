import sys
from PyQt4 import QtCore,QtGui,uic
import eyed3
import vlc
from_class=uic.loadUiType('MusicPlayerTest.ui')[0]
def meta(file):
    loaded=eyed3.load(file)
    try:title=loaded.tag.title
    except:title=file[file.rfind('/')+1:file.rfind('.')]
    try:artist=loaded.tag.artist
    except:artist=''
    try:album=loaded.tag.album
    except:album=''
    try:duration=loaded.info.time_secs
    except:duration=''
    meta=[title,album,artist,duration]
    return meta
class MyWindowClass(QtGui.QMainWindow,from_class):
    def __init__(self,parent = None):
        QtGui.QMainWindow.__init__(self,parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.play)
        self.actionOpen.triggered.connect(self.open)
    def load(self,path):
        try:self.aud.stop()
        except:None
        self.pushButton.setText('Play')
        self.aud=vlc.MediaPlayer(path)
        self.label_8.setText(meta(path)[1])
        self.label_7.setText(meta(path)[0])
        print(meta(path))
    def open(self):
        path=str(QtGui.QFileDialog.getOpenFileName())
        #self.tableWidget.setItem(1,1,self.tableWidget.item(1,1).setText('a'))
        if path!='':
            self.load(path)
    def play(self):
        if self.pushButton.text()=='Play':
            try:
                print('Playing')
                self.aud.play()
                self.pushButton.setText('Pause')
            except:None
        else:
            try:
                print('Paused')
                self.aud.pause()
                self.pushButton.setText('Play')
            except:None
app=QtGui.QApplication(sys.argv)
myWindow=MyWindowClass()
myWindow.show()
app.exec_()
