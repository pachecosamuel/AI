import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from utils.config import EMAIL_SENDER, SMTP_SERVER, SMTP_PORT, SMTP_PASSWORD


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
        return {"message": "✅ E-mail enviado com sucesso!"}
        
    except Exception as e:
        print(f"❌ Erro ao enviar e-mail: {e}")
        raise RuntimeError(f"Erro ao enviar e-mail: {e}")

