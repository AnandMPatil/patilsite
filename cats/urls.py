from django.urls import path
from . import views

# https://docs.djangoproject.com/en/3.0/topics/http/urls/
app_name='cats'
urlpatterns = [
    path('', views.MainView.as_view(), name='all'),
    path('main/create/', views.CatCreate.as_view(), name='cat_create'),
    path('main/<int:pk>/update/', views.CatUpdate.as_view(), name='cat_update'),
    path('main/<int:pk>/delete/', views.CatDelete.as_view(), name='cat_delete'),
    path('lookup/', views.MakeView.as_view(), name='make_list'),
    path('lookup/create/', views.MakeCreate.as_view(), name='make_create'),
    path('lookup/<int:pk>/update/', views.MakeUpdate.as_view(), name='make_update'),
    path('lookup/<int:pk>/delete/', views.MakeDelete.as_view(), name='make_delete'),
]
