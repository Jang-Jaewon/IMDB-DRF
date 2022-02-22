from django.urls        import path

from . import views


urlpatterns = [
    path('stream/', views.StreamPlatformAPIView.as_view(), name='streamplatform'),
    path('stream/<int:pk>/', views.StreamPlatformDetailAPIView.as_view(), name='streamplatform-detail'),
    path('list/', views.ContentListAPIView.as_view(), name='content-list'),
    path('<int:pk>/', views.ContentDetailAPIView.as_view(), name='content-detail'),
    path('stream/<int:pk>/review-create/', views.ReviewCreate.as_view(), name='review-create'),
    path('stream/<int:pk>/review/', views.ReviewList.as_view(), name='review-list'),
    path('stream/review/<int:pk>/', views.ReviewDetail.as_view(), name='review-detail'),
]