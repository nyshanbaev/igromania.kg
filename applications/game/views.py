from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import mixins, viewsets
from applications.game.models import Comment, GameImage, Game
from applications.game.serializers import *
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.viewsets import  ModelViewSet
from rest_framework.pagination import PageNumberPagination
from applications.game.permissions import IsOwner
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views import View



class CustomPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 10000


@method_decorator(cache_page(60 * 15), name='dispatch')
class GameModelViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['owner', 'genre']
    search_fields = ['title']
    ordering_fields = ['id', 'title']
    
    @action(methods=['POST'], detail=True)
    def rating(self, request, pk, *args, **kwargs):
        
        serializer = RatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)


        rating_obj, _ = Rating.objects.get_or_create(owner=request.user, game_id=pk)
        rating_obj.rating = serializer.data['rating']
        rating_obj.save()

        
        return Response('Ok!')

    @action(methods=['POST'], detail=True)
    def like(self, request, pk, *args, **kwargs):
        user = request.user
        like_obj, _ = Like.objects.get_or_create(owner=user, game_id=pk)
        like_obj.is_like = not like_obj.is_like
        like_obj.save()
        status = 'liked'

        if not like_obj.is_like:
            status = 'unliked'
        return Response({'status': status})
 


    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [AllowAny, ]
        else:
            self.permission_classes = [IsAuthenticated, IsOwner]   
        return super(GameModelViewSet, self).get_permissions()         


    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)                  
    


class GameImageModelViewSet(ModelViewSet):
    queryset = GameImage.objects.all()
    serializer_class = GameImageSerializer
    permission_classes = [IsAuthenticated, IsOwner]    


class CommentModelViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [AllowAny, ]
        else:
            self.permission_classes = [IsAuthenticated, IsOwner]   
        return super(CommentModelViewSet, self).get_permissions()         


    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user) 
    

class FavoriteModelViewSet(ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsOwner]
        else:
            self.permission_classes = [IsAuthenticated, IsOwner]   
        return super(FavoriteModelViewSet, self).get_permissions()         


    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user) 


from rest_framework.views import APIView
from rest_framework.response import Response
from loguru import logger

class TestView(APIView):
    def get(self, request, *args, **kwargs):
        logger.info('This is a test log message')
        return Response({'message': 'Hello, world!'})