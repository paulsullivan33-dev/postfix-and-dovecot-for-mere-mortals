# Dovecot, the Postroom

**Outcome: Dovecot reading the same
Maildirs Postfix writes to, with a list
of who may log in — and `doveadm`
proving it sees Bob, his inbox, and the
letter waiting in it.** Dovecot's
default configuration is spread across
`/etc/dovecot/dovecot.conf` and a
`conf.d/` folder of numbered files, one
per topic (10-mail.conf, 10-auth.conf,
10-ssl.conf and friends). The settings
below are given by name, so you can put
each in its natural file; the lab
gathered them into one file so its
transcripts could show the whole
configuration at once.

## Pointing it at the mail

One setting does the chapter's main
work (in `10-mail.conf` on a packaged
install):

```text
mail_location = maildir:~/Maildir
```

*Maildir, in a folder called Maildir in
the user's home.* That is the same
folder chapter 5 told Postfix to
deliver into — the agreement the whole
server rests on. Say it differently in
either program (`mbox`, a `Mail`
folder, a different root) and the two
halves will each work perfectly while
the server as a whole delivers mail
into a void nobody reads. More
first-server failures live in this one
line than in everything else in this
guide combined; it gets its check
below.

## Who may log in

Dovecot separates the two questions a
login asks: *is this password right for
this name?* (the **passdb**) and *where
is this user's mail, and which user
number owns it?* (the **userdb**). This
guide answers both from one small file
of your own — a **passwd-file** — so a
mailbox's name is a full address and
its password exists only for mail:

```text
passdb {
  driver = passwd-file
  args = scheme=SHA512-CRYPT username_format=%u /etc/dovecot/users
}
userdb {
  driver = passwd-file
  args = username_format=%u /etc/dovecot/users
}
```

The file itself holds one line per
mailbox — user, password hash, the
user and group numbers that own the
mail, and the home folder:

```text
bob@example.org:{SHA512-CRYPT}$6$...:1000:1000::/home/bob::
```

Passwords are never written down in
the clear. You mint the hash with
Dovecot's own tool and paste it in:

```bash
doveadm pw -s SHA512-CRYPT
```

It asks for the password twice and
prints the `{SHA512-CRYPT}$6$…` string
(transcript
`postfix-and-dovecot-lab/transcripts/t00-versions-and-setup.txt`
shows the lab doing exactly this for
Bob's lab password). Guard the users
file like the passwords it contains:
owned by root, readable only by
Dovecot's auth service — the lab's
first login failed precisely because
the file's folder would not let the
auth process in, and chapter 14 tells
that story as the lesson it is.

The alternative — checking passwords
against the machine's own user accounts
(PAM) — is Dovecot's packaged default
and perfectly sound for a small server
whose mailbox owners all have logins.
It is described here, not demonstrated:
this guide's lab verified the
passwd-file path, and `criteria.md`
keeps that distinction.

The last settings name the ports (in
`10-master.conf`'s imap-login service):
IMAP on 143, and its encrypted twin
**IMAPS** on 993. The lab shifted both
(1143, 1993) for its loopback rehearsal;
chapter 9 adds the certificate that
makes 993 worth having.

## The check

Dovecot mirrors Postfix's two habits.
`doveconf -n` prints every setting that
differs from default — the lab's whole
deliberate list, nothing else
(transcript
`postfix-and-dovecot-lab/transcripts/t05-dovecot-config-and-user.txt`).
And `doveadm` inspects the living
server's view of the world:

```bash
sudo doveadm user bob@example.org
```

```text
field   value
uid     1000
gid     1000
home    /home/bob
mail    maildir:~/Maildir
```

```bash
sudo doveadm mailbox status -u bob@example.org messages INBOX
```

```text
INBOX messages=1
```

That last line is the agreement of
chapter 5 made visible: Dovecot counts
one message in Bob's inbox — the very
letter Postfix delivered in chapter 6.
If `doveadm user` finds no user, the
passwd-file is not being read (path,
permissions, or a typo in the name). If
the user is right but the count is 0,
the two programs disagree about where
mail lives, and the fix is the
`mail_location` line above, on one side
or the other. Chapter 8 now walks
through the door as a reader.
