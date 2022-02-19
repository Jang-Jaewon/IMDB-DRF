from rest_framework import serializers

from contents.models import Movie


class MovieSerializer(serializers.ModelSerializer):
    len_name = serializers.SerializerMethodField()
    
    class Meta:
        model  = Movie
        fields = "__all__"
        
    def get_len_name(self, object):
        length = len(object.name)
        return length  
    
    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Name is too short!")
        return value
    
    def validate(self, data):
        if data['name'] == data['description']:
            raise serializers.ValidationError("Name and Description should be different!")
        return data