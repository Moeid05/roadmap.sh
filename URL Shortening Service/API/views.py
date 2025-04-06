import json
from django.http import HttpResponse,JsonResponse
from .models import Url
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

@csrf_exempt
def shorten(request,shorten=None) :
    if request.method=="POST":
        return create_url(request)
    elif shorten :
        return handle_shortened_url(request, shorten)
    else :
        return HttpResponse("Invalid request", status=400)

def create_url(request):
    data = request.body.decode('utf-8')
    if not data:
        return HttpResponse("No data provided", status=400)
    try:
        data = json.loads(data)
    except json.JSONDecodeError:
        return HttpResponse("Invalid JSON", status=400)
    url = Url.objects.create(url=data.get("url"))
    return JsonResponse(url.as_json, status=201)

def handle_shortened_url(request, shorten) :
    try :
        url = Url.objects.get(shorten=shorten)
    except :
        return HttpResponse("url doesnt exist")
    #retrieve
    if request.method == "GET" :
        url.increment_access_count()
        return JsonResponse(url.as_json)
    #update
    elif request.method == "PUT" :
        return update_url(request, url)
    #delete
    elif request.method == "DELETE" :
        url.delete()
        return HttpResponse(status = 204)

def update_url(request, url) :
    data = request.body.decode('utf-8')
    if not data:
        return HttpResponse("No data provided", status=400)
    try:
        data = json.loads(data)
    except json.JSONDecodeError:
        return HttpResponse("Invalid JSON", status=400)
    url.update(data.get("url"))
    return JsonResponse(url.as_json)

@csrf_exempt
@require_http_methods(["GET"])
def stats(request,shorten) :
    try :
        if request.method == "GET" :
            url = Url.objects.get(shorten=shorten)
            url.increment_access_count()
            return JsonResponse(url.stats)
        else :
            return HttpResponse("invalid request")
    except Url.DoesNotExist:
        return HttpResponse("url doesnt exist")
    except :
        return HttpResponse("unexpected error")