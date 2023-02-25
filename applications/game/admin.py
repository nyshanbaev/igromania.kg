from django.contrib import admin
from applications.game.models import *


admin.site.register(Category)
admin.site.register(Game)
admin.site.register(Comment)
admin.site.register(GameImage)
admin.site.register(Rating)
admin.site.register(Like)
admin.site.register(Favorite)