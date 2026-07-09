import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)


class Student:
    """Represents a student and their academic information."""

    def __init__(self, student_id, name, age, department, email):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.department = department
        self.email = email
        self.marks = {}

    def add_mark(self, subject, marks):
        """Add marks for a subject."""
        self.marks[subject] = marks

    def update_mark(self, subject, marks):
        """Update marks of an existing subject."""
        if subject in self.marks:
            self.marks[subject] = marks

    def delete_mark(self, subject):
        """Delete subject marks."""
        self.marks.pop(subject, None)

    def calculate_average(self):
        """Calculate average marks."""
        if not self.marks:
            return 0
        return sum(self.marks.values()) / len(self.marks)

    def get_grade(self):
        """Return grade based on average marks."""
        avg = self.calculate_average()

        if avg >= 90:
            return "A+"
        elif avg >= 80:
            return "A"
        elif avg >= 70:
            return "B"
        elif avg >= 60:
            return "C"
        return "F"

    def to_dict(self):
        """Convert student object to dictionary."""
        return {
            "id": self.student_id,
            "name": self.name,
            "age": self.age,
            "department": self.department,
            "email": self.email,
            "marks": self.marks,
        }


class StudentManager:
    """Handles all student-related operations."""

    def __init__(self):
        self.students = {}

    def add_student(self, student):
        if student.student_id in self.students:
            raise ValueError("Student already exists")

        self.students[student.student_id] = student
        logging.info(f"Added student {student.name}")

    def remove_student(self, student_id):
        if student_id in self.students:
            del self.students[student_id]
            logging.info(f"Removed Student ID {student_id}")

    def student_exists(self, student_id):
        return student_id in self.students

    def update_department(self, student_id, department):
        if student_id not in self.students:
            return False

        self.students[student_id].department = department
        return True

    def search_student(self, keyword):
        result = []

        for student in self.students.values():
            if keyword.lower() in student.name.lower():
                result.append(student)

        return result

    def get_student(self, student_id):
        return self.students.get(student_id)

    def list_students(self):
        return list(self.students.values())

    def total_students(self):
        return len(self.students)

    def average_of_department(self, department):
        averages = []

        for student in self.students.values():
            if student.department == department:
                averages.append(student.calculate_average())

        if not averages:
            return 0

        return sum(averages) / len(averages)

    def department_wise_students(self, department):
        """Return all students in a department."""
        return [
            student
            for student in self.students.values()
            if student.department == department
        ]


class ReportGenerator:
    """Generates different reports."""

    def __init__(self, manager):
        self.manager = manager

    def generate_student_report(self, student_id):
        student = self.manager.get_student(student_id)

        if not student:
            return None

        return {
            "Name": student.name,
            "Department": student.department,
            "Email": student.email,
            "Average": student.calculate_average(),
            "Grade": student.get_grade(),
        }

    def department_summary(self):
        summary = {}

        for student in self.manager.list_students():
            dept = student.department
            summary.setdefault(dept, 0)
            summary[dept] += 1

        return summary

    def topper(self):
        students = self.manager.list_students()

        if not students:
            return None

        return max(
            students,
            key=lambda s: s.calculate_average()
        )

    def generate_full_report(self):
        """Generate report of all students."""
        reports = []

        for student in self.manager.list_students():
            reports.append(self.generate_student_report(student.student_id))

        return reports


class FileStorage:
    """Handles saving and loading student data."""

    @staticmethod
    def save(filename, manager):
        data = []

        for student in manager.list_students():
            data.append(student.to_dict())

        try:
            with open(filename, "w") as file:
                json.dump(data, file, indent=4)

            logging.info("Data saved successfully")

        except Exception as e:
            logging.error(e)

    @staticmethod
    def load(filename):
        manager = StudentManager()

        try:
            with open(filename) as file:
                data = json.load(file)

                for item in data:
                    student = Student(
                        item["id"],
                        item["name"],
                        item["age"],
                        item["department"],
                        item["email"],
                    )

                    for subject, mark in item["marks"].items():
                        student.add_mark(subject, mark)

                    manager.add_student(student)

        except FileNotFoundError:
            logging.warning("Student data file not found")

        return manager


def validate_marks(mark):
    """Validate marks."""
    return 0 <= mark <= 100


def create_sample_data(manager):
    s1 = Student(1, "Alice", 20, "CSE", "alice@example.com")
    s1.add_mark("Math", 95)
    s1.add_mark("Python", 91)

    s2 = Student(2, "Bob", 21, "ISE", "bob@example.com")
    s2.add_mark("Math", 82)
    s2.add_mark("Python", 78)

    s3 = Student(3, "Charlie", 22, "CSE", "charlie@example.com")
    s3.add_mark("Math", 87)
    s3.add_mark("Python", 92)

    manager.add_student(s1)
    manager.add_student(s2)
    manager.add_student(s3)


def export_statistics(manager):
    """Export overall statistics."""
    return {
        "generated_at": datetime.now().isoformat(),
        "total_students": manager.total_students(),
        "cse_average": manager.average_of_department("CSE"),
        "ise_average": manager.average_of_department("ISE"),
    }


def main():
    manager = StudentManager()

    create_sample_data(manager)

    report = ReportGenerator(manager)

    print("\nDepartment Summary")
    print(report.department_summary())

    topper = report.topper()

    if topper:
        print("\nTopper")
        print(topper.name, topper.calculate_average())

    print("\nStudent Report")
    print(report.generate_student_report(1))

    print("\nAll Reports")
    print(report.generate_full_report())

    FileStorage.save("students.json", manager)

    stats = export_statistics(manager)

    print("\nStatistics")
    print(stats)


if __name__ == "__main__":
    main()
