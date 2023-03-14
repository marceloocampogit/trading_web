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

    #Lista vacia para guardar todas las noticias de la base de datos
    news_to_create = []

    for article in response['articles']:

        #Si cumple todas las condiciones de un articulo completo, lo guardo en la lista
        if all([article['title'], article['description'], article['url'], article['urlToImage'], article['publishedAt']]):
            
                news_to_create.append(News(
                    title=article['title'],
                    description=article['description'],
                    url_to_news=article['url'],
                    url_to_image=article['urlToImage'],
                    published_at=article['publishedAt'])
                )
        else:
            continue
    
    #Genero todas las noticias de una para performance
    News.object.bulk_create(news_to_create)
    
    return HttpResponse('News fetched successfully')

