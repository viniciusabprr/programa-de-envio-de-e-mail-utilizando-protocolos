import email
from email.header import decode_header
import imaplib
import smtplib


# CONFIGURAÇÕES DE CONTA E MENSAGEM

remetente = "Risktds@gmail.com"
destinatario = "viniciusabpr@gmail.com"
conteudo = "Subject: Teste do Script\n\nMensagem de teste enviada com sucesso!"

Usuario = remetente
Password = "nciw ysew xpuf uwjn"


 #  ENVIANDO O E-MAIL (SMTP)

servidor_email = None
try:
    servidor_email = smtplib.SMTP("smtp.gmail.com", 587, timeout=20)
    servidor_email.starttls()
    servidor_email.login(remetente, Password)
    
    # componentes: de quem, para quem e o conteúdo
    servidor_email.sendmail(remetente, destinatario, conteudo)
    print("E-mail enviado com sucesso!\n")

except Exception as e:
    print(f"Erro ao enviar email: {e}\n")

finally:
    if servidor_email is not None:
        try:
            servidor_email.quit()
        except:
            pass


 # LENDO O ÚLTIMO E-MAIL (IMAP)

servidor_recebe_email = None
try:
    servidor_recebe_email = imaplib.IMAP4_SSL("imap.gmail.com", 993, timeout=20)
    servidor_recebe_email.login(Usuario, Password)

    # Seleciona a caixa de entrada (inbox) em modo leitura
    status, total = servidor_recebe_email.select(mailbox="inbox", readonly=True)

    # Busca todos os e-mails
    respostas, idDosEmails = servidor_recebe_email.search(None, 'ALL')

    # Transforma os IDs em uma lista do Python
    lista_ids = idDosEmails[0].split()

    if not lista_ids:
        print("Nenhum e-mail encontrado na caixa de entrada.")
    else:
        # Pega o ID do último e-mail recebido (o mais recente)
        ultimo_id = lista_ids[-1]
        print(f"Buscando detalhes do e-mail de ID: {ultimo_id.decode()}")

        # Baixa os dados brutos da mensagem pelo ID
        status, dados = servidor_recebe_email.fetch(ultimo_id, "(RFC822)")
        conteudo_bruto = dados[0][1]

        # Converte os bytes em um objeto legível de e-mail
        msg = email.message_from_bytes(conteudo_bruto)

        # 1. Pega e decodifica o Assunto (Subject)
        assunto, codificacao = decode_header(msg.get("Subject", "(Sem assunto)"))[0]
        if isinstance(assunto, bytes):
            assunto = assunto.decode(codificacao or "utf-8", errors="replace")

        # 2. Pega quem enviou
        de_quem = msg.get("From")

        print(f"\nDe: {de_quem}")
        print(f"Assunto: {assunto}")

        # 3. Pega o texto/corpo da mensagem
        corpo = ""
        if msg.is_multipart():
            for parte in msg.walk():
                if parte.get_content_type() == "text/plain":
                    corpo = parte.get_payload(decode=True).decode(errors="replace")
                    break
        else:
            corpo = msg.get_payload(decode=True).decode(errors="replace")

        print(f"Corpo da mensagem:\n{corpo.strip()}")

except Exception as e:
    print(f"Erro ao ler e-mail via IMAP: {e}")

finally:
    # Fecha a pasta e faz o logout limpo da conexão
    if servidor_recebe_email is not None:
        try:
            servidor_recebe_email.close()
        except:
            pass
        servidor_recebe_email.logout()
        print("\nConexão IMAP encerrada.")