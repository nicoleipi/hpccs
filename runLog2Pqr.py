# 2020-03-02

# Kiyoto Aramis Tanemura

# Provided a directory, convert all gaussian log files to PQR format.

import os
from log2Pqr import runLog2Pqr

inpath = './'
outpath = './'

fileList = [x for x in os.listdir(inpath) if x[-3:] == 'log']

for theFile in fileList:
    outputName = theFile.replace('log', 'pqr')
    runLog2Pqr(inpath + theFile, outpath + outputName)

message = str(len(fileList)) + ' log files considered\n' + str(len([x for x in os.listdir(outpath) if x[-3:] == 'pqr'])) + ' PQR files present'
print(message)
with open(outpath + 'output_summary.txt', 'w') as f:
    f.write(message)
