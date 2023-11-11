import traceback

from PyQt5.QtCore import *
from Database import Data
from Api import *
from time import sleep

class Thread_2(QThread):
    signal_monitor = pyqtSignal(int)
    def __init__(self, mainwindow, parent=None):
        QThread.__init__(self, parent)
        self.running = False
        self.mainwindow = mainwindow

    def run(self):
        DayID = None
        try:
            data = Data(self.mainwindow.ui.lineEdit_3.text())
        except:
            print('Не выбрана база данных')
            return
        self.running = True
        tour_id = self.mainwindow.ui.lineEdit.text()
        try:
            DaysIDs = get_days(self.mainwindow.ui.lineEdit_4.text(),  tour_id)['data']['events'][0]['days']
            self.signal_monitor.emit(1)
        except:
            self.signal_monitor.emit(0)

            return

        try:
            current_date = self.mainwindow.ui.dateEdit.date().toString(Qt.DateFormat.ISODate)
            for day in DaysIDs:
                if day['date'][:10] == current_date:
                    DayID = day['id']
        except:
            print(traceback.format_exc())
        if DayID == None:
            self.mainwindow.ui.label_8.setStyleSheet('font: bold 14px;color:rgb(255,0,0)')
            self.mainwindow.ui.label_8.setText('Выберите корректный день!')
            return
        self.mainwindow.ui.label_8.setStyleSheet('font: bold 14px;color:rgb(0,255,0)')
        self.mainwindow.ui.label_8.setText('')


        try:
            temp_res = (get_statistic_by_dayID(self.mainwindow.ui.lineEdit_4.text(),  DayID))['data']['performances']
            self.signal_monitor.emit(1)
        except:
            self.signal_monitor.emit(0)
            return
        print('Поток запущен')
        for res in temp_res:
            print(res)
            try:
                if res['sportsman']:
                    zaezdID = str(res['sportsman']['category']['id'])
                    sportsmenID = res['sportsman']['id']

                    ZaezdPlayerPointsDifficulty = (
                        res['score']["masterDB"] if res['score']["masterDB"] else res['score']["d1"]
                    )
                    ZaezdPlayerPointsDifficulty2 = (
                        res['score']["masterDA"] if res['score']["masterDA"] else res['score']["d3"]
                    )
                    ZaezdPlayerPoints = res['score']["finalScore"] if res['score']["finalScore"] else 0
                    ZaezdPlayerPointsSum = res['score']["finalScore"] if res['score']["finalScore"] else 0
                    ZaezdPlayerPointsShtraf = res['score']["deduction"] if res['score']["deduction"] else 0
                    ZaezdPlayerPointsArtistic = res['score']["finalA"] if res['score']["finalA"] else 0
                    ZaezdPlayerPointsExecution = res['score']["finalE"] if res['score']["finalE"] else 0
                    zaezdplayerid = data.select_player_id_by_ext(str(sportsmenID))


                    res = tuple([ZaezdPlayerPointsSum,ZaezdPlayerPoints, ZaezdPlayerPointsShtraf, ZaezdPlayerPointsDifficulty,
                                 ZaezdPlayerPointsArtistic, ZaezdPlayerPointsExecution,
                                 ZaezdPlayerPointsDifficulty2, int(str(zaezdID) + str(res['kind']['id']) + str(DayID)),
                                 int(zaezdplayerid)])
                    try:
                        data.update_score(res)
                    except:
                        self.mainwindow.ui.pushButton_6.setStyleSheet(
                            'background: rgb(255,0,0);border-style: outset; border-width: 2px;border-radius: 10px;border-color: black;font: bold 14px;')
                        print(traceback.format_exc())
                else:
                    zaezdID = str(res['sportsmanGroup']['category']['id']) +  str(res['kind']['id']) + str(DayID)

                    ZaezdPlayerPointsDifficulty = (
                        res['score']["masterDB"] if res['score']["masterDB"] else res['score']["d1"]
                    )
                    ZaezdPlayerPointsDifficulty2 = (
                        res['score']["masterDA"] if res['score']["masterDA"] else res['score']["d3"]
                    )
                    ZaezdPlayerPoints = res['score']["finalScore"] if res['score']["finalScore"] else 0
                    ZaezdPlayerPointsSum = res['score']["finalScore"] if res['score']["finalScore"] else 0
                    ZaezdPlayerPointsShtraf = res['score']["deduction"] if res['score']["deduction"] else 0
                    ZaezdPlayerPointsArtistic = res['score']["finalA"] if res['score']["finalA"] else 0
                    ZaezdPlayerPointsExecution = res['score']["finalE"] if res['score']["finalE"] else 0



                    res = tuple([ZaezdPlayerPointsSum, ZaezdPlayerPoints, ZaezdPlayerPointsShtraf,
                                 ZaezdPlayerPointsDifficulty,
                                 ZaezdPlayerPointsArtistic, ZaezdPlayerPointsExecution,
                                 ZaezdPlayerPointsDifficulty2,
                                 int(zaezdID),
                                 int(data.select_player_id_by_ext(res['sportsmanGroup']['id']))])

                    try:
                        data.update_score(res)
                        print(res)
                    except:
                        self.mainwindow.ui.pushButton_6.setStyleSheet(
                            'background: rgb(255,0,0);border-style: outset; border-width: 2px;border-radius: 10px;border-color: black;font: bold 14px;')
                        print(traceback.format_exc())

            except:
                print(traceback.format_exc())

        self.mainwindow.ui.pushButton_6.setStyleSheet(
            'border-style: outset; border-width: 2px;border-radius: 10px;border-color: black;font: bold 14px;')

