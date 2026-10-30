# Your First Delivery

**Outcome: a letter that you sent in
through the SMTP front door, found as a
file in the recipient's Maildir, with
the log lines that prove each hop.**
This is the chapter the whole front
half of the guide exists for. It uses
two people who exist only in the lab:
Alice, who sends, and Bob, who has a
mailbox here — a local user named `bob`
whose mail address is
`bob@example.org`.

## Sending the letter

Any program that speaks SMTP will do.
The lab used a short Python script —
`postfix-and-dovecot-lab/send_test_mail.py` —
because Python is on every Linux
machine and the conversation prints in
full. The shape of it, in transcript
`t02`, is the same conversation every
mail server on earth has:

```text
250-mail.example.org
250-PIPELINING
250-SIZE 10240000
...
250-8BITMIME
250 CHUNKING
```

The greeting first: `mail.example.org`
answering, with the list of things it
can do. Then the envelope — *envelope*
because these two lines, not the
letter's own `From:` and `To:` headers,
are what servers act on:

```text
mail FROM:<alice@example.org> size=269
250 2.1.0 Ok
rcpt TO:<bob@example.org>
250 2.1.5 Ok
```

Then `data`, the letter itself, a lone
dot to end it, and the receipt that
matters:

```text
250 2.0.0 Ok: queued as 202D82212BD
```

**Queued as** a queue ID: accepted,
stamped, and the server's problem now.
Everything after this moment can be
followed by searching the mail log for
that ID.

A real mail app does exactly this, plus
a password: it connects to the
submission port and authenticates first
(chapter 9 covers the encryption and
the proving-who-you-are side). The lab
skipped the password because its
Postfix trusted the loopback address
outright — its `mynetworks` was the
machine itself. Never widen that trust
to the open internet; chapter 5 said
why, and chapter 12 says it again.

## Finding the letter

One second later, three log lines tell
the whole story — accept, dispatch,
deliver:

```text
postfix/smtpd: 202D82212BD: client=localhost[127.0.0.1]
postfix/qmgr: 202D82212BD: from=<alice@example.org>, size=546, nrcpt=1 (queue active)
postfix/local: 202D82212BD: to=<bob@example.org>, relay=local, dsn=2.0.0, status=sent (delivered to maildir)
```

(`dsn=2.0.0` is the delivery status
code: 2 means success, as 5 would mean
failure — chapter 14 lives on reading
these.) And the letter itself is a
file, exactly where chapter 5 promised:

```bash
find ~/Maildir -type f
```

```text
Maildir/new/1793333836.V58I2212c0M149470.htch-runtime
```

Open it with any text tool. The top of
the file is the part Postfix added —
`Return-Path`, and the `Received`
header recording when, from where, and
under which queue ID the letter
arrived — followed by Alice's letter
untouched below. That layering is a
habit worth forming now: **headers are
the letter's travel diary**, written by
servers, and the first place to look
when mail goes somewhere unexpected.

## The check

Your version of the lab's result is:
the send ends with `250 … queued as
<an ID>`; the log shows the same ID
accepted by `smtpd`, dispatched by
`qmgr` and `status=sent` by `local`;
and a new file sits in the recipient's
`Maildir/new`. All three or it did not
happen — and if the chain breaks,
chapter 14 starts with the log line
that will tell you at which hop. The
letter is delivered. It is also, so
far, unread: chapter 7 builds the
postroom that hands it back.
