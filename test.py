from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, Qt, QTime, QDateTime, QRect
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QDesktopWidget, QLabel, QTimeEdit, \
    QComboBox, QTextEdit, QMainWindow, QWidget, QFileDialog
from PyQt5.QtGui import QImage, QPixmap, QFont, QScreen

import os
import webbrowser
import sys
import pyautogui
import pyperclip

from playsound import playsound
import speech_recognition as sr
import time
import datetime
import smtplib
import requests
import urllib
from time import strftime
import time
import pyttsx3
from bs4 import BeautifulSoup
import threading

from twilio.rest import Client
import sys
import cv2
from googletrans import Translator
import openai

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt

import cv2
import mediapipe as mp
import numpy as np
import time
import threading
import pyautogui, sys

# API SMS
global text, dock, ID
ID = 2
text = ""
dock = 0
Short_ = ["vi", "en", "zh-CN"]
full_ = ["Tiếng Việt", "English", "Chinese"]
id_voices_combo = [2, 0, 1]
# 2 tiếng việt, 1 tiếng trung, 0 tiếng anh
bot = pyttsx3.init()
voices = bot.getProperty("voices")

model = "text-davinci-003"  # "code-davinci-002"#"text-davinci-003"
dich = Translator()

mp_drawing = mp.solutions.drawing_utils
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5,
                                  min_tracking_confidence=0.5)

LEFT_EYE = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
RIGHT_EYE = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246]
LEFT_IRIS = [474, 475, 476, 477]
RIGHT_IRIS = [469, 470, 471, 472]

bli_leftx = []
bli_lefty = []
bli_rightx = []
bli_righty = []

with open("apikey.txt", "r") as f:
    openai.api_key = f.readline()


def speak(text):
    global content, ID
    if ID == 0:
        text = dich.translate(src="vi", dest="en", text=text)
        text = text.text
    bot.setProperty("voice", voices[ID].id)
    content = text
    print("Bot: " + text)
    bot.say(text)
    bot.runAndWait()


# Chức năng chuyển âm thanh thành văn bản
def get_audio():
    global text, ID
    r = sr.Recognizer()
    speech = "vi-VN"
    if ID == 0:
        speech = "en"
    with sr.Microphone() as source:
        print("Tôi: ", end='')
        audio = r.listen(source, phrase_time_limit=5)
        try:
            text = r.recognize_google(audio, language=speech)
            print(text)
            return text
        except:
            print(". . .")
            return 0


#
def get_text():
    global text, check
    for i in range(100):  # thời gian nói
        text = get_audio()
        # if check == False:
        #     exit(0)
        if text:
            return text.lower()
        # elif i < 20:
        # speak("Bot không nghe rõ. Bạn nói lại được không!")
    time.sleep(1)
    return 0


# Chức năng giao tiếp, chào hỏi

# Chức năng hiển thị thời gian
def get_time(content):
    now = datetime.datetime.now()
    if "giờ" in content or "time" in content:
        speak('Bây giờ là %d giờ %d phút' % (now.hour, now.minute))

    elif "ngày" in content or "day" in content:
        speak("Hôm nay là ngày %d tháng %d năm %d" %
              (now.day, now.month, now.year))
    else:
        speak("Bot chưa hiểu ý của bạn. Bạn nói lại được không?")


# Chức năng mở ứng dụng hệ thống, website và chức năng tìm kiếm từ khóa trên Google
def open_application(text):
    if "bàn phím" in text or "keyboard" in text:
        speak("Bàn phím máy tính đã được bật")
        os.startfile("C:\\WINDOWS\\system32\\osk.exe")
    elif "google" in text:
        speak("Google Chrome đã được mở")
        os.startfile("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
    elif "powerpoint" in text:
        speak("Powerpoint của bạn đã được bật")
        os.startfile("C:\\Program Files (x86)\\Microsoft Office\root\\Office16\\POWERPNT.EXE")
    elif "excel" in text:
        speak("Excel của bạn đã được bật")
        os.startfile("C:\\Program Files (x86)\\Microsoft Office\\root\\Office16\\EXCEL.EXE")
    else:
        speak("Ứng dụng chưa được cài đặt. Bạn hãy thử lại!")


# Chức năng dự báo thời tiết
def current_weather():
    speak("Bạn muốn xem thời tiết ở đâu ạ.")
    ow_url = "http://api.openweathermap.org/data/2.5/weather?"
    city = get_text()
    if not city:
        pass
    api_key = "fe8d8c65cf345889139d8e545f57819a"
    call_url = ow_url + "appid=" + api_key + "&q=" + city + "&units=metric"
    response = requests.get(call_url)
    data = response.json()
    if data["cod"] != "404":
        city_res = data["main"]
        current_temperature = city_res["temp"]
        current_pressure = city_res["pressure"]
        current_humidity = city_res["humidity"]
        suntime = data["sys"]
        sunrise = datetime.datetime.fromtimestamp(suntime["sunrise"])
        sunset = datetime.datetime.fromtimestamp(suntime["sunset"])
        wthr = data["weather"]
        weather_description = wthr[0]["description"]
        now = datetime.datetime.now()
        content = """
        Hôm nay là ngày {day} tháng {month} năm {year}
        Mặt trời mọc vào {hourrise} giờ {minrise} phút
        Mặt trời lặn vào {hourset} giờ {minset} phút
        Nhiệt độ trung bình là {temp} độ C
        Áp suất không khí là {pressure} héc tơ Pascal
        Độ ẩm là {humidity}%
        Trời hôm nay quang mây. Dự báo mưa rải rác ở một số nơi.""".format(day=now.day, month=now.month, year=now.year,
                                                                           hourrise=sunrise.hour,
                                                                           minrise=sunrise.minute,
                                                                           hourset=sunset.hour, minset=sunset.minute,
                                                                           temp=current_temperature,
                                                                           pressure=current_pressure,
                                                                           humidity=current_humidity)
        speak(content)
        time.sleep(15)
    else:
        speak("Không tìm thấy địa chỉ của bạn")


def get_response_from_chatgpt():
    quest = get_text()
    response = openai.Completion.create(
        engine=model,
        prompt=quest,
        max_tokens=1024,
        n=1,
        temperature=0.5
    )

    response_text = response.choices[0].text
    return response_text


# Kết hợp tất cả chức năng Trợ lý ảo Tiếng Việt
def assistant():
    # wikipedia.set_lang('vi')
    # language = 'vi'
    global check, text
    check = True
    text = "Chào bạn"
    if text:
        speak(text)
        while check == True:
            text = get_text()
            # text=input()
            if "dừng" in text or "tạm biệt" in text or "chào robot" in text or "bye" in text:
                sys.exit(0)
            elif "mấy giờ" in text or "time" in text:
                get_time(text)
            elif "hỏi" in text or "question" in text or "ask" in text:
                speak("bạn muốn hỏi về vấn đề gì")
                # quest = get_text()
                speak(get_response_from_chatgpt())
            elif "mở" in text or "open" in text:
                open_application(text)
            elif "thời tiết" in text or "weather" in text:
                current_weather()
            else:
                pass
                # speak("Bạn cần Bot giúp gì ạ?")
            # print("xin chao")


class dock_bar(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        screen = QDesktopWidget().screenGeometry()

        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        s_width = 577
        s_height = 20
        self.setGeometry((screen.width() - s_width) / 2, 0, s_width, s_height)
        self.setObjectName("MainWindow")
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.but_dock = QtWidgets.QPushButton(self.centralwidget)
        self.but_dock.setGeometry(QtCore.QRect(-80, 0, 691, 51))
        self.but_dock.setStyleSheet("background-color:rgba(114, 148, 172, 255)")
        self.but_dock.setText("")
        self.but_dock.setObjectName("dock")
        self.but_dock.clicked.connect(self.open_UI_2)

        self.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(self)
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("dock_bar", "MainWindow"))

    def open_UI_2(self):
        global dock
        dock = dock + 1
        self.ui2 = mainUI_2()
        if (dock % 2 == 1):
            self.ui2.show()
        else:
            self.ui2.hide()


class mainUI_2(QtWidgets.QMainWindow):
    def __init__(self):
        # value
        super().__init__()
        screen = QDesktopWidget().screenGeometry()
        s_width = 1293
        s_height = 140
        # Display & size of display
        self.setObjectName("UI_2")
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setGeometry((screen.width() - s_width) / 2, 20, s_width, s_height)

        # UI_2.resize(1293, 169)
        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(40, 20, 151, 101))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("background-color:rgba(117, 249, 77, 210);\n"
                                      "border-radius: 40px;")

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("picture/picUI2/icons8-home-50.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, -10, 1441, 201))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("picture/picUI2/background.png"))
        self.label.setObjectName("label")

        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QtCore.QSize(50, 50))
        self.pushButton.setCheckable(False)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.open_UI_1)

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(210, 20, 161, 101))
        self.pushButton_2.setStyleSheet("background-color:rgba(12, 87, 118, 255);\n"
                                        "border-radius: 40px;")
        self.pushButton_2.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("picture/picUI2/icons8-keyboard-90.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_2.setIcon(icon1)
        self.pushButton_2.setIconSize(QtCore.QSize(140, 140))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.open_keyboard)

        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(390, 20, 161, 101))
        self.pushButton_3.setStyleSheet("background-color:rgba(12, 87, 118, 255);\n"
                                        "border-radius: 40px;")
        self.pushButton_3.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("picture/picUI2/icons8-chat-100.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_3.setIcon(icon2)
        self.pushButton_3.setIconSize(QtCore.QSize(70, 70))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.open_UI_mess)

        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(570, 20, 161, 101))
        self.pushButton_4.setStyleSheet("background-color:rgba(12, 87, 118, 255);\n"
                                        "border-radius: 40px;")
        self.pushButton_4.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("picture/picUI2/icons8-mic-100.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_4.setIcon(icon3)
        self.pushButton_4.setIconSize(QtCore.QSize(80, 80))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.open_mic)

        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(750, 20, 161, 101))
        self.pushButton_5.setStyleSheet("background-color:rgba(12, 87, 118, 255);\n"
                                        "border-radius: 40px;")
        self.pushButton_5.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("picture/picUI2/icons8-gmail-150.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_5.setIcon(icon4)
        self.pushButton_5.setIconSize(QtCore.QSize(80, 80))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.clicked.connect(self.open_gmail)

        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(930, 20, 161, 101))
        self.pushButton_6.setStyleSheet("background-color:rgba(12, 87, 118, 255);\n"
                                        "border-radius: 40px;")
        self.pushButton_6.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("picture/picUI2/icons8-ellipsis-100.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_6.setIcon(icon5)
        self.pushButton_6.setIconSize(QtCore.QSize(80, 80))
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_6.clicked.connect(self.open_UI_3)

        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_7.setGeometry(QtCore.QRect(1110, 20, 151, 101))
        self.pushButton_7.setStyleSheet("background-color:rgba(255, 51, 36, 180);\n"
                                        "border-radius: 40px;")
        self.pushButton_7.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("picture/picUI2/icons8-esc-90.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_7.setIcon(icon6)
        self.pushButton_7.setIconSize(QtCore.QSize(65, 65))
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_7.clicked.connect(self.exit)
        # -------------------------------------------------------------------
        self.pushButton.raise_()
        self.pushButton_2.raise_()
        self.pushButton_3.raise_()
        self.pushButton_4.raise_()
        self.pushButton_5.raise_()
        self.pushButton_6.raise_()
        self.pushButton_7.raise_()
        self.setCentralWidget(self.centralwidget)
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    # -------------------------------------------------------------------
    # Chức năng
    def open_keyboard(self):
        os.startfile(
            "C:\\Users\\trums\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Accessibility\\On-Screen Keyboard")

    def open_gmail(self):
        webbrowser.open("https://mail.google.com/mail/u/0/#inbox")

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("mainUI_2", "MainWindow"))
        self.pushButton.setText(_translate("mainUI_2", "Home"))

    def open_UI_1(self):
        self.ui1 = mainUI_1()
        self.ui1.show()
        # UI_2.hide()

    def open_UI_3(self):
        self.ui3 = mainUI_3()
        self.ui3.show()

    def open_UI_mess(self):
        self.uimess = mainUI_mess()
        self.uimess.show()

    def open_mic(self):
        self.close()
        global text
        speak("Đặt con trỏ vào ô cần ghi: ")
        time.sleep(10)
        pyperclip.copy(text)
        pyautogui.hotkey("ctrl", "v")
        speak(f"Đã ghi: {text}")

    def exit(self, event):
        # Thoát chương trình
        # QtWidgets.QApplication.quit()
        event.accept()


class mainUI_1(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        screen = QDesktopWidget().screenGeometry()
        self.setObjectName("UI_1")
        # UI_1.resize(1600, 900)
        global current, timee
        current = ""
        timee = 0
        s_width = 1600
        s_height = 900
        # UI_2.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setGeometry((screen.width() - s_width) / 2, (screen.height() - s_height) / 1.5, s_width, s_height)

        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setParent(self.centralwidget)

        # self.plot_.setPixmap(QtGui.QPixmap("../.designer/backup/1.jpg"))
        # self.canvas.setObjectName("plot_")
        self.data = pd.read_csv('plot.csv')  # Thay đổi thành tên file CSV của bạn
        self.is_animating = False
        # self.ax.set_position([0.5, 0.5, 0.5, 0.8])
        self.canvas.setGeometry(QtCore.QRect(160, 680, 801, 151))

        self.task = QtWidgets.QLabel(self.centralwidget)
        self.task.setGeometry(QtCore.QRect(1160, 250, 401, 51))
        self.task.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.task.setObjectName("task")

        self.camera = QtWidgets.QLabel(self.centralwidget)
        self.camera.setGeometry(QtCore.QRect(160, 20, 800, 450))
        self.camera.setFrameShape(QtWidgets.QFrame.Box)
        self.camera.setFrameShadow(QtWidgets.QFrame.Plain)
        self.camera.setLineWidth(3)
        # self.camera.setPixmap(QtGui.QPixmap("picUI1/Untitled.png"))
        self.camera.setObjectName("camera")

        self.camera_1 = QtWidgets.QLabel(self.centralwidget)
        self.camera_1.setGeometry(QtCore.QRect(50, 480, 240, 135))
        self.camera_1.setFrameShape(QtWidgets.QFrame.Box)
        self.camera_1.setFrameShadow(QtWidgets.QFrame.Plain)
        self.camera_1.setLineWidth(3)
        global frame_itf
        self.camera.setPixmap(QtGui.QPixmap(frame_itf))
        # self.camera_1 = frame_itf
        self.camera_1.setObjectName("camera")

        self.camera_2 = QtWidgets.QLabel(self.centralwidget)
        self.camera_2.setGeometry(QtCore.QRect(430, 480, 240, 135))
        self.camera_2.setFrameShape(QtWidgets.QFrame.Box)
        self.camera_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.camera_2.setLineWidth(3)
        # self.camera.setPixmap(QtGui.QPixmap("picUI1/Untitled.png"))
        self.camera_2.setObjectName("camera")

        self.camera_3 = QtWidgets.QLabel(self.centralwidget)
        self.camera_3.setGeometry(QtCore.QRect(810, 480, 240, 135))
        self.camera_3.setFrameShape(QtWidgets.QFrame.Box)
        self.camera_3.setFrameShadow(QtWidgets.QFrame.Plain)
        self.camera_3.setLineWidth(3)
        # self.camera.setPixmap(QtGui.QPixmap("picUI1/Untitled.png"))
        self.camera_3.setObjectName("camera")

        self.x_mouse = QtWidgets.QLabel(self.centralwidget)
        self.x_mouse.setGeometry(QtCore.QRect(1300, 40, 61, 20))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.x_mouse.setFont(font)
        self.x_mouse.setStyleSheet("color:rgba(255,255,255,210);")
        self.x_mouse.setObjectName("x_mouse")

        self.y_mouse = QtWidgets.QLabel(self.centralwidget)
        self.y_mouse.setGeometry(QtCore.QRect(1300, 98, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.y_mouse.setFont(font)
        self.y_mouse.setStyleSheet("color:rgba(255,255,255,210);")
        self.y_mouse.setObjectName("y_mouse")

        self.x_eye = QtWidgets.QLabel(self.centralwidget)
        self.x_eye.setGeometry(QtCore.QRect(1300, 70, 61, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.x_eye.setFont(font)
        self.x_eye.setStyleSheet("color:rgba(255,255,255,210);")
        self.x_eye.setObjectName("x_eye")

        self.y_eye = QtWidgets.QLabel(self.centralwidget)
        self.y_eye.setGeometry(QtCore.QRect(1300, 131, 61, 20))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.y_eye.setFont(font)
        self.y_eye.setStyleSheet("color:rgba(255,255,255,210);")
        self.y_eye.setObjectName("y_eye")

        self.sai_so = QtWidgets.QLabel(self.centralwidget)
        self.sai_so.setGeometry(QtCore.QRect(1300, 185, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.sai_so.setFont(font)
        self.sai_so.setStyleSheet("color:rgba(255,255,255,210);")
        self.sai_so.setScaledContents(False)
        self.sai_so.setObjectName("sai_so")

        self.z_eye = QtWidgets.QLabel(self.centralwidget)
        self.z_eye.setGeometry(QtCore.QRect(1300, 161, 61, 20))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.z_eye.setFont(font)
        self.z_eye.setStyleSheet("color:rgba(255,255,255,210);")
        self.z_eye.setObjectName("z_eye")

        self.lx_mouse = QtWidgets.QLabel(self.centralwidget)
        self.lx_mouse.setGeometry(QtCore.QRect(1190, 40, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lx_mouse.setFont(font)
        self.lx_mouse.setStyleSheet("color:rgba(255,255,255,210)")
        self.lx_mouse.setObjectName("lx_mouse")
        self.ly_mouse = QtWidgets.QLabel(self.centralwidget)
        self.ly_mouse.setGeometry(QtCore.QRect(1190, 70, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.ly_mouse.setFont(font)
        self.ly_mouse.setStyleSheet("color:rgba(255,255,255,210);")
        self.ly_mouse.setObjectName("ly_mouse")

        self.lx_eye = QtWidgets.QLabel(self.centralwidget)
        self.lx_eye.setGeometry(QtCore.QRect(1190, 100, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lx_eye.setFont(font)
        self.lx_eye.setStyleSheet("color:rgba(255,255,255,210);")
        self.lx_eye.setObjectName("lx_eye")

        self.ly_eye = QtWidgets.QLabel(self.centralwidget)
        self.ly_eye.setGeometry(QtCore.QRect(1190, 130, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.ly_eye.setFont(font)
        self.ly_eye.setStyleSheet("color:rgba(255,255,255,210);")
        self.ly_eye.setObjectName("ly_eye")

        self.lz_eye = QtWidgets.QLabel(self.centralwidget)
        self.lz_eye.setGeometry(QtCore.QRect(1190, 160, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lz_eye.setFont(font)
        self.lz_eye.setStyleSheet("color:rgba(255,255,255,210);")
        self.lz_eye.setScaledContents(False)
        self.lz_eye.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.lz_eye.setObjectName("lz_eye")

        self.lsai_so = QtWidgets.QLabel(self.centralwidget)
        self.lsai_so.setGeometry(QtCore.QRect(1190, 190, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lsai_so.setFont(font)
        self.lsai_so.setStyleSheet("color:rgba(255,255,255,210);")
        self.lsai_so.setObjectName("lsai_so")

        self.lreal_time = QtWidgets.QLabel(self.centralwidget)
        self.lreal_time.setGeometry(QtCore.QRect(1380, 40, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lreal_time.setFont(font)
        self.lreal_time.setStyleSheet("color:rgba(255,255,255,210);")
        self.lreal_time.setObjectName("lreal_time")

        self.real_time = QtWidgets.QLabel(self.centralwidget)
        self.real_time.setGeometry(QtCore.QRect(1490, 40, 61, 20))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.real_time.setFont(font)
        self.real_time.setStyleSheet("color:rgba(255,255,255,210);")
        self.real_time.setObjectName("real_time")

        self.ltt_lech = QtWidgets.QLabel(self.centralwidget)
        self.ltt_lech.setGeometry(QtCore.QRect(1380, 70, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.ltt_lech.setFont(font)
        self.ltt_lech.setStyleSheet("color:rgba(255,255,255,210);")
        self.ltt_lech.setObjectName("ltt_lech")
        self.tt_lech = QtWidgets.QLabel(self.centralwidget)
        self.tt_lech.setGeometry(QtCore.QRect(1490, 70, 61, 20))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.tt_lech.setFont(font)
        self.tt_lech.setStyleSheet("color:rgba(255,255,255,210);")
        self.tt_lech.setObjectName("tt_lech")

        self.background = QtWidgets.QLabel(self.centralwidget)
        self.background.setEnabled(True)
        self.background.setGeometry(QtCore.QRect(-60, 0, 2061, 900))
        self.background.setStyleSheet("")
        self.background.setText("")
        self.background.setPixmap(QtGui.QPixmap("picture/picUI1/background.jpg"))
        self.background.setObjectName("background")

        self.table = QtWidgets.QLabel(self.centralwidget)
        self.table.setGeometry(QtCore.QRect(1150, 30, 421, 201))
        self.table.setStyleSheet("background-color:rgba(0, 0, 0, 100);\n"
                                 "border-radius: 20px;")
        self.table.setText("")
        self.table.setObjectName("table")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(1130, 10, 461, 851))
        self.label.setStyleSheet("background-color:rgba(12, 87, 118, 120);\n"
                                 "border-radius: 40px;")
        self.label.setText("")
        self.label.setObjectName("label")

        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(1160, 300, 401, 531))
        self.textEdit.setFrameShape(QtWidgets.QFrame.Box)
        self.textEdit.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.textEdit.setLineWidth(4)
        self.textEdit.setMidLineWidth(4)
        self.textEdit.setObjectName("textEdit")

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(13)
        font.setBold(True)
        self.textEdit.setFont(font)
        self.textEdit.setTextColor(QtGui.QColor(0, 0, 0))  # Màu chữ
        self.textEdit.setStyleSheet("background-color: #F0F0F0")  # Màu nền

        self.input_line = QtWidgets.QLineEdit(self.centralwidget)

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 10, 1071, 851))
        self.label_3.setAcceptDrops(True)
        self.label_3.setStyleSheet("background-color:rgba(12, 87, 118, 120);\n"
                                   "border-radius: 40px;")
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.stick_2 = QtWidgets.QLabel(self.centralwidget)
        self.stick_2.setGeometry(QtCore.QRect(630, 630, 421, 20))
        self.stick_2.setAutoFillBackground(False)
        self.stick_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.stick_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.stick_2.setLineWidth(4)
        self.stick_2.setText("")
        self.stick_2.setAlignment(QtCore.Qt.AlignCenter)
        self.stick_2.setWordWrap(False)
        self.stick_2.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.stick_2.setObjectName("stick_2")

        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(490, 630, 131, 31))
        self.textEdit_2.setStyleSheet("background-color:rgba(248, 218, 208, 120);\n"
                                      "border-radius: 8px;")
        self.textEdit_2.setObjectName("textEdit_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(160, 680, 801, 151))
        self.label_2.setObjectName("label_2")

        self.stick_3 = QtWidgets.QLabel(self.centralwidget)
        self.stick_3.setGeometry(QtCore.QRect(50, 630, 421, 20))
        self.stick_3.setAutoFillBackground(False)
        self.stick_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.stick_3.setFrameShadow(QtWidgets.QFrame.Plain)
        self.stick_3.setLineWidth(4)
        self.stick_3.setText("")
        self.stick_3.setAlignment(QtCore.Qt.AlignCenter)
        self.stick_3.setWordWrap(False)
        self.stick_3.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.stick_3.setObjectName("stick_3")

        # _____________________________________________________________
        self.background.raise_()
        self.label_3.raise_()
        self.label.raise_()
        self.camera.raise_()
        rself.camera_1.raise_()
        self.camera_2.raise_()
        self.camera_3.raise_()
        self.task.raise_()
        self.table.raise_()
        self.y_mouse.raise_()
        self.lreal_time.raise_()
        self.x_eye.raise_()
        self.sai_so.raise_()
        self.y_eye.raise_()
        self.ltt_lech.raise_()
        self.lx_mouse.raise_()
        self.lsai_so.raise_()
        self.real_time.raise_()
        self.tt_lech.raise_()
        self.lz_eye.raise_()
        self.ly_eye.raise_()
        self.x_mouse.raise_()
        self.z_eye.raise_()
        self.ly_mouse.raise_()
        self.lx_eye.raise_()
        self.textEdit.raise_()
        self.canvas.raise_()
        self.textEdit_2.raise_()
        self.stick_2.raise_()
        self.stick_3.raise_()

        self.menuBar = QtWidgets.QMenuBar(self)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1600, 21))
        self.menuBar.setObjectName("menuBar")
        self.menuTi_n_ch = QtWidgets.QMenu(self.menuBar)
        self.menuTi_n_ch.setObjectName("menuTi_n_ch")

        self.setMenuBar(self.menuBar)
        self.actionUI_1 = QtWidgets.QAction(self)
        self.actionUI_1.setObjectName("actionUI_1")
        self.actionUI_2 = QtWidgets.QAction(self)
        self.actionUI_2.setObjectName("actionUI_2")
        self.menuTi_n_ch.addSeparator()
        self.menuTi_n_ch.addAction(self.actionUI_1)
        self.menuTi_n_ch.addAction(self.actionUI_2)
        self.menuBar.addAction(self.menuTi_n_ch.menuAction())

        self.menu_bar()
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        self.timer1 = QTimer()
        self.timer1.timeout.connect(self.new_text)
        self.timer1.start(10000)

        self.timer2 = QTimer()
        self.timer2.timeout.connect(self.update_real_time)
        self.timer2.start(1000)

        self.timer3 = QTimer()
        self.timer3.timeout.connect(self.update_value)
        self.timer3.start(5000)
        # ==============================================================================
        if not self.is_animating:
            self.is_animating = True
            self.animation = FuncAnimation(self.figure, self.update_plot, frames=len(self.data), interval=1000,
                                           blit=False)
            self.canvas.draw()

    def start_animation(self):
        if not self.is_animating:
            self.is_animating = True
            self.animation = FuncAnimation(self.figure, self.update_plot, frames=len(self.data), interval=1000,
                                           blit=False)
            self.canvas.draw()

    # -------------------------------------------------------------------------

    def update_plot(self, frame):
        self.ax.clear()
        self.ax.plot(self.data.iloc[:frame + 1, 0], self.data.iloc[:frame + 1, 1])
        self.ax.set_title('')
        self.ax.set_xlabel('')
        self.ax.set_ylabel('')
        # Kiểm tra điều kiện để dừng animation khi đã đọc hết file
        if frame == len(self.data) - 1:
            self.is_animating = False
            self.animation.event_source.stop()

        self.canvas.draw()

    def update_value(self):
        _translate = QtCore.QCoreApplication.translate

        self.x_mouse.setText(_translate("mainUI_1", "10"))
        self.y_mouse.setText(_translate("mainUI_1", "10"))
        self.x_eye.setText(_translate("mainUI_1", "10"))
        self.y_eye.setText(_translate("mainUI_1", "10"))
        self.sai_so.setText(_translate("mainUI_1", "10"))
        self.z_eye.setText(_translate("mainUI_1", "10"))
        self.tt_lech.setText(_translate("mainUI_1", "10"))

    def update_real_time(self):
        _translate = QtCore.QCoreApplication.translate

        global timee
        timee += 1
        self.real_time.setText(_translate("mainUI_1", str(timee)))

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate

        self.setWindowTitle(_translate("mainUI_1", "MainWindow"))

        self.task.setText(_translate("mainUI_1",
                                     "<html><head/><body><p align=\"center\"><span style=\" font-size:18pt; font-weight:600; text-decoration: underline;\">Lịch sử lệnh</span></p><p><span style=\" font-size:18pt;\"><br/></span></p></body></html>"))
        self.lx_mouse.setToolTip(_translate("mainUI_1", "<html><head/><body><p><br/></p></body></html>"))
        self.lx_mouse.setText(_translate("mainUI_1", "X_mouse:"))
        self.ly_mouse.setToolTip(_translate("mainUI_1", "<html><head/><body><p><br/></p></body></html>"))
        self.ly_mouse.setText(_translate("mainUI_1", "Y_mouse:"))
        self.lx_eye.setToolTip(_translate("mainUI_1", "<html><head/><body><p><br/></p></body></html>"))
        self.lx_eye.setText(_translate("mainUI_1", "x_eye    :"))
        self.ly_eye.setToolTip(_translate("mainUI_1", "<html><head/><body><p><br/></p></body></html>"))
        self.ly_eye.setText(_translate("mainUI_1", "y_eye    :"))
        self.lz_eye.setToolTip(_translate("mainUI_1", "<html><head/><body><p><br/></p></body></html>"))
        self.lz_eye.setText(_translate("mainUI_1", "z_eye    :"))
        self.lsai_so.setToolTip(_translate("mainUI_1", "<html><head/><body><p><br/></p></body></html>"))
        self.lsai_so.setText(_translate("mainUI_1", "Sai số    :"))
        self.lreal_time.setToolTip(_translate("mainUI_1", "<html><head/><body><p><br/></p></body></html>"))
        self.lreal_time.setText(_translate("mainUI_1", "Time     :"))

        self.ltt_lech.setToolTip(_translate("mainUI_1", "<html><head/><body><p><br/></p></body></html>"))
        self.ltt_lech.setText(_translate("mainUI_1", "TT Lệch :"))
        self.textEdit_2.setHtml(_translate("MainWindow",
                                           "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                           "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                           "p, li { white-space: pre-wrap; }\n"
                                           "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                                           "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt; font-weight:600; color:#bcfefe;\">Tỉ lệ</span></p></body></html>"))

    def menu_bar(self):
        _translate = QtCore.QCoreApplication.translate
        self.menuTi_n_ch.setTitle(_translate("mainUI_1", "Tiện ích"))
        self.actionUI_1.setText(_translate("mainUI_1", "UI_1"))
        self.actionUI_2.setText(_translate("mainUI_1", "UI_2"))

    # def open_UI_2(self):
    #     self.UI_2 = QtWidgets.QMainWindow()
    #     self.ui = mainUI_2()
    #     self.ui.setupUi_2(self.UI_2)
    #     self.UI_2.show()
    #     # UI_1.hide()
    def new_text(self):
        # Lấy văn bản từ QLineEdit
        global text, content, current
        # Kiểm tra nếu tin nhắn không rỗng
        if text:
            current = current + "Huyên: " + text + "\nBot: " + content + "\n"

            self.textEdit.setPlainText(current)


class mainUI_3(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        screen = QDesktopWidget().screenGeometry()

        s_width = 1293
        s_height = 275
        # Display & size of display
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setGeometry((screen.width() - s_width) / 2, s_height * 0.8, s_width, s_height)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.background_UI3 = QtWidgets.QLabel(self.centralwidget)
        self.background_UI3.setGeometry(QtCore.QRect(0, -10, 1441, 371))
        self.background_UI3.setText("")
        self.background_UI3.setPixmap(QtGui.QPixmap("picture/picUI2/background.png"))
        self.background_UI3.setObjectName("background_UI3")

        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("picture/picUI3/icons8-word-100.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("picture/picUI3//icons8-powerpoint-100.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("picture/picUI3/icons8-excel-100.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("picture/picUI3/icons8-youtube-250.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("picture/picUI3/icons8-night-100.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("picture/picUI3/icons8-alarm-100.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("picture/picUI3/icons8-news-100.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("picture/picUI3/icons8-zoom-in-100.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("picture/picUI3/icons8-zoom-out-100.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("picture/picUI3/icons8-google-translate-100.png"), QtGui.QIcon.Normal,
                         QtGui.QIcon.Off)

        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap("picture/picUI3/icons8-e-100.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap("picture/picUI3/icons8-face-64.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap("picture/picUI2/icons8-ellipsis-100.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap("picture/picUI3/icons8-up-100.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.but1 = QtWidgets.QPushButton(self.centralwidget)
        self.but1.setGeometry(QtCore.QRect(30, 20, 161, 101))
        self.but1.setStyleSheet("background-color:rgba(12, 87, 118, 255);\n"
                                "border-radius: 40px;")
        self.but1.setText("")
        self.but1.setIcon(icon1)
        self.but1.setIconSize(QtCore.QSize(83, 140))
        self.but1.setObjectName("But1")
        self.but1.clicked.connect(self.word)

        self.but2 = QtWidgets.QPushButton(self.centralwidget)
        self.but2.setGeometry(QtCore.QRect(210, 20, 161, 101))
        self.but2.setStyleSheet("background-color:rgba(12, 87, 118, 255);\n"
                                "border-radius: 40px;")
        self.but2.setText("")

        self.but2.setIcon(icon2)
        self.but2.setIconSize(QtCore.QSize(85, 100))
        self.but2.setObjectName("but2")
        self.but2.clicked.connect(self.powerpoint)

        self.but3 = QtWidgets.QPushButton(self.centralwidget)
        self.but3.setGeometry(QtCore.QRect(390, 20, 161, 101))
        self.but3.setStyleSheet("background-color:rgba(12, 87, 118, 255);\n"
                                "border-radius: 40px;")
        self.but3.setText("")

        self.but3.setIcon(icon3)
        self.but3.setIconSize(QtCore.QSize(86, 83))
        self.but3.setObjectName("but3")
        self.but3.clicked.connect(self.excel)

        self.but4 = QtWidgets.QPushButton(self.centralwidget)
        self.but4.setGeometry(QtCore.QRect(570, 20, 161, 101))
        self.but4.setStyleSheet("background-color:rgba(12, 87, 118, 255);\n"
                                "border-radius: 40px;")
        self.but4.setText("")
        self.but4.setIcon(icon4)
        self.but4.setIconSize(QtCore.QSize(100, 100))
        self.but4.setObjectName("but4")
        self.but4.clicked.connect(self.open_youtube)

        self.but5 = QtWidgets.QPushButton(self.centralwidget)
        self.but5.setGeometry(QtCore.QRect(750, 20, 161, 101))
        self.but5.setStyleSheet("background-color:rgba(12, 87, 118, 255);\n"
                                "border-radius: 40px;")
        self.but5.setText("")
        self.but5.setIcon(icon5)
        self.but5.setIconSize(QtCore.QSize(80, 80))
        self.but5.setObjectName("but5")
        self.but5.clicked.connect(self.open_UI_wea)

        self.but6 = QtWidgets.QPushButton(self.centralwidget)
        self.but6.setGeometry(QtCore.QRect(930, 20, 161, 101))
        self.but6.setStyleSheet("background-color:rgba(12, 87, 118, 255);\n"
                                "border-radius: 40px;")
        self.but6.setText("")

        self.but6.setIcon(icon6)
        self.but6.setIconSize(QtCore.QSize(73, 80))
        self.but6.setObjectName("but6")
        self.but6.clicked.connect(self.open_UI_clock)

        self.but7 = QtWidgets.QPushButton(self.centralwidget)
        self.but7.setGeometry(QtCore.QRect(1110, 20, 161, 101))
        self.but7.setStyleSheet("background-color:rgba(12, 87, 118, 255);\n"
                                "border-radius: 40px;")
        self.but7.setText("")
        self.but7.setIcon(icon7)
        self.but7.setIconSize(QtCore.QSize(80, 80))
        self.but7.setObjectName("but7")
        self.but7.clicked.connect(self.open_UI_news)

        self.but8 = QtWidgets.QPushButton(self.centralwidget)
        self.but8.setGeometry(QtCore.QRect(30, 150, 161, 101))
        self.but8.setStyleSheet("background-color:rgba(179, 179, 179, 240);\n"
                                "border-radius: 40px;")
        self.but8.setText("")
        self.but8.setIcon(icon8)
        self.but8.setIconSize(QtCore.QSize(80, 80))
        self.but8.setObjectName("but8")

        self.but9 = QtWidgets.QPushButton(self.centralwidget)
        self.but9.setGeometry(QtCore.QRect(210, 150, 161, 101))
        self.but9.setStyleSheet("background-color:rgba(179, 179, 179, 240);\n"
                                "border-radius: 40px;")
        self.but9.setText("")
        self.but9.setIcon(icon9)
        self.but9.setIconSize(QtCore.QSize(80, 80))
        self.but9.setObjectName("but9")

        self.but10 = QtWidgets.QPushButton(self.centralwidget)
        self.but10.setGeometry(QtCore.QRect(390, 150, 161, 101))
        self.but10.setStyleSheet("background-color:rgba(12, 87, 118, 255);\n"
                                 "border-radius: 40px;")
        self.but10.setText("")
        self.but10.setIcon(icon10)
        self.but10.setIconSize(QtCore.QSize(80, 80))
        self.but10.setObjectName("but10")
        self.but10.clicked.connect(self.open_UI_tras)

        self.but11 = QtWidgets.QPushButton(self.centralwidget)
        self.but11.setGeometry(QtCore.QRect(570, 150, 161, 101))
        self.but11.setStyleSheet("background-color:rgba(12, 87, 118, 255);\n"
                                 "border-radius: 40px;")
        self.but11.setText("")
        self.but11.setIcon(icon11)
        self.but11.setIconSize(QtCore.QSize(80, 80))
        self.but11.setObjectName("but11")
        self.but11.clicked.connect(self.switch_lang)

        self.but12 = QtWidgets.QPushButton(self.centralwidget)
        self.but12.setGeometry(QtCore.QRect(750, 150, 161, 101))
        self.but12.setStyleSheet("background-color:rgba(12, 87, 118, 255);\n"
                                 "border-radius: 40px;")
        self.but12.setText("")
        self.but12.setIcon(icon12)
        self.but12.setIconSize(QtCore.QSize(90, 90))
        self.but12.setObjectName("but12")
        self.but12.clicked.connect(self.open_deepfake)

        self.but13 = QtWidgets.QPushButton(self.centralwidget)
        self.but13.setGeometry(QtCore.QRect(930, 150, 161, 101))
        self.but13.setStyleSheet("background-color:rgba(12, 87, 118, 255);\n"
                                 "border-radius: 40px;")
        self.but13.setText("")
        self.but13.setIcon(icon13)
        self.but13.setIconSize(QtCore.QSize(80, 80))
        self.but13.setObjectName("but13")

        self.but14 = QtWidgets.QPushButton(self.centralwidget)
        self.but14.setGeometry(QtCore.QRect(1110, 150, 161, 101))
        self.but14.setStyleSheet("background-color:rgba(255, 51, 36, 180);\n"
                                 "border-radius: 40px;")
        self.but14.setText("")

        self.but14.setIcon(icon14)
        self.but14.setIconSize(QtCore.QSize(80, 80))
        self.but14.setObjectName("but14")
        self.but14.clicked.connect(self.close)

        self.setCentralWidget(self.centralwidget)

        QtCore.QMetaObject.connectSlotsByName(self)

    def open_UI_news(self):
        self.ui = mainUInews()
        self.ui.show()
        self.close()

    def open_UI_wea(self):
        self.ui = mainUIwea()
        self.ui.show()
        self.close()

    def open_UI_clock(self):
        self.ui = mainUI_clock()
        self.ui.show()
        self.close()

    def open_deepfake(self):
        self.ui = mainUI_deepfake()
        self.ui.show()
        self.close()

    def open_UI_tras(self):
        self.ui = mainUI_GTranslate()
        self.ui.show()
        self.close()

    def switch_lang(self):
        global ID
        if ID == 2:
            ID = 0
            print(ID)
        else:
            ID = 2
            print(ID)

    def open_youtube(self):
        self.close()
        webbrowser.open("https://www.youtube.com/")

    def word(self):
        self.close()
        os.startfile("C:\\Program Files (x86)\\Microsoft Office\\root\\Office16\\WORD.EXE")

    def powerpoint(self):
        self.close()
        os.startfile("C:\\Program Files (x86)\\Microsoft Office\\root\\Office16\\POWERPNT.EXE")

    def excel(self):
        self.close()
        os.startfile("C:\\Program Files (x86)\\Microsoft Office\\root\\Office16\\EXCEL.EXE")


class mainUI_mess(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # UI_mess.setObjectName("Message")
        screen = QDesktopWidget().screenGeometry()

        s_width = 783
        s_height = 347
        # UI_2.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setGeometry((screen.width() - s_width) / 2, (screen.height() - s_height) / 2, s_width, s_height)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.bg = QtWidgets.QLabel(self.centralwidget)
        self.bg.setGeometry(QtCore.QRect(-370, -180, 1191, 671))
        self.bg.setText("")
        self.bg.setPixmap(QtGui.QPixmap("picture/picUImessage/1_background.png"))
        self.bg.setObjectName("bg")

        self.phone_ = QtWidgets.QTextEdit(self.centralwidget)
        self.phone_.setGeometry(QtCore.QRect(240, 70, 361, 41))
        self.phone_.setStyleSheet("background-color: rgba(255, 255, 255, 255);\n"
                                  "border-radius: 10px;")
        self.phone_.setObjectName("phone_")
        self.phone_.setFont(QtGui.QFont("MS Shell Dlg 2", 12))  # Set font size and style
        # self.phone_.setAlignment(QtCore.Qt.AlignCenter)  # Align text to the center

        self.mess_ = QtWidgets.QTextEdit(self.centralwidget)
        self.mess_.setGeometry(QtCore.QRect(240, 140, 361, 121))
        self.mess_.setStyleSheet("background-color: rgba(255, 255, 255, 255);\n"
                                 "border-radius: 10px;")
        self.mess_.setObjectName("mess_")
        self.mess_.setFont(QtGui.QFont("MS Shell Dlg 2", 14))  # Set font size and style
        # self.mess_.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)  # Align text to the top-left

        self.lphone = QtWidgets.QLabel(self.centralwidget)
        self.lphone.setGeometry(QtCore.QRect(100, 50, 201, 81))
        self.lphone.setStyleSheet("color: rgb(255, 255, 255);\n"
                                  "font: 75 14pt \"MS Shell Dlg 2\";")
        self.lphone.setObjectName("lphone")
        self.ltinnhan = QtWidgets.QLabel(self.centralwidget)
        self.ltinnhan.setGeometry(QtCore.QRect(130, 110, 201, 81))
        self.ltinnhan.setStyleSheet("color: rgb(255, 255, 255);\n"
                                    "font: 75 14pt \"MS Shell Dlg 2\";")
        self.ltinnhan.setObjectName("ltinnhan")

        self.but_mess = QtWidgets.QPushButton(self.centralwidget)
        self.but_mess.setGeometry(QtCore.QRect(380, 290, 75, 23))
        self.but_mess.setObjectName("but_mess")
        self.but_mess.clicked.connect(self.send_message)

        self.setCentralWidget(self.centralwidget)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def send_message(self):
        message = self.mess_.toPlainText()
        phone = self.phone_.toPlainText()

        if phone != "":
            if phone[0] == "0":
                phone = "+84" + phone[1:11]
            print(message)
            print(phone)
            client = Client('ACb06bb74b84ba84294115d1ddb6a9c9fb', 'c4fb99df48d7b92f59f114f8e2726a0f')

            message = client.messages.create(
                body=message,
                from_='+12052870994',
                to=phone
            )
            print("Gửi thành công!")
        else:
            print("Bạn chưa nhập số điện thoại!")
        self.close()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("mainUI_mess", "Send message"))
        self.lphone.setText(_translate("mainUI_mess", "Số điện thoại:"))
        self.ltinnhan.setText(_translate("mainUI_mess", "Tin nhắn:"))
        self.mess_.setHtml(_translate("mainUI_mess",
                                      "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                      "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                      "p, li { white-space: pre-wrap; }\n"
                                      "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                                      "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.but_mess.setText(_translate("mainUI_mess", "Gửi"))


class mainUIwea(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setObjectName("MainWindow")
        self.resize(794, 577)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.bg1 = QtWidgets.QLabel(self.centralwidget)
        self.bg1.setGeometry(QtCore.QRect(40, 80, 711, 191))
        self.bg1.setStyleSheet("background-color:rgba(74, 152, 178, 255);\n"
                               "border-radius: 40px;")
        self.bg1.setText("")
        self.bg1.setObjectName("bg1")
        self.bg2 = QtWidgets.QLabel(self.centralwidget)
        self.bg2.setGeometry(QtCore.QRect(-130, -30, 1001, 711))
        self.bg2.setStyleSheet("background-color:rgba(54, 140, 169, 255);")
        self.bg2.setText("")
        self.bg2.setObjectName("bg2")
        self.textEdit_weather = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_weather.setGeometry(QtCore.QRect(40, 30, 501, 31))
        self.textEdit_weather.setObjectName("textEdit_weather")
        self.but_wea = QtWidgets.QPushButton(self.centralwidget)
        self.but_wea.setGeometry(QtCore.QRect(590, 30, 161, 31))
        self.but_wea.setStyleSheet("font: 75 14pt \"Times New Roman\";\n"
                                   "background-color: rgb(220, 53, 69);\n"
                                   "selection-color: rgb(255, 255, 255);\n"
                                   "")
        self.but_wea.setObjectName("but_wea")
        self.but_wea.clicked.connect(self.process_wea)

        self.calendarWidget = QtWidgets.QCalendarWidget(self.centralwidget)
        self.calendarWidget.setGeometry(QtCore.QRect(50, 280, 701, 271))
        self.calendarWidget.setObjectName("calendarWidget")
        self.locate_wea = QtWidgets.QLabel(self.centralwidget)
        self.locate_wea.setGeometry(QtCore.QRect(70, 90, 271, 41))
        self.locate_wea.setStyleSheet("font: 87 30pt \"Arial\";")
        self.locate_wea.setObjectName("locate_wea")
        self.lablel1 = QtWidgets.QLabel(self.centralwidget)
        self.lablel1.setGeometry(QtCore.QRect(70, 120, 211, 41))
        self.lablel1.setStyleSheet("font: 87 14pt \"Arial\";")
        self.lablel1.setObjectName("lablel1")
        self.temperature = QtWidgets.QLabel(self.centralwidget)
        self.temperature.setGeometry(QtCore.QRect(70, 150, 181, 61))
        self.temperature.setStyleSheet("font: 87 35pt \"Arial\";")
        self.temperature.setObjectName("temperature")
        self.label2 = QtWidgets.QLabel(self.centralwidget)
        self.label2.setGeometry(QtCore.QRect(70, 210, 181, 21))
        self.label2.setStyleSheet("font: 87 14pt \"Arial\";")
        self.label2.setObjectName("label2")
        self.label3 = QtWidgets.QLabel(self.centralwidget)
        self.label3.setGeometry(QtCore.QRect(70, 240, 71, 21))
        self.label3.setStyleSheet("font: 87 14pt \"Arial\";")
        self.label3.setObjectName("label3")
        self.apsuatkk_wea = QtWidgets.QLabel(self.centralwidget)
        self.apsuatkk_wea.setGeometry(QtCore.QRect(230, 210, 250, 21))
        self.apsuatkk_wea.setStyleSheet("font: 87 14pt \"Arial\";")
        self.apsuatkk_wea.setObjectName("apsuatkk_wea")
        self.doam_wea = QtWidgets.QLabel(self.centralwidget)
        self.doam_wea.setGeometry(QtCore.QRect(140, 240, 71, 21))
        self.doam_wea.setStyleSheet("font: 87 14pt \"Arial\";")
        self.doam_wea.setObjectName("doam_wea")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(630, 80, 141, 101))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("picture/icons8-sun.png"))
        self.label.setObjectName("label")
        self.bg2.raise_()
        self.bg1.raise_()
        self.textEdit_weather.raise_()
        self.but_wea.raise_()
        self.calendarWidget.raise_()
        self.locate_wea.raise_()
        self.lablel1.raise_()
        self.temperature.raise_()
        self.label2.raise_()
        self.label3.raise_()
        self.apsuatkk_wea.raise_()
        self.doam_wea.raise_()
        self.label.raise_()

        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("mainUIwea", "Weather"))
        self.but_wea.setText(_translate("mainUIwea", "Tìm kiếm"))

        self.setCentralWidget(self.centralwidget)

        QtCore.QMetaObject.connectSlotsByName(self)

    def process_wea(self):
        _translate = QtCore.QCoreApplication.translate
        ow_url = "http://api.openweathermap.org/data/2.5/weather?"
        locate_ = self.textEdit_weather.toPlainText()
        print(locate_)
        if not locate_:
            pass
        api_key = "fe8d8c65cf345889139d8e545f57819a"
        call_url = ow_url + "appid=" + api_key + "&q=" + locate_ + "&units=metric"
        response = requests.get(call_url)
        data = response.json()  # city
        if data["cod"] != "404":
            city_res = data["main"]
            current_temperature = city_res["temp"]
            current_pressure = city_res["pressure"]
            current_humidity = city_res["humidity"]
            suntime = data["sys"]
            sunrise = datetime.datetime.fromtimestamp(suntime["sunrise"])
            sunset = datetime.datetime.fromtimestamp(suntime["sunset"])
            wthr = data["weather"]
            weather_description = wthr[0]["description"]
            now = datetime.datetime.now()
            self.locate_wea.setText(_translate("mainUIwea", str(locate_)))
            self.lablel1.setText(_translate("mainUIwea", "Dự báo thời tiết hôm nay"))
            self.temperature.setText(_translate("mainUIwea", str(current_temperature) + "°"))
            self.label2.setText(_translate("mainUIwea", "Áp suất không khí:"))
            self.label3.setText(_translate("mainUIwea", "Độ ẩm:"))
            self.apsuatkk_wea.setText(_translate("mainUIwea", str(current_pressure) + " héc tơ Pascal"))
            self.doam_wea.setText(_translate("mainUIwea", str(current_humidity) + "%"))
        else:
            speak("Không tìm thấy địa chỉ")


class mainUI_clock(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Alarm Clock')
        self.setGeometry(0, 0, 300, 150)  # Thiết lập kích thước cửa sổ
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)

        self.time_edit = QTimeEdit(self)
        self.time_edit.setDisplayFormat("HH:mm")
        self.time_edit.setAlignment(Qt.AlignCenter)
        self.time_edit.setGeometry(QRect(110, 20, 60, 20))

        self.start_button = QPushButton('Start', self)
        self.start_button.clicked.connect(self.start_alarm)
        self.start_button.setGeometry(QRect(50, 60, 100, 25))

        self.stop_button = QPushButton('Stop', self)
        self.stop_button.clicked.connect(self.stop_alarm)
        self.stop_button.setGeometry(QRect(150, 60, 100, 25))

        self.status_label = QLabel('Status: Not running', self)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setGeometry(QRect(0, 110, 300, 20))

        self.status_label = QLabel('Status: Not running', self)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setGeometry(QRect(0, 110, 300, 20))

        # Thay đổi màu sắc và phông chữ của các thành phần giao diện
        self.setStyleSheet('''
            background-color: #f0f0f0;
            font-size: 14px;
            QLabel {
                color: #333;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                margin: 5px 0;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QTimeEdit {
                font-size: 18px;
            }
        ''')

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_alarm)

        self.show()

    def start_alarm(self):
        alarm_time = self.time_edit.time()
        current_time = QTime.currentTime()

        # Calculate the time difference
        delta = current_time.secsTo(alarm_time)

        if delta <= 0:
            self.status_label.setText('Status: Invalid alarm time')
        else:
            self.timer.start(delta * 1000)  # Convert seconds to milliseconds
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.status_label.setText('Status: Running')

    def stop_alarm(self):
        self.timer.stop()
        self.start_button.setEnabled(True)
        self.status_label.setText('Status: Not running')
        self.close()

    def check_alarm(self):
        self.timer.stop()
        self.start_button.setEnabled(True)
        self.status_label.setText('Status: Alarm triggered!')
        playsound("nhacchuong.wav")


class mainUInews(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setObjectName("mainUInews")
        self.resize(832, 471)

        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(250, 30, 121, 41))
        self.label.setStyleSheet("color: rgb(255, 255, 255);\n"
                                 "background-color:rgba(12, 87, 118, 255);\n"
                                 "border-radius: 10px;\n"
                                 "font: 75 14pt \"Times New Roman\";")
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(-130, -40, 1001, 541))
        self.label_2.setStyleSheet("background-color:rgba(74, 152, 178, 255);")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")

        self.comboBox = QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(390, 40, 151, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")

        self.textEdit_news = QTextEdit(self.centralwidget)
        self.textEdit_news.setGeometry(QtCore.QRect(40, 90, 751, 341))
        self.textEdit_news.setStyleSheet("background-color:rgba(255, 255, 255, 255);\n"
                                         "border-radius: 40px;")
        self.textEdit_news.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.textEdit_news.setFrameShadow(QtWidgets.QFrame.Plain)
        self.textEdit_news.setLineWidth(0)
        self.textEdit_news.setMidLineWidth(0)
        self.textEdit_news.setObjectName("textEdit_news_news")

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(13)
        font.setBold(True)
        self.textEdit_news.setFont(font)
        self.textEdit_news.setTextColor(QtGui.QColor(0, 0, 0))  # Màu chữ
        self.textEdit_news.setStyleSheet("background-color: #F0F0F0")

        self.label_2.raise_()
        self.label.raise_()
        self.comboBox.raise_()
        self.textEdit_news.raise_()
        self.setCentralWidget(self.centralwidget)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("mainUInews", "mainUInews"))
        self.label.setText(_translate("mainUInews", "  Chọn nguồn:"))
        self.comboBox.setItemText(0, _translate("mainUInews", "baogialai.com.vn"))
        self.comboBox.setItemText(1, _translate("mainUInews", "vnExpress.net"))
        self.comboBox.setItemText(2, _translate("mainUInews", "Thanhnien.vn"))
        self.comboBox.setItemText(3, _translate("mainUInews", "news.google.com"))
        self.comboBox.currentIndexChanged.connect(self.onComboBoxChanged)

    def onComboBoxChanged(self):
        url = self.comboBox.currentText()
        response = requests.get("https://" + url)
        if response.status_code != 200:
            print("Không thể tải trang web.")
            return
        # Phân tích HTML bằng BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        # Tìm các đoạn văn bản chứa tin tức
        news_articles = soup.find_all('p')  # Thay đổi selector tùy thuộc vào trang web bạn đang sử dụng
        # In ra nội dung tin tức

        save = ""
        for article in news_articles:
            content = article.text
            for x in content:
                if x == "\n":
                    pass
                else:
                    save = save + x
            save = save + "\n"
            self.textEdit_news.setPlainText(save)


class mainUI_GTranslate(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName("MainWindow")
        screen = QDesktopWidget().screenGeometry()
        s_width = 881
        s_height = 558
        self.setGeometry((screen.width() - s_width) / 2, (screen.height() - s_height) / 2, s_width, s_height)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(-130, -40, 1171, 621))
        self.label_2.setStyleSheet("background-color:rgba(74, 152, 178, 255);")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(60, 40, 101, 41))
        self.label_3.setStyleSheet("color: rgb(255, 255, 255);\n"
                                   "background-color:rgba(12, 87, 118, 255);\n"
                                   "border-radius: 10px;\n"
                                   "font: 75 14pt \"Times New Roman\";")
        self.label_3.setObjectName("label_3")

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(13)
        font.setBold(True)

        self.TextEdit_Origin = QtWidgets.QTextEdit(self.centralwidget)
        self.TextEdit_Origin.setGeometry(QtCore.QRect(200, 30, 621, 201))

        self.TextEdit_Origin.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.TextEdit_Origin.setFrameShadow(QtWidgets.QFrame.Plain)
        self.TextEdit_Origin.setLineWidth(0)
        self.TextEdit_Origin.setMidLineWidth(0)
        self.TextEdit_Origin.setObjectName("TextEdit_Origin")

        self.TextEdit_Origin.setFont(font)
        self.TextEdit_Origin.setTextColor(QtGui.QColor(0, 0, 0))  # Màu chữ
        self.TextEdit_Origin.setStyleSheet("background-color: #F0F0F0")

        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(60, 320, 101, 41))
        self.label_4.setStyleSheet("color: rgb(255, 255, 255);\n"
                                   "background-color:rgba(12, 87, 118, 255);\n"
                                   "border-radius: 10px;\n"
                                   "font: 75 14pt \"Times New Roman\";")
        self.label_4.setObjectName("label_4")

        self.TextEdit_Translate = QtWidgets.QTextEdit(self.centralwidget)
        self.TextEdit_Translate.setGeometry(QtCore.QRect(200, 300, 621, 211))

        self.TextEdit_Translate.setFont(font)
        self.TextEdit_Translate.setTextColor(QtGui.QColor(0, 0, 0))  # Màu chữ
        self.TextEdit_Translate.setStyleSheet("background-color: #F0F0F0")

        self.TextEdit_Translate.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.TextEdit_Translate.setFrameShadow(QtWidgets.QFrame.Plain)
        self.TextEdit_Translate.setLineWidth(0)
        self.TextEdit_Translate.setMidLineWidth(0)
        self.TextEdit_Translate.setObjectName("TextEdit_Translate")

        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(60, 90, 101, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox_2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_2.setGeometry(QtCore.QRect(60, 370, 101, 22))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(460, 250, 101, 31))
        self.pushButton_2.setStyleSheet("font: 75 14pt \"Times New Roman\"")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.Trans)

        self.setCentralWidget(self.centralwidget)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("mainUI_GTranslate", "MainWindow"))
        self.label_3.setText(_translate("mainUI_GTranslate", "  Ngôn ngữ:"))
        self.label_4.setText(_translate("mainUI_GTranslate", "  Ngôn ngữ:"))
        self.comboBox.setItemText(0, _translate("mainUI_GTranslate", "Tiếng Việt"))
        self.comboBox.setItemText(1, _translate("mainUI_GTranslate", "English"))
        self.comboBox.setItemText(2, _translate("mainUI_GTranslate", "Chinese"))
        self.comboBox_2.setItemText(0, _translate("mainUI_GTranslate", "English"))
        self.comboBox_2.setItemText(1, _translate("mainUI_GTranslate", "Tiếng Việt"))
        self.comboBox_2.setItemText(2, _translate("mainUI_GTranslate", "Chinese"))
        self.pushButton_2.setText(_translate("mainUI_GTranslate", "Translate"))

    def Trans(self):
        ORI = self.comboBox.currentText()
        TRA = self.comboBox_2.currentText()

        for i in range(len(full_)):
            if ORI == full_[i]:
                ORI = Short_[i]
            if TRA == full_[i]:
                TRA = Short_[i]

        translator = Translator()
        Dich = self.TextEdit_Origin.toPlainText()
        Dich = translator.translate(src=ORI, dest=TRA, text=Dich)

        self.TextEdit_Translate.setPlainText(Dich.text)


class mainUI_deepfake(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName("MainWindow")
        self.resize(935, 594)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.lcamera = QtWidgets.QLabel(self.centralwidget)
        self.lcamera.setGeometry(QtCore.QRect(130, 150, 701, 391))
        self.lcamera.setStyleSheet("background-color:rgba(0, 0, 0, 255);")
        self.lcamera.setText("")
        self.lcamera.setObjectName("lcamera")

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(-30, -40, 1001, 731))
        self.label_2.setStyleSheet("background-color:rgba(12, 87, 118, 255);")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")

        self.butBegin = QtWidgets.QPushButton(self.centralwidget)
        self.butBegin.setGeometry(QtCore.QRect(30, 50, 141, 51))
        self.butBegin.setStyleSheet("background-color:rgba(117, 249, 77, 210);\n"
                                    "border-radius: 20px;\n"
                                    "font: 75 14pt \"Times New Roman\";")
        self.butBegin.setObjectName("butBegin")
        self.butBegin.clicked.connect(self.start_recording)

        self.butEnd = QtWidgets.QPushButton(self.centralwidget)
        self.butEnd.setGeometry(QtCore.QRect(30, 50, 141, 51))
        self.butEnd.setStyleSheet("background-color:rgba(255, 51, 36, 180);\n"
                                  "border-radius: 20px;\n"
                                  "font: 75 14pt \"Times New Roman\";")
        self.butEnd.setObjectName("butEnd")
        self.butEnd.clicked.connect(self.stop_recording)
        self.butEnd.hide()

        self.face_plot = QtWidgets.QLabel(self.centralwidget)
        self.face_plot.setGeometry(QtCore.QRect(368, 28, 375, 95))
        self.face_plot.setStyleSheet("background-color:rgba(255,255,255,255);")
        self.face_plot.setFrameShape(QtWidgets.QFrame.Box)
        self.face_plot.setLineWidth(3)
        self.face_plot.setText("")
        self.face_plot.setObjectName("face_plot")

        self.fake_check = QtWidgets.QLabel(self.centralwidget)
        self.fake_check.setGeometry(QtCore.QRect(790, 20, 101, 101))
        self.fake_check.setStyleSheet("background-color:rgba(255,255,255,255);")
        self.fake_check.setFrameShape(QtWidgets.QFrame.Box)
        self.fake_check.setLineWidth(3)
        self.fake_check.setText("")
        self.fake_check.setObjectName("fake_check")
        self.fake_check.setPixmap(QtGui.QPixmap("picture/icons8-verify-96.png"))

        self.real_check = QtWidgets.QLabel(self.centralwidget)
        self.real_check.setGeometry(QtCore.QRect(790, 20, 101, 101))
        self.real_check.setStyleSheet("background-color:rgba(255,255,255,255);")
        self.real_check.setFrameShape(QtWidgets.QFrame.Box)

        self.real_check.setLineWidth(3)
        self.real_check.setText("")
        self.real_check.setObjectName("fake_check")
        self.real_check.setPixmap(QtGui.QPixmap("picture/icons8-x-96.png"))

        self.fake_check.hide()
        # self.real_check.hide()

        self.butFile = QtWidgets.QPushButton(self.centralwidget)
        self.butFile.setGeometry(QtCore.QRect(190, 50, 141, 51))
        self.butFile.setObjectName("butFile")
        self.butFile.clicked.connect(self.choose_file)
        self.butFile.setFont(font)

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setParent(self.centralwidget)

        # self.plot_.setPixmap(QtGui.QPixmap("../.designer/backup/1.jpg"))
        # self.canvas.setObjectName("plot_")
        self.data = pd.read_csv('plot.csv')  # Thay đổi thành tên file CSV của bạn
        self.is_animating = False
        # self.ax.set_position([0.5, 0.5, 0.5, 0.8])
        self.canvas.setGeometry(QtCore.QRect(370, 30, 371, 91))

        self.label_2.raise_()
        self.lcamera.raise_()
        self.butBegin.raise_()
        self.butEnd.raise_()
        self.butFile.raise_()
        self.face_plot.raise_()
        self.fake_check.raise_()
        self.real_check.raise_()
        self.canvas.raise_()
        self.setCentralWidget(self.centralwidget)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_screen)
        self.recording = False  # Update every 30 milliseconds

        if not self.is_animating:
            self.is_animating = True
            self.animation = FuncAnimation(self.figure, self.update_plot, frames=len(self.data), interval=1000,
                                           blit=False)
            self.canvas.draw()

    def start_animation(self):
        if not self.is_animating:
            self.is_animating = True
            self.animation = FuncAnimation(self.figure, self.update_plot, frames=len(self.data), interval=1000,
                                           blit=False)
            self.canvas.draw()

    # -------------------------------------------------------------------------

    def update_plot(self, frame):
        self.ax.clear()
        self.ax.plot(self.data.iloc[:frame + 1, 0], self.data.iloc[:frame + 1, 1])
        self.ax.set_title('')
        self.ax.set_xlabel('')
        self.ax.set_ylabel('')
        # Kiểm tra điều kiện để dừng animation khi đã đọc hết file
        if frame == len(self.data) - 1:
            self.is_animating = False
            self.animation.event_source.stop()

        self.canvas.draw()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("mainUI_deepfake", "MainWindow"))
        self.butBegin.setText(_translate("mainUI_deepfake", "Bắt đầu"))
        self.butEnd.setText(_translate("mainUI_deepfake", "Dừng"))
        self.butFile.setText(_translate("mainUI_deepfake", "Chọn File"))

    def choose_file(self):
        fname = QFileDialog.getOpenFileName(self, 'Chọn file', '/home')
        self.file_path = fname[0]
        print(self.file_path)

    def start_recording(self):
        self.recording = True
        self.butBegin.hide()
        self.butEnd.show()

        self.frames = []
        self.timer.start(100)

    def stop_recording(self):
        self.butBegin.show()
        self.butEnd.hide()
        self.recording = False

        self.timer.stop()

        # Process recorded frames and save them as a video
        if self.frames:
            video_writer = cv2.VideoWriter('screen_recording.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 10,
                                           (self.frames[0].width(), self.frames[0].height()))

            for frame in self.frames:
                image = frame.toImage().convertToFormat(QImage.Format_RGBA8888)
                width, height = image.width(), image.height()
                ptr = image.bits()
                ptr.setsize(height * width * 4)
                arr = np.frombuffer(ptr, np.uint8).reshape((height, width, 4))
                video_frame = cv2.cvtColor(arr, cv2.COLOR_RGBA2BGR)
                video_writer.write(video_frame)

            video_writer.release()

            print("Video saved as 'screen_recording.mp4'")
        else:
            print("No frames recorded")

    def update_screen(self):
        if self.recording:
            screen = QScreen.grabWindow(QApplication.primaryScreen(), QApplication.desktop().winId())
            pixmap = QPixmap(screen)

            width = 701  # set your desired width
            height = 391  # set your desired height
            pixmap_resized = pixmap.scaled(width, height)
            # Process the frame (e.g., save it to a list)
            self.frames.append(pixmap)

            # Display the frame in the QLabel
            self.lcamera.setPixmap(pixmap_resized)


# ----------------------------------------------------------------------------------
def get_frame_global():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    global check_stop, nose_location, count_left_eye, count_right_eye
    global frame_itf, frame_left_eye, frame_right_eye, frame_nose
    check_stop = True
    while True:
        ret, frame = cap.read()
        frame_itf = frame
        frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
        frame_mapping = cv2.resize(frame, (1920, 1080))
        frame_mapping.flags.writeable = False
        frame.flags.writeable = False
        results = face_mesh.process(frame)
        results_mapping = face_mesh.process(frame_mapping)
        frame_mapping.flags.writeable = True
        frame.flags.writeable = True
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        frame_mapping = cv2.cvtColor(frame_mapping, cv2.COLOR_RGB2BGR)

        img_h, img_w, img_c = frame.shape
        img_h_m, img_w_m, img_c_m = frame_mapping.shape
        face_3d = []
        face_2d = []

        if results_mapping.multi_face_landmarks:
            for face_landmarks in results_mapping.multi_face_landmarks:
                for idx, lm in enumerate(face_landmarks.landmark):
                    if idx == 1:
                        nose_location = (int(lm.x * img_w_m), int(lm.y * img_h_m))
                        break
            cv2.circle(frame_mapping, nose_location, 5, (0, 255, 0), 1, cv2.LINE_AA)

        if results.multi_face_landmarks:
            mesh_points = np.array(
                [np.multiply([p.x, p.y], [img_w, img_h]).astype(int) for p in results.multi_face_landmarks[0].landmark])
            (l_cx, l_cy), l_radius = cv2.minEnclosingCircle(mesh_points[LEFT_IRIS])
            (r_cx, r_cy), r_radius = cv2.minEnclosingCircle(mesh_points[RIGHT_IRIS])
            center_left = np.array([l_cx, l_cy], dtype=np.int32)
            center_right = np.array([r_cx, r_cy], dtype=np.int32)
            cv2.circle(frame, center_left, 2, (255, 0, 255), 1, cv2.LINE_AA)
            cv2.circle(frame, center_right, 2, (255, 0, 255), 1, cv2.LINE_AA)

            for face_landmarks in results.multi_face_landmarks:
                for idx, lm in enumerate(face_landmarks.landmark):
                    if idx == 33 or idx == 263 or idx == 1 or idx == 61 or idx == 291 or idx == 199:
                        if idx == 1:
                            nose_2d = (lm.x * img_w, lm.y * img_h)

                        x, y = int(lm.x * img_w), int(lm.y * img_h)

                        face_2d.append([x, y])
                        face_3d.append([x, y, lm.z])

                    if idx == 225:
                        eye_left = (int(lm.x * img_w), int(lm.y * img_h))
                        cv2.circle(frame, (int(lm.x * img_w), int(lm.y * img_h)), 3, (255, 0, 255))
                    if idx == 228:
                        eye_left1 = (int(lm.x * img_w), int(lm.y * img_h))
                        cv2.circle(frame, (int(lm.x * img_w), int(lm.y * img_h)), 3, (255, 0, 255))
                    if idx == 128:
                        eye_left2 = (int(lm.x * img_w), int(lm.y * img_h))
                        cv2.circle(frame, (int(lm.x * img_w), int(lm.y * img_h)), 3, (255, 0, 255))
                    if idx == 221:
                        eye_left3 = (int(lm.x * img_w), int(lm.y * img_h))
                        cv2.circle(frame, (int(lm.x * img_w), int(lm.y * img_h)), 3, (255, 0, 255))

                    if idx == 441:
                        eye_right = (int(lm.x * img_w), int(lm.y * img_h))
                        cv2.circle(frame, (int(lm.x * img_w), int(lm.y * img_h)), 3, (255, 0, 255))
                    if idx == 445:
                        eye_right1 = (int(lm.x * img_w), int(lm.y * img_h))
                        cv2.circle(frame, (int(lm.x * img_w), int(lm.y * img_h)), 3, (255, 0, 255))
                    if idx == 448:
                        eye_right2 = (int(lm.x * img_w), int(lm.y * img_h))
                        cv2.circle(frame, (int(lm.x * img_w), int(lm.y * img_h)), 3, (255, 0, 255))
                    if idx == 412:
                        eye_right3 = (int(lm.x * img_w), int(lm.y * img_h))
                        cv2.circle(frame, (int(lm.x * img_w), int(lm.y * img_h)), 3, (255, 0, 255))
                    if idx in LEFT_IRIS:
                        bli_leftx.append((int(lm.x * img_w)))
                        bli_lefty.append((int(lm.y * img_h)))
                    if idx in RIGHT_IRIS:
                        bli_rightx.append((int(lm.x * img_w)))
                        bli_righty.append((int(lm.y * img_h)))

                face_2d = np.array(face_2d, dtype=np.float64)
                face_3d = np.array(face_3d, dtype=np.float64)

                focal_length = 1 * img_w

                cam_matrix = np.array([[focal_length, 0, img_h / 2],
                                       [0, focal_length, img_w / 2],
                                       [0, 0, 1]])

                dist_matrix = np.zeros((4, 1), dtype=np.float64)
                success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)
                rmat, jac = cv2.Rodrigues(rot_vec)
                angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3((rmat))

                x = angles[0] * 360
                y = angles[1] * 360
                z = angles[2] * 360

                p1 = (int(nose_2d[0]), int(nose_2d[1]))
                p2 = (int(nose_2d[0] + y * 10), int(nose_2d[1] - x * 10))

                cv2.circle(frame, p1, 3, (255, 0, 255))
                cv2.line(frame, (0, p1[1]), (640, p1[1]), (255, 0, 0), 1)
                cv2.line(frame, (p1[0], 0), (p1[0], 480), (255, 0, 0), 1)
                cv2.line(frame, (0, center_right[1]), (640, center_right[1]), (0, 255, 0), 1)
                cv2.line(frame, (center_right[0], 0), (center_right[0], 480), (0, 255, 0), 1)
                cv2.line(frame, (0, center_left[1]), (640, center_left[1]), (0, 255, 0), 1)
                cv2.line(frame, (center_left[0], 0), (center_left[0], 480), (0, 255, 0), 1)

                # --------------------------------------put on interface--------------------------------------
                frame_left_eye = frame[eye_left[1] - 20: eye_left[1] + eye_left1[1] - eye_left[1],
                                 eye_left[0]: eye_left[0] + eye_left3[0] - eye_left[0]]
                frame_right_eye = frame[eye_right[1] - 20: eye_right3[1], eye_right[0]: eye_right1[0]]
                frame_nose = frame[p1[1] - 25: p1[1] + 25, p1[0] - 25: p1[0] + 25]
                # -------------------------------------------------------

                count_left_eye = frame[min(bli_lefty): max(bli_lefty), min(bli_leftx): max(bli_leftx)]
                count_right_eye = frame[min(bli_righty) + 3: max(bli_righty),
                                  min(bli_rightx): max(bli_rightx)]

                bli_lefty.clear()
                bli_leftx.clear()
                bli_rightx.clear()
                bli_righty.clear()

                # mp_drawing.draw_landmarks(image=frame,
                #                         landmark_list=face_landmarks,
                #                         connections=mp_face_mesh.FACEMESH_CONTOURS,
                #                         landmark_drawing_spec=drawing_spec,
                #                         connection_drawing_spec=drawing_spec)

        frame_mapping = cv2.rectangle(frame_mapping, (800, 500), (1000, 600), (0, 255, 0), 3)
        # cv2.imshow('Camera', count_left_eye)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            check_stop = False
            break

    cap.release()
    cv2.destroyAllWindows()


def blinking():
    time.sleep(1)
    global check_stop, count_left_eye, count_right_eye

    check_count_l = False
    check_count_r = False
    check_eye_left = False
    check_eye_right = False
    past_time = time.time()
    count_l = 0
    count_r = 0

    while True:
        left_02 = cv2.cvtColor(count_left_eye, cv2.COLOR_BGR2GRAY)
        _, left_02 = cv2.threshold(left_02, 30, 255, cv2.THRESH_BINARY)
        right_02 = cv2.cvtColor(count_right_eye, cv2.COLOR_BGR2GRAY)
        _, right_02 = cv2.threshold(right_02, 30, 255, cv2.THRESH_BINARY)

        current_right = np.mean(left_02)
        current_left = np.mean(right_02)

        if check_count_r == False:
            if current_left > 200 and check_eye_left == False and check_count_l == False:
                check_eye_left = True
                print("-------------")
            elif current_left < 190 and check_eye_left == True and check_count_l == False:
                print("-------------------Blinking Left--------------------------")
                check_eye_left = False
                check_count_l = True
                past_time = time.time()
            if time.time() - past_time <= 1 and check_count_l == True:
                if current_left > 200 and check_eye_left == False and check_count_l == True:
                    check_eye_left = True
                elif current_left < 190 and check_eye_left == True and check_count_l == True:
                    print("-------------------COUNT--------------------------")
                    check_eye_left = False
                    count_l += 1
            elif count_l == 0 and check_count_l == True:
                print("Click")
                pyautogui.click(button='left')
                check_count_l = False
                count_l = 0
            elif count_l == 1 and check_count_l == True:
                print("DouClick")
                pyautogui.doubleClick()
                check_count_l = False
                count = 0
            elif count_l == 2 and check_count_l == True:
                print("Scolling Up")
                pyautogui.scroll(500)
                check_count_l = False
                count_l = 0
            else:
                check_count_l = False
                count_l = 0

        if check_count_l == False:
            if current_right > 210 and check_eye_right == False and check_count_r == False:
                check_eye_right = True
                print("-------------")
            if current_right < 190 and check_eye_right == True and check_count_r == False:
                print("-------------------Blinking Right--------------------------")
                check_eye_right = False
                check_count_r = True
                past_time = time.time()
            if time.time() - past_time <= 1.5 and check_count_r == True:
                if current_right > 200 and check_eye_right == False and check_count_r == True:
                    check_eye_right = True
                elif current_right < 190 and check_eye_right == True and check_count_r == True:
                    print("-------------------COUNT--------------------------")
                    check_eye_right = False
                    count_r += 1
            elif count_r == 0 and check_count_r == True:
                print("Click_Right")
                pyautogui.click(button='right')
                check_count_r = False
                count_r = 0
            elif count_r == 1 and check_count_r == True:
                print("Copy")
                pyautogui.keyDown('shift')
                pyautogui.click(button='left')
                pyautogui.keyUp('shift')

                pyautogui.keyDown('ctrl')
                pyautogui.press('c')
                pyautogui.keyUp('ctrl')

                check_count_r = False
                count_r = 0
            elif count_r == 2 and check_count_r == True:
                print("Scolling Down")
                pyautogui.scroll(-500)
                check_count_r = False
                count_r = 0
            else:
                check_count_r = False
                count_r = 0

        if check_stop == False:
            break


def mapping_screen():
    time.sleep(1)
    global check_stop, nose_location
    global clocX, clocY
    wScr, hScr = pyautogui.size()
    smoothening = 10
    plocX, plocY = 0, 0
    clocX, clocY = 0, 0

    sum_x, sum_y = 0, 0
    ave_x, ave_y = 0, 0
    count, coef_ave = 0, 5

    while True:
        count += 1
        sum_x += nose_location[0]
        sum_y += nose_location[1]
        if count == coef_ave:
            ave_x = int(sum_x / coef_ave)
            ave_y = int(sum_y / coef_ave)
            sum_x, sum_y, count = 0, 0, 0

            xScr = np.interp(ave_x, (800, 1000), (0, wScr))  # (900,500), (1100, 600)
            yScr = np.interp(ave_y, (500, 600), (0, hScr))
            clocX = plocX + (xScr - plocX) / smoothening
            clocY = plocY + (yScr - plocY) / smoothening
            pyautogui.moveTo(clocX, clocY, 0.1)
            plocX, plocY = clocX, clocY

        if check_stop == False:
            break


if __name__ == "__main__":
    app = QApplication(sys.argv)
    db = dock_bar()

    thread1 = threading.Thread(target=assistant)
    thread1.start()
    x = threading.Thread(target=get_frame_global)
    x.start()
    y = threading.Thread(target=mapping_screen)
    y.start()
    z = threading.Thread(target=blinking)
    z.start()

    db.show()
    sys.exit(app.exec_())