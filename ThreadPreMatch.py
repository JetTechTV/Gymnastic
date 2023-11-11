from PyQt5.QtCore import *
from Database import Data
from Api import *
import traceback
from time import sleep
import pyodbc
class Thread_1(QThread):
    signal_status = pyqtSignal(tuple)

    def __init__(self,mainwindow, parent = None):
        QThread.__init__(self, parent)
        self.running = False
        self.mainwindow = mainwindow


    def run(self):
        url = self.mainwindow.ui.lineEdit_4.text()
        DayID = None

        try:
            data = Data(self.mainwindow.ui.lineEdit_3.text())
            self.mainwindow.ui.label_8.setText('')

        except:
            self.mainwindow.ui.label_8.setStyleSheet('font: bold 14px;color:rgb(255,0,0)')
            self.mainwindow.ui.label_8.setText('Не выбрана база данных!')
            return
        self.running = True
        tour_id = self.mainwindow.ui.lineEdit.text()

        # Достаем ID дня
        try:
            DaysIDs = get_days(self.mainwindow.ui.lineEdit_4.text(), tour_id)['data']['events'][0]['days']
            self.mainwindow.ui.label_8.setText('')
        except:
            self.mainwindow.ui.label_8.setStyleSheet('font: bold 14px;color:rgb(255,0,0)')
            self.mainwindow.ui.label_8.setText('Проблемы с API/Internet')
        try:
            current_date = self.mainwindow.ui.dateEdit.date().toString(Qt.DateFormat.ISODate)
            for day in DaysIDs:
                if day['date'][:10] == current_date:
                    DayID = day['id']
                    self.mainwindow.ui.lineEdit_5.setText(str(DayID))
        except:
            print(traceback.format_exc())

        # Получаем всю инфу
        try:
            temp_res = get_zaezd_by_day_id(self.mainwindow.ui.lineEdit_4.text(), DayID)['data']['performances']
        except:
            print(get_zaezd_by_day_id(self.mainwindow.ui.lineEdit_4.text(), DayID))
            print(traceback.format_exc())
            self.mainwindow.ui.label_8.setStyleSheet('font: bold 14px;color:rgb(255,0,0)')
            self.mainwindow.ui.label_8.setText('Проблемы с API/Internet')
            return

        ZaezdDate = self.mainwindow.ui.dateEdit.date().toString(Qt.DateFormat.ISODate)
        zaezds = []
        players = []
        zaezdmaps = []
        relaySostav = []
        for res in temp_res:
            print(res)
            try:
                if res['sportsman']!=None:
                    try:
                        ZaezdID = str(res['sportsman']['category']['id']) + str(res['kind']['id']) + str(DayID)
                        ZaezdComment = res['sportsman']['category']['type'] + ' ' + res['sportsman']['category']['name']
                        ClassID = 1
                        ZaezdName = res['kind']['name']
                        zaezds.append((ZaezdID, ZaezdName, ClassID, ZaezdDate, ZaezdComment,0))
                    except:
                        print(traceback.format_exc())
                else:
                    try:
                        ZaezdID = str(res['sportsmanGroup']['category']['id']) + str(res['kind']['id']) + str(DayID)
                        ZaezdComment = res['sportsmanGroup']['category']['type'] + ' ' + res['sportsmanGroup']['category']['name']
                        ClassID = 2
                        ZaezdName = res['kind']['name']
                        zaezds.append((ZaezdID, ZaezdName, ClassID, ZaezdDate, ZaezdComment,1))
                    except:
                        self.mainwindow.ui.label_8.setStyleSheet('font: bold 14px;color:rgb(255,0,0)')
                        self.mainwindow.ui.label_8.setText('Проблемы с парсингом')
                        print(traceback.format_exc())
            except:
                print(traceback.format_exc())
                self.signal_status.emit((3, 0))

            # Формируем Players
            try:
                if res['sportsman']!= None:

                    player_id_ext = res['sportsman']['id']
                    player_name = res['sportsman']['firstName']
                    player_surname = res['sportsman']['lastName']
                    try:
                        countryName = res['sportsman']['country']['name']
                    except:
                        countryName = '  '
                    players.append((player_id_ext, player_surname, player_name, countryName))

                else:

                    command_id_ext = res['sportsmanGroup']['id']
                #    player_name = res['sportsmanGroup']['name']
                    player_surname = res['sportsmanGroup']['name']
                    try:
                        countryName = res['sportsmanGroup']['country']['name']
                    except:
                            countryName = '  '
                    players.append((command_id_ext, player_surname, ' ', countryName))
                    zaezdmaps.append((ZaezdID,command_id_ext,0,res['sportsmanGroup']['numberInCategory']))

                    for sportsman in res['sportsmanGroup']['sportsmen']:
                        player_id_ext = sportsman['id']
                        player_name = sportsman['firstName']
                        player_surname = sportsman['lastName']
                        try:
                            countryName = sportsman['country']['name']
                        except:
                            countryName = '  '
                        players.append((player_id_ext, player_surname, player_name, countryName))
                        relaySostav.append((ZaezdID,command_id_ext,player_id_ext,sportsman['numberInCategory']))
            except:
                self.signal_status.emit((4, 0))
                print(traceback.format_exc())


            # Формируем ZaezdMaps
            # ZaezdID,ZaezdPlayerID,ZaezdPlayerPosStart,ZaezdPlayerPosition
            try:
                if res['sportsman']!= None:
                    try:
                        ZaezdPlayerID = res['sportsman']['id']
                        ZaezdPlayerPosStart = 0
                        ZaezdPlayerPosition = res['sportsman']['numberInCategory']
                    except:
                        print(traceback.format_exc())

                    zaezdmaps.append((ZaezdID, ZaezdPlayerID, ZaezdPlayerPosStart, ZaezdPlayerPosition))
            except:
                self.signal_status.emit((5, 0))


        try:
            for zaezd in set(zaezds):
            #    print(zaezd)
                data.insert_zaezd(*zaezd)

            self.signal_status.emit((3,1))
        except pyodbc.IntegrityError:
            self.signal_status.emit((3,1))
        except:
            print(traceback.format_exc())
            self.signal_status.emit((3,0))


            # Player  and ZaezdMaps
        try:
            for player in set(players):
                data.insert_player(*player)
        except:
            print('Ошибка вставки игроков',traceback.format_exc())

        try:
            for i in set(zaezdmaps):
                data.insert_in_zaezdMaps(int(i[0]),data.select_player_id_by_ext(i[1]),i[2],i[3])

            self.signal_status.emit((4,1))
            self.signal_status.emit((5,1))

        except:
            print(traceback.format_exc())
            self.signal_status.emit((4, 0))
            self.signal_status.emit((5, 0))


        # RelaySostav

        try:
            for i in relaySostav:
                print(i[3])
                data.insert_in_relaySostav(i[0],data.select_player_id_by_ext(i[1]),data.select_player_id_by_ext(i[2]),int(i[3]))

        except:
            print(traceback.format_exc())

