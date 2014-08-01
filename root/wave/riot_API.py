import json
import urllib, urllib2
import os

def run_query(summoner):
    root_url = 'https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/'

    curr_dir = os.path.dirname(__file__)
    curr_dir = os.path.abspath(curr_dir)
    API_file = os.path.join(curr_dir, "API.txt")

    with open(API_file, 'r') as f:
        API_key = f.readline().strip()

    url= "{0}{1}?api_key={2}".format(root_url, summoner, API_key)
    results = {}


    try:
        response = urllib2.urlopen(url).read()
        json_response = json.loads(response)

        results['name'] = json_response[summoner]['name']
    except urllib2.URLError, e:
        print "Error when querying Riot games:", e
        print "Best Technical"


    return results


def get_version():
    API_ver = "1.2"

    root_url = "https://na.api.pvp.net/api/lol/static-data/na/v{0}/versions".format(API_ver)

    curr_dir = os.path.dirname(__file__)
    curr_dir = os.path.abspath(curr_dir)
    API_file = os.path.join(curr_dir, "API.txt")

    with open(API_file, 'r') as f:
        API_key = f.readline()

    url = "{0}?api_key={1}".format(root_url ,API_key)

    version = None

    try:
        response = urllib2.urlopen(url).read()
        json_response = json.loads(response)
        version = json_response[0]
        # Latest version is the first entry on list.
    except urllib2.URLError, e:
        print "Error when querying Riot:", e

    return version


if __name__ == '__main__':
    results = run_query("meisnewbie")
    print results
    version = get_version()
    print version
