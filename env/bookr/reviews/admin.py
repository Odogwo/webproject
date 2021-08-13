from django.contrib import admin

# Register your models here.
from .models import Publisher , Book, Contributor, BookContributor, Review


admin.site.register(Publisher)
admin.site.register(Book)
admin.site.register(Contributor)
admin.site.register(BookContributor)
admin.site.register(Review)