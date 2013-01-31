from geo_api import *
from geo_api.gsm_single import *
import sys
import urllib2
import os

def scrape(gse=None, outdir=""):
  assert gse
  G = GSE(gse, populate=False)
  print "Found %d GSMs." % len(G.samples.keys())
  fpath = "%s.gsms.txt"
  if outdir:
    fpath = os.path.join(outdir, fpath)

  # Fetch all studies, load into memory
  GSMs = {}
  probes = set()
  for i, gsm in enumerate(G.samples.keys()):
    print "#%d %s downloading..." % (i, gsm)
    S = GSM_Lite(urllib2.urlopen(URL_PTN%gsm))
    probes |= set(S.rows.keys())
    assert S.id == gsm
    GSMs[gsm] = S
    
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
      row += GSMs[gsm][p]
    print >>fp, "\t".join(row)
  
  
if __name__ == "__main__":
  scrape(**dict((s.split('=') for s in sys.argv[1:])))
