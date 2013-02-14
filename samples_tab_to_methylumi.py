#!/usr/bin/python
"""
Format sample meta data into format for methylumi
sampleDescriptions: A data.frame that contains at least one column,
          SampleID (case insensitive).  This column MUST match the part
          of the column headers before the .Avg_Beta, etc.  Also, if
          a column called SampleLabel (case insensitive), it is used
          for sample labels, IF the sampleLabel column contains unique
          identifiers

e.g.,

SampleID	SampleLabel	Sample	Gender
1632405013_R006_C012	M_1	1	M
"""
FNAME = "/Users/z/Dropbox/gse15745_preprocessing/gse15745_gpl8490_geo_downloader/GSE15745_GPL8490.samples.tab"
def main(fname_out="GSE15745_GPL8490.samples.methylumi.tab"):
  rows = {}
  n = None
  for line in open(FNAME):
    if line[0] == "#": continue
    line = line.rstrip('\n\r')
    row = line.split('\t')
    rows[row[0]] = row[1:]
    if n is None:
      n = len(row[1:])
  fp_out = open(fname_out, "w")
  attrs = list(rows.keys())
  fp_out.write("SampleID\tSampleLabel\t"); fp_out.write("\t".join(attrs)); fp_out.write('\n')
  for i in xrange(n):
    sample_id = rows["title"][i].rpartition('-')[0]
    fp_out.write("%s\t%s\t" % (sample_id, sample_id))
    fp_out.write("\t".join([rows[k][i] for k in attrs]))
    fp_out.write('\n')
  fp_out.close()
  

if __name__ == "__main__":
  main()
