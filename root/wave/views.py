from django.template import RequestContext
from django.shortcuts import render_to_response

from wave.riot_API import get_version, get_id


def index(request):
    context = RequestContext(request)

    version = get_version()
    context_dict = {'version': version}
    if request.method == 'POST':
        summoner = request.POST['query'].strip()
        result = get_id(summoner)
        context_dict['id'] = result


    return render_to_response("wave/index.html", context_dict, context)
