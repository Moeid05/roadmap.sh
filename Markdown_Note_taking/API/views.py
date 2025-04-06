from django.http import JsonResponse, HttpResponseBadRequest,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Note
import requests
import markdown
from django.core import serializers

def ApiDecorator(func):
    def wrapper(request,*args,**kwargs):
        if request.method == 'POST':
            return func(request,*args,**kwargs)
        else:
            return HttpResponseBadRequest("Invalid request method.")
    return wrapper

def correct_grammer(text):
    url = "https://api.languagetoolplus.com/v2/check"
    payload = {
        'text': text,
        'language': 'en-US'
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        matches = response.json().get('matches', [])
        for match in reversed(matches):
            start = match['offset']
            length = match['length']
            replacement = match['replacements'][0]['value'] if match['replacements'] else ''
            text = text[:start] + replacement + text[start + length:]
        return text
    else:
        return text

@csrf_exempt
@ApiDecorator
def Notes_view(request):
    data = Note.objects.all()
    notes_json = serializers.serialize('json', data)
    return JsonResponse(notes_json, safe=False)

@csrf_exempt
@ApiDecorator
def save_text_view(request):
    file = request.FILES.get('file')
    if file:
        text = file.read().decode('utf-8')
        note = Note(title=file.name,content=text)
        note.save()
        return HttpResponse('text saved!', status=200)
    else:
        return HttpResponseBadRequest("No file was uploaded.")

@csrf_exempt
@ApiDecorator
def correct_grammar_view(request):
    file = request.FILES.get('file')
    if file:
        text = file.read().decode('utf-8')
        correct_text = correct_grammer(text)
        return HttpResponse(correct_text, content_type='text/plain', status=200)
    else:
        return HttpResponseBadRequest("No file was uploaded.")

@csrf_exempt
@ApiDecorator
def md_to_html_view(request):
    file = request.FILES.get('file')
    if file:
        text = file.read().decode('utf-8')
        #convert md to html
        html_content = markdown.markdown(text)
        return HttpResponse(html_content, content_type='text/html', status=200)
    else:
        return HttpResponseBadRequest("No file was uploaded.")
    