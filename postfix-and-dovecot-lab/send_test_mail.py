#!/usr/bin/env python3
"""Send one test message to the lab mail server over SMTP.

Run it while the lab Postfix is listening (127.0.0.1, port 2525):

    python3 send_test_mail.py

It prints the whole SMTP conversation, so the transcript shows the
greeting, the envelope, and the server's queue receipt.
"""
import smtplib
import sys

HOST, PORT = "127.0.0.1", 2525
SENDER = "alice@example.org"
RECIPIENT = "bob@example.org"

MESSAGE = """\
From: Alice <alice@example.org>
To: Bob <bob@example.org>
Subject: First lab letter

Hello Bob,

This letter travelled the whole lab: in through SMTP to Postfix,
delivered into your Maildir, and it is waiting for Dovecot to hand
it back over IMAP.

-- Alice
"""

with smtplib.SMTP(HOST, PORT, timeout=15) as smtp:
    smtp.set_debuglevel(1)
    smtp.sendmail(SENDER, [RECIPIENT], MESSAGE)
print("sent OK")
sys.exit(0)
