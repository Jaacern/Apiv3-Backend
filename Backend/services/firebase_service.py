from firebase_config import db, auth

def create_user(user_data):
    try:
        db.child("users").push(user_data)
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def get_users():
    return db.child("users").get().val()

def authenticate_user(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        return user
    except Exception as e:
        print(f"Error: {e}")
        return None
