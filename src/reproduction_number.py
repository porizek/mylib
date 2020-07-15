import regress
import math
import datetime


def dts_decode(dts,mode):
    if mode == "epoch":
        result = datetime.datetime.fromtimestamp(int(dts))
    elif mode == "DMY":
        split =  list(map(int, dts.split("-"))) # split into integer list
        result = datetime.datetime(split[2],split[1],split[0])
    elif mode == "YMD":
        split = list(map(int, dts.split("-")))  # split into integer list
        result = datetime.datetime(split[0], split[1], split[2])

    return result

class Reprod:
    'class for calculationg the reproduction number from history of infection count'
    coldata = {"dts":0, "iso":1 , "day":2, "infect":3, "infect_ln": 4}
    colresult = {"dts": 1, "iso": 0, "day": 2, "k": 3, "r": 4 , "ka" : 5, "kb":6, "ra": 7, "rb":8 }
    ncolresult=5

    def __init__(self, ax, ay, formatdts="dts",limit=0.0, l=7.0, d=9.0,stdevkoef = 10.0):
        self.par_limit=limit
        self.par_l=l
        self.par_d=d
        self.stdevkoef=stdevkoef
        self.log=False
        self.data = []
        if len(ax) != len(ay):
            raise Exception("Linear regression: x is different size than y")

        self.start=dts_decode(ax[0],formatdts) # determine a start date - for now just from the first line of input

        for index, dts in enumerate(ax):
            record = [None] * len(Reprod.coldata)

            stamp = dts_decode(dts,formatdts)
            day = (stamp-self.start).total_seconds()/3600/24
            iso = stamp.strftime("%Y-%m-%dT%H:%M:%S")
            infect = ay[index]
            record[Reprod.coldata["dts"]] = dts
            record[Reprod.coldata["iso"]] = iso
            record[Reprod.coldata["day"]] = day
            record[Reprod.coldata["infect"]] = infect
            self.data.append(record)

    def R0(self,k):
        return 1 + k * (self.par_l + self.par_d) + k * k * self.par_l * self.par_d

    def calculate(self,running = 1):
        result_array = []
        if not self.log:
           for index , record in enumerate(self.data):
               infected = record[Reprod.coldata["infect"]]
               if infected > self.par_limit:
                   self.data[index][Reprod.coldata["infect_ln"]] = math.log(infected)
        if running == 1:  # single differencies calculation
            last = None
            for index, record in enumerate(self.data):
                if not self.data[index][Reprod.coldata["infect_ln"]] is None  :  #  calculated log value exists
                    if not last is None:
                        result = [None] * Reprod.ncolresult

                        infect_this = record[Reprod.coldata["infect_ln"]]
                        infect_prev = self.data[last][Reprod.coldata["infect_ln"]]
                        day_this = record[Reprod.coldata["day"]]
                        day_prev = self.data[last][Reprod.coldata["day"]]
                        k = (infect_this - infect_prev) / (day_this - day_prev)
                        r = self.R0(k)

                        result[Reprod.colresult["dts"]] = record[Reprod.coldata["dts"]]
                        result[Reprod.colresult["iso"]] = record[Reprod.coldata["iso"]]
                        result[Reprod.colresult["day"]] = day_this
                        result[Reprod.colresult["k"]] = k
                        result[Reprod.colresult["r"]] = r
                        result_array.append(result)
                    last=index
            return result_array
        elif running > 2:
            stat = regress.Regress()
            first = []
            for index, record in enumerate(self.data):
                if not self.data[index][Reprod.coldata["infect_ln"]] is None  :  #  calculated log value exists
                    infect= record[Reprod.coldata["infect_ln"]]
                    day= record[Reprod.coldata["day"]]
                    stat.add(day,infect)
                    first.append([day,infect])
                    if stat.n >= running:
                        result = [None] * len(Reprod.colresult)
                        reg = stat.fiterr()
                        k=reg["a"]
                        ka= k - self.stdevkoef * reg["da"]
                        kb= k + self.stdevkoef * reg["da"]
                        r = self.R0(k)
                        ra = self.R0(ka)
                        rb = self.R0(kb)
                        result[Reprod.colresult["dts"]] = record[Reprod.coldata["dts"]]
                        dayavg = stat.sx / stat.n
                        result[Reprod.colresult["day"]] = dayavg
                        stampavg = self.start + datetime.timedelta(dayavg)
                        isoavg = stampavg.strftime("%Y-%m-%dT%H:%M:%S")
                        result[Reprod.colresult["iso"]] = isoavg
                        result[Reprod.colresult["k"]] = k
                        result[Reprod.colresult["r"]] = r
                        result[Reprod.colresult["ka"]] = ka
                        result[Reprod.colresult["ra"]] = ra
                        result[Reprod.colresult["kb"]] = kb
                        result[Reprod.colresult["rb"]] = rb
                        result_array.append(result)
                        # remove first element from statistic
                        day_first,infect_first=first.pop(0)
                        stat.sub(day_first,infect_first)
            return result_array







