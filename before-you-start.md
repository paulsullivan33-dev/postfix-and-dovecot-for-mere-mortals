# Before You Start

**Outcome: a straight answer — from
yourself — to whether your machine,
your network connection and your
domain can run a mail server at all,
before you install anything.** Mail is
the most honest self-hosting project:
the software is the easy half. The
other half is standing — your address's
permission to speak, and the network's
willingness to listen. This chapter is
where this guide earns its keep, by
talking some readers out of it.

## What you need

**A domain you control.** Not a
subdomain someone lends you — a domain
whose **DNS** records you can edit,
because chapter 10 has you publish
half a dozen of them. In this guide the
domain is `example.org` and the server
is `mail.example.org`. Any registrar
will do; what matters is that adding
records is a thing you can do on a
Tuesday evening, not a support ticket.

**A machine that stays on.** Mail
servers keep no office hours: if your
server is asleep when another server
tries to deliver, that server will
retry for a while (typically days) and
then give up and bounce the letter.
An old desktop, a small home server or
a rented virtual machine all qualify.
It needs very little power — this
entire guide's stack serves a household
from a single modest core.

**A stable public address, and port 25
open both ways.** This is the step
where home connections often fail, and
it is better to learn it now:

- Many home internet contracts give you
  an address that *changes*. Sending
  mail from a wandering address is
  miserable: the DNS records of chapter
  10 cannot follow it fast enough. A
  static address, or a rented virtual
  machine that has one, is the usual
  answer.
- Many providers **block port 25** —
  outgoing, incoming, or both — on
  home plans, because it was the spam
  era's favourite door. No port 25, no
  mail server: other servers cannot
  reach you, and you cannot reach them.
  Some providers unblock it on request;
  some never do. Ask, or test, before
  you build.
- You will need to ask your provider to
  set a **reverse DNS** (PTR) record for
  your address, naming your server.
  Chapter 10 explains why receiving
  servers check it. If the provider
  will not, expect large providers to
  refuse your outgoing mail.

**An hour, and then five minutes a
week.** The build in chapters 4 to 9 is
an evening at most. Chapter 12 is the
recurring price: updates, a glance at
the queue and the logs, working
backups. Readers who will not pay the
five minutes should not start; an
unmaintained mail server becomes other
people's problem, and then a blocklist
entry.

## The honest alternatives

Running your own mail is a choice, not
an obligation, and for many people the
right answer is a hosted mailbox on
their own domain — every big provider,
and several small privacy-minded ones,
will host `you@example.org` for a few
units of currency a month, and their
deliverability teams are better staffed
than you. Choose this guide's path
because you want the mail itself on
your disk, under your keys, with no
per-mailbox bill — and because you find
the machinery interesting. Both are
good reasons. "It must be cheaper" is
not: priced against two evenings and a
year of five-minute weeks, it rarely is.

## The check

You can state, in one sentence each:
your domain and where its DNS is
edited; the machine and whether it
stays on; your public address and
whether it is static; whether port 25
is open (or who you will ask); and who
can set your PTR record. Five answers,
no maybes. Chapters 4 to 9 will build
the server on the lab's loopback twin
of this setup, so you can rehearse the
whole build safely even while an answer
is still a support ticket away.
