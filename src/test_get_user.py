from utils.firebase import get_user_by_email_or_username

email = "test@example.com"
username = "test_user"

user_by_email = get_user_by_email_or_username(email)
user_by_username = get_user_by_email_or_username(username)

print(f"Usuário pelo email ({email}):", user_by_email)
print(f"Usuário pelo username ({username}):", user_by_username)
