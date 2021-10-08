import os
import pandas as pd

atomicRadii = {'C': 1.700,
               'O': 1.520,
               'N': 1.550,
               'H': 1.200}


def get_info_from_log(file_with_path):
    # Input Gaussian log file. This function extracts the Mulliken charge and atom information.
    with open(file_with_path, 'r') as f:
        infile = f.readlines()

    # find indices where Mulliken charges are described
    mullikenIndexKeyword = ' Mulliken charges:\n'
    mullikenIndex = infile.index(mullikenIndexKeyword)
    # get list of Mulliken charges
    chargeList = []
    i = mullikenIndex + 2
    while 'Sum' not in infile[i]:
        chargeList.append(infile[i].split()[:3])
        i += 1

    # next find atom info. The atom info is in a paragraph in which the line break can influence the presence of the keyword. Therefore we merge the entire file contents to one string.
    contents = ''.join([x.strip() for x in infile])
    atomInfoIndexKeyword = 'in gas phase\\\\'
    atomInfoIndex = contents.index(atomInfoIndexKeyword)
    atomInfoEndKeyword = 'Version='
    if atomInfoEndKeyword not in contents:
        print((contents[atomInfoIndex:]))
    atomInfoEnd = contents.index(atomInfoEndKeyword)
    atomInfo = contents[atomInfoIndex:atomInfoEnd]
    atomInfo = atomInfo.split('\\')
    atomInfo = [x.split(',') for x in atomInfo]
    atomInfo = [x for x in atomInfo if len(x) == 5]
    return chargeList, atomInfo

def aggregate_data(chargeList, atomInfo):
    # organize data into Pandas DataFrame, ready to write out as PQR
    ATOM = ['ATOM'] * len(atomInfo)
    atomEnumeration = [x[0] for x in chargeList]
    atomName = [x[1] for x in chargeList]
    residueID = ['MOL'] * len(atomInfo)
    chainID = [1] * len(atomInfo)
    xcoord = [str(round(float(x[2]), 2)) for x in atomInfo]
    ycoord = [str(round(float(x[3]), 2)) for x in atomInfo]
    zcoord = [str(round(float(x[4]), 2)) for x in atomInfo]
    MullikenCharge = [str(round(float(x[2]), 4)) for x in chargeList]
    # Add space after nonnegative valued coordinates so that decimal points match
    for i in range(len(xcoord)):
        for theCoords in [xcoord, ycoord, zcoord, MullikenCharge]:
            if theCoords[i][0] != '-':
                theCoords[i] = ' ' + theCoords[i]
    atomicRadius = [' ' + str(atomicRadii[x]) for x in atomName]
    atomID = atomName
    outputData = {'recordName': ATOM, 'serial': atomEnumeration, 'atomName': atomName,
                  'residueName': residueID, 'chainID': chainID, 'X': xcoord, 'Y': ycoord, 'Z': zcoord,
                  'charge': MullikenCharge, 'radius': atomicRadius, 'atomID': atomID}

    outputDf = pd.DataFrame(outputData)
    return outputDf

def save_data(df, outpath_file):
    with open(outpath_file, 'w') as f:
        df.to_csv(f, sep = '\t', header = False, index = False)

def runLog2Pqr(file_with_path, outpath_file):
    chargeList, atomInfo = get_info_from_log(file_with_path)
    outputDf = aggregate_data(chargeList, atomInfo)
    save_data(outputDf, outpath_file)