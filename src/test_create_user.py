from utils.firebase import create_user

try:
    user = create_user(
        username="test_user",
        email="test@example.com",
        password="senha123",
        full_name="Usuário Teste"
    )
    print("Usuário criado com sucesso:", user)
except ValueError as e:
    print("Erro:", e)
