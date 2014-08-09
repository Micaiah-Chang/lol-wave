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
        # if summoner_in_cache(summoner_name):
        #     summoner = Summoner.objects.get(username=summoner_name)
        #     s_id = summoner.id
        # else:
        #     s_id = get_id(summoner_name)
        #     s = Summoner(user_id=s_id, name=summoner_name)
        #     s.save()
        s_id = get_id(summoner_name)
        results = get_team_data(s_id, summoner_name)

        context_dict, team_list = add_player_to_context(context_dict, results)
        context_dict = add_team_to_context(context_dict, team_list)
        context_dict = max_stat_to_context(context_dict, results)

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

def max_stat_to_context(context_dict, all_team):
    most_damage = sorted(all_team, key=lambda x: x[1]['totalDamageDealtToChampions'])[0][0]
    context_dict['most_damage_dealt'] = most_damage

    most_damage_taken = sorted(all_team, key=lambda x:
                               x[1]['totalDamageTaken'])[0][0]
    context_dict['most_damage_taken'] = most_damage_taken

    most_wards_placed = sorted(all_team, key=lambda x: x[1]['wardPlaced'], reverse=True)[0][0]
    context_dict['most_wards_placed'] = most_wards_placed
    return context_dict



def summoner_in_cache(name):
    try:
        Summoner.object.get(user=name)
        return True
    except:
        return False
