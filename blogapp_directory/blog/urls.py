from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('post', views.index, name="index"),
    path('post', views.index, name="index"),
    path('register', views.register_request, name="register"),
    path('login', views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),
    path("post/<int:post_id>", views.post_detail, name="post_detail"),
    path('create_post/', views.create_post, name='create_post'),
    path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('post/<int:post_id>/comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
]