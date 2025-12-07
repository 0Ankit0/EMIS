// Student module - Zod schemas and inferred types
import * as z from "zod";

// ============================================
// STUDENT
// ============================================
export const studentFormSchema = z.object({
    registration_number: z.coerce.number().optional().nullable(),
    roll_number: z.string().optional().nullable(),
    first_name: z.string().min(1, "First name is required"),
    middle_name: z.string().optional(),
    last_name: z.string().min(1, "Last name is required"),
    date_of_birth: z.string().min(1, "Date of birth is required"),
    gender: z.string().min(1, "Gender is required"),
    email: z.string().email("Invalid email address"),
    phone_number: z.string().min(1, "Phone number is required"),
    address: z.string().min(1, "Address is required"),
    city: z.string().min(1, "City is required"),
    state: z.string().min(1, "State is required"),
    postal_code: z.string().min(1, "Postal code is required"),
    country: z.string().min(1, "Country is required"),
    enrollment_date: z.string().min(1, "Enrollment date is required"),
});

export type StudentFormValues = z.infer<typeof studentFormSchema>;

export type Student = StudentFormValues & {
    id: number;
    ukid: string;
    full_name: string;
    enrollment_count: number;
    is_active: boolean;
    is_deleted: boolean;
    deleted_at?: string;
    created_at: string;
    updated_at: string;
};

export type StudentCreateInput = StudentFormValues;
export type StudentUpdateInput = Partial<StudentFormValues> & { is_active?: boolean };

// ============================================
// ENROLLMENT
// ============================================
export const enrollmentFormSchema = z.object({
    program: z.string().min(1, "Program is required"),
    semester: z.string().min(1, "Semester is required"),
    enrollment_date: z.string().min(1, "Enrollment date is required"),
    status: z.enum(["enrolled", "completed", "dropped", "repeated"]),
});

export type EnrollmentFormValues = z.infer<typeof enrollmentFormSchema>;

export type Enrollment = EnrollmentFormValues & {
    id: string;
    student: string;
    student_name?: string;
    created_at: string;
    updated_at: string;
};

export type EnrollmentCreateInput = EnrollmentFormValues & { student: string };
export type EnrollmentUpdateInput = Partial<EnrollmentFormValues>;

// ============================================
// ACADEMIC RECORD
// ============================================
export const academicRecordFormSchema = z.object({
    semester: z.string().min(1, "Semester is required"),
    gpa: z.coerce.number().min(0).max(4, "GPA must be between 0 and 4"),
    total_credits: z.coerce.number().min(0, "Credits must be positive"),
    remarks: z.string().optional(),
});

export type AcademicRecordFormValues = z.infer<typeof academicRecordFormSchema>;

export type AcademicRecord = {
    id: string;
    student: string;
    student_name?: string;
    semester: string;
    gpa: string; // API returns as string
    total_credits: number;
    remarks?: string;
    created_at: string;
    updated_at: string;
};

export type AcademicRecordCreateInput = {
    student: string;
    semester: string;
    gpa: string;
    total_credits: number;
    remarks?: string;
};

export type AcademicRecordUpdateInput = Partial<AcademicRecordCreateInput>;

// ============================================
// SUBJECT RESULT
// ============================================
export const subjectResultFormSchema = z.object({
    subject_name: z.string().min(1, "Subject name is required"),
    marks_obtained: z.string().optional(),
    maximum_marks: z.string().optional(),
    grade: z.string().optional(),
    credit_hours: z.coerce.number().min(1, "Credit hours is required"),
    semester: z.string().min(1, "Semester is required"),
    attempt_type: z.enum(["regular", "re_exam"]),
});

export type SubjectResultFormValues = z.infer<typeof subjectResultFormSchema>;

export type SubjectResult = SubjectResultFormValues & {
    id: string;
    student: string;
    student_name?: string;
    created_at: string;
    updated_at: string;
};

export type SubjectResultCreateInput = SubjectResultFormValues & { student: string };
export type SubjectResultUpdateInput = Partial<SubjectResultFormValues>;

export const resultsImportFormSchema = z.object({
    file: z.any().refine((file) => file instanceof File, "File is required"),
});

export type ResultsImportFormValues = z.infer<typeof resultsImportFormSchema>;

// ============================================
// GUARDIAN
// ============================================
export const guardianFormSchema = z.object({
    first_name: z.string().min(1, "First name is required"),
    last_name: z.string().min(1, "Last name is required"),
    relationship: z.string().min(1, "Relationship is required"),
    email: z.string().email("Invalid email address"),
    phone_number: z.string().min(1, "Phone number is required"),
    address: z.string().min(1, "Address is required"),
});

export type GuardianFormValues = z.infer<typeof guardianFormSchema>;

export type Guardian = GuardianFormValues & {
    id: string;
    student: string[];
    student_names?: string[];
    created_at: string;
    updated_at: string;
};

export type GuardianCreateInput = GuardianFormValues & { student: string[] };
export type GuardianUpdateInput = Partial<GuardianFormValues> & { student?: string[] };

// ============================================
// DOCUMENT
// ============================================
export const documentTypeEnum = z.enum([
    "id_proof", "birth_cert", "transcript", "photo", "medical", "transfer", "other"
]);

export const documentUploadFormSchema = z.object({
    document_type: documentTypeEnum,
    file: z.any().refine((file) => file instanceof File, "File is required"),
});

export type DocumentUploadFormValues = z.infer<typeof documentUploadFormSchema>;

export type Document = {
    id: string;
    student: string;
    student_name?: string;
    document_type: z.infer<typeof documentTypeEnum>;
    file: string;
    is_verified: boolean;
    verified_by?: string;
    verified_at?: string;
    uploaded_at: string;
};

export type DocumentUploadInput = {
    student: string;
    document_type: z.infer<typeof documentTypeEnum>;
    file: File;
};

// ============================================
// FILTERS
// ============================================
export interface StudentFilters {
    search?: string;
    is_active?: boolean;
    enrollment_date_from?: string;
    enrollment_date_to?: string;
    city?: string;
    state?: string;
}

export interface EnrollmentFilters {
    student?: string;
    program?: string;
    semester?: string;
    status?: string;
}

export interface AcademicRecordFilters {
    student?: string;
    semester?: string;
}

export interface SubjectResultFilters {
    student?: string;
    semester?: string;
    subject_name?: string;
    attempt_type?: string;
}

// ============================================
// CONSTANTS
// ============================================
export const GRADE_OPTIONS = [
    { value: "A+", label: "A+" },
    { value: "A", label: "A" },
    { value: "B+", label: "B+" },
    { value: "B", label: "B" },
    { value: "C+", label: "C+" },
    { value: "C", label: "C" },
    { value: "D", label: "D" },
    { value: "F", label: "F" },
    { value: "I", label: "Incomplete" },
    { value: "W", label: "Withdrawn" },
] as const;

export const GENDER_OPTIONS = [
    { value: "Male", label: "Male" },
    { value: "Female", label: "Female" },
    { value: "Other", label: "Other" },
] as const;

export const ENROLLMENT_STATUS_OPTIONS = [
    { value: "enrolled", label: "Enrolled" },
    { value: "completed", label: "Completed" },
    { value: "dropped", label: "Dropped" },
    { value: "repeated", label: "Repeated" },
] as const;

export const ATTEMPT_TYPE_OPTIONS = [
    { value: "regular", label: "Regular" },
    { value: "re_exam", label: "Re-examination" },
] as const;

export const DOCUMENT_TYPE_OPTIONS = [
    { value: "id_proof", label: "ID Proof" },
    { value: "birth_cert", label: "Birth Certificate" },
    { value: "transcript", label: "Academic Transcript" },
    { value: "photo", label: "Photograph" },
    { value: "medical", label: "Medical Certificate" },
    { value: "transfer", label: "Transfer Certificate" },
    { value: "other", label: "Other" },
] as const;
