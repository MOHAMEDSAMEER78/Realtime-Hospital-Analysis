from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import EdgeDataSerializer
from .tasks import process_edge_data
import logging
from rest_framework import status


logger = logging.getLogger(__name__)

@api_view(['POST'])
def receive_data(request):
    serializer = EdgeDataSerializer(data=request.data)
    print(request.data)
    print(serializer.is_valid())
    print(serializer.errors)
    print(serializer.validated_data)
    if serializer.is_valid():
        try:
            print("Valid data received")
            process_edge_data.delay(serializer.validated_data)
            print("Data sent to Celery task")
            print("status", status.HTTP_201_CREATED)
            return Response({"status": "Data received and processed successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"status": "Error processing data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=400)
