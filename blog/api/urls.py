from django.conf.urls import url
from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from . import views

router = routers.DefaultRouter()
router.register(r'posts', views.PostViewSet)
router.register(r'comment', views.PostViewSet)

urlpatterns = [
    url(r'^api/posts/(?P<pk>[0-9]+)$', views.posts_detail),
    url(r'^api/comment/(?P<pk>[0-9]+)$', views.comment_detail),
    path('comment/', views.comment_detail),
    path('posts/', views.posts_list),
    path('', include(router.urls)),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api-token-identificate/', views.token_identificate)
]