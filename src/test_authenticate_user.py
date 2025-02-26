from utils.firebase import authenticate_user

identifier = "test@example.com"  # Pode ser email ou username
password_correct = "senha123"  # Substituir pela senha usada no cadastro
password_wrong = "senha_errada"

user_correct = authenticate_user(identifier, password_correct)
user_wrong = authenticate_user(identifier, password_wrong)

print(f"Autenticação com senha correta: {user_correct}")
print(f"Autenticação com senha errada: {user_wrong}")
