# Aliases and More Users

**Outcome: the standard addresses every
domain is expected to have —
`postmaster`, `abuse` — landing in a
real mailbox, and a second human's
mailbox added the way the first was.**
Two kinds of names live on a mail
server: mailboxes, which belong to a
person, and **aliases**, which are
forwarding instructions — "mail for X
is really for Y".

## Aliases: the forwarding book

Postfix keeps its aliases in a plain
text file, `/etc/aliases`, one per
line:

```text
postmaster: root
abuse: root
MAILER-DAEMON: postmaster
root: bob
```

Read the lab's file as a chain:
`postmaster` mail goes to the system
user `root`; so does `abuse` (the
address strangers use to report trouble
with your domain — a real address you
are expected to read, per the same
trust chapter 1 described); the
`MAILER-DAEMON` name that bounce
messages wear goes to `postmaster`; and
`root`'s own mail — the system's
notices — goes to Bob, a human who
reads mail. Every name resolves, by
following the chain, to a mailbox that
exists.

Two habits go with the file. After
every edit, rebuild its database and
re-check:

```bash
sudo postalias /etc/aliases
sudo postfix check
```

Postfix reads the compiled database
(`aliases.db`), not your text — forget
the first command and your edit is a
wish. (On a distribution install,
`newaliases` does the same job.) And
test the chain end-to-end, not by
reading it: the lab sent Alice's letter
to `postmaster@example.org` and watched
the log line

```text
to=<bob@example.org>, orig_to=<postmaster@example.org>, status=sent (delivered to maildir)
```

— the `orig_to` is the whole point of
aliases made visible (transcript
`postfix-and-dovecot-lab/transcripts/t06-failures-and-alias.txt`).
Bob's inbox count went from one letter
to two, which `doveadm mailbox status`
confirmed.

A stranger at the gates gets the
opposite treatment, and chapter 6's
setup guarantees it: an address that is
neither a user nor an alias is refused
during the SMTP conversation itself —
the lab's letter to `carol@example.org`
earned

```text
550 5.1.1 <carol@example.org>: Recipient address rejected: User unknown in local recipient table
```

Refusing early, rather than accepting
and bouncing later, is a kindness to
the whole network: a bounce to a forged
sender is spam you generated.

## Adding a mailbox

A second person — call her Carol, real
this time — is chapter 7 done twice
over. Postfix's side: nothing to do.
Its `local` postman delivers to
*system users*, so Carol needs a user
account on the machine
(`sudo adduser carol`) for her Maildir
to exist under her home — Postfix will
create the Maildir itself on the first
letter. Dovecot's side: one line in the
passwd-file, with Carol's own hash from
`doveadm pw`, her own uid, gid and home:

```text
carol@example.org:{SHA512-CRYPT}$6$...:1001:1001::/home/carol::
```

Check your work with the same two tools
as chapter 7 — `doveadm user
carol@example.org`, then a real letter
and a real login. Note the division of
labour, because it decides the next
section: Postfix asked the *system*
who Carol is; Dovecot asked *its file*.
Both lists must name her, each in its
own way.

## When the lists outgrow the machine

The setup above is right while
mailboxes and machine logins are the
same people — a household, a small
team. It stops being right when they
are not: a hundred mailboxes should not
mean a hundred shell accounts. The
grown-up shape is **virtual users**:
Postfix tables (`virtual_mailbox_maps`)
and a Dovecot userdb listing people who
exist only as mail identities, with
mail stored under one system user.
Postfix and Dovecot both document it
thoroughly. This guide names the door
and does not walk through it — the lab
ran the two-list setup, and the limits
chapter counts virtual hosting among
the things this guide describes but
does not demonstrate.
