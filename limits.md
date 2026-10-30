# Limits

What this two-program stack does not
do, stated plainly. Some of it the lab
met directly; the rest is the shape of
the tools, and none of it is a defect —
it is the boundary of what you built.

**Deliverability is earned, not
installed.** Chapters 4 to 11 produce a
correct server. Nothing produces a
*trusted* one except time, correct DNS
(chapter 10), and mail that recipients
gladly receive. Large providers weigh a
new, small, residential-looking sender
with open suspicion; your first weeks
of mail may land in spam folders at the
big names while your records are
perfect. This is the ecosystem working
as designed against strangers, and the
only cure is the patience of chapter 12.

**No spam filter is running.** The
server of this guide accepts or refuses
mail by address and syntax — it does
not judge content. Every serious
deployment adds a filter (Rspamd and
SpamAssassin are the usual names,
wired into Postfix as helpers) and this
guide ran neither: what arrives in your
inbox from the internet will include
whatever the internet sends, judged by
nobody. Consider chapter 9's TLS and
this absence together before you invite
the public in.

**Authenticated sending is configured,
not demonstrated.** Readers can *read*
with a password (chapters 7 and 8,
verified). Having Postfix accept
*outgoing* mail from your own apps —
the submission port, with Dovecot's
auth as the password check (the SASL
bridge) — is a standard, documented
configuration the lab did not exercise
on loopback: its clients were trusted
by address instead. On a real server,
that bridge is not optional decoration;
without it your own phone cannot send
through your server from a café.

**Mailboxes are machine users.**
Chapter 11's model — one system
account per mailbox, Dovecot's list
mirroring it — is honest up to a
household or a small team. Virtual
users, quotas, and per-domain
administration exist in both programs
and are documented by them, but they
are another guide's worth of machinery
and this one does not pretend
otherwise.

**No webmail, no calendar, no groups.**
What you built moves and stores
letters. A web page to read them in, a
calendar that accepts invitations, a
mailing list with subscribers — each
is a further program with its own
guide-sized setup. Dovecot will happily
serve the mail side of all of them.

**One machine, one point of failure.**
The server is a single box: disk,
power and provider are all singular,
and strangers' servers will retry a
down server for days but not forever.
A backup MX (a second machine that
holds mail for you) is the classic
answer and is, again, documented rather
than demonstrated here.

**The loopback caveat, once more.**
Every verified transcript in the lab
ran on one machine talking to itself,
with shifted ports and example names.
The internet-facing steps — real port
25, registrar DNS, a signed
certificate, DKIM signing, other
servers' acceptance — are correct as
taught but were, by the sandbox's
nature, *taught*, not *run*. The
criteria page keeps the two lists
separate so no reader has to guess
which is which.
