import logging
from datetime import datetime
from typing import List, Dict, Optional

logging.basicConfig(level=logging.INFO)


class User:
    """Represents a system user."""

    def __init__(self, user_id: int, name: str, email: str):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.created_at = datetime.now()

    def to_dict(self):
        return {
            "id": self.user_id,
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at.isoformat()
        }


class UserRepository:
    """Simulates database operations."""

    def __init__(self):
        self.users = {}

    def add_user(self, user: User):
        if user.user_id in self.users:
            raise ValueError("User already exists")
        self.users[user.user_id] = user
        logging.info(f"User {user.name} added")

    def get_user(self, user_id: int) -> Optional[User]:
        return self.users.get(user_id)

    def delete_user(self, user_id: int):
        if user_id not in self.users:
            raise KeyError("User not found")
        del self.users[user_id]

    def list_users(self) -> List[User]:
        return list(self.users.values())


class EmailService:
    """Handles email notifications."""

    def send_welcome_email(self, user: User):
        logging.info(f"Sending welcome email to {user.email}")

    def send_password_reset(self, user: User):
        logging.info(f"Password reset email sent to {user.email}")


class UserService:
    """Business logic layer."""

    def __init__(self, repository: UserRepository, email_service: EmailService):
        self.repository = repository
        self.email_service = email_service

    def register_user(self, user_id: int, name: str, email: str):
        user = User(user_id, name, email)
        self.repository.add_user(user)
        self.email_service.send_welcome_email(user)
        return user

    def remove_user(self, user_id: int):
        user = self.repository.get_user(user_id)
        if not user:
            raise Exception("Cannot delete non-existing user")
        self.repository.delete_user(user_id)
        logging.info(f"User {user.name} removed")

    def reset_password(self, user_id: int):
        user = self.repository.get_user(user_id)
        if not user:
            raise Exception("User not found")
        self.email_service.send_password_reset(user)


class ReportGenerator:
    """Generates user reports."""

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def generate_summary(self) -> Dict:
        users = self.repository.list_users()

        return {
            "total_users": len(users),
            "generated_at": datetime.now().isoformat(),
            "users": [u.to_dict() for u in users]
        }

    def print_report(self):
        report = self.generate_summary()

        print("=" * 50)
        print("USER REPORT")
        print("=" * 50)
        print(f"Generated At : {report['generated_at']}")
        print(f"Total Users : {report['total_users']}")

        for user in report["users"]:
            print(
                f"{user['id']} | {user['name']} | {user['email']}"
            )


def validate_email(email: str) -> bool:
    """Simple email validation."""
    return "@" in email and "." in email


def calculate_average_age(users: List[Dict]) -> float:
    ages = [u["age"] for u in users if "age" in u]

    if not ages:
        return 0

    return sum(ages) / len(ages)


def main():
    repository = UserRepository()
    email_service = EmailService()
    user_service = UserService(repository, email_service)

    user_service.register_user(1, "Alice", "alice@example.com")
    user_service.register_user(2, "Bob", "bob@example.com")
    user_service.register_user(3, "Charlie", "charlie@example.com")

    report = ReportGenerator(repository)
    report.print_report()

    print(validate_email("admin@test.com"))

    avg = calculate_average_age([
        {"name": "Alice", "age": 22},
        {"name": "Bob", "age": 24},
        {"name": "Charlie", "age": 26},
    ])

    print("Average Age:", avg)


if __name__ == "__main__":
    main()
