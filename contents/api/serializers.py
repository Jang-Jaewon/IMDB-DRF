from rest_framework import serializers

from contents.models import StreamPlatform, Content, Review


class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Review
        exclude = ('content',)

    
class ContentSerializer(serializers.ModelSerializer):
    # reviews = ReviewSerializer(many=True, read_only=True)
    platform = serializers.CharField(source='platform.name')
    
    class Meta:
        model  = Content
        fields = "__all__"
        
        
class StreamPlatformSerializer(serializers.ModelSerializer):
    contentlist = ContentSerializer(many=True, read_only=True)
    
    class Meta:
        model  = StreamPlatform
        fields = "__all__"

