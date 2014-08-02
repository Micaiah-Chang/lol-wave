import json
import urllib, urllib2
import os

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

def append_API_key(url):
    curr_dir = os.path.dirname(__file__)
    curr_dir = os.path.abspath(curr_dir)
    API_file = os.path.join(curr_dir, "API.txt")

    with open(API_file, 'r') as f:
        API_key = f.readline()

    result_url = "{0}?api_key={1}".format(url ,API_key)
    return result_url


if __name__ == '__main__':
    s_id = get_id("meisnewbie")
    latest_game(s_id)
