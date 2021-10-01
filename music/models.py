
from re import S
from django.db import models
from django.db.models.fields import IntegerField
from django.db.models.signals import post_save,  post_delete, m2m_changed
from django.dispatch import receiver
from django.contrib.auth import get_user_model 
User = get_user_model()

# Create your models here.
def upload_Music(instance, filename):
    return 'Music/{filename}'.format(filename=filename)

def upload_artwork(instance, filename):
    return 'ArtWork/{filename}'.format(filename=filename)

class Musics(models.Model):
    title = models.CharField(max_length=500)
    artist = models.CharField(max_length=500)
    key = models.CharField(max_length=100)
    bpm = models.IntegerField(default=0)
    description = models.TextField(max_length=100)
    artWork = models.CharField(max_length=500)
    spotifyId = models.CharField(max_length=250)
    price = models.FloatField(default=0)
    path = models.CharField(max_length=500)
    song = models.FileField(upload_to=upload_Music)
    youtubeId = models.CharField(max_length=250)
    is_shortList = models.BooleanField(default=False)
    sortNumber = models.IntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.title)

class OwnedMusics(models.Model):
    user = models.OneToOneField(User, related_name="owner", on_delete=models.CASCADE)
    music = models.ManyToManyField(Musics, related_name="ownedMusics")
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.user)

class RequestMusic(models.Model):
    title = models.CharField(max_length=500)
    spotifyId = models.CharField(max_length=250)
    spotifyLink = models.CharField(max_length=2000)
    count = models.IntegerField(default=1)
    createdAt = models.DateTimeField(auto_now_add=True)

class SoldMusics(models.Model):
    user = models.ForeignKey(User,  related_name="buyingUser", on_delete=models.CASCADE)
    music = models.ForeignKey(Musics,  related_name="soldMusic", on_delete=models.CASCADE)
    createdAt = models.DateField(auto_now_add=True)

class AddMusicToCart(models.Model):
    user = models.OneToOneField(User, related_name="cartOwner", on_delete=models.CASCADE)
    music = models.ManyToManyField(Musics, related_name="musicInCart")
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.user)



class TopMusicList(models.Model):
    user = models.OneToOneField(User, related_name="topMusic", on_delete=models.CASCADE)
    music = models.ManyToManyField(Musics, related_name="topMusicList")

    def __str__(self) -> str:
        return str(self.user)


class TopMusic(models.Model):
    music = models.ForeignKey(Musics, related_name="topMusic", on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.music)

class AddField(models.Model):
    add1 = models.TextField()
    add2 = models.TextField()
    def __str__(self) -> str:
        return str(self.add1)


class ExtraInfo(models.Model):
    aboutUs = models.TextField()
    contactUs = models.TextField()
    legal = models.TextField()
    termsAndCondition = models.TextField()
    
    def __str__(self) -> str:
        return str(self.aboutUs)


class YoutubeApi(models.Model):
    api= models.CharField(max_length=500)
    count = models.IntegerField(default=30)

    def __str__(self) -> str:
        return str(self.api)



    

@receiver(post_save, sender=User)
def create_UserFollow(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        OwnedMusics.objects.create(user=instance)
        AddMusicToCart.objects.create(user=instance)


