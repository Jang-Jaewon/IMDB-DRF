from rest_framework import serializers

from contents.models import StreamPlatform, Content


class ContentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model  = Content
        fields = "__all__"
        
        
class StreamPlatformSerializer(serializers.ModelSerializer):
    contentlist = ContentSerializer(many=True, read_only=True)
    
    class Meta:
        model  = StreamPlatform
        fields = "__all__"

