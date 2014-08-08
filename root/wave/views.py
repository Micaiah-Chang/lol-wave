from django.template import RequestContext
from django.shortcuts import render_to_response

from wave.models import Summoner

from wave.riot_API import get_version, get_team_data, get_id


def index(request):
    context = RequestContext(request)

    version = get_version()
    context_dict = {'version': version}
    if request.method == 'POST':
        summoner_name = request.POST['query'].strip()
        if summoner_in_cache(summoner_name):
            summoner = Summoner.objects.get(username=summoner_name)
            s_id = summoner.id
        else:
            s_id = get_id(summoner_name)
            s = Summoner(user_id=s_id, name=summoner_name)
            s.save()

        results = get_team_data(s_id, summoner_name)
        context_dict, team_list = add_player_to_context(context_dict, results)
        context_dict = add_team_to_context(context_dict, team_list)


    return render_to_response("wave/index.html", context_dict, context)


def add_player_to_context(context_dict, player_list):
    name, stats = player_list.pop(0)
    context_dict['name'] = name
    context_dict['stats'] = stats
    return context_dict, player_list


def add_team_to_context(context_dict, team_list):
    team = [(t_name, zip(t_stats.keys(), t_stats.values())) for t_name, t_stats in team_list]
    context_dict['teammates'] = team
    return context_dict

def summoner_in_cache(name):
    try:
        Summoner.object.get(user=name)
        return True
    except:
        return False
