from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import json
import sys
from datetime import datetime
from functools import partial
from urllib.request import urlopen
import matplotlib.ticker as plticker


from PyQt5.QtCore import Qt, QTimer, QTime, QDate
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QMainWindow, QLabel, QPushButton, QPlainTextEdit, QMessageBox, QSizePolicy, QFrame
from matplotlib.figure import Figure
#from pip._vendor import requests
import requests


class MainStage(QMainWindow):

    progress = 0
    x, y = 0, 0
    lbl_cities = []
    appid = "d686a273dc94c3dfbf99d950901e55bb"

    def __init__(self):
        super(MainStage, self).__init__()
        # List of major cities
        self.target_cities = ['Banda Aceh', 'Medan', 'Tanjungpinang', 'Pekanbaru', 'Padang',
                         'Jambi', 'Propinsi Bengkulu', 'Palembang', 'Pangkalpinang', 'Bandarlampung',
                         'Jakarta','Serang', 'Bandung', 'Semarang', 'Yogyakarta',
                         'Surabaya', 'Denpasar', 'Mataram', 'Kupang', 'Pontianak',
                         'Palangkaraya', 'Banjarmasin', 'Samarinda', 'Tarakan', 'Makassar',
                         'Mamuju', 'Kendari', 'Palu', 'Gorontalo', 'Manado',
                         'Ambon', 'Kota Ternate', 'Manokwari', 'Ifaar']

        # List of city cooridinates
        self.cities_coordinates = [{'name':'Banda Aceh','x':37,'y':35},{'name':'Medan','x':110, 'y':80},{'name':'Tanjungpinang','x':230,'y':131},{'name':'Pekanbaru','x':150,'y':140},{'name':'Padang','x':120,'y':193},
                                   {'name':'Jambi','x':220,'y':200},{'name':'Propinsi Bengkulu','x':130,'y':252},{'name':'Palembang','x':200,'y':252},{'name':'Pangkalpinang','x':285,'y':218},{'name':'Bandarlampung','x':223,'y':293},
                                   {'name':'Jakarta','x':300,'y':303},{'name':'Serang','x':240,'y':365},{'name':'Bandung','x':298,'y':385},{'name':'Semarang','x':368,'y':322},{'name':'Yogyakarta','x':367,'y':410},
                                   {'name':'Surabaya','x':450,'y':342},{'name':'Denpasar','x':480,'y':430},{'name':'Mataram','x':522,'y':362},{'name':'Kupang','x':700,'y':467},{'name':'Pontianak','x':320,'y':165},
                                   {'name':'Palangkaraya','x':433,'y':205},{'name':'Banjarmasin','x':500,'y':256},{'name':'Samarinda','x':520,'y':164},{'name':'Tarakan','x':565,'y':84},{'name':'Makassar','x':585,'y':338},
                                   {'name':'Mamuju','x':568,'y':234},{'name':'Kendari','x':690,'y':301},{'name':'Palu','x':650,'y':206},{'name':'Gorontalo','x':650,'y':140},{'name':'Manado','x':712,'y':118},
                                   {'name':'Ambon','x':792,'y':306},{'name':'Kota Ternate','x':830,'y':149},{'name':'Manokwari','x':930,'y':174},{'name':'Ifaar','x':1060,'y':228}]

        # List of weather forecasts
        self.fut_list = []
        # List of current weather
        self.cur_list = []
        # Get json
        #self.get_json()

        self.initUI()


    def initUI(self):

        # Size and position
        self.setGeometry(300, 300, 1100, 882)

        # Set center
        qtRec = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRec.moveCenter(centerPoint)
        self.move(qtRec.topLeft())

        # Window title
        self.setWindowTitle('Weather Information in Major Indonesian Cities')
        self.setWindowIcon(QIcon('images/Zephyrus_logo2.png'))
        self.setStyleSheet('QMainWindow{background-color: white}')

        # Set mouse tracking
        self.setMouseTracking(True)

        # First half - map
        lblBG = QLabel(self)
        lblBG.move(0, 0)
        lblBG.resize(1100, 650)
        #lblBG.resize(1200, 500)
        lblBG.setStyleSheet('background-color: white; color: black')
        lblBG.setText('')
        lblBG.setAlignment(Qt.AlignTop)
        lblBG.setFont(QFont("Times", 16))

        # Resize image
        pixmap = QPixmap('images/indonesian_cities_map2.png')
        pixmap = pixmap.scaledToHeight(463)

        lblBG.setPixmap(pixmap)

        # Second half - info1
        self.lbl_info1 = QLabel(self)
        self.lbl_info1.move(10, 653)
        self.lbl_info1.resize(538, 154)
        #self.lbl_info1.setStyleSheet('background-color: rgb(89,182,220); border: 0.5px solid black; border-radius: 10px; color: black')
        self.lbl_info1.setStyleSheet('background-color: lightblue; border-radius: 10px; color: black')
        self.lbl_info1.setAlignment(Qt.AlignTop)
        self.lbl_info1.setFont(QFont("black", 17))
        self.lbl_info1.setText("   Click city to get detailed weather here")
        self.lbl_info1.setFrameShape(QFrame.StyledPanel)
        self.lbl_info1.setFrameShadow(QFrame.Raised)

        # Second half - info2
        self.lbl_info2 = QLabel(self)
        self.lbl_info2.move(550, 653)
        self.lbl_info2.resize(538, 154)
        self.lbl_info2.setStyleSheet('background-color: lightblue; border-radius: 10px; color: black')
        self.lbl_info2.setAlignment(Qt.AlignTop)
        self.lbl_info2.setFont(QFont("black", 17))
        self.lbl_info2.setText("\n")
        self.lbl_info2.setFrameShape(QFrame.StyledPanel)
        self.lbl_info2.setFrameShadow(QFrame.Raised)

        # lbl for search_by_city
        self.lbl_search = QLabel(self)
        self.lbl_search.setFrameShape(QFrame.StyledPanel)
        self.lbl_search.setFrameShadow(QFrame.Raised)
        self.lbl_search.move(10, 815)
        self.lbl_search.resize(1080, 40)
        self.lbl_search.setStyleSheet('background-color: lightblue; color: black')
        self.lbl_search.setFont(QFont("black", 13))
        self.lbl_search.setText("   Search by City: ")

        # Textarea for city name
        self.te = QPlainTextEdit(self.lbl_search)
        self.te.move(200, 5)
        self.te.resize(300, 30)
        self.te.setStyleSheet('background-color: white')
        self.te.insertPlainText("Enter the city name here...")

        # Button for search for current weather
        self.btn_search_cur = QPushButton(self.lbl_search)
        self.btn_search_cur.move(535, 5)
        self.btn_search_cur.resize(250, 30)
        #self.btn_search_cur.setStyleSheet('background-color: rgb(89,182,220); border: 3px solid black; border-radius: 10px; color: black')
        self.btn_search_cur.setText("Search for current weather")
        #self.btn_search_cur.mousePressEvent = self.search_by_postcode_cur

        # Button for search for future weather
        self.btn_search_cur = QPushButton(self.lbl_search)
        self.btn_search_cur.move(800, 5)
        self.btn_search_cur.resize(250, 30)
        self.btn_search_cur.setText("Search for future weather")
        #self.btn_search_cur.mousePressEvent = self.search_by_postcode_fut

        self.city_labels()

        # Timer for the clock
        #timer = QTimer(self)
        #timer.timeout.connect(self.showTime)
        #timer.start(1000)
        #self.showTime()

        #Weather data source
        lblSC = QLabel(self)
        lblSC.move(20, 430)
        lblSC.resize(1280, 254)
        pixmapSC = QPixmap('images/datasource.png')
        pixmapSC = pixmapSC.scaledToHeight(35)
        lblSC.setPixmap(pixmapSC)
        
        #Created by
        lblCB = QLabel(self)
        lblCB.move(904, 428)
        lblCB.resize(1280, 254)
        pixmapCB = QPixmap('images/zephyrus_logo.png')
        pixmapCB = pixmapCB.scaledToHeight(35)
        lblCB.setPixmap(pixmapCB)

        self.show()


    def city_labels(self):
        # Labels of cities
        for i in range(len(self.cities_coordinates)):
            self.lbl_cities.append(QLabel(self))
            self.lbl_cities[i].move(self.cities_coordinates[i]['x']-20,
                                    self.cities_coordinates[i]['y']-34)

        # Tooltips and icon
        for i in range(len(self.cities_coordinates)):
            #icon = QPixmap('images/indonesian_cities_map.png')
            self.progress += 1
            #with urlopen('http://openweathermap.org/img/w/' + icon + '.png') as url:
            #    data = url.read()
            pixmap = QPixmap('images/favicon.ico')
            #pixmap.loadFromData(data)

            pixmap = pixmap.scaledToHeight(45)

            #tool_tip_string = '    City: ' + self.cur_list[i]['name']
            #tool_tip_string += '\n    Humidity: ' + str(self.cur_list[i]['main']['humidity']) + '%'
            #tool_tip_string += '\n    Weather: ' + self.cur_list[i]['weather'][0]['description']
            #tool_tip_string += '\n    Sunrise: ' + str(datetime.fromtimestamp(int(self.cur_list[i]['sys']['sunrise'])))
            #tool_tip_string += '\n    Sunset: ' + str(datetime.fromtimestamp(int(self.cur_list[i]['sys']['sunset'])))
            #tool_tip_string += '\n    Temperature: ' + str(round(self.k_to_f(int(self.cur_list[i]['main']['temp'])), 2)) + '°F'

            #self.lbl_cities[i].mousePressEvent = partial(self.show_info, i)

            self.lbl_cities[i].setPixmap(pixmap)
            #self.lbl_cities[i].setToolTip(tool_tip_string)



if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MainStage()
    sys.exit(app.exec())