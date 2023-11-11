from PyQt5.QtCore import *
from Database import Data
from Api import *
import traceback
from time import sleep
class Thread_1(QThread):
    signal_status = pyqtSignal(tuple)

    def __init__(self,mainwindow, parent = None):
        QThread.__init__(self, parent)
        self.running = False
        self.mainwindow = mainwindow


    def run(self):
        url = self.mainwindow.ui.lineEdit_4.text()

        try:
            data = Data(self.mainwindow.ui.lineEdit_3.text())
        except:
            print('Не выбрана база данных')
            return
        print('Поток запущен')
        self.running = True
        tour_id = self.mainwindow.ui.lineEdit.text()
        try:
          #  data = get_participants(tour_id)

            # Формируем Zaezd
            res = get_participants(url,tour_id)
          #  print(res)
            date = res['data']['events'][0]['days'][0]['date'][:10]
            zaezd = res['data']['events'][0]['categories']
            for i in zaezd:
                temp_id = i['id']
                temp_ZaezdComment = i['name']
                classID = (lambda x: 1 if x == 'INDIVIDUAL' else 2)(i['type'])

                for j in i['kinds']:
                    id = str(temp_id) + str(j['id'])
                    ZaezdComment = temp_ZaezdComment + ' ' + j['name']
                 #   print(id, j['name'], classID, date, ZaezdComment)
                    data.insert_zaezd(id, j['name'], classID, date, ZaezdComment)
            self.signal_status.emit((3,1))
        except:
            print(traceback.format_exc())
            self.signal_status.emit((3,0))


            # Вставляем Players
            # Формируем составы в ZaezdMaps
        try:
            players = res['data']['events'][0]['categories']
            for player in players:
                temp_players = player['sportsmen']
                for i in temp_players:
                    for j in i['category']['kinds']:
                        ZaezdID = str(i['category']['id']) + str(j['id'])
                        try:
                            countryName = i['country']['name']
                        except:
                            countryName = '  '
                        data.insert_player(i['id'], i['lastName'].upper(), i['firstName'],countryName)

                        player_id = data.select_player_id_by_ext(i['id'])
                        data.insert_in_zaezdMaps(ZaezdID, player_id, 0, i['numberInCategory'])
            self.signal_status.emit((4,1))
            self.signal_status.emit((5,1))

        except:
            print(traceback.format_exc())
            self.signal_status.emit((4, 0))
            self.signal_status.emit((5, 0))

