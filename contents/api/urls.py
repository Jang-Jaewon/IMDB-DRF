from django.urls        import path, include

from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('stream', views.StreamPlatformViewset, basename='streamplatform')

urlpatterns = [
    path('', include(router.urls)),
    path('list/', views.ContentListAPIView.as_view(), name='content-list'),
    path('<int:pk>/', views.ContentDetailAPIView.as_view(), name='content-detail'),
    path('stream/<int:pk>/review-create/', views.ReviewCreate.as_view(), name='review-create'),
    path('stream/<int:pk>/review/', views.ReviewList.as_view(), name='review-list'),
    path('stream/review/<int:pk>/', views.ReviewDetail.as_view(), name='review-detail'),
]