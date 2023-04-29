from django.contrib import admin

class BookrAdminSite(admin.AdminSite):
    site_header = 'Aplikacja administracyjna Bookr'
    site_title = 'Bookr site admin'
    index_title = 'Bookr administration'