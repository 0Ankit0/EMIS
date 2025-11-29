import os
import asyncio
from django.http import FileResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .automation import process_exam_results
from asgiref.sync import async_to_sync

class ExamAutomationView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Extract parameters
        params = {
            'result_type': request.data.get('result_type'),
            'year': request.data.get('year'),
            'session': request.data.get('session'),
            'semester': request.data.get('semester'),
            'program': request.data.get('program'),
        }
        
        delay = float(request.data.get('delay', 1))

        try:
            # Read file into memory
            file_content = file_obj.read()
            
            # Run automation
            # Since we are in a sync view, we need to run the async function
            output_buffer = async_to_sync(process_exam_results)(file_content, params, delay=delay)
            
            # Return the processed file
            filename = f"processed_{file_obj.name}"
            response = FileResponse(output_buffer, as_attachment=True, filename=filename)
            return response

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
