from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import StringProcessSerializer
from .HotelRag import push_query

# Create your views here.
class HotelRag(APIView):
    # @api_view(['GET'])
    # def get_string(request):
    #     return Response(StringProcessSerializer({"input_string": "Hello guys!"}).data)

    # @api_view(['POST'])
    def post(self, request):
        serializer = StringProcessSerializer(data=request.data)
        if(serializer.is_valid()):
            input_string = serializer.validated_data['input_string']
            print(input_string)
            output_string = self.process_string(input_string)
            print(output_string)
            return Response({'output_string': output_string}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def process_string(slef, input_string):
        output = push_query(input_string)
        return output