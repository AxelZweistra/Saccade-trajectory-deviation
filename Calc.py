import os # for walking through folders
import fnmatch # for matching filenames
import numpy as np
import scipy as sp
import pandas as pd
from scipy import io
from matplotlib import pyplot as plt

#%%
datafold = (r'C:\Users\Axelz\OneDrive\Bureaublad\Jaar 3 Psychologie\Scriptie\data')
matches = []
FixPos = (840,525)
CClist = [1,1,2,2,1,2,1,2,1]
OutPut = np.zeros((1,8))
plt.figure()


#%%
for root, dirnames, filenames in os.walk(datafold):
    for filename in fnmatch.filter(filenames,"*.mat"):
        matches.append(os.path.join(root, filename))

NTrials = np.zeros((len(matches),7))

for a in range(0,len(matches)):       
    data = sp.io.loadmat(matches[a])                    #load .m file into dict object
    df = pd.DataFrame(data['Exp'][0,:])                 #create pandas dataframe
    arr = df.to_numpy()                                 #converts dataframe to numpy array
    columnnames = list(df)                              #creates list of data headers

    for b in range(0,len(columnnames)):                 #creates seperate arrays from data headers
        c = columnnames[b]
        vars()[c] = arr[0,b]
    
    ##############################################- Selectiecriteria
    
    Data = DataMatrix
    
    if len(np.unique(Data[:,0])) < len(Data[:,0]):      # test for duplicates
 
        if np.sum(np.where(Data[:,0] == 1)) > 0 :       # test if index 1 occurs more than once

            d = np.array(np.where(Data[:,0] == 1))      # find indices of 1
            d = int(d[d>1])
            Data = Data[d:,:]                           # remove practice trials
    
    NTrials[a,0] = len(Data[:,0])                       #amount of trials before selection index 0
            
    Data = Data[Data[:,5] > 80]                         #latency boven 80ms  
    NTrials[a,3] = len(Data[:,0]) / NTrials[a,0]        #selectiepercentage na latency 80 index 3
    Data = Data[Data[:,5] < 400]                        #latency onder 400ms
    NTrials[a,4] = len(Data[:,0]) / NTrials[a,0]        #selectiepercentage na latency 400 index 4
    Data = Data[Data[:,6] < 1]                          #blink verwijderen
    Data = Data[abs(FixPos[0] - Data[:,11]) < 50]       # removing if startx is further than 50 px from fix
    Data = Data[abs(FixPos[1] - Data[:,12]) < 50]       # idem, for Y
    NTrials[a,5] = len(Data[:,0]) / NTrials[a,0]        #selectiepercentage na fix dist index 5
    Data = Data[Data[:,15] > 4]                         # amp boven 4
    NTrials[a,6] = len(Data[:,0]) / NTrials[a,0]        #selectiepercentage na amp index 6

    DataL = Data[Data[:,1] == 1]                        #create seperate array for left targets
    DataLDir = DataL[(DataL[:,30:35] < 840).all(1)]     #includes if all samples t=10:15 are closer to target than fixationcross    
    DataR = Data[Data[:,1] == 2]                        #create seperate array for right targets
    DataRDir = DataR[(DataR[:,30:35] > 840).all(1)]     #includes if all samples t=10:15 are closer to target than fixationcross
    Data = np.concatenate((DataLDir,DataRDir),0)        #adds arrays together again
    
    NTrials[a,1] = len(Data[:,0])                       #amount of trials after selection index 1
    NTrials[a,2] = NTrials[a,1] / NTrials[a,0]          #percentage index 2
    
    #%%       Declaring outcome matrices
    
    OutputMatrix = np.zeros((len(Data[:,0]),len(Data[0,:])-120))
    OverallDeviation = np.zeros((len(Data[:,0]),1))
    InitialDirection = np.zeros((len(Data[:,0]),1))
    Participant = np.zeros((len(Data[:,0]),1))
    Phase = np.zeros((len(Data[:,0]),1))
    ConditionedColour = np.zeros((len(Data[:,0]),1))
    CSplus = np.zeros((len(Data[:,0]),1))
    
    #%%       Mirroring
    
    for e in range(0,len(Data[:,0])):                            #for trials
        if Data[e,1] == 1:                                       #if target is left
            Data[e,7] = 1289                                     #change targetx to right position
            Data[e,11] = 840 +  (840 - Data[e,11])               #mirror ssaccx
            Data[e,13] = 840 + (840 - Data[e,13])                #mirror essaccx
            
            for g in range(0,100):                               #for x samples
                if Data[e,20+g] != 0:                            #if sample is not 0
                    Data[e,20+g] = 840 + (840 - Data[e,20+g])    #mirrors the x samples
            
        if Data[e,1] == 2 and Data[e,3] == 2:                    #if target is originally right and dis is down
        
            Data[e,12] = 525 - (Data[e,12] - 525)                #mirror ssaccy
            Data[e,14] = 525 - (Data[e,12] - 525)                #mirror ssaccy
            
            for h in range(0,59):                                #for y samples
                if Data[e,120+h] != 0:                           #if the sample is not 0
                    Data[e,120+h] = 525 - (Data[e,120+h] - 525)  #mirrors y samples
                    
        if Data[e,2] == 1:                                       #if distractor is close
            Data[e,9], Data[e,10] = 1274, 409                    #set distractor to upperright close position
        if Data[e,2] == 2:                                       #if distractor is remote 
            Data[e,9], Data[e,10] = 1129, 181                    #set distractor to upperright remote position   
        if Data[e,2] == 3:                                       #if distractor is absent
            Data[e,9], Data[e,10] = np.nan, np.nan               #set distractor values to NaN
            
        #%%%    Plotting
        # nx = (len(Data[0,:]) - 120) + 20                         #fixes x sample length
        # samplex = Data[:,20:nx]
        # samplex[samplex == 0 ] = np.nan       
        # sampley = Data[:,120:]
        # sampley[sampley == 0 ] = np.nan
        
        # plt.clf()
        # plt.plot(samplex[e], sampley[e])           #saccade
        # plt.plot(Data[e,7],Data[e,8],'ro')         #target
        # plt.plot(FixPos[0],FixPos[1],'k+')         #fixation cross
        
        # if Data[e,4] == 2: 
        #     plt.plot(Data[e,9],Data[e,10],'bo')                     #blue distractor
        # if Data[e,4] == 1:
        #     plt.plot(Data[e,9],Data[e,10],'o',color = 'orange')     #orange distractor
        
        # plt.title(str(matches[a][68:81]) + ' - Trial: ' + str(e+1))
        # plt.xlim([0,1680])
        # plt.ylim([0,1050])
        # plt.gca().invert_yaxis()
        # plt.show()
        #%% Calculating deviation
        
        for z in range(0,len(Data[0,:])-121):                        #for y samples (n-y changes every datafile)
            if Data[e,20+z] == Data[e,13] and Data[e,120+z] == Data[e,14]:
                break
       
            DeltaX = Data[e,13] - Data[e,11]                         #check, deltax for ssaccx and essaccx
            DeltaY = Data[e,14] - Data[e,12]                         #check, deltay for ssaccy and essaccy
            SideA = np.sqrt((DeltaX**2) + (DeltaY**2))
        
            DeltaX = Data[e,20+z] - Data[e,11]                       #check, deltax for ssaccx and samplex
            DeltaY = Data[e,120+z] - Data[e,12]                      #check, deltay for ssaccy and sampley
            SideB = np.sqrt((DeltaX**2) + (DeltaY**2))
        
            DeltaX = Data[e,13] - Data[e,20+z]                       #check, deltax for essaccx and samplex
            DeltaY = Data[e,14] - Data[e,120+z]                      #check, deltay for essaccy and sampley
            SideC = np.sqrt((DeltaX**2) + (DeltaY**2))        

            try:
                fraction = (SideA**2 + SideB**2 - SideC**2) / (2 * SideA * SideB)
                np.degrees(np.math.acos(fraction))
            except:
                OutputMatrix[e,z] = np.nan
                print(str(matches[a][68:81]) + ' - Trial: ' + str(e+1) + ' - Sample: ' + str(z))
            else:
                fraction = (SideA**2 + SideB**2 - SideC**2) / (2 * SideA * SideB)
                OutputMatrix[e,z] = np.degrees(np.math.acos(fraction))
        
        OutputMatrix[OutputMatrix == 0] = np.nan
        OverallDeviation[e] = np.nanmean(OutputMatrix[e,:])   
        InitialDirection[e] = np.nanmean(OutputMatrix[e,:11]) #uses the first 11 datapoints as index 0 is always NAN
        Participant[e] = int(matches[a][68:70])
        
        if matches[a][70:72] == 'pr':                         #following encodes pre or post conditioning: pre = 0, post = 1
            Phase[e] = 0
        if matches[a][70:72] == 'po':
            Phase[e] = 1
            
        ConditionedColour[e] = CClist[int(matches[a][69:70])-1]
        
        if ConditionedColour[e] == Data[e,4]:
            CSplus[e] = 1
            
        if Data[e,4] == 3:
            CSplus[e] = 3
        
    # Making outputarray, see word file for indexing    
    DataAppend = np.stack((Participant[:,0],Phase[:,0],ConditionedColour[:,0],Data[:,4],Data[:,0],Data[:,2],OverallDeviation[:,0], InitialDirection[:,0]), axis=1)    
    OutPut = np.concatenate((OutPut,DataAppend), axis = 0)
    
np.savetxt('Datafile.csv', OutPut, delimiter = ',', fmt='%f' )
    