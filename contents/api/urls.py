from django.urls        import path

from .views import StreamPlatformAPIView, StreamPlatformDetailAPIView, ContentListAPIView, ContentDetailAPIView


urlpatterns = [
    path('stream/', StreamPlatformAPIView.as_view(), name='stream'),
    path('stream/<int:pk>', StreamPlatformDetailAPIView.as_view(), name='stream-detail'),
    path('list/', ContentListAPIView.as_view(), name='content-list'),
    path('<int:pk>/', ContentDetailAPIView.as_view(), name='content-detail'),
]