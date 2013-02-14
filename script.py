#!/usr/bin/python
"""
Download data from all GSMs associated with directly associated with a GEO GSE.

$ python script.py gse=GSE15222 outdir=~/Desktop
"""
from geo_api import *
from geo_api.gsm_single import *
from geo_api.download import *
import sys
import urllib2
import os

def scrape(gse=None, gpl=None, outdir="", use_downloader=True):
  assert gse
  G = GSE(gse, populate=False)
  if G.type == "SUPER" and gpl is None:
    print "%s is a super study containing multiple studies/platforms. Specify one GPL platform from:" % gse
    print ", ".join([GG.platform.id for GG in G.substudies.values()])
    print "exiting..."
    sys.exit(1)
  if G.type != "SUPER" and gpl:
    if gpl != G.platform.id:
      print "WARNING: given GPL %s != actual GPL %s" % (gpl, G.platform.id)
  if G.type == "SUPER" and gpl:
    found = False
    for ggsm, GG in G.substudies.items():
      if GG.platform.id == gpl:
        print "Chose %s substudy / platform." % ggsm
        G = GG
        found = True
        break
    if not found:
      print "ERROR: could not find %s in platforms included under this super study %s. Specify one GPL platform from:" % (gpl, gse)
      print ", ".join([GG.platform.id for GG in G.substudies.values()])
      print "exiting..."
      sys.exit(1)

  #Sample_platform_id
  print "Found %d GSMs." % len(G.samples)
  fpath = "%s.gsms.txt" % gse
  if outdir:
    fpath = os.path.join(outdir, fpath)

  # Fetch all studies, load into memory
  GSMs = {}
  probes = set()

  for i, gsm in enumerate(G.samples.keys()):
    print "#%d %s downloading..." % (i+1, gsm)
    if use_downloader:
      h = Download(URL_PTN%gsm)
      fp = h.read()
      S = GSM_Lite(fp)
      fp.close()
    else:
      S = GSM_Lite(urllib2.urlopen(URL_PTN%gsm))
    # Only download samples from the requested platform
    if gpl:
      if gpl != S.attr['platform_id'][0]:
        print "%s is platform %s != %s. Skipping..." % (gse, S.attr['platform_id'][0], gpl)
        continue
    probes |= set(S.rows.keys())
    assert S.id == gsm
    GSMs[gsm] = S

  print "Downloaded %d of %d GSMs." % (len(GSMs), len(G.samples))
  # Print to text file.
  print "Writing combined table to %s" % fpath
  fp = open(fpath, "w")
  
  gsm_list = sorted(GSMs.keys())
  header = ["ID_REF"]
  for gsm in gsm_list:
    header += ["%s_%s"%(gsm, s) for s in GSMs[gsm].col_headers[1:]]
  print >>fp, "\t".join(header)
  for p in probes:
    row = [p]
    for gsm in gsm_list:
      row += GSMs[gsm].rows[p]
    print >>fp, "\t".join(row)
  
  
if __name__ == "__main__":
  scrape(**dict((s.split('=') for s in sys.argv[1:])))
