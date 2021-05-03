from django.shortcuts import render
from .models import Artist, Album, Track
import json
# Create your views here.
from ninja import NinjaAPI
from django.http import JsonResponse
from base64 import b64encode
api = NinjaAPI()
url = "http://127.0.0.1:8000/api/"

#test
@api.get("/hello")
def hello(request):
    return JsonResponse("Hello world", safe=False)

def codificar(nombre):
    string = nombre
    encoded = b64encode(string.encode()).decode('utf-8')
    
    if len(encoded) > 22:
        encoded = encoded[:22]

    return encoded

##get albums
@api.get("/albums")
def read_albums(request):
    artistas = Album.objects.all()
    lista= []
    for artista in artistas:
        lista.append(artista.dictionary())
    return JsonResponse(lista, safe=False)

##get tracjs
@api.get("/tracks")
def read_tracks(request):
    artistas = Track.objects.all()
    lista= []
    for artista in artistas:
        lista.append(artista.dictionary())
    return JsonResponse(lista, safe=False)
#########GET post artist#######

@api.api_operation(["GET","POST"],"/artists")
def read_artists(request):
    if request.method == "GET":
        artistas = Artist.objects.all()
        lista= []
        for artista in artistas:
            lista.append(artista.dictionary())
        return JsonResponse(lista, safe=False)
    if request.method == "POST":
        load = json.load(request)
        if "name" in load and "age" in load:
            name = load["name"]
            age = load["age"]
            artist_id = codificar(name)

            if Artist.objects.filter(pk=artist_id).exists():
                return JsonResponse("artista ya existe", status = 409, safe=False)

            else:
                artist = Artist.objects.create(id = artist_id, name = name, age = age, albums = url+"artists/"+artist_id+"/albums", tracks = url+"artists/"+artist_id+"/tracks",Self = url+"artists/"+artist_id)
                return JsonResponse(artist.dictionary(), status=201)
        else:
                return JsonResponse("input inválido",status = 400, safe=False)

##get artist
####agregar delete
@api.api_operation(["DELETE","GET"],"/artists/{artist_id}")
def read_artist(request, artist_id):
    if request.method == "GET":
        if Artist.objects.filter(pk=artist_id).exists():
            artistas = Artist.objects.get(pk=artist_id)
            return JsonResponse(artistas.dictionary(), safe=False)
        else:
            return JsonResponse("artista  no encontrado", status = 409, safe=False)  
    if request.method == "DELETE":
        if Artist.objects.filter(pk=artist_id).exists():
            album = Artist.objects.get(pk=artist_id)
            album.delete()
            albumes = Album.objects.all()
            tracks = Track.objects.all()
            for album in albumes:
                if album.artist_id == artist_id:
                    album.delete()
            for track in tracks:
                if track.artist_id == artist_id:
                    track.delete()

            return JsonResponse(("artista eliminado".encode()).decode('utf-8'), status = 204, safe=False)
        else:
            return JsonResponse("artista  no encontrado", status = 409, safe=False)   

##get albums artista o post album
@api.api_operation(["POST","GET"],"/artists/{artist_id}/albums")
def read_artist_albums(request, artist_id):
    if request.method == "POST":
        if Artist.objects.filter(pk=artist_id).exists():
            load = json.load(request)
            if ("genre" in load) and ("name" in load):
                name = load["name"]
                genre = load["genre"]
                album_id = codificar(name + ":" + artist_id)
                if Album.objects.filter(pk=album_id).exists():
                    return JsonResponse("album ya existe", status = 409, safe=False)
                else:
                    artist = Album.objects.create(id = album_id, artist_id = str(artist_id), name = name, genre = genre, artist = url+"artists/"+artist_id, tracks = url+"albums/"+album_id+"/tracks", Self = url+"albums/"+album_id)
                    return JsonResponse(artist.dictionary(), status=201)
            else:
                return JsonResponse("input inválido",status = 400, safe=False)
        else:
            return JsonResponse("artista noya existe", status = 409, safe=False)   
    if request.method == "GET":
        if Artist.objects.filter(pk=artist_id).exists():
                artist = Artist.objects.get(pk=artist_id)
                albumes = Album.objects.all()
                lista =  []
                for album in albumes:
                    if album.artist_id == artist.id:
                        lista.append(album.dictionary())
                return JsonResponse(lista, safe=False)
        else:
            return JsonResponse("artista no existe", status = 409, safe=False)
##get tracks artista
@api.get("/artists/{artist_id}/tracks")
def read_artist_tracks(request, artist_id):  
    if request.method == "GET":
        if Artist.objects.filter(pk=artist_id).exists():
                artist = Artist.objects.get(pk=artist_id)
                albumes = Album.objects.all()
                tracks = Track.objects.all()
                lista =  []
                for album in albumes:
                    if album.artist_id == artist.id:
                        for track in tracks:
                            lista.append(track.dictionary())
                return JsonResponse(lista, safe=False)
        else:
            return JsonResponse("artista no existe", status = 409, safe=False)
  



##get o delete album
@api.api_operation(["DELETE","GET"],"/albums/{album_id}")
def read_album(request, album_id):
    if request.method == "DELETE":
        if Album.objects.filter(pk=album_id).exists():
            album = Album.objects.get(pk=album_id)
            album.delete()
            tracks = Track.objects.all()
            for track in tracks:
                if track.album_id == album_id:
                    track.delete()
            return JsonResponse(("álbum eliminado".encode()).decode('utf-8'), status = 204, safe=False)
            
        else:
            return JsonResponse("álbum no encontrado", status = 409, safe=False)   
    if request.method == "GET":
        if Album.objects.filter(pk=album_id).exists():
                album = Album.objects.get(pk=album_id)
                
                return JsonResponse(album.dictionary(), safe=False)
        else:
            return JsonResponse(("álbum no encontrado".encode()).decode('utf-8'), status = 409, safe=False)

##get post albums  track
@api.api_operation(["POST","GET"],"/albums/{album_id}/tracks")
def read_album_tracks(request, album_id):
    if request.method == "POST":
        if Album.objects.filter(pk=album_id).exists():
            load = json.load(request)
            if ("name" in load) and ("duration" in load):
                name = load["name"]
                duracion = load["duration"]
                id = codificar(name + ":" + album_id)
                if Track.objects.filter(pk=id).exists():
                    return JsonResponse("cancion ya existes", status = 409, safe=False)
                else:
                    album_actual = Album.objects.filter(pk=album_id).get()
                    artist = Track.objects.create(id = id, artist_id = album_actual.artist_id, album_id= album_id, name=name, duration = duracion, times_played = 0, artist = url+"artists/"+album_actual.artist_id, album = url + "albums/"+album_id, Self = url+"tracks/"+id)
                    return JsonResponse(artist.dictionary(), status=201)
            else:
                return JsonResponse("input inválido",status = 400, safe=False)
        else:
            return JsonResponse("album no existe", status = 409, safe=False)   
    if request.method == "GET":
        if Album.objects.filter(pk=album_id).exists():
                artist = Album.objects.get(pk=album_id)
                albumes = Album.objects.all()
                lista =  []
                for album in albumes:
                    if album.artist_id == artist.id:
                        lista.append(album.dictionary())
                return JsonResponse(lista, safe=False)
        else:
            return JsonResponse("artista no existe", status = 409, safe=False)
    


##get o delete cancion
@api.api_operation(["DELETE","GET"],"/tracks/{track_id}")
def read_track(request, track_id):
    if request.method == "DELETE":
        if Track.objects.filter(pk=track_id).exists():
            track= Track.objects.get(pk=track_id)
            track.delete()
            return JsonResponse(("cancion eliminado".encode()).decode('utf-8'), status = 204, safe=False)
            
        else:
            return JsonResponse("cancion no encontrado", status = 409, safe=False)   
    if request.method == "GET":
        if Track.objects.filter(pk=track_id).exists():
                track = Track.objects.get(pk=track_id)
                
                return JsonResponse(track.dictionary(), safe=False)
        else:
            return JsonResponse(("cancion no encontrado".encode()).decode('utf-8'), status = 409, safe=False)
    

###puts artista
@api.put("/artists/{artist_id}/albums/play")
def put_artist(request, artist_id):
    if Artist.objects.filter(pk=artist_id).exists():
        tracks = Track.objects.all()
        lista_tracks =[]
        for track in tracks:
            if track.artist_id == artist_id:
                lista_tracks.append(track)
        for track in lista_tracks:
            track.times_played += 1
            track.save()
        return JsonResponse("todas las canciones del artista fueron reproducidas", status = 200, safe=False)
    else:
        return JsonResponse("artista no encontrado", status = 404, safe=False)

###puts album
@api.put("/albums/{album_id}/tracks/play")
def put_album(request, album_id):
    if Album.objects.filter(pk=album_id).exists():
        tracks = Track.objects.all()
        for track in tracks:
            if track.album_id == album_id:
                track.times_played += 1
                track.save()

        return JsonResponse("canciones del álbum reproducidas", status = 200, safe=False)
    else:
        return JsonResponse("album no encontrado", status = 404, safe=False)
    
###puts track
@api.put("/tracks/{track_id}/play")
def put_track(request, track_id):
    if Track.objects.filter(pk=track_id).exists():
        track= Track.objects.get(pk=track_id)
        track.times_played += 1
        track.save()

        return JsonResponse("cancion reproducida", status = 200, safe=False)
    else:
        return JsonResponse("cancion no encontrado", status = 404, safe=False)
