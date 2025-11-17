"""Report API endpoints"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from apps.finance.services.report_service import ReportService
from apps.core.middleware.rbac import require_permission
from drf_spectacular.utils import extend_schema, OpenApiParameter
from datetime import datetime


class ReportViewSet(viewsets.ViewSet):
    """ViewSet for finance reports"""
    
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        parameters=[
            OpenApiParameter('date_from', str, description='Start date (YYYY-MM-DD)'),
            OpenApiParameter('date_to', str, description='End date (YYYY-MM-DD)'),
            OpenApiParameter('academic_year', str, description='Academic year'),
            OpenApiParameter('semester', str, description='Semester'),
            OpenApiParameter('program', str, description='Program'),
        ],
        responses={200: dict}
    )
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    @require_permission('finance', 'read')
    def fee_collection(self, request):
        """
        Get fee collection summary report
        
        GET /reports/fee-collection/
        
        Query parameters:
        - date_from: Start date (YYYY-MM-DD)
        - date_to: End date (YYYY-MM-DD)
        - academic_year: Academic year
        - semester: Semester
        - program: Program
        """
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        academic_year = request.query_params.get('academic_year')
        semester = request.query_params.get('semester')
        program = request.query_params.get('program')
        
        # Parse dates
        date_from_obj = None
        date_to_obj = None
        
        if date_from:
            try:
                date_from_obj = datetime.strptime(date_from, '%Y-%m-%d').date()
            except ValueError:
                return Response(
                    {'error': 'Invalid date_from format. Use YYYY-MM-DD'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        if date_to:
            try:
                date_to_obj = datetime.strptime(date_to, '%Y-%m-%d').date()
            except ValueError:
                return Response(
                    {'error': 'Invalid date_to format. Use YYYY-MM-DD'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        summary = ReportService.generate_fee_collection_summary(
            date_from=date_from_obj,
            date_to=date_to_obj,
            academic_year=academic_year,
            semester=semester,
            program=program
        )
        
        return Response(summary)
    
    @extend_schema(
        parameters=[
            OpenApiParameter('student_id', int, description='Student ID', required=True),
        ],
        responses={200: dict}
    )
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    @require_permission('finance', 'read')
    def student_fees(self, request):
        """
        Get fee report for a specific student
        
        GET /reports/student-fees/?student_id=123
        """
        student_id = request.query_params.get('student_id')
        
        if not student_id:
            return Response(
                {'error': 'student_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            report = ReportService.generate_student_fee_report(int(student_id))
            return Response(report)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @extend_schema(
        parameters=[
            OpenApiParameter('academic_year', str, description='Academic year'),
            OpenApiParameter('semester', str, description='Semester'),
            OpenApiParameter('overdue_only', bool, description='Filter overdue only'),
        ],
        responses={200: list}
    )
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    @require_permission('finance', 'read')
    def outstanding_fees(self, request):
        """
        Get outstanding fees report
        
        GET /reports/outstanding-fees/
        
        Query parameters:
        - academic_year: Academic year
        - semester: Semester
        - overdue_only: Filter overdue invoices (true/false)
        """
        academic_year = request.query_params.get('academic_year')
        semester = request.query_params.get('semester')
        overdue_only = request.query_params.get('overdue_only') == 'true'
        
        report = ReportService.get_outstanding_fees_report(
            academic_year=academic_year,
            semester=semester,
            overdue_only=overdue_only
        )
        
        return Response(report)
    
    @extend_schema(
        parameters=[
            OpenApiParameter('date_from', str, description='Start date (YYYY-MM-DD)'),
            OpenApiParameter('date_to', str, description='End date (YYYY-MM-DD)'),
            OpenApiParameter('academic_year', str, description='Academic year'),
            OpenApiParameter('semester', str, description='Semester'),
            OpenApiParameter('format', str, description='Export format (csv, pdf, excel)'),
        ],
        responses={200: bytes}
    )
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    @require_permission('finance', 'read')
    def export(self, request):
        """
        Export fee collection report
        
        GET /reports/export/
        
        Query parameters:
        - date_from: Start date (YYYY-MM-DD)
        - date_to: End date (YYYY-MM-DD)
        - academic_year: Academic year
        - semester: Semester
        - format: Export format (csv, pdf, excel) - default: csv
        """
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        academic_year = request.query_params.get('academic_year')
        semester = request.query_params.get('semester')
        export_format = request.query_params.get('format', 'csv')
        
        # Parse dates
        date_from_obj = None
        date_to_obj = None
        
        if date_from:
            try:
                date_from_obj = datetime.strptime(date_from, '%Y-%m-%d').date()
            except ValueError:
                return Response(
                    {'error': 'Invalid date_from format. Use YYYY-MM-DD'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        if date_to:
            try:
                date_to_obj = datetime.strptime(date_to, '%Y-%m-%d').date()
            except ValueError:
                return Response(
                    {'error': 'Invalid date_to format. Use YYYY-MM-DD'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        if export_format == 'csv':
            csv_content = ReportService.export_collection_report_csv(
                date_from=date_from_obj,
                date_to=date_to_obj,
                academic_year=academic_year,
                semester=semester
            )
            
            response = HttpResponse(csv_content, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="fee_collection_report.csv"'
            return response
        elif export_format in ['pdf', 'excel']:
            # TODO: Implement PDF and Excel export
            return Response(
                {'error': f'{export_format} format not yet implemented'},
                status=status.HTTP_501_NOT_IMPLEMENTED
            )
        else:
            return Response(
                {'error': f'Invalid format: {export_format}. Supported: csv, pdf, excel'},
                status=status.HTTP_400_BAD_REQUEST
            )
