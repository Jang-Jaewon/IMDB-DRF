from django.urls        import path, include

from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register('stream', views.StreamPlatformModelViewset, basename='streamplatform')

urlpatterns = [
    path('', include(router.urls)),
    path('list/', views.ContentListAPIView.as_view(), name='content-list'),
    path('<int:pk>/', views.ContentDetailAPIView.as_view(), name='content-detail'),
    path('<int:pk>/review-create/', views.ReviewCreate.as_view(), name='review-create'),
    path('<int:pk>/review/', views.ReviewList.as_view(), name='review-list'),
    path('review/<int:pk>/', views.ReviewDetail.as_view(), name='review-detail'),
    path('review/', views.UserReviewList.as_view(), name='user-review-detail'),
]