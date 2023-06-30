from django.http import JsonResponse
from django.core.cache import cache

from .models import Post


def RedisLoadTest(request):
    posts = cache.get_or_set('posts', Post.objects.all().values('id', 'text'))
    return JsonResponse(list(posts), safe=False)


def VanilaLoadTest(request):
    posts = Post.objects.all().values('id', 'text')
    context = {"posts": posts}
    return JsonResponse(list(posts), safe=False)