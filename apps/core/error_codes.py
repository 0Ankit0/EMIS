"""
Error code registry for EMIS
Format: MODULE_CATEGORY_SUBCODE

Error Code Ranges:
- CORE_000-099: Core system errors
- AUTH_001-099: Authentication & Authorization
- ADMISSIONS_101-199: Admissions module
- FINANCE_201-299: Finance module
- ACADEMIC_301-399: Courses & Academic module
- LMS_401-499: Learning Management System
- LIBRARY_501-599: Library module
- HR_601-699: HR & Faculty module
- ANALYTICS_701-799: Analytics & Reporting
"""

ERROR_CODES = {
    # Core Errors (000-099)
    'CORE_000': 'Unknown error occurred',
    'CORE_001': 'Validation error',
    'CORE_002': 'Resource not found',
    'CORE_003': 'Business rule violation',
    'CORE_004': 'Database error',
    'CORE_005': 'External service error',
    'CORE_006': 'Configuration error',
    'CORE_007': 'Rate limit exceeded',
    'CORE_008': 'Operation timeout',
    
    # Authentication & Authorization (001-099)
    'AUTH_001': 'Invalid credentials',
    'AUTH_002': 'Permission denied',
    'AUTH_003': 'Token expired',
    'AUTH_004': 'Invalid token',
    'AUTH_005': 'Account locked',
    'AUTH_006': 'Account inactive',
    'AUTH_007': 'Password expired',
    'AUTH_008': 'Password too weak',
    'AUTH_009': 'Session expired',
    'AUTH_010': 'Two-factor authentication required',
    'AUTH_011': 'Invalid two-factor code',
    'AUTH_012': 'User not found',
    'AUTH_013': 'Email already exists',
    'AUTH_014': 'Username already exists',
    'AUTH_015': 'Role not found',
    'AUTH_016': 'Permission not found',
    'AUTH_017': 'Cannot modify own permissions',
    'AUTH_018': 'Insufficient privileges',
    
    # Admissions (101-199)
    'ADMISSIONS_101': 'Application not found',
    'ADMISSIONS_102': 'Invalid application status',
    'ADMISSIONS_103': 'Application already submitted',
    'ADMISSIONS_104': 'Missing required documents',
    'ADMISSIONS_105': 'Application deadline passed',
    'ADMISSIONS_106': 'Merit list not found',
    'ADMISSIONS_107': 'Merit list already generated',
    'ADMISSIONS_108': 'Invalid ranking criteria',
    'ADMISSIONS_109': 'Enrollment failed',
    'ADMISSIONS_110': 'Program capacity full',
    'ADMISSIONS_111': 'Invalid eligibility criteria',
    'ADMISSIONS_112': 'Document verification failed',
    
    # Finance (201-299)
    'FINANCE_201': 'Invoice not found',
    'FINANCE_202': 'Payment failed',
    'FINANCE_203': 'Insufficient payment amount',
    'FINANCE_204': 'Payment already processed',
    'FINANCE_205': 'Fee structure not found',
    'FINANCE_206': 'Invalid installment',
    'FINANCE_207': 'Late fee calculation error',
    'FINANCE_208': 'Refund not allowed',
    'FINANCE_209': 'Payment gateway error',
    'FINANCE_210': 'Transaction timeout',
    'FINANCE_211': 'Invalid payment method',
    'FINANCE_212': 'Duplicate transaction',
    
    # Academic/Courses (301-399)
    'ACADEMIC_301': 'Course not found',
    'ACADEMIC_302': 'Enrollment failed',
    'ACADEMIC_303': 'Prerequisites not met',
    'ACADEMIC_304': 'Course capacity full',
    'ACADEMIC_305': 'Assignment not found',
    'ACADEMIC_306': 'Submission deadline passed',
    'ACADEMIC_307': 'Submission already exists',
    'ACADEMIC_308': 'Grade not found',
    'ACADEMIC_309': 'Grade already finalized',
    'ACADEMIC_310': 'Cannot modify finalized grade',
    'ACADEMIC_311': 'Transcript not available',
    'ACADEMIC_312': 'Incomplete grade records',
    'ACADEMIC_313': 'Invalid grade value',
    'ACADEMIC_314': 'Module not found',
    'ACADEMIC_315': 'Invalid course status',
    
    # LMS (401-499)
    'LMS_401': 'Content not found',
    'LMS_402': 'Quiz not found',
    'LMS_403': 'Quiz timeout',
    'LMS_404': 'Invalid quiz attempt',
    'LMS_405': 'Discussion forum closed',
    'LMS_406': 'Live session not found',
    'LMS_407': 'Integration error',
    'LMS_408': 'File upload failed',
    'LMS_409': 'File too large',
    'LMS_410': 'Unsupported file format',
    
    # Library (501-599)
    'LIBRARY_501': 'Book not found',
    'LIBRARY_502': 'No copies available',
    'LIBRARY_503': 'Borrowing limit reached',
    'LIBRARY_504': 'Overdue items exist',
    'LIBRARY_505': 'Fine not paid',
    'LIBRARY_506': 'Reservation failed',
    'LIBRARY_507': 'Item already reserved',
    'LIBRARY_508': 'Digital resource access denied',
    
    # HR (601-699)
    'HR_601': 'Employee not found',
    'HR_602': 'Leave balance insufficient',
    'HR_603': 'Leave request overlaps',
    'HR_604': 'Payroll processing failed',
    'HR_605': 'Contract expired',
    'HR_606': 'Performance review not found',
    
    # Analytics (701-799)
    'ANALYTICS_701': 'Metric not found',
    'ANALYTICS_702': 'Report generation failed',
    'ANALYTICS_703': 'Insufficient data',
    'ANALYTICS_704': 'Invalid date range',
    'ANALYTICS_705': 'Export failed',
}


def get_error_message(code):
    """Get error message for a given error code"""
    return ERROR_CODES.get(code, ERROR_CODES['CORE_000'])


def is_valid_error_code(code):
    """Check if error code is valid"""
    return code in ERROR_CODES
