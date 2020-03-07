#!/usr/bin/python3

from   glob    import glob
from   os.path import getctime
import sys
import re
import hiredis
from   redis   import Redis


dateiListe   = glob("*.tex")
neuesteDatei = max(dateiListe, key = getctime)
text         = ""

with open(neuesteDatei) as datei:
    zeilen  = datei.readlines()
    zeilen  = [zeile.strip() for zeile in zeilen]
    subject = [zeile for zeile in zeilen if re.search("subject", zeile)]
    zeilen  = [zeile for zeile in zeilen if len(zeile) > 0]
    text    = ("\n").join(zeilen[30:-5])
    zeilen  = enumerate(zeilen[0:-5])
    

match   = re.search(r"{ ((\S+\s?)+) }", subject[0], re.S)
subject = str(match.group())
subject = re.sub(r"(^{ | }$)", "", subject)
tokens  = re.findall("\S+", text)
tokens  = [token for token in tokens if not token.startswith("\\")]
tokens  = [token.strip(":.,") for token in tokens]

rds = Redis()

rds.hmset(subject, dict(enumerate(tokens)))
