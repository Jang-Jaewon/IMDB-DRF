from django.urls        import path

from .views import StreamPlatformAPIView, StreamPlatformDetailAPIView, ContentListAPIView, ContentDetailAPIView, ReviewList, ReviewDetail


urlpatterns = [
    path('stream/', StreamPlatformAPIView.as_view(), name='streamplatform'),
    path('stream/<int:pk>/', StreamPlatformDetailAPIView.as_view(), name='streamplatform-detail'),
    path('list/', ContentListAPIView.as_view(), name='content-list'),
    path('<int:pk>/', ContentDetailAPIView.as_view(), name='content-detail'),
    path('stream/<int:pk>/review/', ReviewList.as_view(), name='review-list'),
    path('stream/review/<int:pk>', ReviewDetail.as_view(), name='review-detail'),
]