import numpy as np 
import pandas as pd
import dill
from datetime import datetime
from codetiming import Timer



def rexp(r):
    delt = -np.log(np.random.uniform(0,1))/r
    return(delt)

def increamentOne(array,index):
    array = array
    array[index] += 1 
    return(array)

class gillespie():
    def __init__(self,r,p,C0,tCutoff = 5 ):
        self.r = r
        self.p = p
        self.C = np.zeros(shape=(1,48)) # index 0 is none
        self.C[0,:] = C0
        self.t = [0]

        self.eventTypes = [i for i in range(48)]
        self.tCutoff = tCutoff

    def oneIte(self,index=0):
        Ct = self.C[index,:].copy()
        rates = self.r*( self.p @ Ct)
        totRate = np.sum(rates)
        pEvent = [i/totRate for i in rates]
        event = np.random.choice(self.eventTypes,size=1,p=pEvent)[0]
        delt = rexp(totRate)
        self.t.append(self.t[-1]+delt)

        Cnext = increamentOne(Ct,event)
        self.C = np.vstack((self.C,Cnext))
    
    def oneSim(self):
        index = 0
        while self.t[-1] <self.tCutoff:
            self.oneIte(index)
            index += 1 

def multiSim(nSim, r,p,C0,tCutoff,time=False):
    record = dict(outputs=[],r=r,p=p,C0=C0,tCutoff=tCutoff,nSim=nSim)
    for i in range(nSim):
        if time:
            with Timer():
                sim = gillespie(r,p,C0,tCutoff)
                sim.oneSim()
                record["outputs"].append( dict(case=sim.C,time=sim.t))
        else:
            sim = gillespie(r,p,C0,tCutoff)
            sim.oneSim()
            record["outputs"].append( dict(case=sim.C,time=sim.t))
    return(record)

def saveData(rec,path):
    date = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = path + date + ".dl"
    with open(path,"wb") as f:
        dill.dump(rec,f)
    return(path)
