from django.conf.urls import patterns, include, url
from hackanation import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^under-rated-prizes/', views.under_rated_prizes, name='under_rated_prizes'),
    url(r'^loved-prizes/', views.most_loved_prizes, name='most_loved_prizes'),
    url(r'^rewarded-prizes/', views.most_rewarded_prizes, name='most_rewarded_prizes'),
    url(r'^search/', views.search, name='search'),
    url(r'^prize', views.prize, name='prize'),
    url(r'^admin/', include(admin.site.urls)),
)
