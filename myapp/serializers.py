from rest_framework import serializers

class StringProcessSerializer(serializers.Serializer):
    input_string = serializers.CharField(max_length=200)