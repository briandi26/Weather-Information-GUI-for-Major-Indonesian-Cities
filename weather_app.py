#weather_app

"""
This is a python project about current and future weather
information of major Indonesian cities.
"""

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
        self.get_json()

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
        self.btn_search_cur.setText("Search for current weather")
        self.btn_search_cur.mousePressEvent = self.search_by_city_cur

        # Button for search for future weather
        self.btn_search_cur = QPushButton(self.lbl_search)
        self.btn_search_cur.move(800, 5)
        self.btn_search_cur.resize(250, 30)
        self.btn_search_cur.setText("Search for future weather")
        self.btn_search_cur.mousePressEvent = self.search_by_city_fut

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

        self.city_labels()

        # Timer for the clock
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        self.showTime()

        self.show()


    # Show date and clock
    def showTime(self):
        time = QTime.currentTime()
        text = QDate.currentDate().toString() + ' ' + time.toString('hh:mm:ss')

        self.statusBar().showMessage('   Today:    ' + text)


    def city_labels(self):
        # Labels of cities
        for i in range(len(self.cities_coordinates)):
            self.lbl_cities.append(QLabel(self))
            self.lbl_cities[i].move(self.cities_coordinates[i]['x'] - 20,
                                    self.cities_coordinates[i]['y'] - 34)

        # Tooltips and icon
        for i in range(len(self.cities_coordinates)):
            icon = self.cur_list[i]['weather'][0]['icon']
            self.progress += 1
            with urlopen('http://openweathermap.org/img/w/' + icon + '.png') as url:
                data = url.read()
            pixmap = QPixmap()
            pixmap.loadFromData(data)

            pixmap = pixmap.scaledToHeight(45)

            tool_tip_string = '    City: ' + self.cur_list[i]['name']
            tool_tip_string += '\n    Humidity: ' + str(self.cur_list[i]['main']['humidity']) + '%'
            tool_tip_string += '\n    Weather: ' + self.cur_list[i]['weather'][0]['description']
            tool_tip_string += '\n    Sunrise: ' + str(datetime.fromtimestamp(int(self.cur_list[i]['sys']['sunrise'])))
            tool_tip_string += '\n    Sunset: ' + str(datetime.fromtimestamp(int(self.cur_list[i]['sys']['sunset'])))
            tool_tip_string += '\n    Temperature: ' + str(round(self.k_to_c(self.cur_list[i]['main']['temp']), 2)) + '°C'
            tool_tip_string += '\n    Wind: ' + str(round(self.cur_list[i]['wind']['speed'], 2)) + ' m/s'

            self.lbl_cities[i].mousePressEvent = partial(self.show_info, i)

            self.lbl_cities[i].setPixmap(pixmap)
            self.lbl_cities[i].setToolTip(tool_tip_string)


    # Search for future weather by city name
    def search_by_city_fut(self, event):
        cityname = self.te.toPlainText()

        #if cityname.isdigit():
        url = "http://api.openweathermap.org/data/2.5/forecast?q=" + cityname + ",id&appid=" + self.appid
        weather = requests.get(url).json()

        try:
            title = "City: " + weather['city']['name']
            info1 = ""
            info2 = ""
            for i in range(0, 20, 2):
                info1 += "\n    Time: " + weather['list'][i]['dt_txt']
                info1 += "\n    Weather: " + weather['list'][i]['weather'][0]['description']
                info1 += "\n    Temperature: " + str(round(self.k_to_c(weather['list'][i]['main']['temp']), 2)) + "°C" + "\n"

            for i in range(20, len(weather['list']), 2):
                info2 += "\n    Time: " + weather['list'][i]['dt_txt']
                info2 += "\n    Weather: " + weather['list'][i]['weather'][0]['description']
                info2 += "\n    Temperature: " + str(round(self.k_to_c(weather['list'][i]['main']['temp']), 2)) + "°C" + "\n"

            self.new_window = ForecastWindow()
            self.new_window.lbl_info1.setText(info1)
            self.new_window.lbl_info2.setText(info2)
            self.new_window.lbl_Title.setText(title)
            self.new_window.show()
            self.new_window1 = Stat(weather)
            self.new_window1.show()
        except:
            QMessageBox.about(self, "Error", "Please enter a valid city name.")

        #else:
        #    QMessageBox.about(self, "Error", "Numbers only.")



    # Search for current weather by city name
    def search_by_city_cur(self, event):
        cityname = self.te.toPlainText()

        #if cityname.isdigit():
        url = "http://api.openweathermap.org/data/2.5/weather?q=" + cityname + ",id&appid=" + self.appid
        weather = requests.get(url).json()

        try:
            # First half weather info
            info1 = '    City: ' + weather['name']
            info1 += '\n    Humidity: ' + str(weather['main']['humidity']) + '%'
            info1 += '\n    Weather: ' + weather['weather'][0]['description']
            info1 += '\n    Pressure: ' + str(weather['main']['pressure']) + ' hPa'

            # Second half weather info
            info2 = '    Sunrise: ' + str(datetime.fromtimestamp(int(weather['sys']['sunrise'])))
            info2 += '\n    Sunset: ' + str(datetime.fromtimestamp(int(weather['sys']['sunset'])))
            info2 += '\n    Temperature: ' + str(round(self.k_to_c(weather['main']['temp']), 2)) + ' °C'
            info2 += '\n    Wind: ' + str(round(weather['wind']['speed'], 2)) + ' m/s'

            self.lbl_info1.setText(info1)
            self.lbl_info2.setText(info2)
        except:
            QMessageBox.about(self, "Error", "Please enter a valid city name.")
        #else:
        #    QMessageBox.about(self, "Error", "Numbers only.")


    # Display current weather on the lbl_info
    def show_info(self, i, event):
        # First half weather info
        info1 = '    City: ' + self.cur_list[i]['name']
        info1 += '\n    Humidity: ' + str(self.cur_list[i]['main']['humidity']) + '%'
        info1 += '\n    Weather: ' + self.cur_list[i]['weather'][0]['description']
        info1 += '\n    Pressure: ' + str(self.cur_list[i]['main']['pressure']) + ' hPa'

        # Second half weather info
        info2 = '    Sunrise: ' + str(datetime.fromtimestamp(int(self.cur_list[i]['sys']['sunrise'])))
        info2 += '\n    Sunset: ' + str(datetime.fromtimestamp(int(self.cur_list[i]['sys']['sunset'])))
        info2 += '\n    Temperature: ' + str(round(self.k_to_c(self.cur_list[i]['main']['temp']), 2)) + ' °C'
        info2 += '\n    Wind: ' + str(round(self.cur_list[i]['wind']['speed'], 2)) + ' m/s'

        self.lbl_info1.setText(info1)
        self.lbl_info2.setText(info2)


    # Write into json file
    def get_json(self):
        for city in self.target_cities:
            # self.future_weather(city)
            self.current_weather(city)


    #
    # Get weather forecast from OpenWeatherMap.org
    def future_weather(self, city):
        api_address = 'http://api.openweathermap.org/data/2.5/forecast?q=' + city + ',id&appid=' + self.appid
        fut_wea = requests.get(api_address).json()
        self.fut_list.append(fut_wea)


    # Get current weather from OpenWeatherMap.org
    def current_weather(self, city):
        api_address = 'http://api.openweathermap.org/data/2.5/weather?q=' + city + ',id&appid=' + self.appid
        curr_wea = requests.get(api_address).json()
        self.cur_list.append(curr_wea)


    # # Mouse coordinates for adjustment
    # def mouseMoveEvent(self, e):
    #     self.x, self.y = e.x(), e.y()
    #
    #     self.statusBar().showMessage('x: ' + str(self.x) + ' y: ' + str(self.y))


    # Convert K to f:
    def k_to_c(self, k):
        return k - 273.15


class ForecastWindow(QWidget):

    def __init__(self):
        super(ForecastWindow, self).__init__()

        self.initUI()


    def initUI(self):

        self.move(100, 100)
        self.resize(600, 880)
        self.setWindowTitle("Weather Forecast")
        self.setWindowIcon(QIcon('images/Zephyrus_logo2.png'))
        self.setStyleSheet("background-color: lightblue")

        self.lbl_Title = QLabel(self)
        self.lbl_Title.setAlignment(Qt.AlignCenter)
        self.lbl_Title.move(150, 10)
        self.lbl_Title.resize(300, 40)
        self.lbl_Title.setFont(QFont("black", 14))
        self.lbl_Title.setStyleSheet("background-color: white")
        self.lbl_Title.setFrameShape(QFrame.StyledPanel)

        self.lbl_info1 = QLabel(self)
        self.lbl_info1.move(5, 60)
        self.lbl_info1.setFont(QFont("black", 12))
        self.lbl_info1.resize(290, 800)
        self.lbl_info1.setAlignment(Qt.AlignTop)
        self.lbl_info1.setStyleSheet("background-color: white")
        self.lbl_info1.setFrameShape(QFrame.StyledPanel)
        self.lbl_info1.setFrameShadow(QFrame.Raised)

        self.lbl_info2 = QLabel(self)
        self.lbl_info2.move(305, 60)
        self.lbl_info2.setFont(QFont("black", 12))
        self.lbl_info2.resize(290, 800)
        self.lbl_info2.setAlignment(Qt.AlignTop)
        self.lbl_info2.setStyleSheet("background-color: white")
        self.lbl_info2.setFrameShape(QFrame.StyledPanel)
        self.lbl_info2.setFrameShadow(QFrame.Raised)

        self.show()


class Stat(QMainWindow):

    def __init__(self, weather):
        super(Stat, self).__init__()
        self.weather = weather
        self.initUI()


    def initUI(self):
        self.setWindowTitle("Temperature Trend")
        self.setWindowIcon(QIcon('images/Zephyrus_logo2.png'))
        self.setGeometry(700, 100, 900, 410)

        m = PlotCanvas(self, width=9, height=7, dpi=100, weather=self.weather)
        m.move(0, 0)

        self.show()


class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=10, height=10, dpi=100, weather=None):
        fig = Figure(figsize=(width, height), dpi=dpi)

        self.weather = weather

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()


    def plot(self):
        # self.weather = json.load(open('future_weather.json'))
        self.time = []
        self.temps = []
        for i in range(len(self.weather['list'])):
            result = self.weather['list'][i]['dt_txt']
            result = result[result.find("-") + 1:result.find(":")]
            self.time.append(result)
            temp = round((self.weather['list'][i]['main']['temp'] - 273.15), 1)
            self.temps.append(temp)

        # Set area
        ax = self.figure.add_subplot(211)

        ax.set_title('Temperature Trend in Next 5 Days', fontsize=18)
        ax.set_xlabel('Date and Time', fontsize=12)
        ax.set_ylabel('Temperature (°C)', fontsize=12)

        x = range(len(self.time))
        ax.plot(x, self.temps)

        # Customize x bar label
        ax.set_xticklabels(self.time, rotation=35, fontsize=7)

        # Set axis max and min values
        ax.axis([0, len(self.weather['list']) - 1, min(self.temps) - 10, max(self.temps) + 10])

        # Set x bar intervals
        loc = plticker.MultipleLocator(base = 1)
        ax.xaxis.set_major_locator(loc)

        self.draw()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = MainStage()
    sys.exit(app.exec())


