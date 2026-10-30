# Running It Day to Day

**Outcome: the five-minute weekly round
— queue, log, updates, backup — that
keeps a small mail server boring, which
is the highest state a mail server can
achieve.** Chapters 4 to 11 built the
machine. This one keeps it trusted,
because with mail the standing is the
product: a server nobody has vouched
for lately is a server drifting towards
someone's spam folder.

## Look at the queue

The queue is the server's conscience.
Healthy, it is empty or nearly — mail
passes through in seconds. Letters
*sitting* in it are letters failing:

```bash
sudo postqueue -p
```

```text
Mail queue is empty
```

—that is the lab's answer and the one
you want. A queue that grows names its
reasons in the same listing (a
destination refusing, a DNS failure, a
full disk at the other end). Postfix
retries on its own schedule and gives
up after days, bouncing the letter to
its sender; your job is only to notice
*patterns* — everything stuck for one
domain is information about that
domain, everything stuck for everyone
is information about you. The emergency
verbs are few: `sudo postsuper -d
<queue-id>` deletes one poison letter,
`sudo postqueue -f` asks for an
immediate retry of all of them. The lab
never needed either; a healthy queue
is the norm this chapter exists to
protect.

## Read a little log

Five minutes, one file — the mail log
(`/var/log/mail.log` on a distribution
install, or `journalctl -u postfix`):

```bash
grep -E "status=(sent|bounced|deferred)" /var/log/mail.log | tail
```

You are not reading for pleasure; you
are learning what your server's
*normal* looks like, so that abnormal
is visible the week it happens: a burst
of `bounced`, deliveries to users you
do not recognise, or the auth log's
`imap-login: Disconnected (auth
failed…)` repeated a hundred times from
one address — the sound of someone
guessing passwords, and Fail2Ban's cue
(chapter 9) if you set it up.

## Keep the machine patched and backed up

Mail servers are internet-facing and
handle hostile input by design; security
updates are not optional homework. Let
the distribution's unattended-upgrades
handle them, and read the reboot it
occasionally wants as part of the rent.

Backups, happily, are this design's
reward: **all the mail is files.** Every
letter is one file in a Maildir,
copyable while the server runs, and a
backup of three things is a backup of
the whole service: the Maildir folders,
the two configuration trees
(`/etc/postfix`, `/etc/dovecot`,
including the users file), and the TLS
keys. Restore is the reverse — install
the packages, put the files back, start
the services. The Backups guide in this
series covers the general discipline
(3-2-1, and testing a restore before
you need it); mail asks only that its
three folders be inside whatever
discipline you already keep.

## Mind the scoreboard

Once a month, ask the network how you
look, in the places receivers actually
check: your address against the public
blocklists (a `dig` of your reversed
address against `zen.spamhaus.org`
answering "not listed" is the healthy
result), your DMARC reports (chapter
10) still showing your own mail
passing, and your PTR and A records
still agreeing. None of this is
tooling; all of it is the price of the
promise from chapter 1. Servers do not
lose their standing in a day. They lose
it in a month of nobody looking — and
the looking is five minutes.
