# Envio e Leitura de E-mail com SMTP e IMAP

Trabalho desenvolvido para a atividade da disciplina de **Redes de Computadores**.

**Autores:** Vinícius de Abreu Pereira, Vítor Higen Marés de Souza

## O que faz

Programa em Python que:
- **Envia** e-mails via **SMTP** (`smtplib`, porta 587 com STARTTLS)
- **Lê** e-mails recebidos via **IMAP** (`imaplib`, porta 993 com SSL)

Usa o servidor do Gmail (`smtp.gmail.com` e `imap.gmail.com`).

## Antes de rodar

1. Ative a verificação em duas etapas na conta Google.
2. Gere uma **senha de app** (Conta Google → Segurança → Senhas de app).
3. Ative o IMAP no Gmail.

> A senha normal da conta não funciona (erro `535 BadCredentials`). Use a senha de app no código.

## Como executar

```bash
python enviar_email.py
python ler_email.py
```
