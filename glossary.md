# Glossary

**Alias** — a forwarding instruction:
mail for one name is delivered to
another. Kept in `/etc/aliases`,
compiled with `postalias`, and the
mechanism that makes `postmaster` a
person instead of a void.

**DKIM** — DomainKeys Identified Mail.
The sending server signs parts of each
outgoing letter with a private key;
receivers fetch the public half from
DNS (`<selector>._domainkey`) and check
nothing was altered on the way.

**DMARC** — Domain-based Message
Authentication, Reporting and
Conformance. A DNS record that ties
SPF and DKIM together: it states what
receivers should do when a letter
claiming your domain fails those
checks (`none`, `quarantine`,
`reject`), and where to send reports
about it.

**Envelope** — the two addresses a
transfer actually acts on — `MAIL FROM`
and `RCPT TO` in the SMTP conversation.
They can differ from the letter's own
`From:` and `To:` headers, which are
part of the letter and shown to humans.

**IMAP** — Internet Message Access
Protocol. How a mail app logs in,
lists, reads and organises mail that
stays on the server. Ports 143 (with
STARTTLS) and 993 (always encrypted).

**IMAPS** — IMAP over an implicit TLS
connection, port 993. The connection is
encrypted from the first byte.

**Maildir** — a mail storage format:
one folder per mailbox with `tmp`,
`new` and `cur` inside, one file per
letter, flags encoded in filenames.
The format Postfix and Dovecot agree
on in this guide.

**MDA / MTA / MUA** — the three agents.
The **MUA** (Mail User Agent) is the
app a person reads with. The **MTA**
(Mail Transfer Agent — Postfix) moves
mail between servers over SMTP. The
delivery and serving side (Dovecot,
and Postfix's `local`) is often grouped
as the **MDA**, the Mail Delivery
Agent.

**MX record** — the DNS record naming
which machines accept a domain's mail,
with a preference number; lower is
tried first.

**Open relay** — a server that will
forward mail from anyone, to anyone.
The cardinal sin of mail operation:
found within hours, abused at scale,
and blocklisted without appeal.

**passwd-file** — Dovecot's name for a
plain file of mail users and password
hashes, in the shape of the Unix
password file. This guide's user list.

**POP3** — the older fetch protocol:
download the letters, usually deleting
the server's copies. Dovecot can serve
it; this guide teaches IMAP instead.

**PTR record** — reverse DNS: the
record that answers, for an IP address,
what its name is. Set by the address's
owner (your provider), checked by
receivers against the server's name.

**Queue** — Postfix's on-disk waiting
room for letters in transit, and the
first place to look when mail is stuck.
Inspected with `postqueue -p`.

**Queue ID** — the tracking number
Postfix assigns each letter on
acceptance ("queued as …"). Every log
line about that letter carries it.

**Relay** — to accept a letter for a
domain that is not yours and pass it
onward. Legitimate for your own users
and networks; forbidden fruit for
everyone else.

**SASL** — the framework by which
Postfix borrows Dovecot's password
checking, so mail apps can prove who
they are when *sending* through the
submission port.

**Smarthost** — a bigger server you
hand all outgoing mail to, instead of
delivering directly. A respectable
answer to a poor sending address.

**SMTP** — Simple Mail Transfer
Protocol. The text conversation by
which servers pass letters to each
other (port 25), and by which apps
submit them (port 587).

**SPF** — Sender Policy Framework. A
DNS TXT record listing which machines
may send for a domain; receivers check
the connecting machine against it.

**STARTTLS** — the upgrade spell: a
plain connection (IMAP 143, SMTP 25 or
587) that converts itself into a TLS
connection before anything private —
a password, a letter — crosses it.

**Submission** — port 587, where mail
apps hand outgoing letters to their own
server, with a login. Distinct from
port 25, which is server-to-server and
expects no password.

**TLS** — Transport Layer Security, the
encryption (and, with a verified
certificate, the identity proof) under
HTTPS, IMAPS and STARTTLS alike.
