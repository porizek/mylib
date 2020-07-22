import math

class Regress:
    'Class for linear regression'

    def add(self,x,y):
        """add point (x,y) to the regression statistics"""
        self.n += 1
        self.sx += x
        self.sy += y
        self.sxx += x * x
        self.syy += y * y
        self.sxy += x * y


    def sub(self,x,y):
        """subtract point (x,y) from the regression statistics (for running regression feature)"""
        self.n -= 1
        self.sx -= x
        self.sy -= y
        self.sxx -= x * x
        self.syy -= y * y
        self.sxy -= x * y

    # add multiple points from vectors vx,vy to the regression statistics
    def addv(self,vx,vy):
        if len(vx) != len(vy):
            raise Exception("Linear regression: x is different size than y")
        for iter in range(len(vx)):
            x=vx[iter]
            y=vy[iter]
            self.add(x,y)


    def __init__(self, vx=[], vy=[]):
        self.n = 0.0
        self.sx = 0.0
        self.sy = 0.0
        self.sxx = 0.0
        self.syy = 0.0
        self.sxy = 0.0
        self.addv(vx,vy)

    # fir - do simple regression, calculate a,b
    def fit(self):
        a=(self.n*self.sxy-self.sx*self.sy)/(self.n*self.sxx-self.sx*self.sx)
        b=(self.sy-a*self.sx)/self.n
        return (a,b)

    # extrapolate : calculate a value on the regression line for a given x
    def valuefn(self,x):
        (a,b)=self.fit()
        return a*x+b

    # interseption : calculate the x-value of the interseption point for given y
    def intercept(self,y):
        (a,b)=self.fit()
        return (y-b)/a

    # fit - complex calculation of R and coeficients deviations - a dictionary object is returned
    def fiterr(self):
        n = self.n
        sx = self.sx
        sxx = self.sxx
        sy = self.sy
        syy = self.syy
        sxy = self.sxy

        (a,b) = self.fit()
        # correlation coeficient rxy
        try:
            rxy = (n*sxy - sx*sy)
            rxy2 = rxy*rxy / (n*sxx - sx*sx) / (n*syy - sy*sy)
            rxy = math.sqrt(rxy2)
        except (ZeroDivisionError,ValueError):
            rxy2 = None
            rxy = None
        # dee = b*b*n + a*a*sxx - 2*a*sx*sy + syy + 2*a*b*sx - 2*b*sy
        # daa = n/(n-2) * dee/(n*sxx - sx*sx)
        try:
            dee = (n*syy - sy*sy - a*a*(n*sxx - sx*sx))/n/(n-2)
            daa = n*dee/(n*sxx - sx*sx)
            dbb = daa * sxx / n
            da = math.sqrt(daa)
            db = math.sqrt(dbb)
        except (ZeroDivisionError,ValueError):
            dee = None
            daa = None
            dbb = None
            da = None
            db = None
        result = {
            "a":a,
            "b":b,
            "da":da,
            "db":db,
            "daa":daa,
            "dbb":dbb,
            "n": n,
            "dee": dee,
            "rxy2": rxy2,
            "rxy": rxy
        }
        return result

    # print the regression details in the xmgrace linear regression style
    def details_xmgrace(self):
        result = self.fiterr()
        n=result["n"]
        sx=self.sx
        sy=self.sy
        a=result["a"]
        b=result["b"]

        print(
"Number of observations			 = %d\n"
"Mean of independent variable	 = %8f\n"
"Mean of dependent variable		 = %8f\n"
"Standard dev. of ind. variable	 = %8f\n"
"Standard dev. of dep. variable	 = %8f\n"
"Correlation coefficient		 = %8f\n"
"Regression coefficient (SLOPE)	 = %8f\n"
"Standard error of coefficient	 = %8f\n"
"t - value for coefficient		 = N/A\n"
"Regression constant (INTERCEPT) = %8f\n"
"Standard error of constant		 = %8f\n"
"t - value for constant			 = N/A\n"
            % (n,sx/n,sy/n,
               math.sqrt(n*self.sxx - sx*sx)/n,
               math.sqrt(n*self.syy - sy*sy)/n, result["rxy"], a, result["da"], b, result["db"]))
        print(
"\n"
"Analysis of variance\n"
"Source		 d.f	 Sum of squares	 Mean Square	 F\n"
"Regression	   1	N/A              N/A  	         N/A\n"
"Residual	   %d	%8f	     %8f\n"
"Total		   %d	N/A\n"
            % (n-2, n*result["dee"], result["dee"], n-1) )
        print("y = %6f %+6f * x" % (result["b"], result["a"]))





