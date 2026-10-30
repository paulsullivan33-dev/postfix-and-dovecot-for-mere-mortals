# TLS and Passwords

**Outcome: logins that travel encrypted
— a certificate on the postroom door, a
fetch over IMAPS to prove it works, and
passwords stored as hashes worth
stealing-resisting.** An unencrypted
IMAP login sends the mailbox password
readably across whatever networks lie
between the reader and your server.
Chapter 8's plain login was a lab
convenience on a loopback wire nobody
else could see. On any real network it
would be negligence, and this chapter
is the fix.

## The certificate

TLS needs the server to prove its name
with a **certificate**: a small signed
document saying "the key for
`mail.example.org` is this one". Two
ways to get it:

**For practice, sign your own.** One
command mints a **self-signed**
certificate, good for a year:

```bash
openssl req -x509 -newkey rsa:2048 -nodes -days 365 \
  -subj "/CN=mail.example.org" \
  -keyout key.pem -out cert.pem
```

The lab did exactly this (transcript
`t00`), and transcript
`postfix-and-dovecot-lab/transcripts/t04-imaps-tls-fetch.txt`
shows the payoff and the price in one
glance: `openssl s_client` reports
*Protocol version: TLSv1.3*, *Peer
certificate: CN = mail.example.org* —
and *Verification error: self-signed
certificate*. The encryption is fully
real; the *identity* is only your own
word for it. Any client can be told to
accept it (the lab's fetch script did,
deliberately, for loopback only), but
strangers' mail apps will warn, loudly
and correctly.

**For production, have it signed.**
**Let's Encrypt** issues real
certificates, free, to anyone who can
prove they control the domain — the
`certbot` tool does it in minutes and
renews automatically. This is the
certificate a public server should
carry, for Dovecot and Postfix alike.
The lab could not demonstrate the
issuance — a loopback machine controls
no public domain — so the step is
described here from the tool's
documentation, not presented as run.
The DNS guide in this series covers
the domain-control background.

## Turning it on

Dovecot needs three lines (in
`10-ssl.conf` on a packaged install):

```text
ssl = yes
ssl_cert = </etc/dovecot/cert.pem
ssl_key = </etc/dovecot/key.pem
```

(The `<` is Dovecot's own syntax for
"read the value from this file".) With
those set, the imaps listener on 993
serves TLS, and port 143 offers
STARTTLS. Two more settings are worth
their lines on a public server:
`ssl_min_protocol = TLSv1.2`, refusing
ancient protocol versions, and
`disable_plaintext_auth = yes`, which
makes the plain login of chapter 8
impossible until the connection is
encrypted — passwords then never cross
any wire unreadably.

The lab's proof was the same letter,
fetched the same way, through the
encrypted door (`fetch_mail.py --tls`):
same greeting minus STARTTLS — the
connection is *already* encrypted — same
login, same letter, over TLS 1.3.

Postfix takes the same certificate for
its own STARTTLS on ports 25 and 587;
the settings (`smtpd_tls_cert_file`,
`smtpd_tls_key_file`,
`smtpd_tls_security_level = may` for
incoming, and the submission service's
stricter `encrypt`) live in `main.cf`
and `master.cf`. Opportunistic TLS on
port 25 deserves one honest sentence:
most server-to-server mail is encrypted
in transit nowadays *because* servers
offer it, but the offering side cannot
force a stranger to accept — `may` is
the realistic setting, and the
glossary's STARTTLS entry says why.

## Passwords, briefly and seriously

The passwd-file of chapter 7 stores
hashes from `doveadm pw` — SHA512-CRYPT
in this guide, a deliberately slow
one-way scrambling. Slow matters: if
the file ever leaks, each password
costs real time to guess, and a
genuinely long passphrase (four or five
random words) puts guessing out of
reach entirely. What hashing cannot
save is a password reused from
elsewhere or typed into a fake login
page — the human rules from the
Cybersecurity guide in this series
apply unchanged. And because failed
logins are the internet's background
noise, point **Fail2Ban** (this series
has a guide) at Dovecot's log: it
watches for repeated failures and
firewalls the offenders, and it takes
ten minutes to set up once this
chapter's logging exists.

## The check

From another machine — or the lab's
stand-in, `openssl`:

```bash
openssl s_client -connect mail.example.org:993 -brief
```

You want: the protocol at TLS 1.2 or
better, your server's name on the
certificate, and — for the production
certificate — **no verification
error**. Then log in with your mail
app and fetch chapter 6's letter
through 993. Encrypted, verified, and
the password never once readable on
the wire: the postroom is fit for
strangers now. What strangers still
need is directions to it — chapter 10.
