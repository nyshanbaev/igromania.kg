from rest_framework import serializers
from applications.game.models import *
from django.db.models import Avg


class RatingSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    # game = serializers.ReadOnlyField(source = 'game_id')
    
    class Meta:
        model = Rating
        fields = ('rating', 'owner')
        # read_only_fields = ('game',)   


class FavoriteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Favorite
        fields = '__all__'
class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ('owner', 'game')


class GameSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    like = LikeSerializer(many=True, read_only=True)
    rating = RatingSerializer(many=True, read_only=True)
    class Meta:
        model = Game
        fields = '__all__'
        # read_only_fields = ('game',)      

    def to_representation(self, instance):
            representation = super().to_representation(instance)
            representation['images'] = GameImageSerializer(instance.images.all(), many=True, context=self.context).data
            representation['like_count'] = instance.likes.filter(is_like=True).count()
            representation['rating'] = instance.ratings.all().aggregate(Avg('rating'))['rating__avg']

            return representation    
            

class GameImageSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    

    class Meta:
        model = GameImage
        fields = '__all__'

    def _get_image_url(self, obj):
            if obj.image:
                url = obj.image.url
                request = self.context.get('request')
                if request is not None:
                    url = request.build_absolute_uri(url)
                else:
                    url = ''
            return url

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     print(instance, '..............')
    #     representation['images'] = GameImageSerializer(instance.images.all(), many=True, context=self.context).data
        


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Comment
        fields = '__all__'        


