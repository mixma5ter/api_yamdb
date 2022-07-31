from django.contrib import admin

from reviews.models import Genre, Category, Title, Review, Comment


admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(Title)
admin.site.register(Review)
admin.site.register(Comment)
