# holehe_chk

A really badly coded holehe script that allows me to give file input for emails or email as standalone and output to file in json format.

I have edited this script to be a bit more robust and more efficient. It still sucks.

----

## Install:

I just did:

```python3
git clone https://github.com/dleto614/holehe_chk && cd holehe_chk
python3 -m venv venv
source venv/bin/activate
pip3 install argparse trio httpx holehe
```

-------

## Usage:

```python3
python3 main.py --input emails.txt --output test-socials-emails.json
```

```python3
python3 main.py --email youremail@example.com --output test-socials-email.json
```

Can omit the `--output` flag.

------

##### Help:

```python3
$ python3 main.py -h
usage: main.py [-h] [--email EMAIL] [--input INPUT] [--output OUTPUT]
               [--sites SITES] [--list-sites] [--verbose] [--log] [--debug]
               [--log-file LOG_FILE]
               [--log-level {debug,info,warning,error,critical}]

Check if an email is associated with various online accounts.

options:
  -h, --help            show this help message and exit
  --email, -e EMAIL     Email to check.
  --input, -i INPUT     File with emails (one per line).
  --output, -o OUTPUT   File to save results to (JSON format).
  --sites, -s SITES     Comma-separated list of sites to check.
  --list-sites, -l      List all available sites and exit.
  --verbose, -v         Show verbose output (number of sites being checked).
  --log                 Set logging or not.
  --debug, -d           Set debug.
  --log-file LOG_FILE   Path to log file for internal debugging.
  --log-level {debug,info,warning,error,critical}
                        Set logging level for console/file output (default:
                        warning).
```
