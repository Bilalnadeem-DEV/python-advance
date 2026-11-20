from fastapi import APIRouter, HTTPException

from app.schemas.user_schema import UserBase, UserResponse

router = APIRouter()

# Temporary database
users = []

# Auto increment ID
user_id_counter = 1


# 1. CREATE USER
@router.post("/users", response_model=UserResponse)
def create_user(user: UserBase):

    global user_id_counter

    new_user = {
        "id": user_id_counter,
        "name": user.name,
        "age": user.age,
        "email": user.email,
        "message": "User created successfully"
    }

    users.append(new_user)

    user_id_counter += 1

    return new_user


# 2. GET ALL USERS
@router.get("/users", response_model=list[UserResponse])
def get_users():

    return users


# 3. GET USER BY ID
@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):

    for user in users:

        if user["id"] == user_id:
            return user

    raise HTTPException(
        status_code=404,
        detail="User not found"
    )


# 4. UPDATE USER
@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, updated_user: UserBase):

    for user in users:

        if user["id"] == user_id:

            user["name"] = updated_user.name
            user["age"] = updated_user.age
            user["email"] = updated_user.email

            return {
                **user,
                "message": "User updated successfully"
            }

    raise HTTPException(
        status_code=404,
        detail="User not found"
    )


# 5. DELETE USER
@router.delete("/users/{user_id}")
def delete_user(user_id: int):

    for index, user in enumerate(users):

        if user["id"] == user_id:

            deleted_user = users.pop(index)

            return {
                "message": "User deleted successfully",
                "user": deleted_user
            }

    raise HTTPException(
        status_code=404,
        detail="User not found"
    )