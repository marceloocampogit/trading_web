from django.shortcuts import render, HttpResponse

import requests

from django_base.settings import NEWS_API_KEY

from news.models import News

# Create your views here.

def fetch_news(request):

    response = requests.get(f'https://newsapi.org/v2/everything?q=bitcoin&apiKey={NEWS_API_KEY}')

    if response.status_code != 200:
        return HttpResponse(response.status_code)
    
    response = response.json()

    for article in response['articles']:

        if all([article['title'], article['description'], article['url'], article['urlToImage'], article['publishedAt']]):
            #Si cumple todas las condiciones de un articulo completo, lo cargo en la base de datos
            News.objects.create(
                title=article['title'],
                description=article['description'],
                url_to_news=article['url'],
                url_to_image=article['urlToImage'],
                published_at=article['publishedAt'])
            
        else:
            #Sino sigo buscando
            continue
    
    return HttpResponse('News fetched successfully')

