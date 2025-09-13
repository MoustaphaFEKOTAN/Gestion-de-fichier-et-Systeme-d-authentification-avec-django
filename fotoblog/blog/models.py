# blog/models.py
from django.conf import settings
from django.db import models
from PIL import Image # Pour la manipulation des images

#Explication des classes ci-dessous:
# Photo: représente une photo téléchargée par un utilisateur. Elle contient une image, une légende, un utilisateur qui l'a téléchargée et une date de création.
# Blog: représente un article de blog. Il contient une photo (optionnelle), un titre, un contenu, un auteur (utilisateur), une date de création et un indicateur pour savoir si l'article est mis en avant (starred).
#la relation entre Photo et Blog est une relation de clé étrangère (ForeignKey), ce qui signifie qu'un article de blog peut être associé à une photo, mais une photo peut être associée à plusieurs articles de blog.
class Photo(models.Model):
    image = models.ImageField()
    caption = models.CharField(max_length=128, blank=True)
    # uploader est un utilisateur de l'application d'authentification personnalisée
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

# class Photo(models.Model):
#     ...
#     IMAGE_MAX_SIZE = (800, 800)
    
#     def resize_image(self):
#         image = Image.open(self.image)
#         image.thumbnail(self.IMAGE_MAX_SIZE)
#         # sauvegarde de l’image redimensionnée dans le système de fichiers
#         # ce n’est pas la méthode save() du modèle !
#         image.save(self.image.path)
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     self.resize_image()

class Blog(models.Model):
    photo = models.ForeignKey(Photo, null=True, on_delete=models.SET_NULL, blank=True)
    title = models.CharField(max_length=128)
    content = models.CharField(max_length=5000)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    #  La relation ManyToMany entre Blog et User est gérée via la table intermédiaire BlogContributor.
    contributors = models.ManyToManyField(settings.AUTH_USER_MODEL, through='BlogContributor', related_name='contributions')
    date_created = models.DateTimeField(auto_now_add=True)
    starred = models.BooleanField(default=False)


#Table intermédiaire pour la relation ManyToMany entre Blog et User
# Elle permet de stocker des informations supplémentaires sur la contribution d'un utilisateur à un blog,
class BlogContributor(models.Model):
    contributor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    contribution = models.CharField(max_length=255, blank=True)
    
    #  Nous avons défini l’attribut   unique_together  dans la classe   Meta  pour garantir 
    # qu’il n’y a qu’une seule instance de  BlogContributor  pour chaque paire   contributor  -   blog  
    class Meta:
        unique_together = ('contributor', 'blog')