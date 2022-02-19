from rest_framework import serializers

from contents.models import StreamPlatform, Content


class StreamPlatformSerializer(serializers.ModelSerializer):
    
    class Meta:
        model  = StreamPlatform
        fields = "__all__"


class ContentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model  = Content
        fields = "__all__"