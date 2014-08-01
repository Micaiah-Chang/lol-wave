from django.template import RequestContext
from django.shortcuts import render_to_response

def index(request):
    context = RequestContext(request)

    context_dict = {}
    return render_to_response("wave/index.html", context_dict, context)
