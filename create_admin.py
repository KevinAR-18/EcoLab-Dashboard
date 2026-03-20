"""
Script untuk membuat admin pertama kali di Firebase
Run ini HANYA jika admin belum ada di Firebase
"""
from auth_service import TrialLoginService

def create_first_admin():
    """Buat admin pertama di Firebase"""
    print("=" * 50)
    print("CREATE FIRST ADMIN IN FIREBASE")
    print("=" * 50)

    # Init service
    service = TrialLoginService()

    # Default admin credentials
    email = "admin@ecolab.com"
    password = "admin123"

    print(f"\n📧 Email: {email}")
    print(f"🔑 Password: {password}")

    try:
        # Coba create admin
        result = service.create_admin(email, password)

        if result.get("status") == "success":
            print("\n✅ SUCCESS!")
            print(f"✓ Admin created successfully!")
            print(f"✓ User ID: {result.get('user_id')}")
            print(f"\n🎯 You can now login with:")
            print(f"   Email: {email}")
            print(f"   Password: {password}")
        else:
            print(f"\n❌ ERROR: {result.get('message')}")

    except Exception as e:
        error_msg = str(e)

        # Cek jika admin sudah ada
        if "EMAIL_EXISTS" in error_msg or "email already exists" in error_msg.lower():
            print("\n⚠️  WARNING: Admin already exists!")
            print(f"✓ Admin with email {email} already created")
            print(f"\n🎯 You can login with:")
            print(f"   Email: {email}")
            print(f"   Password: {password}")
        else:
            print(f"\n❌ ERROR: {error_msg}")
            print("\n💡 Tips:")
            print("   1. Check Firebase connection")
            print("   2. Verify firebase_service_account.json")
            print("   3. Check Firebase project settings")

    print("\n" + "=" * 50)

if __name__ == "__main__":
    create_first_admin()
