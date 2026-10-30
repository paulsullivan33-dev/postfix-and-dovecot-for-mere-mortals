# The Moving Parts

**Outcome: when something misbehaves,
you can guess which of the half-dozen
small programs inside Postfix and
Dovecot is responsible — and look in
the right log line.** Neither tool is
one big program. Both are a supervised
family of small ones, each with a
single job. You will never configure
most of them, but knowing their names
turns a frightening log into a story.

## Inside Postfix

Postfix's **master** program starts
first and supervises the rest, starting
and stopping them as mail comes and
go. Which services exist, and on which
ports, is written in one file:
`master.cf`. The cast you will meet:

- **smtpd** — the doorman. It holds the
  SMTP conversation with the outside
  world, checks the sender and
  recipient against your rules, and
  either refuses the letter on the spot
  or accepts it and answers with a
  **queue ID** — the letter's tracking
  number, which appears in every later
  log line about it.
- **cleanup** — the clerk. It stamps
  the headers Postfix adds (including
  the `Received` line and a `Message-Id`
  if one is missing) and puts the
  letter in the queue.
- **qmgr** — the queue manager. It owns
  the **queue**, a set of folders on
  disk, and decides which delivery
  program gets each waiting letter, and
  when to retry one that failed.
- **local** — the postman for this
  machine's own users. It resolves
  **aliases** (chapter 11) and writes
  the letter into the user's Maildir.
- **smtp** — the outgoing postman. It
  carries letters to other servers,
  doing the DNS lookup and the port-25
  conversation from the other side.
- **postlogd** — the scribe, catching
  log lines from the chatted services
  and writing them to the mail log.

Every other Postfix behaviour — the
machine's name, the domains it serves,
the storage format — lives in the
second file, `main.cf`, written as
plain `name = value` lines. Postfix
ships with hundreds of settings; this
guide changes about eight, and chapter
5 walks through each one.

## Inside Dovecot

Dovecot's master process supervises
its own family:

- **imap-login** — the postroom door.
  It listens on the IMAP ports (143, or
  993 for the always-encrypted form),
  runs the TLS handshake, and takes the
  login attempt.
- **auth** — the guard behind the door.
  It checks the name and password
  against whatever list you configure —
  this guide uses a small **passwd-file**
  — and answers yes or no. It never
  touches mail.
- **imap** — the clerk for one logged-in
  user. Started fresh for each reader,
  running *as* that user, it lists,
  fetches, moves and deletes letters in
  the user's Maildir, and nothing
  outside it.

Alongside them stands **`doveadm`**,
the administrator's command-line tool:
it does not serve mail, it inspects
and manages — who the users are, what
is in a mailbox, how much space it
takes. Chapter 7 uses it as the check
that Dovecot sees the world the way
you think it does.

## The folder they agree on

The two programs never talk to each
other directly. They agree on one
thing: the **Maildir**. A Maildir is a
folder with three subfolders — `tmp`,
`new` and `cur` — holding one file per
letter. Postfix's postman writes a new
letter into `new`. Dovecot's clerk
reads from `new` and `cur`, moving a
letter to `cur` and renaming it as its
flags change (read, replied, flagged —
the letters after the comma in the
filename *are* the flags). The format
is deliberately boring: no database,
no locking puzzles, safe for two
programs to share, and every letter
recoverable with `cp` if the worst
happens. Its older rival, **mbox** —
all letters in one big file — is named
here only so you can decline it:
sharing one file between two programs
is exactly as fragile as it sounds.

## The check

Run nothing yet; this chapter's check
is a map you can test against reality
later. After chapters 6 and 7 you will
be able to open the mail log and match
its lines to names above — `smtpd`
accepting, `qmgr` dispatching, `local`
delivering (transcript
`postfix-and-dovecot-lab/transcripts/t02-smtp-delivery.txt`
shows all three for one letter). If a
log line names a program this chapter
has not introduced, it is one of the
specialists this guide leaves alone —
and the glossary will usually cover it.
