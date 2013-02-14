#!/usr/bin/python
"""Download GSM samples from a list of GSM IDS from the GEO website."""

# insert GSM ID as first string.
URL_PTN = "http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=%s&targ=self&form=text&view=full"
ID_FILE = "gpl8490_gsm_ids.txt"
OUTDIR = "gpl8490_gsm"

import urllib2
import os

def make_dir(outdir):
  try:
    os.makedirs(outdir)
  except OSError, e:
    if e.errno != errno.EEXIST: raise
  return outdir
make_dir(OUTDIR)

gsm_ids = [s.strip('\n\r') for s in open(ID_FILE)]
os.chdir(OUTDIR)
for gsm in gsm_ids:
  url = URL_PTN % gsm
  print "Downloading %s..." % (url)
  fp = open("%s.txt" % gsm, "w")
  http = urllib2.urlopen(url)
  for line in http:
    fp.write(line)
  fp.close()
  http.close()
  
