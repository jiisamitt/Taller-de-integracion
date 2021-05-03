from django.urls import path
from tareapp import views

urlpatterns = [
    path('', views.api.urls, name="api-overview"),
    path('hello/', views.hello),

    ###GET
    path('artists/', views.read_artists, name="artists"),
    path('artists/<artist_id>', views.read_artist, name="artist"),
    path('artists/<artist_id>/albums', views.read_artist_albums, name="artist_albums"),
    path('artists/<artist_id>/tracks', views.read_artist_tracks, name="artist_traks"),
    path('albums/', views.read_albums, name="albums"),
    path('albums/<album_id>', views.read_album, name="album"),
    path('albums/<album_id>/tracks', views.read_album_tracks, name="album_tracks"),
    path('tracks/', views.read_tracks, name="tracks"),
    path('tracks/<track_id>', views.read_track, name="track"),




]