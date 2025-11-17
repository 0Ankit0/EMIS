"""
Error response serializers
"""
from rest_framework import serializers


class ErrorResponseSerializer(serializers.Serializer):
    """
    Standard error response format with MODULE_ERROR_CODE
    """
    code = serializers.CharField(
        help_text="Error code in MODULE_ERROR_CODE format (e.g., AUTH_001, ADMISSIONS_101)"
    )
    message = serializers.CharField(
        help_text="Human-readable error message"
    )
    details = serializers.DictField(
        required=False,
        help_text="Additional error details"
    )
    correlation_id = serializers.UUIDField(
        help_text="Correlation ID for request tracking"
    )


class ValidationErrorSerializer(serializers.Serializer):
    """Serializer for field validation errors"""
    field = serializers.CharField()
    errors = serializers.ListField(child=serializers.CharField())
