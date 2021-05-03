from django.shortcuts import render
from models import Artist, Album, Track

# Create your views here.
from ninja import NinjaAPI
from django.http import JsonResponse

api = NinjaAPI()


@api.get("/hello")
def hello(request):
    return JsonResponse("Hello world", safe=False)

#########GET#######

@api.get("/artists/{artist_id}")
def read_artist(request, artist_id: int):
    a = Artist.models.get(id = artist_id)

    return JsonResponse(a.diccionario())

