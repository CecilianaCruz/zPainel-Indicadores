from flask import Flask, render_template, request, redirect
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

# Configuração do e-mail
EMAIL_ADDRESS = "seuemail@gmail.com"
EMAIL_PASSWORD = "suasenha"
DESTINATION_EMAIL = "destino@gmail.com"

@app.route('/')
def index():
    return '''
    <h1>Contato</h1>
    <form method="POST" action="/send-email" enctype="multipart/form-data">
        <label for="name">Seu Nome:</label><br>
        <input type="text" id="name" name="name" required><br><br>
        
        <label for="email">Seu Email:</label><br>
        <input type="email" id="email" name="email" required><br><br>
        
        <label for="subject">Assunto:</label><br>
        <input type="text" id="subject" name="subject" required><br><br>
        
        <label for="message">Mensagem:</label><br>
        <textarea id="message" name="message" required></textarea><br><br>
        
        <label for="attachment">Anexar Imagem:</label><br>
        <input type="file" id="attachment" name="attachment" accept="image/*"><br><br>
        
        <input type="submit" value="Enviar">
    </form>
    '''

@app.route('/send-email', methods=['POST'])
def send_email():
    name = request.form['name']
    sender_email = request.form['email']
    subject = request.form['subject']
    message_content = request.form['message']
    attachment = request.files['attachment']

    # Criação do e-mail
    msg = EmailMessage()
    msg['Subject'] = f"{subject} - {name}"
    msg['From'] = sender_email
    msg['To'] = DESTINATION_EMAIL
    msg.set_content(f"Nome: {name}\nEmail: {sender_email}\n\n{message_content}")

    # Adiciona o anexo se houver
    if attachment:
        attachment_data = attachment.read()
        msg.add_attachment(attachment_data, maintype='image', subtype=attachment.filename.split('.')[-1], filename=attachment.filename)

    # Envio do e-mail
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

    return '<h1>E-mail enviado com sucesso!</h1><p><a href="/">Voltar</a></p>'

if __name__ == "__main__":
    app.run(debug=True)
