# DNS, the Address Book

**Outcome: the six records that make
your server findable and believable,
ready to paste into your registrar —
and the checks to run after you do.**
Nothing in chapters 4 to 9 can be
rehearsed past this point on a private
machine: DNS is the public part. **This
chapter is therefore the documented
half of the guide.** The lab had no
registrar and no public address, so it
did not publish these records or watch
them work; they are the standard,
current practice, written with the
example domain and the documentation
address range (`203.0.113.25` stands in
for your static public address), and
the DNS guide in this series explains
the machinery underneath if any term
here is new.

You publish these where your domain's
DNS is edited — usually your registrar
or your DNS host's control panel. Every
record below is about `example.org`,
whose server is `mail.example.org`.

## The records that deliver mail

**A — the server's address.**

```text
mail.example.org.    A     203.0.113.25
```

Everything else points at the name;
this record points at the machine.

**MX — who takes this domain's mail.**

```text
example.org.         MX    10 mail.example.org.
```

The record Alice's server looked up in
chapter 1. Without it, senders fall
back to guessing `example.org` itself
is the server — publish it even if the
names coincide. The `10` is a
preference: lower wins, and a second
server (a backup MX) would take a
higher number. One server needs one
line.

**PTR — the address's name, backwards.**
Set by whoever gave you the address
(your provider, not your registrar),
the reverse lookup of `203.0.113.25`
must answer `mail.example.org` — and
the thorough receivers also check the
forward A record matches back. A
missing or generic PTR
(`cust-113.example-isp.net`) is the
single most common reason home-sent
mail is refused by large providers.

## The records that vouch for mail

These three do not move letters; they
let a receiver check a letter's claims.

**SPF — who may send for the domain.**

```text
example.org.         TXT   "v=spf1 mx -all"
```

Read it as: "mail From `example.org`
may come from the machines in its MX
records (`mx`) — and from nowhere else
(`-all` is the full stop)." Receivers
compare the connecting machine against
this list. If you also send through a
provider (a smarthost, a newsletter
tool — though chapter 1's rule applies),
its documented `include:` goes in
before the `-all`.

**DKIM — a signature on outgoing mail.**
Your server signs each outgoing letter's
headers with a private key; receivers
fetch the matching public key from DNS
and check the signature survived the
journey. You generate the key pair with
a signing tool — **OpenDKIM** is the
usual partner for Postfix — which also
writes the record for you, shaped like:

```text
mail2026._domainkey.example.org.  TXT  "v=DKIM1; k=rsa; p=MIIBIjANBg..."
```

(`mail2026` is a *selector*, a label
you choose, so keys can rotate.) The
key is long; expect the panel to split
it, and that is normal. Setting up the
signer itself is this guide's most
consequential documented-only step:
it is standard, it is well documented
by the OpenDKIM project, and the lab
did not run it — `criteria.md` says so
in as many words. Do not skip it
because it is fiddly: unsigned mail
from a small server is exactly what
spam filters are trained to distrust.

**DMARC — what to do when the checks
fail.**

```text
_dmarc.example.org.  TXT   "v=DMARC1; p=none; rua=mailto:postmaster@example.org"
```

Publish this **last**, and start with
`p=none`: it asks receivers only to
*report* (to the `rua` address — a
mailbox on your own new server) how
your mail fared against SPF and DKIM,
and to change nothing. Read the reports
for a few weeks; when they show your
real mail passing and nothing else
sending as you, tighten to
`p=quarantine`, and later `p=reject` —
the setting that tells the world
"mail failing these checks is not from
me, bin it."

## The check

DNS changes take a while to spread
(the records' TTL — an hour is common —
is the outer bound). Then each record
has a question to ask of any public
resolver:

```bash
dig MX example.org
dig TXT example.org
dig TXT mail2026._domainkey.example.org
dig TXT _dmarc.example.org
dig -x 203.0.113.25
```

Each answer should show exactly the
record you published — character for
character, because SPF and DKIM are
parsed by machines and a stray space
or a missing quote is a silent failure
that only shows up as other people's
spam folders. Send yourself a letter
from a big provider and reply to it;
then read your DMARC reports when they
arrive. The server is built, named,
and vouched for. Chapters 11 and 12
make it liveable.
