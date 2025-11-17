"""
Custom exceptions for EMIS with MODULE_ERROR_CODE support
"""


class EMISException(Exception):
    """Base exception for all EMIS errors"""
    
    def __init__(self, message, code=None, details=None):
        self.message = message
        self.code = code or 'CORE_000'
        self.details = details or {}
        super().__init__(self.message)
    
    def to_dict(self):
        return {
            'code': self.code,
            'message': self.message,
            'details': self.details,
        }


class AuthenticationException(EMISException):
    """Authentication-related errors"""
    
    def __init__(self, message, code='AUTH_001', details=None):
        super().__init__(message, code, details)


class AuthorizationException(EMISException):
    """Authorization/permission errors"""
    
    def __init__(self, message, code='AUTH_002', details=None):
        super().__init__(message, code, details)


class ValidationException(EMISException):
    """Data validation errors"""
    
    def __init__(self, message, code='CORE_001', details=None):
        super().__init__(message, code, details)


class NotFoundException(EMISException):
    """Resource not found errors"""
    
    def __init__(self, message, code='CORE_002', details=None):
        super().__init__(message, code, details)


class BusinessRuleException(EMISException):
    """Business logic/rule violations"""
    
    def __init__(self, message, code='CORE_003', details=None):
        super().__init__(message, code, details)


class AdmissionsException(EMISException):
    """Admissions module errors"""
    
    def __init__(self, message, code='ADMISSIONS_101', details=None):
        super().__init__(message, code, details)


class FinanceException(EMISException):
    """Finance module errors"""
    
    def __init__(self, message, code='FINANCE_201', details=None):
        super().__init__(message, code, details)


class AcademicException(EMISException):
    """Academic/courses module errors"""
    
    def __init__(self, message, code='ACADEMIC_301', details=None):
        super().__init__(message, code, details)
