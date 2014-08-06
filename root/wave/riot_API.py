import json
import urllib, urllib2
import os
import time

# Warning! Currently region is only set to NA!

BLUE_ID = 100
PURPLE_ID = 200


def get_id(summoner):
    root_url = 'https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/'

    summon_url = "{0}{1}".format(root_url, summoner)
    url = append_API_key(summon_url)
    results = {}


    try:
        response = urllib2.urlopen(url).read()
        json_response = json.loads(response)

        results['id'] = json_response[summoner][u'id']
    except urllib2.URLError, e:
        print "Error when querying Riot games:", e
        print "Best Technical"

    return results['id']
# Results is a bad name. Refactor to something else.

def get_version():
    API_ver = "1.2"

    root_url = "https://na.api.pvp.net/api/lol/static-data/na/v{0}/versions".format(API_ver)

    version = None
    url = append_API_key(root_url)
    try:
        response = urllib2.urlopen(url).read()
        json_response = json.loads(response)
        version = json_response[0]
        # Latest version is the first entry on list.
    except urllib2.URLError, e:
        print "Error when querying Riot:", e

    return version

def get_stat_with_id(id, teammates=False):
    root_url = "https://na.api.pvp.net/api/lol/na/v1.3/game/by-summoner/{0}/recent".format(id)

    url = append_API_key(root_url)
    results = []
    try:
        response = urllib2.urlopen(url).read()
        json_response = json.loads(response)

        # print json.dumps(json_response, sort_keys=True, indent=4, separators=(',', ': '))

        game = get_game(json_response)
        result = get_game_stats(game)
    except urllib2.URLError, e:
        print "Where was team", e

    if teammates:
        return result
    else:
        return result, game


def get_game(json_response, game_id=0):
    if not game_id:
        game = json_response['games'][0]
    else:
        game = match_game_id(json_response['games'], game_id)

    return game

def get_game_stats(game):
    recent_stats = game['stats']
    stats = [u"totalDamageTaken",  u"totalDamageDealtToChampions", u"wardPlaced",u"wardKilled"]
    result_dict = {stat: recent_stats.get(stat, 0) for stat in stats}
    # The above assumes all relevant stats which can be NULL in the json are numerical ones.

    return result_dict



# look through games for the matching id.
def match_game_id(games, game_id):
    for games_index, game in games:
        if game['id'] == game_id:
            return games[game_index]

    return {} # if not seen in latest, return nothing.

def get_teammates(game):
    players = game["fellowPlayers"]

    teammate_ids = [str(player["summonerId"]) for player in players]

    id_delimit = ",".join(teammate_ids)
    root_url = "https://na.api.pvp.net/api/lol/na/v1.4/summoner/{0}/name".format(id_delimit)

    url = append_API_key(root_url)

    try:
        response = urllib2.urlopen(url).read()
        json_response = json.loads(response)
        teammates = json_response
    except urllib2.URLError, e:
        print "Cannot access riot API", e

    return teammates


def append_API_key(url):
    curr_dir = os.path.dirname(__file__)
    curr_dir = os.path.abspath(curr_dir)
    API_file = os.path.join(curr_dir, "API.txt")

    with open(API_file, 'r') as f:
        API_key = f.readline()

    result_url = "{0}?api_key={1}".format(url ,API_key)
    return result_url

def get_team_data(name):
    s_id = get_id(name)
    result, game = get_stat_with_id(s_id)
    teammates = get_teammates(game)
    results = [(name, result)]

    for (teammate_id, teammate_name) in teammates.items():
        time.sleep(1)
        stat = get_stat_with_id(teammate_id, teammates=True)
        results.append((teammate_name, stat))

    return results


def main():
    summoner_name = "meisnewbie"
    results = get_team_data(summoner_name)
    summoner_stats = results.pop(0)
    name, stats = summoner_stats


if __name__ == '__main__':
    main()
