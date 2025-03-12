import smtplib
from email.mime.text import MIMEText
from utils.config import SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, EMAIL_SENDER, EMAIL_DESTINATION

subject = "Assunto do Email"
body = "Este é o corpo da mensagem de texto"
sender = EMAIL_SENDER # Seu endereço de email do Outlook
recipients = [EMAIL_DESTINATION]  # Endereços de email dos destinatários
password = SMTP_PASSWORD  # Sua senha específica para o aplicativo

def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP('smtp-mail.outlook.com', 587) as smtp_server:
        smtp_server.ehlo()  # Pode ser omitido
        smtp_server.starttls()  # Protege a conexão
        smtp_server.ehlo()  # Pode ser omitido
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Mensagem enviada!")

send_email(subject, body, sender, recipients, password)