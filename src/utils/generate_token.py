from security import create_access_token
from datetime import timedelta

token = create_access_token({"sub": "usuario_teste"}, expires_delta=timedelta(minutes=30))
print(token)
