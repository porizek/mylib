
# zdroj: https://mapa.covid.chat/export/csv
# zdroj: https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/nakazeni-vyleceni-umrti-testy.csv

mypath=~/PycharmProjects/pythonProject/mylib
# cd /cygdrive/d/rado/python/mylib/

cd $mypath/data/wrk
wget http://mapa.covid.chat/export/csv &&  mv csv korona.gov.sk.csv
mv nakazeni-vyleceni-umrti-testy.csv nakazeni-vyleceni-umrti-testy.bak
wget https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/nakazeni-vyleceni-umrti-testy.csv
cd $mypath/test
python3 reproduction_number-test.py
cd $mypath/data/wrk

#slovensko
# http://mapa.covid.chat/export/csv
#cd /cygdrive/d/rado/python/mylib/data/wrk
    xmgrace -nxy reproduction_number-test2-14.dat -nxy reproduction_number-test2-7.dat -nxy reproduction_number-test2-4.dat -nxy reproduction_number-test2-1.dat -nxy reproduction_number-test-tail2-14.dat -p ../cfg/reproduction_number-test6.par

#cesko
# https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/nakazeni-vyleceni-umrti-testy.csv
# cd /cygdrive/d/rado/python/mylib/data/wrk
  xmgrace -nxy reproduction_number-test3-14.dat -nxy reproduction_number-test3-7.dat -nxy reproduction_number-test3-4.dat -nxy reproduction_number-test3-1.dat -nxy reproduction_number-test-tail3-14.dat -p ../cfg/reproduction_number-test6.par

# test only
#
#&
#./cfg/
awk '{print $1, $4, $4-0.01, $4-0.02}'  reproduction_number-test2-14.dat > growthrate-ruska.dat
xmgrace -nxy  growthrate-ruska.dat -block reproduction_number-test3-14.dat  -bxy 1:4 -p ../cfg/growth-rate-cs.par

#
#2020-03-25T12:00:00 0.09186639031190973 0.0818664 0.0718664
#cat > robopol2.dat

# death growth rate
xmgrace
