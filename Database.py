import pyodbc
class Data:
    def __init__(self, road):
        self.static_road = 'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + road
        self.conn = pyodbc.connect(self.static_road)


    def insert_player(self,player_id_ext:str,player_name:str,player_surname:str,countryName:str):
        sql_insert = """
                                       Insert into Players (PlayerID_EXT,F,I,CountryID)
                                       VALUES (?,?,?,?)
                                    """
        cursor = self.conn.cursor()
        countryID = self.get_countyID(countryName)
        # Проверяем есть ли Игрок в БД
        all_id_ext = self.select_player_id_ext()
        if player_id_ext in all_id_ext:
            return

        for char in player_name:
            if 1040 <= ord(char) <= 1103:
                sql_insert = """
                                Insert into Players (PlayerID_EXT,F,I,CountryID)
                                VALUES (?,?,?,?)
                             """
            else:
                sql_insert = """
                                Insert into Players (PlayerID_EXT,F_eng,I_eng,CountryID)
                                VALUES (?,?,?,?)
                             """
            break



        cursor.execute(sql_insert,(player_id_ext,player_name.upper(),player_surname.lower().capitalize(),countryID))
        cursor.commit()

        cursor.close()



    def select_player_id_ext(self):
        cursor = self.conn.cursor()

        sql = """
                                SELECT  PlayerID_EXT FROM Players 
                              """

        temp_res = cursor.execute(sql)
        res = [i[0] for i in temp_res]
        cursor.close()
        return res



    def insert_zaezd(self,ZaezdID,ZaezdName,ClassID,ZaezdDate,ZaezdComment,ZaezdRELAY):
        # Проверяем есть ли Zaezd в БД
        zaezd_ids = self.select_zaezd_id_ext()
        if ZaezdID in zaezd_ids:
            return
        cursor = self.conn.cursor()
        ZaezdNumber =self.select_zaezd_Number()
        ZaezdNameID = self.select_id_from_zaezd_name(ZaezdName)
        print('ZaezdNameID = ',ZaezdNameID)


        sql = """
                    Insert into Zaezd (ZaezdID,ZaezdNameID,ZaezdNumber,ClassID,ZaezdDate,ZaezdRate,ZaezdType,ZaezdRoundID,ZaezdComment1,ZaezdRELAY)
                    VALUES (?,?,?,?,?,?,?,?,?,?)
              """
        cursor.execute(sql,(ZaezdID,ZaezdNameID,ZaezdNumber,ClassID,ZaezdDate,'очки(1.000)','1','4',ZaezdComment,ZaezdRELAY))
        cursor.commit()
        cursor.close()




    def select_id_from_zaezd_name(self, zaezdname: str):
        cursor = self.conn.cursor()

        sql = """
                   SELECT ZaezdNameID FROM ZaezdName WHERE ZaezdName = ?
                 """

        cursor.execute(sql, (zaezdname))
        res = cursor.fetchone()
      #  cursor.close()
        if res!= None:
            cursor.close()
            return res[0]
        sql = """
                           SELECT ZaezdNameID FROM ZaezdName WHERE ZaezdNameEng = ?
                         """

        cursor.execute(sql, (zaezdname))
        res = cursor.fetchone()
        if res != None:
            cursor.close()
            return res[0]

        sql  = """
                    Select ZaezdNameID FROM ZaezdName 
               """

        cursor.execute(sql)
        id = max([i[0] for i in cursor.fetchall() ]) + 1

        for char in  zaezdname:
            if 1040 <= ord(char) <= 1103:
                sql_insert = """
                                Insert into ZaezdName  (ZaezdNameID,ZaezdName)
                                           VALUES (?,?)
                             """
                break
            else:
                sql_insert = """
                                                Insert into ZaezdName  (ZaezdNameID,ZaezdNameEng)
                                                           VALUES (?,?)
                                             """
                break


        cursor.execute(sql_insert,(id,zaezdname))
        return id
        cursor.close()


    def insert_in_zaezdMaps(self,ZaezdID,ZaezdPlayerID,ZaezdPlayerPosStart,ZaezdPlayerPosition):
        # Проверяем есть ли там уже игроки
        cursor = self.conn.cursor()

        sql_check = """
                        Select ZaezdID,ZaezdPlayerID From ZaezdMaps
                    """

        res_check = [tuple([int(i[0]),int(i[1])]) for i in cursor.execute(sql_check) ]

        if tuple([int(ZaezdID),int(ZaezdPlayerID)]) in res_check:
            return
        sql_insert  = """
                        Insert into ZaezdMaps (ZaezdID,ZaezdPlayerID,ZaezdPlayerPosStart,ZaezdPlayerPosition)
                        VALUES (?,?,?,?)
                      """
        cursor.execute(sql_insert,(ZaezdID,ZaezdPlayerID,ZaezdPlayerPosStart,ZaezdPlayerPosition))

        cursor.commit()
        cursor.close()


    def select_zaezd_id_ext(self):
        cursor = self.conn.cursor()

        sql = """
                                SELECT  ZaezdID FROM Zaezd
                              """

        temp_res = cursor.execute(sql)
        res = [i[0] for i in temp_res]
        cursor.close()
        return res




    def select_zaezd_Number(self):
        cursor = self.conn.cursor()

        sql = """
                                SELECT ZaezdNumber FROM Zaezd  ORDER BY ZaezdNumber DESC
                              """

        temp_res = cursor.execute(sql)
        res = [i[0] for i in temp_res]
        cursor.close()
        if res:
            return res[0] + 10
        return 10


    def select_player_id_by_ext(self,id_ext:str):
        cursor = self.conn.cursor()

        sql = """
                                        SELECT PlayerID FROM Players Where PlayerID_EXT = ?
                                      """

        temp_res = cursor.execute(sql,(id_ext))
        res = [i[0] for i in temp_res]
        cursor.close()
        return res[0]



    def update_score(self,item:tuple):
        cursor = self.conn.cursor()



        sql = """
                Update ZaezdMaps SET ZaezdPlayerPointsSum = ? , ZaezdPlayerPoints =? ,ZaezdPlayerPointsShtraf = ?, ZaezdPlayerPointsDifficulty = ?,
                ZaezdPlayerPointsArtistic = ?,ZaezdPlayerPointsExecution = ?,ZaezdPlayerPointsDifficulty2 = ?
                 WHERE ZaezdID = ? AND ZaezdPlayerID = ?
              """
        cursor.execute(sql,item)
        cursor.commit()
        cursor.close()


    def clear_database(self):
        cursor = self.conn.cursor()
        tables = ('ZaezdMaps', 'Zaezd', 'Players')
        for table in tables:

            sql = f"""Delete from {table}"""
            cursor.execute(sql)

        self.conn.commit()

    def get_countyID(self,countryName:str):

        cursor = self.conn.cursor()

        sql = """
                                                SELECT CountryID FROM Countries Where CountryName = ?
                                              """

        temp_res = cursor.execute(sql, (countryName))
        res = [i[0] for i in temp_res]
       # cursor.close()
        if res:
            return res[0]
        else:
            sql_id = """Select MAX(CountryID) From Countries"""
            ID = cursor.execute(sql_id).fetchone()[0] + 1
            sql_insert = """Insert into Countries (CountryID,CountryName)
                        VALUES (?,?)"""
            cursor.execute(sql_insert,(ID,countryName))
            cursor.commit()
            cursor.close()
            return ID


    def insert_in_relaySostav(self,ZaezdID,ZaezdPlayerID,RelayPlayerID,RelayPos):
        # Проверяем есть ли там уже игроки
        cursor = self.conn.cursor()

        sql_check = """
                        Select ZaezdID,ZaezdPlayerID,RelayPlayerID From RelaySostav
                    """

        res_check = [tuple([int(i[0]),int(i[1]),int(i[2])]) for i in cursor.execute(sql_check) ]

        if tuple([int(ZaezdID),int(ZaezdPlayerID),int(RelayPlayerID)]) in res_check:
            print('Не вставляем')
        sql_insert  = """
                        Insert into RelaySostav (ZaezdID,ZaezdPlayerID,RelayPlayerID,RelayPos)
                        VALUES (?,?,?,?)
                      """
        print('Вставляю',ZaezdID,ZaezdPlayerID,RelayPlayerID,RelayPos)
        cursor.execute(sql_insert,(ZaezdID,ZaezdPlayerID,RelayPlayerID,RelayPos))

        cursor.commit()
        cursor.close()



