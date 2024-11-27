from requests.sessions import Session
from bs4 import BeautifulSoup
import json
from application import app
from .queries import add_user, add_transaction, get_user, user_exists, update_user


# Perform a request for Slippi user data
# Send data to database
async def hit_slippi_API(connectCode):
    # Make a POST request to Slippi's GraphQL API

    payload = {
        "operationName": "AccountManagementPageQuery",
        "variables": connectCode,
        "query": "fragment profileFields on NetplayProfile {\n  id\n  ratingOrdinal\n  ratingUpdateCount\n  wins\n  "
        "losses\n  dailyGlobalPlacement\n  dailyRegionalPlacement\n  continent\n  characters {\n    id\n    "
        "character\n    gameCount\n    __typename\n  }\n  __typename\n}\n\nfragment userProfilePage on User "
        "{\n  fbUid\n  displayName\n  connectCode {\n    code\n    __typename\n  }\n  status\n  "
        "activeSubscription {\n    level\n    hasGiftSub\n    __typename\n  }\n  rankedNetplayProfile {\n    "
        "...profileFields\n    __typename\n  }\n  netplayProfiles {\n    ...profileFields\n    season {\n    "
        "  id\n      startedAt\n      endedAt\n      name\n      status\n      __typename\n    }\n    "
        "__typename\n  }\n  __typename\n}\n\nquery AccountManagementPageQuery($cc: String!, $uid: String!) {"
        "\n  getUser(fbUid: $uid) {\n    ...userProfilePage\n    __typename\n  }\n  getConnectCode(code: "
        "$cc) {\n    user {\n      ...userProfilePage\n      __typename\n    }\n    __typename\n  }\n}\n"
    }

    headers = {
        "Host": "gql-gateway-dot-slippi.uc.r.appspot.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://slippi.gg/",
        "content-type": "application/json",
        "apollographql-client-name": "slippi-web",
        "Content-Length": "1070",
        "Origin": "https://slippi.gg",
        "Connection": "close",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "TE": "trailer"
    }

    with Session() as request_session:
        slippi_response = request_session.post('https://gql-gateway-dot-slippi.uc.r.appspot.com/graphql', json=payload, headers=headers)

        if slippi_response.status_code != 200:
            app.logger.error("Error retrieving rank; user doesn't exist or connection refused: " + slippi_response.status_code)
            return slippi_response.status_code

        else:
            app.logger.info("Successfully retrieved rank") 

            response_json = json.loads(slippi_response.content)
            if response_json['data']['getConnectCode'] is None:
                app.logger.error("Error retrieving rank; user doesn't exist or connection refused")
                return json.dumps({'success':False}), 404, {'ContentType':'text/html'}

            cleaned_data = dict()
            cleaned_data['ratingOrdinal'] = response_json['data']['getConnectCode']['user']['rankedNetplayProfile']['ratingOrdinal']
            cleaned_data['code'] = response_json['data']['getConnectCode']['user']['connectCode']['code']
            cleaned_data['displayName'] = response_json['data']['getConnectCode']['user']['displayName']
            cleaned_data['updateCount'] = response_json['data']['getConnectCode']['user']['rankedNetplayProfile']['ratingUpdateCount']
            cleaned_data['wins'] = response_json['data']['getConnectCode']['user']['rankedNetplayProfile']['wins']
            cleaned_data['losses'] = response_json['data']['getConnectCode']['user']['rankedNetplayProfile']['losses']
            cleaned_data['regionalRank'] = response_json['data']['getConnectCode']['user']['rankedNetplayProfile']['dailyRegionalPlacement']
            cleaned_data['globalRank'] = response_json['data']['getConnectCode']['user']['rankedNetplayProfile']['dailyGlobalPlacement']
            cleaned_data['continent'] = response_json['data']['getConnectCode']['user']['rankedNetplayProfile']['continent']

            assert cleaned_data['code'] == connectCode['cc'], "Connect code doesn't match"
            
            if user_exists(cleaned_data['code']) == False:
                add_user(cleaned_data)
                update_user(cleaned_data)
                add_transaction(cleaned_data)
                return cleaned_data
            
            elif get_user(cleaned_data['code']).UpdateCount == cleaned_data['updateCount']:
                update_user(cleaned_data)
                # Do not add transaction, since there have been no additional wins or losses
                return cleaned_data
            
            else:
                update_user(cleaned_data)
                add_transaction(cleaned_data)
                return cleaned_data


def api_logic(connect_code):
    if user_exists(connect_code):
        return hit_slippi_API(connect_code)
    
    elif user_exists(connect_code) is False:
        return