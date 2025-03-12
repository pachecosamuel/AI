import smtplib, ssl
from email.mime.text import MIMEText
from utils.config import EMAIL_DESTINATION, EMAIL_SENDER, SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, EMAIL_SENDER, EMAIL_DESTINATION

port = SMTP_PORT  # For SSL
smtp_server = SMTP_SERVER
smtp_sender = EMAIL_SENDER
smpt_destination = EMAIL_DESTINATION
password = SMTP_PASSWORD
message = """\
Subject: Hi there

This message is sent from Python."""

# Create a secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(smtp_sender, password)
    server.sendmail(smtp_sender, smpt_destination, message)





# # Definição dos dados
# subject = "Assunto do Email"
# body = "Este é o corpo da mensagem de texto"
# sender = EMAIL_SENDER
# recipients = [EMAIL_DESTINATION]
# password = SMTP_PASSWORD

# send_email(subject, body, sender, recipients, password)
# def send_email(subject, body, sender, recipients, password):
#     msg = MIMEText(body)
#     msg['Subject'] = subject
#     msg['From'] = sender
#     msg['To'] = ', '.join(recipients)

#     # Cria o contexto SSL para criptografia segura
#     context = ssl.create_default_context()

#     with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp_server:
#         smtp_server.ehlo()
#         smtp_server.starttls(context=context)  # Usa o contexto SSL
#         smtp_server.ehlo()
#         smtp_server.login(sender, password)
#         smtp_server.sendmail(sender, recipients, msg.as_string())

#     print("Mensagem enviada!")

# # Definição dos dados
# subject = "Assunto do Email"
# body = "Este é o corpo da mensagem de texto"
# sender = EMAIL_SENDER
# recipients = [EMAIL_DESTINATION]
# password = SMTP_PASSWORD

# send_email(subject, body, sender, recipients, password)
