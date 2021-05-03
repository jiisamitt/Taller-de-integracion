from django.shortcuts import render

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
    return {"artist_id": artist_id}

