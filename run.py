from PyQt5 import QtWidgets, QtGui,QtCore
from PyQt5.QtGui import QMovie
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import pyttsx3
import speech_recognition as sr
import os
import time
import webbrowser
import datetime


flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint)




engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)
engine.setProperty('rate',120)



    

class mainT(QThread):
    status=pyqtSignal(str)
    doctor=pyqtSignal(str)
    user=pyqtSignal(str)
    
    
    def __init__(self):
            super(mainT,self).__init__()
    

    def speak(self,audio):
        self.doctor.emit("Dr Gideon :- "+audio)
        engine.say(audio)
        engine.runAndWait()

    def wish(self):
        hour = int(datetime.datetime.now().hour)
        
        if hour>=0 and hour <12:
            self.speak("Good morning")
        elif hour>=12 and hour<18:
            self.speak("Good Afternoon")
        else:
            self.speak("Good evening")

        self.speak(" My name is Doctor gedion and i am  AI created to help you diagnose possible diseases base on the symptoms ")

    
    def run(self):
        self.commands()
    
    def STT(self):
        R = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...........")
            self.status.emit("Listening...........")
          
            audio = R.listen(source)
        try:
            print("Recog......")
            self.status.emit("Recog......")
          
            text = R.recognize_google(audio,language='en-in')
            print(">> ",text)
        except Exception:
            self.speak("Sorry Speak Again")
            return "None"
        text = text.lower()
        self.user.emit("User :- "+text)
        return text

    def commands(self):
        self.wish()
        while True:
            self.query = self.STT()
            if 'goodbye' in self.query:
                sys.exit()
            elif 'open google' in self.query:
                self.speak("Sure sir, what should i search on google?")
                sc=self.STT().lower()
                self.speak("Searching google for "+sc)
                url= "https://www.google.com/search?q="+sc
                webbrowser.open(url)
                self.speak("opening google")

            elif 'doctor' in self.query:
                self.checkup()
            else:
                self.speak("again!!")
    
    
    def checkup(self):
        self.speak("OKay sir Please list all the symptoms you are facing ")
        self.sym=self.STT()
        if self.sym in ('cold' or 'cough' or  'sore throat'):
            self.speak("You might be having a case of Common cold ")
            self.speak("i advice you to ")
            self.speak("Sip warm liquids  or")
            self.speak("Soothe a sore throat that is A saltwater gargle — 1/4 to 1/2 teaspoon salt dissolved in an 8-ounce glass of warm water — can temporarily relieve a sore or scratchy throat.")
            self.speak("Please take care of your self")
        else:
            self.speak("Sorry i was not able to find correct diseases the following symptoms")
        


            
      




FROM_MAIN,_ = loadUiType(os.path.join(os.path.dirname(__file__),"./AI.ui"))

class Main(QMainWindow,FROM_MAIN):
    def __init__(self,parent=None):
        super(Main,self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(1920,1080)

        self.exitB.setStyleSheet("background-image:url(./img/exit - Copy.png);\n"
        "border:none;")
        self.exitB.clicked.connect(self.close)
        self.setWindowFlags(flags)

        self.movie= QMovie("./img/unscreen")
        self.label_5.setMovie(self.movie)
    
        self.movie1= QMovie("./img/gify")
        self.label_4.setMovie(self.movie1)

        self.movie2= QMovie("./img/gify")
        self.label_3.setMovie(self.movie1)

        self.movie3= QMovie("./img/init")
        self.label_9.setMovie(self.movie3)

        self.startAnimation()
        self.Dspeak=mainT()
        self.startTask()
        self.Dspeak.status.connect(self.statusUpdate)
        self.Dspeak.doctor.connect(self.doctorUpdate)
        self.Dspeak.user.connect(self.userUpdate)
        
    def statusUpdate(self,string):
        self.statusL.setText(string)

    def doctorUpdate(self,string):
        self.gideonL.setText(string)
    
    def userUpdate(self,string):
        self.userL.setText(string)
    
    
    def startTask(self):
        self.Dspeak.start()
        

    def startAnimation(self):
        self.movie.start()
        self.movie1.start()
        self.movie2.start()
        self.movie3.start()
  
    def stopAnimation(self):
        self.movie.stop()
        self.movie1.stop()
        self.movie2.stop()
        self.movie3.stop()


app = QtWidgets.QApplication(sys.argv)
main = Main()
main.show()
exit(app.exec_())