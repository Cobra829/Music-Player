#If Phonon is required: https://srinikom.github.io/pyside-docs/PySide/phonon/Phonon.VolumeSlider.html 


import sys
from PyQt4 import QtCore,QtGui,uic
import eyed3
import vlc
import pickle
import os.path

from_class=uic.loadUiType('MusicPlayerTest.ui')[0]
playlist=[]
meta=[]
curr=0
def genmeta(file):
    global meta
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
        self.actionSave_Playlist.triggered.connect(self.svlst)
        self.actionOpen_Playlist.triggered.connect(self.oplst)
        self.pushButton_5.clicked.connect(self.test)
        self.pushButton_3.clicked.connect(self.back)
        self.pushButton_6.clicked.connect(self.frwd)
        self.pushButton_7.clicked.connect(self.clr)
        #self.pushButton_2.clicked.connect(self.loop)
        self.connect(self.volumeslider,
                     QtCore.SIGNAL("valueChanged(int)"),
                     self.setVolume)
        
        '''self.positionslider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.positionslider.setToolTip("Position")
        self.positionslider.setMaximum(1000)
        self.connect(self.positionslider,
                     QtCore.SIGNAL("sliderMoved(int)"), self.setPosition)'''


#JUST GET VOLUME TO WORK FIRST




    '''def setPosition(self, position):
        """Set the position
        """
        # setting the position to where the slider was dragged
        self.mediaplayer.set_position(position / 1000.0)
        # the vlc MediaPlayer needs a float value between 0 and 1, Qt
        # uses integer variables, so you need a factor; the higher the
        # factor, the more precise are the results
        # (1000 should be enough)

    def updateUI(self):
        """updates the user interface"""
        # setting the slider to the desired position
        self.positionslider.setValue(self.mediaplayer.get_position() * 1000)

        if not self.mediaplayer.is_playing():
            # no need to call this function if nothing is played
            self.timer.stop()
            if not self.isPaused:
                # after the video finished, the play button stills shows
                # "Pause", not the desired behavior of a media player
                # this will fix it
                self.Stop()'''


    def back(self):
        global curr
        curr=(curr-1)%len(playlist)
        self.load(playlist[curr])
    def frwd(self):
        global curr
        curr=(curr+1)%len(playlist)
        self.load(playlist[curr])
    def clr(self):
        global playlist
        playlist=[playlist[curr]]
        while self.tableWidget.rowCount()>1:self.tableWidget.removeRow(0)
        self.tblupdate()
    def test(self):
        print(self.aud.is_playing())
    def tblupdate(self):
        i=0
        self.tableWidget.setRowCount(len(playlist))
        print(playlist)
        for row in playlist:
            genmeta(row)
            for col in range(4):
                self.tableWidget.setItem(i,col,QtGui.QTableWidgetItem(meta[col]))
            i+=1
    def load(self,path):
        try:self.aud.stop()
        except:None
        genmeta(path)
        self.pushButton.setText('Play')
        self.aud=vlc.MediaPlayer(path)
        self.label_7.setText(meta[0])
        self.label_8.setText(meta[1])
    def svlst(self):
        path=str(QtGui.QFileDialog.getSaveFileName())
        with open(path,'wb') as f:
            pickle.dump(playlist,f)
    def oplst(self):
        global playlist,curr
        curr=0
        path=str(QtGui.QFileDialog.getOpenFileName())
        with open(path, 'rb') as f:
            playlist=pickle.load(f)
        self.load(playlist[curr])
        self.tblupdate()
    def open(self):
        path=str(QtGui.QFileDialog.getOpenFileName())
        if path!='':
            self.load(path)
            playlist.append(path)
            self.tblupdate()
    def play(self):
        if self.pushButton.text()=='Play':
            try:
                self.aud.play()
                self.pushButton.setText('Pause')
                print('Playing')
            except:None
        else:
            try:
                self.aud.pause()
                self.pushButton.setText('Play')
                print('Paused')
            except:None
            

    def setVolume(self, Volume):
        """Set the volume
        """
        #self.volumeslider.setValue(self.aud.audio_get_volume())
        self.mediaplayer.audio_set_volume(Volume)
        
app=QtGui.QApplication(sys.argv)
myWindow=MyWindowClass()
myWindow.show()
app.exec_()
