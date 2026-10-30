# Postfix & Dovecot for Mere Mortals

Almost everyone's mail lives on someone
else's computer: you write a letter, it
travels to a company's servers, and it
waits there until the other person's
mail program asks for it. **Your own
mail server** does the same job with the
landlord left out. Two programs divide
the work between them. **Postfix** is
the front door: it takes letters in from
the network, hands local ones to the
right mailbox, and sends yours out.
**Dovecot** is the postroom: it guards
the stored mail and hands it to your
mail app when you log in and ask. The
mail itself sits on your disk, in
ordinary files you can list, read and
back up.

This guide builds that server, piece by
piece, and proves each piece before
moving on. By the end you will have a
machine that accepts mail for your
domain over **SMTP**, stores it in
**Maildir** folders, and serves it back
over **IMAP** with **TLS** encryption —
plus the **DNS** records (MX, SPF, DKIM,
DMARC) that persuade the rest of the
internet your server is who it claims
to be.

One honest warning before any of that,
because it shapes everything else in
this guide: **a mail server is a promise
you keep in public.** Other servers
decide whether to trust yours, and they
keep score. A badly run server — an
open relay that forwards anything for
anyone, a spam cannon, a machine that
falls over and loses letters — does not
just fail its owner; it pollutes the
network for everyone and gets its
address blocked, sometimes for good.
So this guide's rule, stated once and
applied throughout: **never run an open
relay, and only ever send mail to people
who asked for it.** If that is not the
server you want, this is the wrong
project — and chapter 3 will help you
decide before you spend an evening on it.

The lab behind this guide ran the real
thing: **Postfix 3.8.6** and **Dovecot
2.3.21**, the current Ubuntu 24.04
packages, on one machine talking only
to itself (the loopback address,
127.0.0.1), under the example domain
`mail.example.org`. Against that stack
the lab checked the configuration with
the programs' own tools, sent a letter
in through the SMTP front door and
watched Postfix stamp it, queue it and
deliver it into a test user's Maildir,
then logged in over IMAP — plainly, and
again inside TLS — and fetched the same
letter back. It also did the rude
things on purpose: mail to a user who
does not exist (refused, 550), a wrong
IMAP password (refused), and a letter to
`postmaster`, which arrived by an alias
chain, exactly as configured.

What the lab could not do, it did not
fake. A loopback machine has no public
address, no registrar and no other mail
servers to talk to, so the DNS chapter
teaches the records properly — the same
records, with documentation addresses —
but labels them as the part **you**
publish at your registrar, and gives you
the `dig` checks to run once you have.
Sending mail out to the real internet,
and the reputation work that makes big
providers accept it, is taught the same
honest way: explained, not demonstrated.
`criteria.md` keeps the full ledger of
what was run and what was only read.

## What this guide covers

- [**What a mail server is**](what-a-mail-server-is.md) —
  the three jobs every mail system
  splits into, the journey of one
  letter, and the ports it all happens on
- [**The moving parts**](the-moving-parts.md) —
  Postfix's daemons, Dovecot's services,
  and the Maildir folder both sides agree on
- [**Before you start**](before-you-start.md) —
  what you need (a domain, a machine, a
  usable address) and the questions to
  answer honestly before installing anything
- [**Installing Postfix and Dovecot**](installing.md) —
  the two packages, the one question the
  installer asks, and the version check
  that proves both run
- [**Postfix, the front door**](postfix-the-front-door.md) —
  `main.cf` line by line: the machine's
  name, the mail it accepts, who may
  relay, and where delivered mail goes
- [**Your first delivery**](your-first-delivery.md) —
  one letter in through SMTP, watched in
  the log, and found as a file in a Maildir
- [**Dovecot, the postroom**](dovecot-the-postroom.md) —
  pointing Dovecot at the same Maildirs,
  giving it a list of users and passwords,
  and checking its work with `doveadm`
- [**Reading your mail**](reading-your-mail.md) —
  an IMAP login that fetches the letter
  back, and what to type into a real mail app
- [**TLS and passwords**](tls-and-passwords.md) —
  encrypting the postroom's door: a
  self-signed certificate for practice, a
  real one for production, and passwords
  worth storing
- [**DNS, the address book**](dns-the-address-book.md) —
  MX, SPF, DKIM and DMARC records for the
  example domain, what each one proves,
  and the checks to run after publishing
- [**Aliases and more users**](aliases-and-more-users.md) —
  `postmaster` and friends, adding a
  second mailbox, and what changes when
  addresses outgrow the machine's users
- [**Running it day to day**](running-it-day-to-day.md) —
  the queue, the logs, updates, backups of
  plain files, and the weekly five minutes
  that keep a server trusted
- [**Limits**](limits.md) — no webmail,
  no spam filter, no magic deliverability:
  what this two-program stack does not do
- [**Troubleshooting**](troubleshooting.md) —
  the 550 for a stranger, the failed
  login, the letter stuck in the queue,
  and the traps this guide's lab fell into
- [**Glossary**](glossary.md) — the
  terms, collected in one place

## What it doesn't cover

Sending bulk mail, newsletters or
marketing: different rules, different
tools, and against this guide's opening
promise. A webmail page (Roundcube and
friends are a third program, with their
own guide's worth of setup). Spam
filtering beyond naming the tools —
the lab ran none, and chapter 13 says
so. Hosting mail for hundreds of
strangers: that is an operations
business, not a home server. And
Microsoft Exchange, Google Workspace
and the other hosted suites are pointed
at as alternatives in chapter 3, not
taught.

## How to use this guide

Read chapter 1 for the model and
chapter 3 before installing anything —
mail rewards people who decide with
their eyes open. Chapters 5 to 9 build
the working server on one machine;
each ends with a check you can run, and
you should not move on until yours
matches. Chapter 10 is the one that
makes the server real to the outside
world, and it cannot be rehearsed
locally — read it twice. The lab's
transcripts live in
`postfix-and-dovecot-lab/transcripts/`;
its two small test scripts are
`postfix-and-dovecot-lab/send_test_mail.py`
and `postfix-and-dovecot-lab/fetch_mail.py`.

---

## Part of the series

This guide is one of the [For Mere Mortals](https://paulsullivan33-dev.github.io/mere-mortals/) guides: plain-language guides to the tools programmers and makers use.

Related guides:

- [DNS for Mere Mortals](https://paulsullivan33-dev.github.io/dns-for-mere-mortals/)
- [Networking for Mere Mortals](https://paulsullivan33-dev.github.io/networking-for-mere-mortals/)
- [Linux for Mere Mortals](https://paulsullivan33-dev.github.io/linux-for-mere-mortals/)
- [Fail2Ban for Mere Mortals](https://paulsullivan33-dev.github.io/fail2ban-for-mere-mortals/)

## License

The writing in this guide is licensed under [CC BY 4.0](https://github.com/paulsullivan33-dev/postfix-and-dovecot-for-mere-mortals/blob/main/LICENSE). Code examples and lab scripts are licensed under the [MIT License](https://github.com/paulsullivan33-dev/postfix-and-dovecot-for-mere-mortals/blob/main/LICENSE-CODE).
