from graphqlclient import GraphQLClient

query = """
            subscription ScoreUpdated {
            scoreUpdated(dayId:3) {
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




client = GraphQLClient('https://nsk1.rgrussia.com/graphql')

while True:
    result = client.execute(query)
    print(result)






# while True:
#     with GraphQLClient('wss://nsk1.rgrussia.com/graphql') as client:
#         sub_id = client.subscribe(query, variables={'limit': 10}, callback=callback)
#         print(sub_id)