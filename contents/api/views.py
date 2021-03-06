from django.http      import Http404

from rest_framework                import status
from rest_framework.response       import Response
from rest_framework.views          import APIView
from rest_framework                import generics
from rest_framework                import viewsets
from rest_framework.exceptions     import ValidationError
from rest_framework.permissions    import IsAuthenticated
from rest_framework.throttling     import AnonRateThrottle, ScopedRateThrottle
from django_filters.rest_framework import DjangoFilterBackend

from contents.models import StreamPlatform, Content, Review
from contents.api    import serializers, permissions, throttling, pagination


class UserReviewList(generics.ListAPIView):
    serializer_class   = serializers.ReviewSerializer
    
    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        return Review.objects.filter(review_user__username=username)

class ReviewCreate(generics.CreateAPIView):
    serializer_class   = serializers.ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes   = [AnonRateThrottle, throttling.ReviewCreateThrotlling]
    
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):
        pk              = self.kwargs.get('pk')
        content         = Content.objects.get(pk=pk)
        review_user     = self.request.user
        review_queryset = Review.objects.filter(content=content, review_user=review_user)
        
        if review_queryset.exists():
            raise ValidationError('You have already reivewed this content!')
        
        if content.number_rating == 0:
            content.avg_rating = serializer.validated_data['rating']
        else:
            content.avg_rating = (content.avg_rating + serializer.validated_data['rating']) / 2
        content.number_rating = content.number_rating + 1
        content.save()
        
        serializer.save(content=content, review_user=review_user)
        

class ReviewList(generics.ListAPIView):
    serializer_class   = serializers.ReviewSerializer
    throttle_classes   = [AnonRateThrottle, throttling.ReviewListThrotlling]
    filter_backends    = [DjangoFilterBackend]
    filterset_fields   = ['review_user__username', 'active']

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(content=pk)
    

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset         = Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    permission_classes = [permissions.IsReviewUserOrReadOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'
    

class StreamPlatformModelViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAdminOrReadOnly]
    queryset           = StreamPlatform.objects.all()
    serializer_class   = serializers.StreamPlatformSerializer
    
    
class ContentListAPIView(APIView):
    permission_classes = [permissions.IsAdminOrReadOnly]
    pagination_class   = pagination.ContentListPagination
    
    def get(self, request):
        contents   = Content.objects.all()
        serializer = serializers.ContentSerializer(contents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = serializers.ContentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContentDetailAPIView(APIView):
    permission_classes = [permissions.IsAdminOrReadOnly]
    
    def get_object(self, pk):
        try:
            return Content.objects.get(pk=pk)
        except Content.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        content    = self.get_object(pk)
        serializer = serializers.ContentSerializer(content)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        content    = self.get_object(pk)
        serializer = serializers.ContentSerializer(content, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        content = self.get_object(pk)
        content.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
