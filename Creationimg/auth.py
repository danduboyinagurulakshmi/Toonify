import bcrypt
from db import users_collection

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)

def create_user(name, email, password):
    if users_collection.find_one({"email": email}):
        return False, "User already exists"
    hashed_pw = hash_password(password)
    users_collection.insert_one({
        "name": name,
        "email": email,
        "password": hashed_pw
    })
    return True, "Account created successfully"

def login_user(email, password):
    user = users_collection.find_one({"email": email})
    if not user:
        return False, "User not found"
    if verify_password(password, user["password"]):
        return True, user["name"]
    return False, "Invalid password"