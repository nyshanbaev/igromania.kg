from django.urls import path, include
from applications.game.views import *
from rest_framework.routers import DefaultRouter



router = DefaultRouter()
router.register('game', GameModelViewSet)
router.register('image', GameImageModelViewSet)
router.register('comment', CommentModelViewSet)
router.register('favorite', FavoriteModelViewSet)


urlpatterns =[
    path('', include(router.urls)),
]