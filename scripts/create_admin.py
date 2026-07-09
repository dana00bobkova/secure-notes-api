from app.database import SessionLocal
from app.models import User
from app.auth.security import hash_password


db = SessionLocal()

admin_email = "admin_test@example.com"
admin_password = "Password123!"

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
print("Admin password:", admin_password)