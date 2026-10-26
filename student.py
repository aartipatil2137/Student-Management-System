
class Student:
    """Represents a student and validates student details."""

    def __init__(self, name, email, phone, course, marks):
        self.id = None
        self.name = name
        self.email = email
        self.phone = phone
        self.course = course
        self.marks = marks

    def validate(self):
        errors = []

        if not self.name:
            errors.append("Name is required.")

        if not self.email or "@" not in self.email:
            errors.append("Enter a valid email address.")

        if not self.course:
            errors.append("Course is required.")

        if self.marks == "":
            errors.append("Marks are required.")
        else:
            try:
                value = float(self.marks)

                if not 0 <= value <= 100:
                    errors.append("Marks must be between 0 and 100.")
                else:
                    self.marks = value

            except (ValueError, TypeError):
                errors.append("Marks must be a number between 0 and 100.")

        return errors