#!/usr/bin/env python3
"""Fetch the lab mailbox back over IMAP, plain and (optionally) TLS.

    python3 fetch_mail.py           # plain IMAP on 127.0.0.1:1143
    python3 fetch_mail.py --tls     # IMAPS on 127.0.0.1:1993

The TLS mode accepts the lab's self-signed certificate without
verification — the right shortcut for a loopback lab, and the wrong
one anywhere else.
"""
import argparse
import imaplib
import ssl
import sys

USER = "bob@example.org"
PASSWORD = "lab-password-123"

parser = argparse.ArgumentParser()
parser.add_argument("--tls", action="store_true", help="use IMAPS (port 1993)")
args = parser.parse_args()

if args.tls:
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE  # self-signed lab certificate
    mailbox = imaplib.IMAP4_SSL("127.0.0.1", 1993, ssl_context=context)
else:
    mailbox = imaplib.IMAP4("127.0.0.1", 1143)

print("server greeting:", mailbox.welcome.decode(errors="replace"))
mailbox.login(USER, PASSWORD)
print("login OK as", USER)

typ, data = mailbox.select("INBOX")
count = int(data[0])
print(f"INBOX selected: {count} message(s)")

typ, data = mailbox.fetch("1", "(RFC822)")
raw = data[0][1]
print("--- message 1, exactly as stored ---")
print(raw.decode(errors="replace"))

mailbox.logout()
print("logout OK")
sys.exit(0)
