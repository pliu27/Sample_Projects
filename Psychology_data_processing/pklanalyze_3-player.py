import pickle, sys
from scipy import mean

subs = [3, 7, 9, 11, 13, 15, 17, 19, 23, 25, 27, 35, 45, 49, 53, 57, 2, 4, 6, 8, 10, 12, 14, 16, 20, 22, 24, 30, 34, 42, 44, 46, 56, 89]      #subject numbers
for s in subs: #for each subject,
    fn = 'PD_3-player' + str(s) +'.pkl'      #generate the file name for that subject
    #print(fn)       #print the file name, so that you can see which file is being processed at any point
    f = open(fn,'r') #open the file for the subject
    expData = pickle.load(f) #load subjects data into this program
    f.close() #close file

    numTrials = 90
    lastN = 10

    hiChoices = []
    loChoices = []

    if s % 2 == 1:
        for i in range(80, 90):
            if expData[i]['opp'] == 1:
                highOpp = expData[i]['choice']
                #print(highOpp)
                hiChoices.append(expData[i]['choice'])
            elif expData[i]['opp'] == 2:
                lowOpp = expData[i]['choice']
                #print(lowOpp)
                loChoices.append(expData[i]['choice'])
    elif s % 2 == 0: 
        for i in range(80, 90):
            if expData[i]['opp'] == 2:
                highOpp = expData[i]['choice']
                #print(highOpp)
                hiChoices.append(expData[i]['choice'])
            elif expData[i]['opp'] == 1:
                lowOpp = expData[i]['choice']
                #print(lowOpp)
                loChoices.append(expData[i]['choice'])
    else:
        print('Something went wrong')

    sys.stdout.write(str(s) + '\thi\t')
    if len(hiChoices) > 0:
        sys.stdout.write(str(float(sum(hiChoices))/len(hiChoices)))
    else:
        sys.stdout.write('.')
    sys.stdout.write('\tlo:\t')  #'float' is to make the number not integer (in the form of one decimal digit)
    if len(loChoices) > 0:
        sys.stdout.write(str(float(sum(loChoices))/len(loChoices) ))
    else:
        sys.stdout.write('.')
    sys.stdout.write('\n')
pass

#fn = 'file name.pkl'
#f = open(fn,'r') #'r' means read mode, 'a' means append, 'w' means write, etc
#allTrials = pickle.load(f)
#print allTrials[0]['RT'] #prints the reaction time of the first trial
#print allTrials[5]['response'] #prints the response from the sixth trial
#
#for i in range(1,len(allTrials)): #starts at second trial
#if allTrials[i-1]['response'] == 1: