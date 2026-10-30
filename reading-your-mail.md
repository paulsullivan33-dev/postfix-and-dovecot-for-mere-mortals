# Reading Your Mail

**Outcome: the letter from chapter 6,
fetched back over IMAP by a program
that logged in as Bob — the round trip
closed — and the four settings a real
mail app needs to do the same.**
Everything so far was the server's view.
This chapter is the reader's.

## The login, up close

The lab fetched with the second of its
scripts, `postfix-and-dovecot-lab/fetch_mail.py`,
built on Python's `imaplib` — again
because it shows its working. Dovecot
greets it:

```text
* OK [CAPABILITY IMAP4rev1 SASL-IR LOGIN-REFERRALS ID ENABLE IDLE LITERAL+ STARTTLS AUTH=PLAIN AUTH=LOGIN] Dovecot (Ubuntu) ready.
```

Read the greeting once, carefully; it
is the postroom's noticeboard. It names
the protocol (IMAP4rev1), the tricks it
knows (IDLE, so apps can be told about
new mail the moment it lands), and —
the important part — that it can do
**STARTTLS** (upgrade this connection
to an encrypted one) and takes logins
by `AUTH=PLAIN` and `AUTH=LOGIN`. The
script then logs in as
`bob@example.org` with the lab
password, selects the inbox, and
fetches message 1 in full:

```text
login OK as bob@example.org
INBOX selected: 1 message(s)
--- message 1, exactly as stored ---
Return-Path: <alice@example.org>
...
Subject: First lab letter
```

— and there the letter is, headers and
all, the same bytes Postfix wrote to
disk in chapter 6 (transcript
`postfix-and-dovecot-lab/transcripts/t03-imap-fetch.txt`).
Note what fetching did to the stored
file: reading marked the letter seen,
and Dovecot moved it within the Maildir
from `new` to `cur`, adding its flags
to the filename. Nothing about the
letter changed; everything about its
bookkeeping did. That is the Maildir
agreement working as designed — and it
is why chapter 7's message count, run
after a fetch, would call the letter
read, not new.

## What a real mail app needs

A mail app asks for four things, and
you now own all four answers:

- **Server**: `mail.example.org` — the
  name from chapter 5.
- **Port and security**: 993, with SSL/TLS
  (or 143 with STARTTLS — never 143 with
  "no security"; chapter 9 is next for
  a reason).
- **Username**: the full address,
  `bob@example.org` — the passwd-file's
  `username_format=%u` from chapter 7.
- **Password**: the one whose hash you
  minted with `doveadm pw`.

For sending, the same screen usually
wants the SMTP side: the same server,
port 587 (submission), STARTTLS, and
the same username and password —
Postfix must be told to accept
authenticated sending through Dovecot's
guard, a documented step this guide's
limits chapter is honest about not
demonstrating on loopback.

## The check

Yours is the round trip itself: log in
from a *different program* than the one
that delivered — ideally a different
device — and see Alice's letter listed,
open it, and watch a reply you send Bob
from outside appear in the same inbox.
When a phone and a server run by
strangers agree about a mailbox, the
postroom is done. What is left is to
lock its door properly — the subject of
the next chapter.
