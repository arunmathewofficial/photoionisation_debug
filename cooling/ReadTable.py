# Author: Arun Mathew
# Created: 11-09-2022


# New comments:
# 2022-09-11 AM: scripted ReadTable
# 2022-11-13 AM: scripted ReadTable_Advance

import numpy

def ReadTable(Table):
    # Create an empty array for the following:
    log_Temp = []  # log10(T/K)
    l01 = []  # j(E>0.1keV)
    l02 = []  # j(E>0.2keV)
    l03 = []  # j(E>0.3keV)
    l05 = []  # j(E>0.5keV)
    l1  = []  # j(E>1keV)
    l2  = []  # j(E>2keV)
    l5  = []  # j(E>5keV)
    l10 = []  # j(E>10keV)

    # Read a line of numbers out of a text file:
    print('Reading data from ' + Table)
    with open(Table) as table:
        for line in table:
            data = line.split()
            if data[0] == "#":
                continue
            log_Temp.append(float(data[0]))
            l01.append(float(data[3]))
            l02.append(float(data[4]))
            l03.append(float(data[5]))
            l05.append(float(data[6]))
            l1.append(float(data[7]))
            l2.append(float(data[8]))
            l5.append(float(data[9]))
            l10.append(float(data[10]))

    return {'log_Temp': log_Temp, 'l01': l01, 'l02': l02, 'l03': l03,
            'l05': l05, 'l1': l1, 'l2': l2, 'l5': l5, 'l10': l10}


def ReadTable_Advance(Table):
    # Read a line of numbers out of a text file:
    print('Reading tabulated data: ' + Table)
    # count number of rows and columns and
    # store entire table data in 2D vector.
    N_row = 0
    N_col = 0
    data = []
    Temperature = []
    with open(Table) as table:
        for line in table:
            row = line.split()
            if line.startswith('#'):
                continue
            else:
                N_row += 1
                row = numpy.asarray(line.split(","), dtype=float)
                Temperature.append(row[0])
                row = row[1:] #remove the first element
                N_col = len(row)
                data.append(row)

    #Create N_col arrays
    columns = [[] for _ in range(N_col)]
    #Append corresponding data into each columns
    for col in range(N_col):
        for row in range(N_row):
            columns[col].append(data[row][col])

    return {'N_row': N_row, 'N_col': N_col, 'Temperature':Temperature, 'columns': columns}













