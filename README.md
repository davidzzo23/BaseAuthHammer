# BaseAuthHammer

## A Powerful, Customizable HTTP Basic Authentication Brute-Force Tool

**BaseAuthHammer** is a Python-based brute-force tool designed to test credentials on services protected with **HTTP Basic Authentication**. It includes features to evade detection, improve performance, and efficiently log successful attempts.

With multithreading, random User-Agent rotation, adjustable delays, and the ability to save valid credentials, BaseAuthHammer is an essential tool for penetration testers, security researchers, and ethical hackers.

## Features

- **Multithreading**: Parallelize brute-force attacks to increase efficiency.
- **Random User-Agent Rotation**: Bypass basic detection mechanisms by rotating User-Agent headers.
- **Adjustable Delays**: Throttle requests with custom delays to avoid rate-limiting or detection.
- **Save Successful Attempts**: Log valid credentials to a specified file for later reference.
- **Proxy Support**: Route traffic through a proxy to obfuscate source IP (e.g., Burp Suite or external proxies).
- **Custom Input Files**: Provide username and password lists for tailored brute-force attempts.

## Requirements

Ensure the following Python libraries are installed:

- requests
- colorama

To install them, run:

```bash
pip install requests colorama
```

## Usage

### Basic Syntax

```bash
python baseauthhammer.py -H <URL> [-u USERNAME | -U USERLIST] [-p PASSWORD | -P PASSFILE] [options]
```

### Options

| **Option** | **Description** | **Example** |
| --- | --- | --- |
| -H, --host | Target URL requiring Basic Authentication. | -H http://example.com/login |
| -u, --user | Single username to test. | -u admin |
| -U, --userlist | File containing a list of usernames. | -U users.txt |
| -p, --password | Single password to test. | -p password123 |
| -P, --passfile | File containing a list of passwords. | -P passwords.txt |
| -x | Enable proxy mode (default is [http://127.0.0.1:8080](http://127.0.0.1:8080/)) | -x |
| -d, --delay | Add a delay (in seconds) between requests to evade detection. | -d 2 |
| -t, --threads | Number of threads for parallel execution. | -t 5 |
| -o, --output | Save successful credentials to a file. | -o success.txt |

### Examples

1. Brute-force with single username and a password file:

```bash
python baseauthhammer.py -H http://example.com -u admin -P passwords.txt
```

2. Brute-force using a list of usernames and passwords:

```bash
python baseauthhammer.py -H http://example.com -U users.txt -P passwords.txt
```

3. Brute-force with a delay of 2 seconds between attempts:

```bash
python baseauthhammer.py -H http://example.com -u admin -P passwords.txt -d 2
```

4. Brute-force with 5 threads for faster execution:

```bash
python baseauthhammer.py -H http://example.com -U users.txt -P passwords.txt -t 5
```

5. Save successful credentials to a file:

```bash
python baseauthhammer.py -H http://example.com -u admin -P passwords.txt -o success.txt
```

6. Use proxy for traffic routing:

```bash
python baseauthhammer.py -H http://example.com -u admin -P passwords.txt -x
```

## Notes

- Use this script **responsibly**. It is designed for penetration testing and research purposes only. Ensure you have proper authorization before testing any systems.
- Avoid using on production environments or without permission to prevent unintended consequences.

## Disclaimer

The author is not responsible for any misuse or damages caused by this tool. Use at your own risk and only for ethical purposes.
