#!/usr/bin/python
## FIX THIS SCRIPT
import os
import re
import sys
import numpy as np

DIR = "gpl8490_gsm"
RX_FNAME = re.compile("(GSM\d+)\.txt")
RX_TITLE = re.compile("!Sample_title = (.+?)-CpG")
BEGIN_TABLE = "!sample_table_begin"
END_TABLE = "!sample_table_end"

def main(indir=DIR, outdir=None, fname_out="gse15745_gpl8490_methylumi2.tab"):
  n_read = 0
  n_rows = None
  row_ids = None
  col_ids = None
  if outdir is None:
    outdir = dir

  arrays = {}
  for fname in os.listdir(indir):
    m = RX_FNAME.match(fname)
    if not m: continue
    n_read += 1
    fp = open(os.path.join(indir, fname))
    title = None
    for line in fp:
      line = line.rstrip('\r\n')
      if line == BEGIN_TABLE:
        break
      m = RX_TITLE.match(line)
      if m:
        title = m.group(1)
    assert title is not None
    M = np.genfromtxt(fp, skip_footer=1, names=True, delimiter="\t", dtype="S11,S11,S11,S11,S11,S11,S11,S11,S11,S11")
    fp.close()
    arrays[title] = M
    if n_rows is None:
      n_rows = np.size(M,0)
    else:
      assert n_rows == np.size(M,0)
    if row_ids is None:
      row_ids = [r[0] for r in M]
    else:
      for i,s in enumerate(row_ids):
        assert s == M[i][0], "%s @ line %d: %s != %s" % (fname, i+1, s, M[i][0])
    if col_ids is None:
      col_ids = list(M.dtype.names)
      for i in xrange(len(col_ids)):
        s = col_ids[i]
        if s == "Detection_Pval":
          col_ids[i] = "Detection Pval"
          
    else:
      assert col_ids == M.dtype.names, fname

  print "Read %d arrays of %d rows with matching row and column IDs." % (n_read, n_rows)
  

  fp_out = open(fname_out, "w")
  # write headers
  fp_out.write("TargetID\t")
  for i, title in enumerate(arrays):
    fp_out.write("%s.AVG_Beta\t" % title)
    fp_out.write("\t".join(["%s.%s" % (title, s) for s in col_ids[2:]]))
    if i < len(arrays)-1:
      fp_out.write("\t")
  fp_out.write("\n")
  for i, row_id in enumerate(row_ids):
    fp_out.write("%s" % row_id)
    for title, M in arrays.items():
      for j in xrange(1,len(M[i])):
        fp_out.write("\t"); fp_out.write(M[i][j])
    fp_out.write('\n')
    
  return arrays


if __name__ == "__main__":
  main(**dict([s.split('=') for s in sys.argv[1:]]))
