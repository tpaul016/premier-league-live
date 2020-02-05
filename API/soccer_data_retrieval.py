import http.client
import json
import secrets

connection = http.client.HTTPConnection('api.football-data.org')
headers = { 'X-Auth-Token': secrets.football_auth_token}

team_abbreviations = {
"AFC Bournemouth": "BOU",
"Arsenal FC": "ARS",
"Aston Villa FC": "AVA",
"Brighton & Hove Albion FC": "BRH",
"Burnley FC": "BUR",
"Chelsea FC": "CHE",
"Crystal Palace FC": "CRY",
"Everton FC": "EVE",
"Leicester City FC": "LEI",
"Liverpool FC": "LIV",
"Manchester City FC": "MCI",
"Manchester United FC": "MUN",
"Newcastle United FC": "NEW",
"Norwich City FC": "NOR",
"Sheffield United FC": "SHU",
"Southampton FC": "SOU",
"Tottenham Hotspur FC": "TOT",
"Watford FC": "WAT",
"West Ham United FC": "WHU",
"Wolverhampton Wanderers FC": "WLV"
}

def getSchedule(dateTo):
    connection.request('GET', '/v2/competitions/2021/matches?dateFrom=2020-01-20&dateTo=2020-02-04', None, headers)
    response = json.loads(connection.getresponse().read().decode())
    return json.dumps(formatSchedule(response))

def formatSchedule(data):
    matches = data['matches']
    formatted_matches = []
    for match in matches:
        formatted_match = {}
        formatted_match['Date'] = match['utcDate'].split('T')[0]
        formatted_match['Home Team'] = match['homeTeam']['name']
        formatted_match['Away Team'] = match['awayTeam']['name']
        formatted_match['Keyword'] = team_abbreviations[formatted_match['Home Team']] + team_abbreviations[formatted_match['Away Team']]
        formatted_matches.append(formatted_match)
    return formatted_matches
