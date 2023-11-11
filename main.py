import json
import sys
import traceback
import os
import  configparser
from PyQt5.QtCore import *
from PyQt5.QtWidgets import  QMainWindow,QApplication,QTableWidgetItem,QFileDialog,QApplication
from window import Ui_Football
from pathlib import Path
from Database import Data
from ThreadPreMatch import Thread_1
from Thread_2 import Thread_2
from graphqlclient import GraphQLClient
from  Api import query
from time import sleep
from queue import Queue

queue = Queue()


def callback(_id,data):
    return data

class ReceiveData(QThread):

    def __init__(self, mainwindow, parent=None):
        QThread.__init__(self, parent)
        self.mainwindow = mainwindow
        self.queue = queue


    def run(self):
        try:
            day_id = self.mainwindow.ui.lineEdit_5.text()
            query = f"""
                        subscription ScoreUpdated {{
                        scoreUpdated(dayId:{day_id}) {{
                          performance {{
                                mainNumber
                                kind {{
                                  id
                                  name
                                }}
                                sportsman {{
                                  id
                                  firstName
                                  lastName
                                  category {{
                                    id
                                    name
                                  }}
                                }}
    
                            sportsmanGroup {{
                                    id
                                    name
                                    category {{
                                      id
                                      name
                                      type
                                    }}
                                    }}
                                    sportsman {{
                                      id
                                      numberInCategory
                                      firstName
                                      lastName
                                      country {{
                                                name
                                                }}
                                    }}
                        score {{
                                finalScore
                                d1
                                d2
                                d3
                                finalA
                                finalE
                                masterDB
                                masterDA
                                deduction
                            }}
    
                      }}
    
    
    
                    }}
                }}
                    """
            client = GraphQLClient(self.mainwindow.ui.lineEdit_4.text())

            while True:
                data = client.execute(query)
                data = json.loads(data)
                print(type(data))
                try:
                    data['payload']
                    self.queue.put(data['payload']['data']['scoreUpdated']['performance'])
                except:
                    print(data)
                    print('Жду данных')
                self.write_logs(data)
        except:
            print(traceback.format_exc())


    def write_logs(self,data):
        file = open("logs_subscription.txt", "a")
        json.dump(data,file)
        file.write('\n')



class ProcessData(QThread):
    def __init__(self, mainwindow, parent=None):
        QThread.__init__(self, parent)
        self.mainwindow = mainwindow
        self.queue = queue
        self.database = Data(self.mainwindow.ui.lineEdit_3.text())

    def run(self):
        DayID = self.mainwindow.ui.lineEdit_5.text()
        EventID = self.mainwindow.ui.lineEdit.text()
        while True:
            if self.queue.not_empty:
                try:

                    data = queue.get()

                    # Обработка и вставка резов спортсмена в БД

                    KindID =data['kind']['id']
                    ZaezdPlayerPointsDifficulty = (
                        data['score']["masterDB"] if data['score']["masterDB"] else data['score']["d1"]
                    )
                    ZaezdPlayerPointsDifficulty2 = (
                        data['score']["masterDA"] if data['score']["masterDA"] else data['score']["d3"]
                    )
                    ZaezdPlayerPoints = data['score']["finalScore"] if data['score']["finalScore"] else 0
                    ZaezdPlayerPointsSum = data['score']["finalScore"] if data['score']["finalScore"] else 0
                    ZaezdPlayerPointsShtraf = data['score']["deduction"] if data['score']["deduction"] else 0
                    ZaezdPlayerPointsArtistic = data['score']["finalA"] if data['score']["finalA"] else 0
                    ZaezdPlayerPointsExecution = data['score']["finalE"] if data['score']["finalE"] else 0

                    if data['sportsman']!= None:
                        SportsmanID = data['sportsman']['id']
                        CategoryID = data['sportsman']['category']['id']
                    else:
                        SportsmanID = data['sportsmanGroup']['id']
                        CategoryID = data['sportsmanGroup']['category']['id']

                    ZaezdID = str(CategoryID) +  str(KindID) + DayID
                    try:
                        SportsmanID = self.database.select_player_id_by_ext(SportsmanID)
                    except:
                        print('Спортсмен не найден')
                        return
                    res = tuple(
                        [ZaezdPlayerPointsSum, ZaezdPlayerPoints, ZaezdPlayerPointsShtraf, ZaezdPlayerPointsDifficulty,
                         ZaezdPlayerPointsArtistic, ZaezdPlayerPointsExecution,
                         ZaezdPlayerPointsDifficulty2, ZaezdID,
                         SportsmanID])
                    print(res)
                    # Вставляем в БД
                    try:
                        self.database.update_score(res)
                    except:
                        print(traceback.format_exc())

                except:
                    pass




class ImageDialog(QMainWindow):

    def __init__(self):
        super().__init__()
        self.settings = QSettings('FootballRuStat', 'FootballRuStat')

        # Set up the user interface from Designer.
        self.ui =Ui_Football()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.pick_database)
        self.ui.pushButton_2.clicked.connect(self.launch_thread)
        self.ui.pushButton_4.clicked.connect(self.clear_database)
        self.ui.pushButton_6.clicked.connect(self.launch_thread2)
        self.ui.pushButton_5.clicked.connect(self.start_subscription)
        self.set_old_values()
    def pick_database(self):
        home_dir = str(Path.home())
        fname = QFileDialog.getOpenFileName(self, 'Выбрать базу данных', home_dir, "*.mdb")
        temp = fname[0].split('/')
        road_database = fname[0]
        try:
            databasa = Data(road_database)
        except:
            print(traceback.format_exc())
        self.ui.lineEdit_3.setText(road_database)
        self.ui.pushButton.setText(temp[-1])

    def launch_thread(self):
        try:
            if self.mythread_2.isRunning():
                self.mythread_2.terminate()
                self.mythread_2 = Thread_1(mainwindow=self)
                self.mythread_2.signal_status.connect(self.change_status_prematch)

                self.mythread_2.start()

            else:
                self.mythread_2 = Thread_1(mainwindow=self)
                self.mythread_2.signal_status.connect(self.change_status_prematch)

                self.mythread_2.start()
        except:
            self.mythread_2 = Thread_1(mainwindow=self)
            self.mythread_2.signal_status.connect(self.change_status_prematch)
            self.mythread_2.start()



    def change_status_prematch(self,item:tuple):
        if item[0] == 3:
            if item[1] == 1:
                self.ui.label_3.setStyleSheet('font: bold 14px;color:rgb(0,170,0)')
                self.ui.label_3.setText('Zaezd')
            else:
                self.ui.label_3.setStyleSheet('font: bold 14px;color:rgb(255,0,0)')
                self.ui.label_3.setText('Zaezd')

        elif item[0] == 4:
            if item[1] == 1:
                self.ui.label_4.setStyleSheet('font: bold 14px;color:rgb(0,170,0)')
                self.ui.label_4.setText('Players')
            else:
                self.ui.label_4.setStyleSheet('font: bold 14px;color:rgb(255,0,0)')
                self.ui.label_4.setText('Players')

        elif item[0] == 5:
            if item[1] == 1:
                self.ui.label_5.setStyleSheet('font: bold 14px;color:rgb(0,170,0)')
                self.ui.label_5.setText('ZaezdMaps')
            else:
                self.ui.label_5.setStyleSheet('font: bold 14px;color:rgb(255,0,0)')
                self.ui.label_5.setText('ZaezdMaps')

    def set_old_values(self):
        try:
            self.ui.lineEdit.setText(self.settings.value('tour_id'))
            self.ui.lineEdit_3.setText(self.settings.value('road_database'))
            self.ui.lineEdit_4.setText(self.settings.value('url'))
            self.ui.lineEdit_5.setText(self.settings.value('day_id'))
        except:
            print(traceback.format_exc())

    def closeEvent(self, event):
        self.settings.setValue('url', self.ui.lineEdit_4.text())
        self.settings.setValue('road_database', self.ui.lineEdit_3.text())
        self.settings.setValue('tour_id', self.ui.lineEdit.text())
        self.settings.setValue('day_id',self.ui.lineEdit_5.text())

    def clear_database(self):
        database = Data(self.ui.lineEdit_3.text())
        database.clear_database()



    def launch_thread2(self):
        self.ui.pushButton_6.setStyleSheet(
            'background: rgb(0,255,0);border-style: outset; border-width: 2px;border-radius: 10px;border-color: black;font: bold 14px;')

        try:
            if self.mythread_2.isRunning():
                self.mythread_2.terminate()
                self.mythread_2 = Thread_2(mainwindow=self)
                self.mythread_2.signal_monitor.connect(self.monitor_api_status)

                self.mythread_2.start()

            else:
                self.mythread_2 = Thread_2(mainwindow=self)
                self.mythread_2.signal_monitor.connect(self.monitor_api_status)

                self.mythread_2.start()
        except:
            self.mythread_2 = Thread_2(mainwindow=self)
            self.mythread_2.signal_monitor.connect(self.monitor_api_status)
            self.mythread_2.start()


    def monitor_api_status(self,item):
        print('Я в емите')
        if item:
            self.ui.label_9.setStyleSheet('font: bold 14px;color:rgb(0,170,0)')
            self.ui.label_9.setText('API')
        else:
            self.ui.label_9.setStyleSheet('font: bold 14px;color:rgb(0,255,0)')
            self.ui.label_9.setText('API')



    def start_subscription(self):
        try:
            self.receiveThread = ReceiveData(mainwindow=self)
            self.processThread = ProcessData(mainwindow=self)
            self.receiveThread.start()
            self.processThread.start()

        except:
            print(traceback.format_exc())









app = QApplication(sys.argv)
window = ImageDialog()
window.show()

sys.exit(app.exec())