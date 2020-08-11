from django.urls import path, reverse_lazy
from . import views
#from . import models
from django.views.generic import TemplateView
#from myarts.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView
#from django.urls import path, reverse_lazy

app_name='myarts'
urlpatterns = [
    path('', views.ArticleListView.as_view(), name='all'),
    path('ads', views.ArticleListView.as_view(), name='ads'),
    path('article/<int:pk>', views.ArticleDetailView.as_view(), name='article_detail'),
    path('ad/<int:pk>', views.ArticleDetailView.as_view(), name='ad_detail'),
    path('article/create',views.ArticleCreateView.as_view(success_url=reverse_lazy('myarts:all')), name='article_create'),
    path('article/<int:pk>/update',views.ArticleUpdateView.as_view(success_url=reverse_lazy('myarts:all')), name='article_update'),
    path('article/<int:pk>/delete',views.ArticleDeleteView.as_view(success_url=reverse_lazy('myarts:all')), name='article_delete'),

    path('myarts_picture/<int:pk>', views.stream_file, name='myarts_picture'),

    path('article/<int:pk>/comment', views.CommentCreateView.as_view(), name='article_comment_create'),
    path('comment/<int:pk>/delete', views.CommentDeleteView.as_view(success_url=reverse_lazy('myarts:all')), name='article_comment_delete'),

    path('article/<int:pk>/favorite', views.AddFavoriteView.as_view(), name='article_favorite'),
    path('article/<int:pk>/unfavorite', views.DeleteFavoriteView.as_view(), name='article_unfavorite'),

    path('page1', TemplateView.as_view(template_name='myarts/main_menu.html'), name='page1'),
    path('page2', TemplateView.as_view(template_name='myarts/main_menu.html'), name='page2'),
    path('page3', TemplateView.as_view(template_name='myarts/main_menu.html'), name='page3'),
]
