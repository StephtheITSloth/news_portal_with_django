from django.urls import path
from .views import WelcomeView, ArticleView, NewsView, CreateView
urlpatterns = [
    path("", WelcomeView.as_view()),
    path("news/", NewsView.as_view()),
    path('news/<int:link>/', ArticleView.as_view(), name='article_page'),
    path('news/create/', CreateView.as_view())
]