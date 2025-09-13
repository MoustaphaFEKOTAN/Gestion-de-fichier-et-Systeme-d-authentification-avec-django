# authentication/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from blog.models import Blog
class User(AbstractUser):

    CREATOR = 'creator'
    SUBSCRIBER = 'subscriber'

    ROLE_CHOICES = (
    (CREATOR, 'Créateur'),
    (SUBSCRIBER, 'Abonné'),
)
    profile_photo = models.ImageField(verbose_name='Photo de profil')
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, verbose_name='Rôle')

    follows = models.ManyToManyField(
        'self',
        limit_choices_to={'role': CREATOR},
        symmetrical=False,
        verbose_name='suit',
    )
#     Le premier argument dans le  ManyToManyField  est le modèle avec lequel vous nouez une relation. 
#     Dans notre cas, il s’agit du même modèleUser, auquel nous référons avec'self'.

# Vous pouvez limiter quels utilisateurs peuvent être suivis en utilisant le mot-clé optionnel limit_choices_to. 
# Nous voulons que seuls les utilisateurs avec le rôle  CREATOR  puissent être suivis.

# Dans ce cas particulier, où les deux modèles dans la relation plusieurs-à-plusieurs sont les mêmes, vous devez 
# également préciser si la relation est symétrique. Les relations symétriques sont celles où 
# il n’y a aucune différence entre les deux acteurs de la relation, comme quand on lie deux amis.
# Un utilisateur en suit un autre, donc vous précisez  symmetrical=False  .
# L’argument  symmetrical  n’est pas  requis si vous liez à un autre modèle que celui dans lequel le  ManyToManyField  est déclaré.


