"""
Script untuk membuat admin pertama kali di Firebase.
Run ini hanya jika admin belum ada di Firebase.
"""

import getpass

from auth.auth_service import FirebaseAuthService


def create_first_admin():
    """Buat admin pertama di Firebase."""
    print("=" * 50)
    print("CREATE FIRST ADMIN IN FIREBASE")
    print("=" * 50)

    # Reuse the same service layer as the main app so account creation follows
    # the same Firebase configuration and database schema.
    service = FirebaseAuthService()

    email = input("\nAdmin email: ").strip()
    if not email:
        print("\nERROR: Admin email wajib diisi.")
        return

    password = getpass.getpass("Admin password: ").strip()
    if not password:
        print("\nERROR: Admin password wajib diisi.")
        return

    try:
        result = service.create_admin(email, password)

        if result.get("status") == "success":
            print("\nSUCCESS")
            print("Admin created successfully.")
            print(f"User ID: {result.get('user_id')}")
            print("Admin account is ready to use.")
        else:
            print(f"\nERROR: {result.get('message')}")

    except Exception as exc:
        error_msg = str(exc)

        if "EMAIL_EXISTS" in error_msg or "email already exists" in error_msg.lower():
            print("\nWARNING: Admin already exists.")
            print(f"Admin with email {email} is already registered.")
        else:
            print(f"\nERROR: {error_msg}")
            print("\nTips:")
            print("   1. Check Firebase connection")
            print("   2. Verify firebase_service_account.json")
            print("   3. Check Firebase project settings")

    print("\n" + "=" * 50)


if __name__ == "__main__":
    create_first_admin()
