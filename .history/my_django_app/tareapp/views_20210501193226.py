from django.shortcuts import render

# Create your views here.
from ninja import NinjaAPI
from django.http import JsonResponse

api = NinjaAPI()


@api.get("/hello")
def hello(request):
    return JsonResponse("Hello world")