"""Djeddit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from Djeddit import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('post/', views.post_view),
    path('post/<slug:subreddit>/', views.post_view),
    path('create_subreddit/', views.create_subreddit_view),
    path('signup/', views.signup_view),
    path('', views.front_page_view, name='frontpage'),
    path('login/', views.login_view),
    path('r/<slug:subreddit>/', views.subreddit_view),
    path('explore/', views.ExploreView.as_view()),
    path('thanks/', views.thanks_view),
    path('u/<slug:author>/', views.profile_view),
    path('p/<int:post>/', views.individual_post_view),
    path('subscribe/<slug:subreddit>/', views.subscription_view),
    path('unsubscribe/<slug:subreddit>/', views.unsubscription_view),
    path('ajax/vote/', views.ajax_vote),
    path('moderatoradd/', views.moderatoradd_view),
    path('logout/', views.LogoutView.as_view()),
    path('bio/<slug:user>/', views.bio_view),
    path('p/<int:post>/delete/<int:comment>/', views.delete_comment_view),
    path('subdelete/<int:subreddit>/', views.DeleteSubView.as_view()),
    path('r/<slug:subreddit>/delete/<int:post>/', views.delete_post_view),
    path('p/<int:post>/delete/', views.delete_individual_post_view),
    path('subdelete/<int:subreddit>/', views.delete_sub_view),
    path('p/<int:post>/reply/<int:comment>/', views.reply_view),
    path('p/<int:post>/delete_reply/<int:reply>/', views.delete_reply_view)
    path('testform/', views.test_cookie),
    path('p/<int:post>/reply/<int:comment>/', views.reply_view),
]
