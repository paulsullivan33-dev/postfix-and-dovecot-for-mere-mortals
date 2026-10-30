# What a Mail Server Is

**Outcome: you can follow one letter
from the moment it is sent to the
moment it is read, and name which
program did each part of the carrying.**
Every mail system on earth, from a
bedroom server to a giant provider,
splits the work the same three ways.
Learn the split once and the rest of
this guide is just plumbing.

## The three jobs

**Sending and receiving between
servers is SMTP's job.** The **Simple
Mail Transfer Protocol** is how one
mail server talks to another: a short
text conversation ("I have a letter
from Alice, for Bob — do you take mail
for Bob?") followed by the letter
itself. The program that does this is
the **MTA**, the Mail Transfer Agent.
In this guide the MTA is Postfix. When
you press Send in a mail app, your app
usually hands the letter to an MTA as
the first hop of the same journey.

**Keeping the letter safe until it is
read is the mailbox's job.** The letter
ends its SMTP journey stored on the
receiving server's disk. In this guide
it is stored as a **Maildir**: a folder
per user, one file per letter, so
ordinary file tools — `ls`, `cp`, a
backup program — can see and copy the
mail exactly as it lies.

**Handing stored mail to the reader is
IMAP's job.** The **Internet Message
Access Protocol** is how a mail app
logs in, lists what is waiting, and
fetches letters — leaving them on the
server, so a phone, a laptop and a
tablet all see the same mailbox. The
program that does this is the **MDA**
in the broad sense used here, and in
this guide it is Dovecot. (There is an
older fetch protocol, POP3, which
downloads letters and usually deletes
them from the server. Dovecot can do
it; this guide teaches IMAP, because
keeping one true copy on the server is
what most people now expect.)

Your mail **app** — Thunderbird, a
phone client, a webmail page — is the
**MUA**, the Mail User Agent. It is the
only part a non-technical user ever
sees, and it is the part this guide
does *not* install: the server is the
same whatever app you read with.

## The journey of one letter

Alice, on some other network, writes to
`bob@example.org`. Her server looks up
**DNS** — the internet's address book —
for `example.org`, and finds an **MX
record** naming the machine that takes
its mail: `mail.example.org`. Her
server opens a connection to that
machine on **port 25** and holds the
SMTP conversation. Postfix checks that
the letter really is for one of its
domains and one of its users, accepts
it, stamps a **Received** header on it,
and puts it in its **queue**. Within a
second the queue hands it to the
delivery program, which writes it as a
new file in Bob's Maildir and leaves
the queue empty. The letter now sits
still — possibly for days — until Bob's
phone connects to Dovecot on **port
993**, logs in with Bob's password
inside an encrypted **TLS** connection,
and asks what is new. Dovecot checks
the password, opens the same Maildir
Postfix wrote to, and hands the letter
back. Bob reads it, never knowing two
programs and one folder shook hands
underneath.

Outgoing mail is the same journey in
reverse: Bob's app submits the letter
to Postfix (on the **submission** port,
587, with his password proving it is
really him), Postfix looks up the MX
record of the destination domain, and
delivers the letter to that server on
port 25.

## The check

No software yet — this is a thinking
chapter. The check is that you can
answer, without looking: *a letter for
Bob arrives. Which protocol brings it
to your building (SMTP), which program
takes it in (Postfix), where does it
wait (a Maildir on disk), and which
program and protocol hand it to Bob's
phone (Dovecot, IMAP)?* If that chain
is clear, chapter 2 names the parts
inside each program.

## The rule, early

Email is one of the oldest open
networks: any server may knock on any
other's port 25, and the system runs on
trust backed by reputation. That is
why the README's rule — never an open
relay, never mail people did not ask
for — is not etiquette but engineering:
servers that break it are identified
and refused by the rest of the network,
automatically and without appeal.
Chapter 12 returns to keeping that
trust once you have earned it.
