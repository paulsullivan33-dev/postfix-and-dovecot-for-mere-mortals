# Postfix, the Front Door

**Outcome: a Postfix configuration you
can read aloud — what the machine is
called, which mail it accepts as its
own, who is allowed to relay through
it, and where delivered letters land —
and `postfix check` agreeing with it.**
Almost everything Postfix does is
decided by one file, `/etc/postfix/main.cf`,
written as plain `name = value` lines.
This chapter is that file, eight
settings at a time.

## The configuration

```text
myhostname = mail.example.org
mydomain = example.org
myorigin = $mydomain
mydestination = $myhostname, localhost.$mydomain, localhost, $mydomain
```

Four lines about identity.
**`myhostname`** is the machine's full
name — the name it greets other servers
with, and the name in its `Received`
stamps. **`mydomain`** is the domain it
serves. **`myorigin`** is the domain
stamped on mail that leaves without one
(locally generated mail, mostly).
**`mydestination`** is the important
one: the list of domains Postfix
considers *final* — mail addressed to
these is delivered to local users,
never relayed onward. A domain missing
from this list is a domain whose mail
your server will refuse or forward; a
domain wrongly on it is mail you will
silently swallow. Read it twice.

```text
mynetworks = 127.0.0.0/8
inet_interfaces = all
relayhost =
```

Three lines about trust. **`mynetworks`**
names the addresses allowed to hand
Postfix mail for *anywhere* — the
relay privilege. The lab set it to the
loopback range alone, `127.0.0.0/8`:
only the machine itself. On a real
server you add your own network if you
must, and not one address more — an
over-wide `mynetworks` is precisely
what "open relay" means, and the
internet finds them within hours.
**`inet_interfaces`** says which of the
machine's addresses to listen on (`all`
for a real server; the lab used the
loopback only). **`relayhost`** left
empty means "deliver outgoing mail
directly, doing the DNS lookups
yourself" — the self-hosted way; some
operators instead name a provider's
**smarthost** here and let it do the
sending, a respectable fallback if your
address's reputation is poor
(chapter 3).

```text
home_mailbox = Maildir/
```

One line about storage: deliver each
letter as a file in a `Maildir` folder
in the user's home. Chapter 2 explained
why the format matters — Dovecot will
be told to read the very same folders
in chapter 7.

The listening port lives in the other
file, `/etc/postfix/master.cf`: the
`smtp` service line is what binds port
25. (The lab's `master.cf` bound 2525
instead, and switched the chroot column
off — a distribution install manages
the chroot for you, and the lab's
extracted tree could not. Neither
change affects anything else in this
guide.)

## The check

Two commands, and both are habits worth
keeping for every future edit:

```bash
sudo postfix check
postconf -n
```

`postfix check` reads the whole
configuration and the queue folders'
ownership and permissions, and reports
problems. **Silence is success** — the
lab's run printed nothing and exited 0
(transcript
`postfix-and-dovecot-lab/transcripts/t01-postfix-check-and-config.txt`).
`postconf -n` prints every setting that
differs from the built-in default. On
the lab machine that is a short,
readable list — the eight settings
above, the aliases paths of chapter 11,
and a handful of lab-only folder paths.
If your list contains a line you cannot
explain, that line is a question to
answer before the server meets the
internet. Make an edit, run both
commands: that loop, repeated, is most
of Postfix administration.

Then start it:

```bash
sudo systemctl restart postfix
sudo postfix status
```

"The Postfix mail system is running"
is the answer you want. Chapter 6 sends
the first letter through the door you
have just built.
