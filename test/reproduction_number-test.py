#! /bin/usr/env python3
import sys
sys.path.append('../src')

from reproduction_number import *

datsrc = "../data/src/reproduction_number-test"
datout = "../data/out/reproduction_number-test"
dattail =  "../data/out/reproduction_number-test-tail"
wrksrc = "../data/wrk/"
wrkout = "../data/wrk/reproduction_number-test"
wrktail = "../data/wrk/reproduction_number-test-tail"

def makedat(infile, outfile, outtailfile="", running=1, formatdts="dts", delim=",", coldts=0, colinfected=1, colhealed=2,
        colactive=None, limit=0.0, par_l=7.0, par_d=9.0):
    # read data from input file
    ax = []
    ay = []
    skip = 1
    for line in open(infile):
        if skip == 1:  # ignore the first line of headers - slovak file contains some non-ascii chars there causing problems
            skip=0
            continue
        if not line.startswith("#"):  # ignore comment lines
            split = line.split(delim)
            dts = split[coldts]
            infected = int(split[colinfected])
            healed = int(split[colhealed])
            active = infected - healed
            if not colactive is None:
                if active != int(split[colactive]):
                    raise IOError(
                        "Expected active = infected - healed in file %s. To ignore, set colactive=None" % infile)
            ax.append(dts)
            ay.append(active)
    # calculate
    reprod = Reprod(ax, ay, formatdts, limit, par_l, par_d)
    result = reprod.calculate(running)
    # write result in xmgrace format into output file
    with open(outfile, "w") as f:
        for line in open(infile):
            if line.startswith("#"):  # copy comment lines
                print(line, file=f, end='')
        for record in result:
            print(*record, file=f)
    # calcuate tail
    if len(outtailfile) > 0  and  running >= 3:
        tailresult =  reprod.calculate(running, tail=True)
        # write result tail  in xmgrace format into output file
        with open(outtailfile, "w") as f:
            for record in tailresult:
                print(*record, file=f)


#########################################################################
# read covid input files, calculate the reproduction number and write output in format for xmgrace
# test0 : constructed set
# test1 : Jena
# test2 : Slovensko
# test3 : Cesko

test=0
delim=','
for days in [1,5]:
    input_file = datsrc + str(test) + ".csv"
    output_file = datout + str(test) + "-" + str(days) + ".dat"
    tail_file = dattail + str(test) + "-" + str(days) + ".dat"
    makedat(input_file, output_file, tail_file, days, "YMD", ",", coldts=0, colinfected=1,
            colhealed=2, colactive=None, limit=9, par_l=7.0, par_d=9.0)

days_list=[1,4,7,14]
dts_format={1:"epoch", 2:"DMY", 3:"YMD"}
delim={1:",",2:";", 3:","}
for test in range(1,4):
    for days in days_list:
        input_file = datsrc + str(test) + ".csv"
        output_file = datout + str(test) + "-" + str(days) + ".dat"
        tail_file = dattail + str(test) + "-" + str(days) + ".dat"
        makedat(input_file,output_file, tail_file, days, dts_format[test], delim[test], coldts=0, colinfected=1, colhealed=2, colactive=None, limit=0.0, par_l=7.0, par_d=9.0 )

# current status calculation
# 1. download wrk/korona.gov.sk.csv from https://mapa.covid.chat/export/csv
# 2. download wrk/nakazeni-vyleceni-umrti-testy.csv from https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/nakazeni-vyleceni-umrti-testy.csv
# 3. comment header line in both files

input_file_list = {2:"korona.gov.sk.csv", 3:"nakazeni-vyleceni-umrti-testy.csv"}
for test in range(2,4):
    for days in days_list:
        input_file= wrksrc + input_file_list[test]
        output_file = wrkout + str(test) + "-" + str(days) + ".dat"
        tail_file = wrktail + str(test) + "-" + str(days) + ".dat"
        makedat(input_file,output_file, tail_file, days, dts_format[test], delim[test], coldts=0, colinfected=1, colhealed=2, colactive=None, limit=0.0, par_l=7.0, par_d=9.0 )

