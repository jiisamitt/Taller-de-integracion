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




############POST###########
@api.post("/path")
def post_operation(request):
    body = json.load(request)

        if 'name' in body and 'age' in body:
            name = body['name']
            age = body['age']
            artist_id = coder(name)

            if Artista.objects.filter(id=artist_id).exists():
                data = 'Ya existe este artista'
                return JsonResponse(data,status = 409, safe=False)

            else:
                to_create = {
                    'id': artist_id,
                    'name': name, 
                    'age': age,
                    'albums': base_url+'atists/'+str(artist_id)+'/albums',
                    'tracks': base_url+'atists/'+str(artist_id)+'/tracks',
                    'Self': base_url+'atists/'+str(artist_id),
                    }
                artist = Artista.objects.create(**to_create)
                return JsonResponse(artist.diccionario(), status=201)

