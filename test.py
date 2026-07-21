import logging
from datetime import datetime
from typing import List, Dict, Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class User:
    """Represents a system user."""

    def __init__(self, user_id: int, name: str, email: str, role: str):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.role = role
        self.created_at = datetime.now()
        self.last_login = None
        self.active = True

    def login(self):
        self.last_login = datetime.now()

    def deactivate(self):
        self.active = False

    def activate(self):
        self.active = True

    def to_dict(self):
        return {
            "id": self.user_id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "active": self.active,
            "created_at": self.created_at.isoformat(),
            "last_login": self.last_login.isoformat() if self.last_login else None
        }


class UserRepository:
    """Handles user storage."""

    def __init__(self):
        self.users = {}

    def add_user(self, user: User):
        if user.user_id in self.users:
            raise ValueError("User ID already exists")
        self.users[user.user_id] = user
        logging.info(f"Added user {user.name}")

    def get_user(self, user_id: int) -> Optional[User]:
        return self.users.get(user_id)

    def update_email(self, user_id: int, new_email: str):
        user = self.get_user(user_id)

        if not user:
            raise ValueError("User not found")

        user.email = new_email
        logging.info(f"Updated email for {user.name}")

    def delete_user(self, user_id: int):
        if user_id not in self.users:
            raise KeyError("User not found")

        del self.users[user_id]
        logging.info(f"Deleted user {user_id}")

    def list_users(self):
        return list(self.users.values())

    def search_by_role(self, role: str):
        return [u for u in self.users.values() if u.role.lower() == role.lower()]


class NotificationService:
    """Handles notifications."""

    def send_welcome_email(self, user: User):
        logging.info(f"Welcome email sent to {user.email}")

    def send_password_reset(self, user: User):
        logging.info(f"Password reset sent to {user.email}")

    def send_account_deactivated(self, user: User):
        logging.info(f"Account deactivated notification sent to {user.email}")


class AuditService:
    """Stores application logs."""

    def __init__(self):
        self.logs = []

    def record(self, action: str):
        entry = {
            "action": action,
            "time": datetime.now().isoformat()
        }
        self.logs.append(entry)

    def show_logs(self):
        print("\nAUDIT LOGS")
        print("-" * 40)

        for log in self.logs:
            print(f"{log['time']} -> {log['action']}")


class UserService:
    """Business logic."""

    def __init__(
        self,
        repository: UserRepository,
        notification: NotificationService,
        audit: AuditService
    ):
        self.repository = repository
        self.notification = notification
        self.audit = audit

    def register_user(self, user_id, name, email, role):

        if "@" not in email:
            raise ValueError("Invalid email")

        user = User(user_id, name, email, role)

        self.repository.add_user(user)
        self.notification.send_welcome_email(user)

        self.audit.record(f"Registered {name}")

        return user

    def login(self, user_id):

        user = self.repository.get_user(user_id)

        if not user:
            raise Exception("User not found")

        user.login()

        self.audit.record(f"{user.name} logged in")

    def deactivate_user(self, user_id):

        user = self.repository.get_user(user_id)

        if not user:
            raise Exception("User not found")

        user.deactivate()

        self.notification.send_account_deactivated(user)

        self.audit.record(f"{user.name} deactivated")

    def reset_password(self, user_id):

        user = self.repository.get_user(user_id)

        if not user:
            raise Exception("User not found")

        self.notification.send_password_reset(user)

        self.audit.record(f"Password reset for {user.name}")

    def update_email(self, user_id, email):
        self.repository.update_email(user_id, email)
        self.audit.record(f"Updated email of user {user_id}")


class ReportGenerator:
    """Generates reports."""

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def generate_summary(self):

        users = self.repository.list_users()

        active = len([u for u in users if u.active])
        inactive = len(users) - active

        roles = {}

        for user in users:
            roles[user.role] = roles.get(user.role, 0) + 1

        return {
            "total_users": len(users),
            "active_users": active,
            "inactive_users": inactive,
            "roles": roles,
            "generated_at": datetime.now().isoformat()
        }

    def print_report(self):

        report = self.generate_summary()

        print("\n========== USER REPORT ==========")
        print("Generated :", report["generated_at"])
        print("Total Users :", report["total_users"])
        print("Active Users :", report["active_users"])
        print("Inactive Users :", report["inactive_users"])

        print("\nUsers By Role")

        for role, count in report["roles"].items():
            print(f"{role} : {count}")


def validate_email(email: str):

    if "@" not in email:
        return False

    if "." not in email:
        return False

    return True


def calculate_average_age(users: List[Dict]):

    ages = []

    for user in users:
        if "age" in user:
            ages.append(user["age"])

    if len(ages) == 0:
        return 0

    return sum(ages) / len(ages)


def main():

    repository = UserRepository()

    notification = NotificationService()

    audit = AuditService()

    service = UserService(repository, notification, audit)

    service.register_user(
        1,
        "Alice",
        "alice@example.com",
        "Admin"
    )

    service.register_user(
        2,
        "Bob",
        "bob@example.com",
        "Employee"
    )

    service.register_user(
        3,
        "Charlie",
        "charlie@example.com",
        "Manager"
    )

    service.login(1)

    service.update_email(
        2,
        "bob_new@example.com"
    )

    service.reset_password(3)

    service.deactivate_user(2)

    report = ReportGenerator(repository)

    report.print_report()

    admins = repository.search_by_role("Admin")

    print("\nAdmins")

    for admin in admins:
        print(admin.name)

    average = calculate_average_age([
        {"name": "Alice", "age": 24},
        {"name": "Bob", "age": 28},
        {"name": "Charlie", "age": 30}
    ])

    print("\nAverage Age :", average)

    audit.show_logs()


if __name__ == "__main__":
    main()
