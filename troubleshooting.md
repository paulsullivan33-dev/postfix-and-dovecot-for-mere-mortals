# Troubleshooting

The failures the lab met for real, plus
the standard ones every new mail
operator meets, in roughly the order
you will meet them. Transcripts:
`postfix-and-dovecot-lab/transcripts/`
— `t06-failures-and-alias.txt` unless
another is named.

## Mail to a real person is refused: "User unknown"

```text
550 5.1.1 <carol@example.org>: Recipient address rejected: User unknown in local recipient table
```

Postfix refuses, during the
conversation, any local address that is
neither a system user nor an alias.
That refusal is correct behaviour (the
lab provoked it deliberately). If the
person is real, one of three things is
missing: the system account, the alias
line (plus `postalias` after editing —
chapter 11), or the domain in
`mydestination` — without the third,
Postfix does not consider the address
local at all and the error changes its
shape entirely. `postconf mydestination`
and `doveadm user <the address>` divide
the suspects between them.

## IMAP says the password is wrong — and it isn't

```text
[UNAVAILABLE] Temporary authentication failure.
```

That was the lab's first login exactly
(transcript `t03` keeps the run made
after the fix). The
password was right; the **auth process
could not read the users file** — the
folder above it denied it entry, and
Dovecot's own log said so in as many
words: *passwd-file … Permission denied
(euid=…dovecot) … missing +x perm*.
Lessons that generalise: Dovecot's log
names the real cause more often than
the client's error does; a *temporary*
failure means the server failed, not
the password; and the permissions that
matter are the whole path — every
folder above the file needs its
traverse bit for the user the auth
service runs as. The plain
`[AUTHENTICATIONFAILED]` answer, by
contrast, really does mean the password
(or the hash in the file) is wrong:
re-mint it with `doveadm pw` and
compare the line character by character.

## A letter was accepted but never arrived

Follow its queue ID through the log
(chapters 2 and 6). The line where the
story stops is the culprit's name:
`smtpd` accepted and nothing more means
the queue is stalled (`postqueue -p`
will show it, with its reason);
`local` reporting a bounce with a
permission error means the recipient's
home or Maildir is not writable by its
owner — the lab's first delivery died
exactly there, because a folder *above*
the home directory would not let the
delivery agent pass. Two programs
agreeing on the Maildir path (chapter
7's check) rules out the other classic:
delivered perfectly, somewhere nobody
reads.

## `postfix check` will not stay silent

Warnings name files: ownership,
permissions, a map whose database is
older than its text. The commonest is
the last — an edited `aliases` or map
file without its rebuild (`postalias`).
Treat every warning as a sentence to
read, not noise to suppress: the check
is the cheapest audit your server will
ever get, and chapter 5's loop — edit,
check, `postconf -n` — is the whole
discipline.

## Other servers refuse or folder your mail

Work the list of chapter 10 in order:
MX published and answering; PTR set and
matching the A record; SPF passing
(`dig TXT` and read your own record as
a stranger would); DKIM signing and
verifying (the reports in your DMARC
mailbox show both, per sender); DMARC
not yet tightened past what your
sending justifies. Then the harder
truth of chapter 13: a new small
server's reputation is built in weeks,
and there is no configuration line for
hurry. Check the public blocklists for
your address before assuming malice —
a predecessor at a recycled address may
have left you their history, and most
lists have a delisting door for exactly
that.

## Port 25 connects to nothing

From outside: is anything listening
(`ss -tlnp | grep :25` on the server)?
Is the firewall's door open (the UFW
guide in this series covers the
grammar)? And the question from
chapter 3 that outranks both: does
your provider block port 25 on your
plan? Test from a machine that is not
yours — a friend's shell account, a
rented instance — because a router's
view from inside its own network lies
about exactly this.
