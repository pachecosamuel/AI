import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utils.config import EMAIL_SENDER, EMAIL_DESTINATION, SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD

def send_email(subject, body, recipients):
    """Envia um e-mail usando SMTP."""
    sender = EMAIL_SENDER
    password = SMTP_PASSWORD

    # Criar a mensagem de e-mail
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    msg['Subject'] = subject

    # Adicionar corpo do e-mail
    msg.attach(MIMEText(body, "html"))  # Suporte para HTML

    try:
        # Criar contexto SSL
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            server.login(sender, password)
            server.sendmail(sender, recipients, msg.as_string())
        print("✅ E-mail enviado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao enviar e-mail: {e}")

# Testando envio
send_email(
    subject="Teste de E-mail",
    body="<h1>Olá!</h1><p>Este é um e-mail de teste enviado pelo Python.</p>",
    recipients=[EMAIL_DESTINATION]
)
