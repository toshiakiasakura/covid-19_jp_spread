import numpy as np 
import pandas as pd
import japanmap as jm
import matplotlib
import matplotlib.pyplot as plt
import datetime
# custom modules
import pathList as pL

def getPossibleAreas(C0):
    ind0 = list(np.where(C0 ==0)[0]) # delete areas already with reported cases
    ind0.remove(0)
    for l in pL.notIn.values(): # delete areas with no airport.
        if l in ind0:
            ind0.remove(l)
    return(ind0)

def getEnterProbPref(prefInd,d):
    outputs, *_,tCutoff, nSim = d.values()

    tLine = np.linspace(0,tCutoff,tCutoff+1)
    casePref = np.zeros(shape=(0,len(tLine)))

    for out in outputs:
        inds = []
        cases ,ts =  out.values()
        for t in tLine:
            ind = np.argmin(abs(ts-t))
            inds.append(ind)
        case = cases[np.array(inds),prefInd]
        casePref = np.vstack((casePref,case))
    entProbPref = (casePref > 0).sum(axis=0)/nSim
    return(tLine,entProbPref)    

def timeSeriesProb(ind0,d):
    n = len(ind0)

    fig = plt.figure(figsize=(5,n),dpi=150)
    igfont = {"family":"IPAPGothic" }

    for i,prefInd in enumerate(ind0):
        t,prob = getEnterProbPref(prefInd,d)
        prefName  = jm.pref_names[prefInd]
        
        if i ==0  :
            ax1 = fig.add_subplot(n,1,i+1 )
            ax = ax1 
        else:
            ax = fig.add_subplot(n,1,i+1 ,sharex=ax1)
        ax.plot(t,prob)
        ax.set_ylabel(f"{prefName}",**igfont)
        ax.set_ylim([0,0.4])
        if prefInd not in  [31,46]:
            ax.tick_params(labelbottom=False)

    plt.tight_layout()
    plt.show()

def getEnterProb(tExt,d):
    "get prob. of new infections at date 'tExt'."     
    outputs, *_,tCutoff, nSim = d.values()
    if tCutoff < tExt :
        raise ValueError(f"tExt is {tExt}, tCutoff is {tCutoff}")
        
    caseTs  = np.zeros(shape=(0,48))
    for out in outputs:
        cases ,ts =  out.values()
        index  = np.argmin( abs(np.array(ts) - tExt ) )
        case = cases[index]
        caseTs = np.vstack((caseTs,case))
        
    enterProb = (caseTs>0).sum(axis=0)/nSim
    return(enterProb)

def japanVis(v_,tExt,savePath =None,notInList={}):
    # figure setting 
    plt.rcParams['figure.figsize'] = 8, 8
    plt.rcParams['figure.dpi'] = 250
    # add colormap 
    gray = plt.get_cmap("gray")
    cmap = plt.get_cmap('tab20c')  
    norm = matplotlib.colors.Normalize(vmin=0, vmax=1)
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    plt.colorbar(sm)

    # picture() がnumpy.uint8型を受け付けないみたいなのでintに変換
    def tint(t):
        return tuple(int(_) for _ in t)
    d_ = {}
    for i in range(1,48):
        if v_[i] == 0:
            if i in notInList.values():
                d_[i] = tint(gray(0,bytes=True)[:3])
            else:
                d_[i] = tint(cmap(v_[i],bytes=True)[:3])
        else:
            d_[i] =tint(cmap(v_[i],bytes=True)[:3])
    plt.imshow(jm.picture(d_))
    date = pL.baseDate + datetime.timedelta(days=tExt)
    date = date.strftime("%Y/%m/%d")

    # 不要なティックやラベルを削除する
    plt.tick_params(bottom=False, top=False, left=False, right=False,
                    labelbottom=False, labeltop=False, labelleft=False, labelright=False)
    plt.title(f"Date is {date}.")
    plt.xlabel(f"Black colored areas do not have airport.\nGray colored areas have already reported cases.")
    if savePath:
        plt.savefig(savePath, bbox_inches="tight")
        
    plt.show()
    print("-"*100)
