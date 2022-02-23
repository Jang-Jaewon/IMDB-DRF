from django.http      import Http404

from rest_framework            import status
from rest_framework.response   import Response
from rest_framework.views      import APIView
from rest_framework            import generics
from rest_framework            import viewsets

from contents.models import StreamPlatform, Content, Review
from .serializers    import StreamPlatformSerializer, ContentSerializer, ReviewSerializer


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    
    def perform_create(self, serializer):
        pk      = self.kwargs.get('pk')
        content = Content.objects.get(pk=pk)
        serializer.save(content=content)
        

class ReviewList(generics.ListAPIView):
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(content=pk)
    

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset         = Review.objects.all()
    serializer_class = ReviewSerializer
    

class StreamPlatformModelViewset(viewsets.ModelViewSet):
    queryset         = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    
    
class ContentListAPIView(APIView):
    
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