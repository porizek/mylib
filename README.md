mylib
=====

Author: Radoslav Porizek

mylib is my math library.
Recomended application: xmgrace for plotting graphs

Linear regression
=================

I write a code for calculating linear regresssion myself,
as I was too lazy to understand how to use  extrenal libraries like sklearn.linear_model
It allows also to do "running linear average" = add and subtract points from the set for linear regression.

The linear regression is calculated from the statistic values stored in class Regress.

Methods:
--------
* **Regress** - constructor 
* **add**/**addv** - add point/vector of points to Regress
* **sub** - remove point from Regress
* **fit** - single regression, returns [a,b]  
coeficients of the regression line y=a*x+b
* **fiterr** - detailed regression, returns [a,b] coeficients,
 their standart error, correlation coefficent R and anothers.
* **value** - calculate y for given x, y=a*x+b
* **intercept** - calculate x, for given Y, y=a*x+b
* **details_xmgrace** show regression results 
    in the format of xmgrace application
    
Testing
-------
The code has been tested on this 
[wiki example](https://www.immagic.com/eLibrary/ARCHIVES/GENERAL/WIKIPEDI/W120619S.pdf)
, the test script is `test/regress-test.py`    

Reproduction Number
===================

The COVID-19 is nowhere calculated the way, which I want: 
with error interval,
average from several days and with provided infectious period parameter, on which reproduction number dependent.
The only exception is publication from
[Centre for Mathematical Modelling of Infectious diseases](https://cmmid.github.io/topics/covid19/global-time-varying-transmission.html)
, but this one is not up-to-date (Feb+March data).

The eproduction number is calculated from SEIR model is:
R = 1 + k \* (l+d) + k\*k\*l\*d
where:  
l is _latent period_  - infected but not infectious  (default value 7)
d is _infectious period_ (default value 9)
Sources e.g. [wiki](https://en.wikipedia.org/wiki/Basic_reproduction_number)

Other articles:
[Estimating epidemic exponential growth rate and basic reproduction number](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6962332/)  

Methods:
--------
* **Reprod** constructor for loading data and parameters
* **calculate(days)** return reproductions numbers values with growth rate + the error intervals  
  _days_ is number of days for averaging
* **R0** (internal) - calculate reproduction number R from the groth rate
* ***dts_decode*** (internal) for decoding various time formats like _epoch_, _DMY_ and _YMD_
  
Testing:
--------
Test script _reproduction_number-test_ is producing data files of reproduction number in a format which can be plotted in xmgrace application.
_out_ dir is for fixed input testing, while _wrk_ is designed to download fresh files:  
`korona.gov.sk.csv`  and `nakazeni-vyleceni-umrti-testy.csv`  
whose can updated from 
[slovak](https://mapa.covid.chat/export/csv) and [czech](https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/nakazeni-vyleceni-umrti-testy.csv) web pages of ministry of health.

The graphs can be plotted in xmgrace application, see `bin/make.sh` for commnads.

  


