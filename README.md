# holehe_chk

A really badly coded holehe script that allows me to give file input for emails or email as standalone and output to file in json format.

----

## Install:

I just did:

```python3
git clone https://github.com/dleto614/holehe_chk && cd holehe_chk
python3 -m venv venv
venv/bin/pip3 install argparse trio httpx holehe
```

-------

## Usage:

```python3
venv/bin/python3 main.py --input emails.txt --output test-usernames.json
```

```python3
venv/bin/python3 main.py --email youremail@example.com --output test-usernames.json
```

Can omit the `--output` flag.

------

##### Help:

```python3
$ venv/bin/python3 main.py 
usage: main.py [-h] [--email EMAIL] [--input INPUT] [--output OUTPUT]

Simple python3 program to check if an email is associated with any of the import online account modules.

options:
  -h, --help            show this help message and exit
  --email EMAIL, -e EMAIL
                        Email to check.
  --input INPUT, -i INPUT
                        File with emails one on each line.
  --output OUTPUT, -o OUTPUT
                        Specify a file to save results to.
```
