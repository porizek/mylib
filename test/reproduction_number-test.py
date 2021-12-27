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
            colactive=None, limit=0.0, duration_R=7.0):
    '''
    Wrapper for reading data from common COVID files and passing then further for the reproduction number calculation
    @param infile:  filename of the common input CSV file to be read
    @param outfile:  filename of output file with data for xmgrace graph application
    @param outtailfile: output file with data for graph - tail part only
    @param running: number of points for running averages
             Format of the input CSV file:
    @param formatdts:
    @param delim: CSV delimiter, usually "," or ";" for regional formats
    @param coldts: which colum has timestamp
    @param colinfected: which colum has infected - cumulative positive tests
    @param colhealed: which colum has healed count - cumulative
    @param colactive: which colum has active count (= infected - healed)
    @param limit: what is the limit count of active to be included into calculation
    @param duration_R:
    @return: none - the output files are created
    '''

    # reading date
    ax = []
    ay = []
    lastactive = None
    skip = 1
    for line in open(infile):
        if skip == 1:  # ignore the first line of headers - slovak file contains some non-ascii chars there causing problems
            skip=0
            continue
        if not line.startswith("#"):  # ignore comment lines
            split = line.split(delim)
            dts = split[coldts]
            """ Colums code:
            colinfected colhealed colactive 
               valid      valid    NONE      count = colinfected - colhealed
               valid      valid     >0       count = colinfected - colhealed  + check: count = colactive ?  
               NONE        NONE     >0       count = colactive
               NONE        NONE     <0       cound = colactive(this) - colactive(previous)
            """
            if (colactive is not None and colactive > 0) and (colinfected is None) and (colhealed is None):
                active=int(split[colactive])
                ax.append(dts)
                ay.append(active)
            elif (colactive is not None and colactive < 0) and (colinfected is None)  and (colhealed is None) :
              active = int(split[-colactive])
              if not lastactive is None :
                  ax.append(dts)
                  ay.append(active-lastactive)
              lastactive = active
            elif ( colinfected is not None )  and ( colhealed is not None ) :
                infected = int(split[colinfected])
                healed = int(split[colhealed])
                active = infected - healed
                # if all three colums are provided do test if they are equal. However there are sometimes differnet in Slovak data, so it does no0t have a real use
                if not colactive is None:
                    if active != int(split[colactive]):
                        raise IOError(
                            "Expected active = infected - healed in file %s. To ignore, set colactive=None" % infile)
                ax.append(dts)
                ay.append(active)
            else :
              raise IOError(
                    "Invalid definition of input colums: colinfected = %d, colhealed = %d ,colactive =%d " % (colinfected,colhealed,colactive) )
    # calculate
    reprod = Reprod(ax, ay, formatdts, limit, duration_R)
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

# standart test for designed datafile test=0
# "../data/src/reproduction_number-test0.csv"
# "../data/out/reproduction_number-test0-1.dat"  + "../data/out/reproduction_number-test-tail0-1.dat"
# "../data/out/reproduction_number-test0-5.dat"  + "../data/out/reproduction_number-test-tail0-5.dat"
test=0
delim=','
for days in [1,5]:
    input_file = datsrc + str(test) + ".csv"
    output_file = datout + str(test) + "-" + str(days) + ".dat"
    tail_file = dattail + str(test) + "-" + str(days) + ".dat"
    makedat(input_file, output_file, tail_file, days, "YMD", ",", coldts=0, colinfected=1,
            colhealed=2, colactive=None, limit=9, duration_R=7.0)

# standart test for real datafile
# test=1 Jena - Germany
# test=2 Slovensko
# test=3 Cesko
# "../data/src/reproduction_number-test[1,2,3].csv"
# "../data/out/reproduction_number-test[1,2,3]-[1,4,7,14].dat"  + "../data/out/reproduction_number-test-tail[1,2,3]-[1,4,7,14].dat"
days_list=[1,4,7,14]  # no averanging, 4-day averaging, week averaging and two weeks averaging
dts_format={1:"epoch", 2:"DMY", 3:"YMD"} # 1:epoch - Jena, 2:DMY - Slovensko, 3:YMD - Cesko
delim={1:",",2:";", 3:","}  # 1:"," - Jena ,2:" - Slovensko ;", 3:"," - Cesko
for test in range(1,4): # [1,2,3]
    for days in days_list: # [1,4,7,14]
        input_file = datsrc + str(test) + ".csv"
        output_file = datout + str(test) + "-" + str(days) + ".dat"
        tail_file = dattail + str(test) + "-" + str(days) + ".dat"
        makedat(input_file, output_file, tail_file, days, dts_format[test], delim[test], coldts=0, colinfected=1, colhealed=2, colactive=None, limit=0.0, duration_R=7.0)

# no real testing, rather recalculation of the current status
# 1. download wrk/korona.gov.sk.csv from https://mapa.covid.chat/export/csv
# 2. download wrk/nakazeni-vyleceni-umrti-testy.csv from https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/nakazeni-vyleceni-umrti-testy.csv
# 3. comment header line in both files

input_file_list = {2:"korona.gov.sk.csv", 3:"nakazeni-vyleceni-umrti-testy.csv"}
for test in range(2,4): # [2-slovensko,3-cesko]
    for days in days_list: # [1,4,7,14]
        input_file= wrksrc + input_file_list[test]
        output_file = wrkout + str(test) + "-" + str(days) + ".dat"
        tail_file = wrktail + str(test) + "-" + str(days) + ".dat"
        makedat(input_file, output_file, tail_file, days, dts_format[test], delim[test], coldts=0, colinfected=1, colhealed=2, colactive=None, limit=0.0, duration_R=5.0)

# recalculation od Flegr "4 000 nakazenych za tyzden, 10 000 nakazenych za 2 tyzdne"
# test=3  # cesko
# days=14 # 14 day averaging
#input_file= wrksrc + input_file_list[test]
#output_file = "../data/wrk/flegr-thumb_rule" + str(test) + "-" + str(days) + ".dat"
#tail_file = "../data/wrk/flegr-thumb_rule-tail" + str(test) + "-" + str(days) + ".dat"
#makedat(input_file, output_file, tail_file, days, dts_format[test], delim[test], coldts=0, colinfected=None, colhealed=None,
#        colactive=-1, limit=0.0, standart_period=5.0)

# CR growth rate of death
test=3  # cesko
days=14 # 14 day averaging
input_file= wrksrc + input_file_list[test]
output_file = "../data/wrk/death" + str(test) + "-" + str(days) + ".dat"
tail_file = "../data/wrk/death-tail" + str(test) + "-" + str(days) + ".dat"
makedat(input_file, output_file, tail_file, days, dts_format[test], delim[test], coldts=0, colinfected=None, colhealed=None,
        colactive=-3, limit=0.0, duration_R=5.0)

# CR cumulative infected
test=3  # cesko
days=14 # 14 day averaging
input_file= wrksrc + input_file_list[test]
output_file = "../data/wrk/cumulative" + str(test) + "-" + str(days) + ".dat"
tail_file = "../data/wrk/cumulative-tail" + str(test) + "-" + str(days) + ".dat"
makedat(input_file, output_file, tail_file, days, dts_format[test], delim[test], coldts=0, colinfected=None, colhealed=None,
        colactive=1, limit=0.0, duration_R=5.0)
