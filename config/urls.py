from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('content/', include('contents.api.urls')),
    path('account/', include('users.api.urls')),
    # path('api-auth/', include('rest_framework.urls')),
]