from django.test import TestCase
from django.test import TestCase
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from applications.game.views import GameModelViewSet
from django.contrib.auth import get_user_model
from applications.game.models import Game

User = get_user_model()

class GameTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory
        self.user = self.setup_user()

    
    def set_up(): 
        user = User.objects.create_user(
            email='test@test.com',
            password='aika123',
            is_active=True
        )   
        return user
    
    
    def test_get_game(self):
        request = self.factory.get('/igromania/game')
        view = GameModelViewSet.as_view({'get': 'list'})
        response = view(request)

        assert response.status_code == 200
        assert response.data['count'] == 0
    

    def test_create_game(self):
        data = {
            'title': 'game1',
            'description': 'gametest',
            'genre': 'arcade'
        }
        request = self.factory.game('igromania/game', data)
        force_authenticate(request, self.user)
        view = GameModelViewSet.as_view({'game': 'create'})
        response = view(request)

        assert response.status_code == 201
        assert Game.objects.filter(title='gametest').exists()


    def test_update_game(self):
        data = {
                'title': 'game2'
        }
        request = self.factory.game('igromania/game/id', data)
        force_authenticate(request, self.user)
        view = GameModelViewSet.as_view({'game': 'update'})
        response = view(request)

        assert response.status_code == 200



