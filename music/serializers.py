from django.db import models
from django.db.models import Sum, fields
import re
from essentia.standard import *
from rest_framework import serializers
from .models import (Musics, OwnedMusics, RequestMusic, SoldMusics, AddMusicToCart, TopMusicList, 
AddField, TopMusic, ExtraInfo, YoutubeApi)
from accounts.models import NewUsers
import requests
import base64
import essentia.standard as es
from django.core.files.storage import default_storage
from midi2audio import FluidSynth
import midi2audio
from django.contrib.auth import get_user_model, login
from rest_framework.pagination import PageNumberPagination

User = get_user_model()
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 3
    page_query_param='p'
    page_size_query_param = 'page'
    max_page_size = 3


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUsers
        fields = ['id', 'email','first_name', 'last_name' ]

class MusicCreateSerializers(serializers.ModelSerializer):
    class Meta:
        model = Musics
        fields = ['song', 'price']
    
    def create(self, validated_data):
        print('created')
        song = validated_data['song']
        price = validated_data['price']
        strSong = str(song)
        key = re.findall("\sof\s([^\)]+)\)\.mid", strSong)
        artistFinder = re.search("-", strSong)
        titlefinder = re.findall("\-\s([^\(]+)", strSong)
        titlefinder = titlefinder[0].strip()
        artist = strSong[0:artistFinder.span()[0]]
        # print(titlefinder)

        title = strSong[:artistFinder.span()[0]]+titlefinder

        
        query = title
        print(title, query)
# Tessa Violet & lovelytheband - Games (In the key of Ab Major).mid
# Olivia Rodrigo - 1 step forward, 3 steps back (in the key of D Major).mid
        # youtube search
        youTubeChannelId = ['UCNJljyodBlW1AIgU3QpwyFg','UCfMZNJ5CDIQ5EusW4SQcMMg', 'UCPfDF8O9GllZ-79F76Q7LXA', 
        'UCsyIzFRuX1G3qiPf-Jyk6nw', 'UC0doyxBxP2MWUe91HxYLm7Q','UC54aXORkg8jg50_USVal0Dw','UCPr1LWrxZAIfkjFbgK5oOOw',
        'UCCt3lxbdR5oVVotKhDMJyiQ' ]

        for channel in youTubeChannelId:
            youtubeapi = YoutubeApi.objects.all().order_by('-count')[0]
            if youtubeapi.count>=1:
                youtubeapi.count = youtubeapi.count-1
                youtubeapi.save()
                try:
                    youtubeSearch = requests.get(f"https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={channel}&key={youtubeapi.api}&q={query}").json()
                    print(youtubeSearch)
                    if youtubeSearch:
                        try:
                            if youtubeSearch['items'][0]:
                                break
                        except:
                            continue
                except:
                    pass
            else:
                raise serializers.ValidationError({'youtube':'Blocked'})

             
        if len(youtubeSearch)<1:
            raise serializers.ValidationError({'youtube':'No music found in youtube'})

        youtubeId = youtubeSearch['items'][0]['id']['videoId']
        print(youtubeId)
     
    #  https://www.youtube.com/c/PianoHits ->  UCNJljyodBlW1AIgU3QpwyFg 
    # https://www.youtube.com/c/PianoMixhits -> UCfMZNJ5CDIQ5EusW4SQcMMg
    # https://www.youtube.com/c/EasyPianohits -> UCPfDF8O9GllZ-79F76Q7LXA
    # https://www.youtube.com/c/PianoLoop -> UCsyIzFRuX1G3qiPf-Jyk6nw
    # https://www.youtube.com/channel/UC0doyxBxP2MWUe91HxYLm7Q  -> UC0doyxBxP2MWUe91HxYLm7Q
    # https://www.youtube.com/channel/UC54aXORkg8jg50_USVal0Dw  -> UC54aXORkg8jg50_USVal0Dw
    # https://www.youtube.com/c/thepianokidrequestnobodyelsecovers -> UCPr1LWrxZAIfkjFbgK5oOOw
    # https://www.youtube.com/channel/UCCt3lxbdR5oVVotKhDMJyiQ -> UCCt3lxbdR5oVVotKhDMJyiQ





        # spotify 
        tokenUrl = 'https://accounts.spotify.com/api/token'
        client_id = '85f1bf218aa944c7891d5d2ef5215095'
        client_secret = '8dbb87f6587a4041ad8fe0a20e964d5a'
        client_creds = f"{client_id}:{client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        decoded_client_creds = client_creds_b64.decode()

        # spotify  authentication
        response = requests.post(
			tokenUrl,
            data = {
                "grant_type":"client_credentials",
            },
			headers={
                
				"Authorization": f"Basic {decoded_client_creds}"
			}
		)
        token = response.json()
        auth_token = token['access_token']
       
        # search song on spotify
        url = f"https://api.spotify.com/v1/search?q={query}&offset=0&type=track"
        response = requests.get(
			url,
			headers={
				"Content-Type": "application/json",
				"Authorization": f"Bearer {auth_token}"
			}
		)
        response_json = response.json()
        spotify_id = response_json['tracks']['items'][0]['id']
        artWork = response_json['tracks']['items'][0]['album']['images'][0]['url']
        if len(response_json['tracks']['items'])<1:
            raise serializers.ValidationError({"no song in soptify"})
       
        # save music to database    
        music = Musics.objects.create(title=titlefinder, artist=artist,
        artWork=artWork, spotifyId=spotify_id, price=price, song=song, youtubeId=youtubeId)

        fs = midi2audio.FluidSynth()
        if strSong[-3:]=='mid':
            # conver song midi file to mp3
            fs.midi_to_audio(str(music.song.path), str(music.song.path)[0:-4]+'.mp3')

            # count bpm
            audio = MonoLoader(filename=str(music.song.path)[0:-4]+'.mp3')()

            # Compute beat positions and BPM
            rhythm_extractor = RhythmExtractor2013(method="multifeature")
            bpm, beats, beats_confidence, _, beats_intervals = rhythm_extractor(audio)

            default_storage.delete((music.song.path)[0:-4]+'.mp3')

        else:
            # count bpm
            audio = MonoLoader(filename=str(music.song.path)[0:-4]+'.mp3')()

            # Compute beat positions and BPM
            rhythm_extractor = RhythmExtractor2013(method="multifeature")
            bpm, beats, beats_confidence, _, beats_intervals = rhythm_extractor(audio)
            
        # update music
        music.bpm=bpm
        music.key=key[0]
        music.path = music.song.url
        music.description = str(query)+' - '+ 'BPM : '+ str(bpm)
        music.save()

        return music

class MusicRUDSerializers(serializers.ModelSerializer):
    is_downloaded = serializers.SerializerMethodField(read_only=True)
    is_added_to_cart = serializers.SerializerMethodField(read_only=True)
    in_favourite = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Musics
        fields = ['id', 'title', 'artist', 'key', 'bpm', 'description', 'artWork', 'spotifyId', 
        'price', 'path', 'song', 'youtubeId', 'is_shortList', 'sortNumber', 'createdAt', "is_downloaded", "is_added_to_cart",'in_favourite']

    def get_is_downloaded(self, obj):
        user='none'
        bool=False
        request = self.context.get("request")

        try:
            request = self.context.get("request")
            user = request.user
            ownedMusic = OwnedMusics.objects.get(user=user)
            if ownedMusic.music.all() and obj in ownedMusic.music.all():
            
                bool=True
        except:
            pass
       
        return bool

    def get_is_added_to_cart(self, obj):
        user='none'
        bool=False
        context = self.context
        try:
            request = self.context.get("request")
            user = request.user
            cart = AddMusicToCart.objects.get(user=user)
            if cart.music.all() and obj in cart.music.all():
                bool=True
        except:
            pass
       
        return bool

    def get_in_favourite(self, obj):
        bools=False
        try:
            
            for i in TopMusic.objects.all():
                if obj.id == i.music.id:
                    bools=True
        except:
            pass
            print(bools)
    
        return bools

class OwnedMusicSerializer(serializers.ModelSerializer):
    music = MusicRUDSerializers(many=True)
    user = UserSerializer()
    class Meta:
        model = OwnedMusics
        fields = ['user', 'music']


class RequestMusicSerializers(serializers.ModelSerializer):

    class Meta:
        model = RequestMusic
        fields = ['id', 'title', 'spotifyId', 'spotifyLink', 'count' ]

    def create(self, validated_data):
        print('helloooo')
        title = validated_data['title']
        spotifyId = validated_data['spotifyId']
        spotifyLink = validated_data['spotifyLink']
        print(spotifyId)
        requested = RequestMusic.objects.filter(spotifyId=spotifyId).first()
        print(requested, 'requestd')
        if requested:
            requested.count = requested.count+1
            requested.save()
        else:
           requested= RequestMusic.objects.create(title=title, spotifyId=spotifyId, spotifyLink=spotifyLink)
        return requested

        

class SoldMusicSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    music = MusicRUDSerializers()
    class Meta:
        model = SoldMusics
        fields = ['id', 'user', 'music', 'createdAt']
    
 

class AddToCartSerializer(serializers.ModelSerializer):
    music = MusicRUDSerializers(many=True)
    totalPrice = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = AddMusicToCart
        fields = ['user', 'music', 'totalPrice']


    def get_totalPrice(self, obj):
        cart = AddMusicToCart.objects.get(user__email=obj)
        count = cart.music.all().aggregate(Sum('price'))['price__sum']

        return  count

# class TopMusicSerializer(serializers.ModelSerializer):

#     music = MusicRUDSerializers(many=True)
#     class Meta:
#         model = TopMusicList
#         fields = ['id', 'music']


class AdsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddField
        fields = '__all__'

class SearchSongReviewSerializers(serializers.Serializer):
    id = serializers.CharField(max_length=100)
    name = serializers.CharField(max_length=1000)
    artwork = serializers.CharField(max_length=2000)
    artist = serializers.CharField(max_length=500)
    key = serializers.CharField(max_length=200)
    bpm = serializers.CharField(max_length=200)
    price = serializers.CharField(max_length=200)
    spotifyId = serializers.CharField(max_length=200)
    spotifyLink = serializers.CharField(max_length=200)
    is_abailable = serializers.BooleanField(default=False)
    

class TopMusicSerializer(serializers.ModelSerializer):
    music = MusicRUDSerializers()
    class Meta:
        model = TopMusic
        fields = ['id', 'music']

class ExtraInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtraInfo
        fields = '__all__'