from django.contrib import admin
from django.contrib.admin import AdminSite
from reviews.models import (Review, Book, Publisher, Contributor, BookContributor)
from bookr.admin import BookrAdminSite


class BookAdmin(admin.ModelAdmin):
    search_fields = ('title', 'isbn')
    date_hierarchy = 'publication_date'
    list_display = ('title', 'isbn13')
    list_filter = ('publisher', 'publication_date')
    # exclude = ('isbn',)
    # fields = ('title','publisher', 'publication_date')
    fieldsets = ('Daty', {'fields': ('publication_date',)}), \
        ('Informacje o książce', {'fields': ('title', 'isbn', 'publisher')}),

    def isbn13(self, obj):
        return obj.isbn[:3] + '-' + obj.isbn[3:4] + '-' + obj.isbn[4:6] + '-' + obj.isbn[6:12] + '-' + obj.isbn[12:13]


admin_site = BookrAdminSite(name='bookr')

admin_site.register(Review)
admin_site.register(Book, BookAdmin)
admin_site.register(Publisher)
admin_site.register(Contributor)
admin_site.register(BookContributor)

# Register your models here.
