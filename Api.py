import traceback

import requests

#url = 'https://9af6-88-85-171-83.ngrok-free.app/graphql'
def get_tournament_requst(url,tournament_id:str):
    tournament = f"""
    query Events {{
        events(where: {{id: {{equals:{tournament_id} }}}}) {{
            id
            name
            createdAt
            updatedAt
        }}
    }}
    """

    response = requests.post(url, json={'query': tournament})
    print(response.status_code)
    return response.json()


def get_participants(url,tournament_id:str):
    participants_query = f"""
    query Events {{
        events(where: {{id: {{equals: {tournament_id}}}}}) {{
            id
            name
            days {{
                    date
                }}
            categories {{
                id
                name
                type
                kinds {{
                    id
                    name
                }}
                
                sportsmen {{
                    id
                    numberInCategory
                    firstName
                    lastName
                    country {{
                    name
                    }}
                    category {{
                        name
                        sportsmanCount
                        id
                        kinds {{
                            id
                            name
                        }}
                    }}
                }}
            }}
        }}
    }}
    """
    response = requests.post(url, json={'query': participants_query})
    return response.json()



def get_statistic(url,tournament_id:str):
    statistic_query = f"""
        query {{
          events(where: {{ id: {{ equals: {tournament_id} }}}}) {{
          categories {{
              id
              name
              sportsmen {{
                id
                firstName
                lastName
                performances {{
                  kind {{
                    id
                    name
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
          }}
        }}
    """
    response = requests.post(url, json={'query': statistic_query})
    return response.json()




def get_days(url,tournament_id:str):
    days_query = f"""
                query Events {{
                events(where: {{id: {{ equals: {tournament_id} }}}}) {{
                    id
                    days {{
                        id
                        date
                        eventId
                    }}
                }}
            }}
            """

    response = requests.post(url, json={'query': days_query})
    return response.json()







def get_statistic_by_dayID(url:str,day_id:str):
    query = f"""
            query {{
          performances (where: {{ dayId: {{ equals: {day_id} }} }}, orderBy: {{ mainNumber: asc}}) {{
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
                    sportsmen {{
                      id
                      numberInCategory
                      firstName
                      lastName
                      country {{
                                name
                                }}
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
         """

    response = requests.post(url, json={'query': query})
    return response.json()


def get_zaezd_by_day_id(url:str,day_id:str):
    query = f"""
            query {{
              performances (where: {{ dayId: {{ equals: {day_id} }} }}, orderBy: {{ mainNumber: asc}}) {{
                mainNumber
                kind {{
                  id
                  name
                }}
                sportsman {{
                  id
                  firstName
                  lastName
                  numberInCategory
                  category {{
                    id
                    name
                    type
                  }}
                }}
                sportsmanGroup {{
                    id
                    name
                    numberInCategory
                    country {{
                      name
                    }}
                    category {{
                      id
                      name
                      type
                    }}
                    sportsmen {{
                      id
                      numberInCategory
                      firstName
                      lastName
                      country {{
                                name
                                }}
                    }}
                    }}
                
            }}
            }}
            """

    response = requests.post(url, json={'query': query})
    return response.json()


query = """
            subscription ScoreUpdated {
            scoreUpdated(dayId:4) {
              performance {
                    mainNumber
                    kind {
                      id
                      name
                    }
                    sportsman {
                      id
                      firstName
                      lastName
                      category {
                        id
                        name
                      }
                    }

                sportsmanGroup {
                        id
                        name
                        category {
                          id
                          name
                          type
                        }}
                        sportsman {
                          id
                          numberInCategory
                          firstName
                          lastName
                          country {
                                    name
                                    }
                        }
            score {
                    finalScore
                    d1
                    d2
                    d3
                    finalA
                    finalE
                    masterDB
                    masterDA
                    deduction
                }

          }



        }
    }
        """























# res = (get_statistic('https://f5a6-88-85-171-83.ngrok-free.app/graphql','69'))['data']
#
#
# temp_res = res['events'][0]['categories']
#
# for zaezd in temp_res:
#     zaezdID = zaezd['id']
#     for sportsmen in zaezd['sportsmen']:
#         sportsmenID = sportsmen['id']
#         for res in sportsmen['performances']:
#            # print(str(zaezdID)+str(res['kind']['id']),sportsmenID,res['score'])
#          #   zaezdID = str(zaezdID)+str(res['kind']['id'])
#             ZaezdPlayerPointsDifficulty = (
#                 res['score']["masterDB"] if res['score']["masterDB"] else res['score']["d1"]
#             )
#             ZaezdPlayerPointsDifficulty2 = (
#                 res['score']["masterDA"] if res['score']["masterDA"] else res['score']["d3"]
#             )
#             ZaezdPlayerPoints = res['score']["finalScore"] if res['score']["finalScore"] else 0
#             ZaezdPlayerPointsSum = res['score']["finalScore"] if res['score']["finalScore"] else 0
#             ZaezdPlayerPointsShtraf = res['score']["deduction"] if res['score']["deduction"] else 0
#             ZaezdPlayerPointsArtistic = res['score']["finalA"] if res['score']["finalA"] else 0
#             ZaezdPlayerPointsExecution = res['score']["finalE"] if res['score']["finalE"] else 0
#             zaezdplayerid = data.select_player_id_by_ext(str(sportsmenID))
#             res = tuple([ZaezdPlayerPoints,ZaezdPlayerPointsShtraf,ZaezdPlayerPointsDifficulty,ZaezdPlayerPointsArtistic,ZaezdPlayerPointsExecution,ZaezdPlayerPointsDifficulty2,int(str(zaezdID)+str(res['kind']['id'])),int(zaezdplayerid)])
#             try:
#                 print(res)
#                 data.update_score(res)
#             except:
#                 print(traceback.format_exc())



# res = get_participants('https://5c1d-81-200-157-170.ngrok-free.app/graphql','43')
# print(res)
# date = res['data']['events'][0]['days'][0]['date'][:10]
# zaezd = res['data']['events'][0]['categories']
# for i in zaezd:
#     temp_id = i['id']
#     temp_ZaezdComment = i['name']
#     classID = (lambda x: 1 if x == 'INDIVIDUAL' else 2)(i['type'])
#
#     for j in i['kinds']:
#         id = str(temp_id)+ str(j['id'])
#         ZaezdComment = temp_ZaezdComment + ' ' + j['name']
#         print(id,j['name'],classID,date,ZaezdComment)
#         data.insert_zaezd(id,j['name'],classID,date,ZaezdComment)


# players = res['data']['events'][0]['categories']
# for player in players:
#     temp_players = player['sportsmen']
#     for i in temp_players:
#      #   print(i)
#         for j in i['category']['kinds']:
#             ZaezdID = str(i['category']['id']) + str(j['id'])
#          #   print(i['id'], i['firstName'], i['lastName'],ZaezdID)
#             data.insert_player(i['id'],i['lastName'].upper(),i['firstName'])
#             print(ZaezdID,i['id'],i['numberInCategory'])
#             player_id = data.select_player_id_by_ext(i['id'])
#             data.insert_in_zaezdMaps(ZaezdID,player_id,0,i['numberInCategory'])






# res = (32.85, 0, 9.8, 8.25, 8.4, 6.4, 20494, 1328)
# try:
#     data.update_score(res)
# except:
#     print(traceback.format_exc())

