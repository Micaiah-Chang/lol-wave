from django.template import RequestContext
from django.shortcuts import render_to_response

from wave.riot_API import get_version, get_team_data


def index(request):
    context = RequestContext(request)

    version = get_version()
    context_dict = {'version': version}
    if request.method == 'POST':
        summoner_name = request.POST['query'].strip()
        results = get_team_data(summoner_name)
        name, stats = results.pop(0)
        team = [(t_name, zip(t_stats.keys(), t_stats.values())) for t_name, t_stats in results]
        context_dict['name'] = name
        context_dict['teammates'] = team


    return render_to_response("wave/index.html", context_dict, context)
