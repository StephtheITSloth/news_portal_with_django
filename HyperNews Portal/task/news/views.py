from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.conf import settings
from django.shortcuts import render, redirect
import json
from collections import OrderedDict
from datetime import datetime
from itertools import groupby
from random import randrange




class WelcomeView(View):

    def get(self,request):
        return redirect('/news/')
# Create your views here.

class NewsView(View):
    def get(self, request):
        q = (request.GET.get('q') or "").strip()
        context = {}
        with open(settings.NEWS_JSON_PATH, 'r', encoding='utf-8') as file:
            news_list = json.load(file)
            for item in news_list:
                item['created'] = datetime.strptime(item['created'], '%Y-%m-%d %H:%M:%S')
            sorted_news = sorted(news_list, key=lambda x: x['created'], reverse=True)
            grouped_news = OrderedDict()
            for date, items in groupby(sorted_news, key=lambda x: x['created'].date()):
                grouped_news[date] = list(items)

            search_result = []
            if q:
                for item in sorted_news:
                    if q.lower() in item['title'].lower():
                        search_result.append(item)

        if q:
            return render(request, 'news_page.html', {'news':search_result})
        else:
            return render(request, 'news_page.html', {'grouped_news': grouped_news})

class ArticleView(View):

    def get(self, request, link, *args, **kwargs):
        file_name = settings.NEWS_JSON_PATH
        with open(file_name, 'r') as file:
            data = json.load(file)
        template_name = 'article.html'
        for item in data:
            if item['link'] == link:
                context = {'article':item}
                return render(request, template_name, context)

class CreateView(View):

    def get(self, request):
        template_name = 'create.html'
        return render(request, template_name, {})

    def create_new_link(self, links):
        new_link = randrange(1,3478, 4)
        if new_link in links:
            new_link = new_link * 251
        return new_link
    def post(self, request, *args, **kwargs):
        title = (request.POST.get('title') or " ").strip()
        text = (request.POST.get('text') or " ").strip()
        file_name = settings.NEWS_JSON_PATH
        with open(file_name, 'r') as file:
            data = json.load(file)

        links = []
        for d in data:
            links.append(d['link'])


        if request.method == "POST":
            new_link = self.create_new_link(links)
            new_link = str(new_link)
            #"2020-02-22 14:00:00"
            dt_format = '%Y-%m-%d %H:%M:%S'
            today_date = datetime.strftime(datetime.now(), dt_format)
            new_article = {
                "created": today_date,
                "title": title,
                "text": text,
                "link": new_link
            }

            data.append(new_article)

            with open(file_name, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False)

            return redirect('/news/')
