# Domain Checker

A simple Python script to monitor domain name availability and notify you via email when a domain becomes available.

## Features

- Checks a list of domains for registration status.
- Sends email notifications when a domain is available.
- Easy configuration via `.env` and `domain-list` file.

## Setup

### 1. Clone the Repository and install dependencies

Clone the repo, make sure you have a command-line "whois" available and install python dependencies.

```sh
git clone https://github.com/stefnnn/domain-checker.git
cd domain-checker
# apt install whois
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and fill in your SMTP and email details:

```sh
cp .env.example .env
```

Edit `.env`:

```env
SMTP_HOST=your.smtp.host
SMTP_USER=your_smtp_username
SMTP_PASSWORD=your_smtp_password
EMAIL_FROM=your@email.com
EMAIL_TO=recipient@email.com
EMAIL_SUBJECT=Domain-Checker found a domain
```

### 3. Prepare the Domain List

Copy `domain-list.example` to `domain-list` and edit it to include the domains you want to monitor (one per line):

```sh
cp domain-list.example domain-list
```

Example `domain-list`:

```
some-domain.com
unavailable.com
maybe.org
```

### 5. Run the Script

```sh
python domain-checker.py
```

## Setting Up a Cronjob

To check domains every hour, add the following line to your crontab:

```sh
crontab -e
```

Add:

```
0 * * * * cd /path/to/domain-checker && /usr/bin/env python3 domain-checker.py >> domain-checker.log 2>&1
```

Replace `/path/to/domain-checker` with the actual path to your project directory.

## License

MIT Licensed.
