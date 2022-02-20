from rest_framework import serializers

from contents.models import StreamPlatform, Content, Review


class ReviewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Review
        fields = "__all__"

    
class ContentSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    
    class Meta:
        model  = Content
        fields = "__all__"
        
        
class StreamPlatformSerializer(serializers.HyperlinkedModelSerializer):
    contentlist = ContentSerializer(many=True, read_only=True)
    
    class Meta:
        model  = StreamPlatform
        fields = "__all__"

