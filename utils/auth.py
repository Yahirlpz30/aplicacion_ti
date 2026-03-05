import pandas as pd
import hashlib


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def check_login(user, password):

    users = pd.read_excel("data/user-pass.xlsx")

    hashed = hash_password(password)

    user_row = users[
        (users["user"] == user) &
        (users["password"] == hashed)
    ]

    return not user_row.empty
