# Installing Postfix and Dovecot

**Outcome: both programs installed from
your distribution's packages, each able
to state its version.** Installation is
the shortest chapter in this guide —
not because it is unimportant, but
because the distributions have done
this work ten thousand times and the
defaults they give you are the floor
this guide builds on.

The examples are Ubuntu 24.04, the
lab's system; Debian is the same with
the same commands, and other
distributions carry the same two
programs under the same names with a
different package tool.

## The one command

```bash
sudo apt update
sudo apt install postfix dovecot-imapd
```

`dovecot-imapd` pulls in `dovecot-core`
on its own; there is no need to name
it. The Postfix installer asks one real
question — the **configuration type**.
Choose **Internet Site**: it means
"this machine sends and receives mail
directly on the internet", which is
the server this guide is building. It
then asks for the **system mail name**:
give your domain, `example.org`. The
installer writes a first `main.cf`
with sensible answers — your machine's
name, your domain — which chapter 5
then takes apart and rebuilds on
purpose, so you know what every line
is doing there.

That is all. Neither installer starts
a finished service you must race to
secure: Postfix begins life listening
as a local server with the defaults
from your answers, and Dovecot waits
with its own stock configuration.
Chapters 5 and 7 replace both
deliberately.

## A note from the lab

The lab verified this guide with the
exact packages above — Postfix
**3.8.6** and Dovecot **2.3.21**, the
Ubuntu 24.04 builds. Its sandbox could
not take a system-wide install, so it
downloaded the same `.deb` packages and
ran the identical binaries from an
extracted tree, with configuration
files pointing at lab folders instead
of `/etc` and `/var`. Where the lab's
setup differs from a real install —
paths, and the three listening ports,
shifted to 2525, 1143 and 1993 so the
lab could not disturb anything else on
its machine — the chapters say so at
the point it matters. The programs,
their behaviour and their outputs are
the distribution's own, unmodified
(transcript
`postfix-and-dovecot-lab/transcripts/t00-versions-and-setup.txt`).

## The check

Two commands, two version numbers:

```bash
postconf mail_version
dovecot --version
```

```text
mail_version = 3.8.6
2.3.21 (47349e2482)
```

Your numbers may be newer — both
projects release steadily, and nothing
in this guide depends on the third
digit. What matters is that both
programs answer. A command-not-found
means the package did not install;
re-run the install and read its output
before going further — every later
check assumes this one passed.
