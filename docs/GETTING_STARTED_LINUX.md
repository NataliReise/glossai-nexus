# Getting started on Linux

This guide helps you run **Nexus 0.1 - First Spark** from a local Linux terminal.

It is written for people who may be new to Git, Python, or terminal-based projects.

## Current platform focus

The current public seed is Linux-first.

First Spark is a local terminal prototype written in Python and currently developed and checked on Linux.

Other platforms may become possible later, but the first stable path is a local Linux terminal.

## What you need

You need:

- a Linux system,
- a terminal,
- Git,
- Python 3,
- an internet connection for cloning the repository.

## Open a terminal

On many Linux desktops, you can open a terminal with:

```text
Ctrl + Alt + T
```

You can also search for `Terminal` in your application menu.

## Check Git

In the terminal, run:

```bash
git --version
```

If Git is installed, you should see a version number.

If Git is missing, install it with your Linux distribution's package manager.

On Debian, Ubuntu, Linux Mint, or related systems, you can usually use:

```bash
sudo apt update
sudo apt install git
```

## Check Python 3

In the terminal, run:

```bash
python3 --version
```

If Python 3 is installed, you should see a version number.

If Python 3 is missing, install it with your Linux distribution's package manager.

On Debian, Ubuntu, Linux Mint, or related systems, you can usually use:

```bash
sudo apt update
sudo apt install python3
```

## Clone the repository

Choose a folder where you want to keep the project.

For example, you can use your home folder:

```bash
cd ~
```

Then clone the public repository:

```bash
git clone https://github.com/NataliReise/glossai-nexus.git
```

Enter the project folder:

```bash
cd glossai-nexus
```

## Run First Spark

From the repository root, run:

```bash
python3 modules/nexus_01_nexus_mesomerie/first_spark/run_first_spark.py
```

First Spark should start in your terminal.

## Stop First Spark

Inside First Spark, you can usually type:

```text
quit
```

You can also press:

```text
Ctrl + C
```

This interrupts First Spark and returns you to the terminal.

## Try the automated test

From the repository root, you can run:

```bash
python3 modules/nexus_01_nexus_mesomerie/first_spark/tests/test_first_spark_flow.py
```

Expected output:

```text
First Spark flow tests passed.
```

## Public and private files

The public repository contains public code, neutral example data, and public-safe documentation.

Do not post or commit private activation files.

In particular, do not publish:

- `activation.local.json`,
- private activation messages,
- private gift messages,
- recipient-specific information,
- return artifacts,
- screenshots that reveal private activation content.

When unsure, leave private details out.

## If you need help

Use the `Help and Support` category in GitHub Discussions:

```text
https://github.com/NataliReise/glossai-nexus/discussions
```

When asking for help, describe what you tried and where you got stuck.

Do not paste private activation data or screenshots that reveal private content.
