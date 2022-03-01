from django.http      import Http404

from rest_framework             import status
from rest_framework.response    import Response
from rest_framework.views       import APIView
from rest_framework             import generics
from rest_framework             import viewsets
from rest_framework.exceptions  import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly


from contents.models import StreamPlatform, Content, Review
from .serializers    import StreamPlatformSerializer, ContentSerializer, ReviewSerializer
from contents.api.permissions import IsAdminOrReadOnly, IsReviewUserOrReadOnly


class ReviewCreate(generics.CreateAPIView):
    serializer_class   = ReviewSerializer
    permission_classes = [IsAuthenticated]
    
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
    serializer_class   = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(content=pk)
    

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset         = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly]
    

class StreamPlatformModelViewset(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset           = StreamPlatform.objects.all()
    serializer_class   = StreamPlatformSerializer
    
    
class ContentListAPIView(APIView):
    permission_classes = [IsAdminOrReadOnly]
    
    def get(self, request):
        contents   = Content.objects.all()
        serializer = ContentSerializer(contents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = ContentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContentDetailAPIView(APIView):
    permission_classes = [IsAdminOrReadOnly]
    
    def get_object(self, pk):
        try:
            return Content.objects.get(pk=pk)
        except Content.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        content    = self.get_object(pk)
        serializer = ContentSerializer(content)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        content    = self.get_object(pk)
        serializer = ContentSerializer(content, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        content = self.get_object(pk)
        content.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)