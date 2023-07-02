import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from django.urls import path

def search(request):
    query = request.GET.get('q', '')
    html = requests.get(f'https://www.google.com/search?q={query}').text
    soup = BeautifulSoup(html, 'html.parser')
    data = soup.select('a:has(h3)')
    result = []
    for item in data:
        if not item.get('href').startswith('/search'):
            result.append({
                'title': item.h3.div.contents[0],
                'link': item.get('href').replace('/url?q=', '').split('&', 1)[0]
            })
    return render(request, 'search/search.html', {'result': result, 'query': query})
                  
urlpatterns = [
    path('', search),
]