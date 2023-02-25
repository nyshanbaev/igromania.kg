from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator



User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, primary_key=True)

    def __str__(self):
        return self.title


class Game(models.Model):
    title = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='games')
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    video = models.FileField(upload_to='uploads/video', validators=[FileExtensionValidator(allowed_extensions=['mp4'])], blank=True, null=True)
    file = models.FileField(upload_to='uploads/game', validators=[FileExtensionValidator(allowed_extensions=['apk'])])
    genre = models.ManyToManyField(Category)

    def __str__(self):
        return self.title
    

class GameImage(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='images')
    images = models.ImageField(upload_to='uploads/images')
    
    def __str__(self):
        return f'{self.game.title}'
    

class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='comments')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.owner} -> {self.game}'


class Rating(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='ratings')
    rating = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)], blank=True, null=True)

    def __str__(self):
        return f'{self.owner}'
    

class Favorite(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='favorites')

    def __str__(self):
        return f'{self.game.title}'
    

class Like(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')   
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='likes') 
    is_like = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.owner} liked -{self.game.title}'