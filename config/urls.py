from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('dashboard/', admin.site.urls),
    path('api/content/', include('contents.api.urls')),
    path('api/account/', include('users.api.urls')),
    # path('api-auth/', include('rest_framework.urls')),
]