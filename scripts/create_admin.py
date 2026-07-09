from getpass import getpass

from app.auth.security import hash_password
from app.database import SessionLocal
from app.models import User


db = SessionLocal()

admin_email = input("Admin email: ").strip()
admin_password = getpass("Admin password: ")

if not admin_email:
    raise ValueError("Admin email is required.")

if len(admin_password) < 8:
    raise ValueError("Admin password must be at least 8 characters.")

existing_admin = db.query(User).filter(User.email == admin_email).first()

if existing_admin:
    existing_admin.role = "admin"
    print("Existing user updated to admin.")
else:
    admin_user = User(
        email=admin_email,
        hashed_password=hash_password(admin_password),
        role="admin"
    )

    db.add(admin_user)
    print("New admin user created.")

db.commit()
db.close()

print("Admin email:", admin_email)
