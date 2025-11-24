// API Response Types
export interface APIResponse<T> {
    success: boolean;
    data?: T;
    error?: string;
    message?: string;
}

// Pagination Types
export interface PaginatedResponse<T> {
    count: number;
    next: string | null;
    previous: string | null;
    results: T[];
}

// Common Entity Types
export interface Student {
    id: number;
    student_id: string;
    first_name: string;
    last_name: string;
    email: string;
    phone: string;
    date_of_birth: string;
    gender: string;
    address: string;
    grade: string;
    section: string;
    enrollment_date: string;
    status: 'active' | 'inactive' | 'graduated';
}

export interface Attendance {
    id: number;
    student: number;
    date: string;
    status: 'present' | 'absent' | 'late' | 'excused';
    marked_by: number;
    remarks?: string;
}

export interface Fee {
    id: number;
    student: number;
    fee_type: string;
    amount: number;
    due_date: string;
    paid_date?: string;
    status: 'pending' | 'paid' | 'overdue';
    invoice_number?: string;
}

export interface Book {
    id: number;
    isbn: string;
    title: string;
    author: string;
    category: string;
    publisher: string;
    published_year: number;
    total_copies: number;
    available_copies: number;
    status: 'available' | 'unavailable';
}

export interface BookIssue {
    id: number;
    book: number;
    student: number;
    issue_date: string;
    due_date: string;
    return_date?: string;
    status: 'issued' | 'returned' | 'overdue';
    fine?: number;
}

export interface Exam {
    id: number;
    name: string;
    course: number;
    date: string;
    duration: string;
    total_marks: number;
    passing_marks: number;
    status: 'scheduled' | 'ongoing' | 'completed';
}

export interface Grade {
    id: number;
    exam: number;
    student: number;
    marks_obtained: number;
    grade: string;
    remarks?: string;
}

export interface Employee {
    id: number;
    employee_id: string;
    first_name: string;
    last_name: string;
    email: string;
    phone: string;
    department: string;
    position: string;
    hire_date: string;
    salary: number;
    status: 'active' | 'inactive';
}

export interface Course {
    id: number;
    code: string;
    name: string;
    description: string;
    credits: number;
    instructor: number;
    semester: string;
    status: 'active' | 'inactive';
}

// Form Input Types
export interface CreateStudentInput {
    student_id: string;
    first_name: string;
    last_name: string;
    email: string;
    phone: string;
    date_of_birth: string;
    gender: string;
    address: string;
    grade: string;
    section: string;
}

export interface MarkAttendanceInput {
    student_id: number;
    date: string;
    status: 'present' | 'absent' | 'late' | 'excused';
    remarks?: string;
}

export interface CreateFeeInput {
    student_id: number;
    fee_type: string;
    amount: number;
    due_date: string;
}

export interface IssueBookInput {
    book_id: number;
    student_id: number;
    due_date: string;
}

// API Error Types
export class APIError extends Error {
    constructor(
        message: string,
        public statusCode?: number,
        public response?: any
    ) {
        super(message);
        this.name = 'APIError';
    }
}

export class ValidationError extends APIError {
    constructor(message: string, public errors: Record<string, string[]>) {
        super(message, 400);
        this.name = 'ValidationError';
    }
}

export class AuthenticationError extends APIError {
    constructor(message: string = 'Authentication required') {
        super(message, 401);
        this.name = 'AuthenticationError';
    }
}

export class AuthorizationError extends APIError {
    constructor(message: string = 'Permission denied') {
        super(message, 403);
        this.name = 'AuthorizationError';
    }
}

export class NotFoundError extends APIError {
    constructor(message: string = 'Resource not found') {
        super(message, 404);
        this.name = 'NotFoundError';
    }
}
