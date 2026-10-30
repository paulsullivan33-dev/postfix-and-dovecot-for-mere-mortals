# Writing criteria for this guide

Every "for Mere Mortals" guide is written to the same nine-point
standard, so a reader who trusts one can trust the rest. Here it
is, with the verification notes for this particular guide below.

1. **Fix it first.** Reader outcomes lead, not action items: each
   chapter opens by naming the outcome it delivers, shows a check
   the reader can run to confirm they got it, and a reasonable
   reader finishes able to state what was done, what it means,
   and what to try next.
2. **Plain language.** Short sentences, everyday vocabulary,
   technical terms defined on first use. No slang, and no
   idioms that only make sense in one country — the reader may
   be translating as they go.
3. **No dead ends.** A guide never tells the reader to do
   something it cannot show them how to verify. Every claim a
   reader relies on — an install, a command, an output — is
   something this guide demonstrates or clearly labels
   documented-only below.
4. **Live-verified where it matters.** Procedures are run for
   real in the guide's lab wherever the build machine allows it,
   and the transcripts kept in the repository are the evidence.
   What could not be run is listed honestly below, never
   presented as if it had been.
5. **General audiences.** Nothing in this guide — examples,
   fixtures, names, addresses — is modelled on any particular
   reader or author's real life, network, or organisations.
   The domain is `example.org`, the people are Alice and Bob,
   and the one street address used is the documentation range
   203.0.113.0/24, reserved for examples.
6. **Standalone.** A reader needs this guide, its lab, and
   nothing else. Where another guide would genuinely help, it
   is pointed to once, by name, and the chapter still completes
   without it.
7. **Honest about limits.** Chapter 13 names what this setup
   cannot do: deliverability that must be earned over time, no
   content spam filter running, authenticated sending
   configured but not demonstrated, mailboxes tied to machine
   users, no webmail or calendar, one machine as a single
   point of failure, and the loopback nature of the lab
   itself.
8. **The ethics rule is in the text, early.** Running a mail
   server is joining a trust network, so the rule is stated in
   the README and again in chapter 1, before any procedure:
   never run an open relay, and only ever send mail to people
   who asked for it. The refusal behaviour that backs the rule
   — unknown recipients rejected in the conversation, relaying
   confined to the machine itself — is among the things the
   lab actually demonstrated.
9. **Builds clean.** The site builds with MkDocs in strict mode
   with no warnings, and a fresh reader following the chapters
   in order reaches the stated outcome of each.

## Verification notes for this guide

The build machine is a shared Ubuntu 24.04 sandbox that could
not take a system-wide package install, so the lab downloaded
the distribution's own packages — Postfix **3.8.6-1ubuntu0.1**,
Dovecot **2.3.21** (`dovecot-core` and `dovecot-imapd`,
1:2.3.21+dfsg1-2ubuntu6.5), plus the `libnsl2` library
Postfix links against — extracted them with `dpkg -x` into a
lab folder (`~/workspace/postfix-labwork`, kept out of /tmp),
and ran the **unmodified binaries** from that tree. The
daemons' expected system users and groups (postfix, postdrop,
dovecot, dovenull, and the test user bob) were created in the
sandbox, and a few symlinks let the extracted binaries find
their libraries and helper programs at their compiled-in
paths. Configuration files are the guide's own, with paths
pointing into the lab folder; the settings themselves are the
ones the chapters teach.

The whole lab ran on **loopback only** (127.0.0.1), under the
domain `mail.example.org`, with the standard ports shifted —
SMTP 2525, IMAP 1143, IMAPS 1993 — so the rehearsal could not
disturb, or be disturbed by, anything else. Nothing left the
machine: no DNS was published, no other server was contacted,
no real mail exists anywhere in it. All transcripts live in
`postfix-and-dovecot-lab/transcripts/`; the lab's two test
scripts (`send_test_mail.py`, `fetch_mail.py`) are kept beside
them.

Run for real, with transcripts as evidence:

- Versions of both stacks from the packages themselves, a
  self-signed TLS certificate minted with `openssl`, and
  Bob's password hash generated with `doveadm pw` into the
  passwd-file (t00).
- `postalias` building the alias database, `postfix check`
  exiting 0 in silence, and the full `postconf -n` list of
  deliberate settings (t01).
- A complete SMTP conversation — greeting, envelope, letter,
  "queued as 202D82212BD" — followed through the log
  (smtpd → qmgr → local, `status=sent (delivered to
  maildir)`) to the letter as a file in Bob's
  `Maildir/new`, headers and all (t02).
- An IMAP login as `bob@example.org` and the fetch of that
  same letter, byte for byte, over the plain port (t03).
- The same fetch over IMAPS: `openssl s_client` showing a
  TLS 1.3 handshake and the self-signed certificate
  (verification error reported, not hidden), then the login
  and letter inside the encrypted connection (t04).
- `doveconf -n`, `doveadm user` resolving Bob's uid, gid,
  home and mail location, `doveadm mailbox list`, and a
  mailbox status count agreeing with Postfix's delivery
  (t05).
- The refusals and the alias: mail to the nonexistent
  `carol@example.org` rejected with 550 5.1.1 in the SMTP
  conversation, a wrong IMAP password refused with
  AUTHENTICATIONFAILED, and a letter to `postmaster`
  delivered to Bob by the alias chain
  (`orig_to=<postmaster@example.org>`), raising his inbox
  count to 2 (t06).
- Two failures the lab caused and fixed, kept as
  troubleshooting material: the auth service unable to read
  the passwd-file through a folder that denied it entry
  (Dovecot's log named the missing traverse permission), and
  the first delivery bouncing because a folder above the
  recipient's home denied the delivery agent the same way.

Documented only — described from the projects' and
distributions' documentation, not run, and the text does not
claim otherwise:

- The `apt install` dialogue itself (the Internet Site
  choice and the system mail name): the lab ran the same
  packages from an extracted tree, as explained above,
  rather than through the installer.
- Everything in chapter 10: MX, A and PTR records, SPF,
  DKIM signing (including the OpenDKIM setup that produces
  the record) and DMARC policy — correct, standard records
  for the example domain, but unpublished and unobserved by
  the lab, with the `dig` checks given for after a reader
  publishes them.
- A publicly trusted certificate (Let's Encrypt / certbot):
  the lab's certificate is self-signed, and its verification
  error is shown, not edited away.
- Postfix-side TLS settings and authenticated submission
  through the Dovecot SASL bridge; content spam filtering
  (Rspamd, SpamAssassin); virtual users and domains; a
  backup MX; webmail. All are named, characterised, and
  pointed at — none is presented as set up.
- Sending to, or receiving from, any real server on the
  internet, and the deliverability behaviour of any real
  provider.

Fixtures are this guide's own and deliberately generic: the
reserved example domain, two stock names, a lab password
used only inside the transcripts, and the documentation IP
range. No real organisation, mailbox, or message appears
anywhere in the lab or the text.
