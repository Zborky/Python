from posts.models import Post,Tag
from django.db.models import Count,Q

def get_recommended_posts(user,limit = 10):
    #ziskanie najoblubenejsich hashatov, ktore pouzivatel komentoval alebo lajkovaj
    favorite_tags = list(Tag.objects.filter(
    Q(posts__likes=user) | Q(posts__comments__user=user)
).annotate(
    score=Count('posts')
).order_by('-score')[:5]) 
    
    #Navrh postov s tymito tagmi, nie od uzivatela a nezobrazene pred tym
    recommended = Post.objects.filter(
    tags__in=favorite_tags
    ).exclude(user=user).distinct().order_by('-created_at')[:limit]
    return recommended    