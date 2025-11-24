import StudentFormPage from "../../new/page";

export default function EditStudentPage() {
    // In a real app, we would fetch student data here and pass it to the form
    // For now, we'll just reuse the form component which defaults to empty values
    // Ideally, StudentFormPage should accept initialValues prop
    return <StudentFormPage />;
}
