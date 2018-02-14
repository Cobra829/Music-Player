import sys
from PyQt4 import QtCore,QtGui,uic
import eyed3
import vlc
path='I:\Music-Player-master\Kalimba.mp3'
aud=vlc.MediaPlayer(path)
from_class=uic.loadUiType('MusicPlayerTest.ui')[0]
curr=eyed3.load(path)
class MyWindowClass(QtGui.QMainWindow,from_class):
    def __init__(self,parent = None):
        QtGui.QMainWindow.__init__(self,parent)
        self.setupUi(self)
        a=curr.tag.artist+' - '+curr.tag.title
        self.label_7.setText(a)
        self.label_8.setText(curr.tag.album)
        self.pushButton.clicked.connect(self.play)
        self.actionOpen.triggered.connect(self.a)
    def a(self):
        print('hello world')
    def play(self):
        if self.pushButton.text()=='Play':
            print('Playing')
            aud.play()
            self.pushButton.setText('Pause')
        else:
            print('Paused')
            aud.pause()
            self.pushButton.setText('Play')
app=QtGui.QApplication(sys.argv)
myWindow=MyWindowClass()
myWindow.show()
app.exec_()
