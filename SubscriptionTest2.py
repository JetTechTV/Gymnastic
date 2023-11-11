from websocket import create_connection
import json
url = 'wss://nsk1.rgrussia.com/graphql'
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
def on_message(ws,message):
    data = json.loads(message)
    print(data)


ws = create_connection(url)
ws.send(json.dumps(query))
while True:
    data = ws.recv()
    print(data)
