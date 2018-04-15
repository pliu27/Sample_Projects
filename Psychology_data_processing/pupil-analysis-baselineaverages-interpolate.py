import pandas
import numpy
import math
import sys

def checkOnset(d):
    # Detect stimulus onsets
    if type(d) == type('asdf') and d[0:11] == 'SYNCTIME 16':
        return True
    return False

def checkOnset2(d): 
    # Detect onset of full outcome on focus rounds
    if type(d) == type('asdf') and d[0:11] == 'SYNCTIME 32':
        return True
    return False

def interpolateBlinks(trialData):
    # Linearly interpolate over blinks if there are any

    # this controls how many points immediately before
    # and immediately after a blink are discarded before
    # doing the interpolation
    nPtstoDitch = 50

    print(sum(numpy.isnan(trialData)))

    # Check for blinks
    if sum(numpy.isnan(trialData)) == 0:
        # There are no blinks
        return trialData
    elif sum(numpy.isnan(trialData)) > (1/5. * len(trialData)):
        # There is no data in this trial
        return []

    else:
        # There are blinks

        # Check to see if a trial begins with a blink
        if numpy.isnan(trialData[0]):
            for dIndx in range(len(trialData)):
                if not numpy.isnan(trialData[dIndx]): #check if a data point is a blink (look for the 1st point that is not a blink)
                    firstPoint = dIndx + nPtstoDitch
                    break
            trialData[0:firstPoint-1] = numpy.linspace(trialData[firstPoint], trialData[firstPoint], num=firstPoint-1)

        # Check to see if a trial ends with a blink
        if numpy.isnan(trialData[-1]):
            for dIndx in reversed(range(len(trialData))):
                if not numpy.isnan(trialData[dIndx]):
                    lastPoint = dIndx - nPtstoDitch
                    break
            trialData[lastPoint:-1] = numpy.linspace(trialData[lastPoint], trialData[lastPoint], num=len(trialData)-lastPoint)
            
        # Eliminate datapoints immediately before/after blink
        inblink = 0
        for dIndx in range(len(trialData)):
            datapoint = trialData[dIndx]
            if not inblink and numpy.isnan(datapoint):
                inblink = 1
                if dIndx - nPtstoDitch < 0:
                    firstPoint = 0
                else:
                    firstPoint = dIndx - nPtstoDitch
            if inblink and not numpy.isnan(trialData[dIndx]):
                inblink = 0
                if dIndx + nPtstoDitch > len(trialData):
                    lastPoint = len(trialData)-1
                else:
                    lastPoint = dIndx + nPtstoDitch
                # Interpolate!
                firstPointData = trialData[firstPoint]
                lastPointData = trialData[lastPoint]
                trialData[firstPoint:lastPoint+1] = numpy.linspace(firstPointData, lastPointData, num=(lastPoint-firstPoint)+1)

        if inblink:
            firstPointData = trialData[firstPoint]
            trialData[firstPoint:] = numpy.linspace(firstPointData, firstPointData, num=(len(trialData)-firstPoint)-1)

        return trialData


# Read in data

# Change the subject number
SN = 220
df = pandas.read_csv('PD'+str(SN)+'.xls', delimiter='\t', na_values='.')

# Set up data structures
tftPupilData = []
oddballPupilData = []
tftFPupilData = []
oddFPupilData = []
tftFPupilData2 = []
oddFPupilData2 = []
nTFT = 0.
nOddball = 0.
nTFTF = 0.
nOddF = 0.
nTFTF2 = 0.
nOddF2 = 0.
nSampPre = 1000
nSampPost = 1500


# Find all the "outcome" stimulus onsets
index = df['SAMPLE_MESSAGE'].index[df['SAMPLE_MESSAGE'].apply(checkOnset)]
index2 = df['SAMPLE_MESSAGE'].index[df['SAMPLE_MESSAGE'].apply(checkOnset2)]

# Loop through each onset and select the nSampPre samples before
# and the nSampPost samples after
firstTFT = 1
firstOdd = 1
firstTFTF = 1
firstOddF = 1
for i in index:
    trialData1 = df['LEFT_PUPIL_SIZE'].ix[i-nSampPre:i+nSampPost].astype(numpy.float).tolist()

    trialData = interpolateBlinks(trialData1)

    if not trialData == []:

        if df['cond'].ix[i] == 'tft':
            nTFT += 1
            if firstTFT:
                firstTFT = 0
                tftPupilData = numpy.array([trialData])
            else:
                tftPupilData = numpy.concatenate([tftPupilData, [trialData]])
        elif df['cond'].ix[i] == 'not':
            nOddball += 1
            #print(df['cond'].ix[index[0]])
            if firstOdd:
                firstOdd = 0
                oddballPupilData = numpy.array([trialData])
            else:
                oddballPupilData = numpy.concatenate([oddballPupilData, [trialData]])
        elif df['cond'].ix[i] == 'tft-focus':
            nTFTF += 1
            #print(df['cond'].ix[index[0]])
            if firstTFTF:
                firstTFTF = 0
                tftFPupilData = numpy.array([trialData])
            else:
                tftFPupilData = numpy.concatenate([tftFPupilData, [trialData]])
        elif df['cond'].ix[i] == 'not-focus':
            nOddF += 1
            #print(df['cond'].ix[index[0]])
            if firstOddF:
                firstOddF = 0
                oddFPupilData = numpy.array([trialData])
            else:
                oddFPupilData = numpy.concatenate([oddFPupilData, [trialData]])


#Get pupil data during full outcome on focus rounds
firstTFTF2 = 1
firstOddF2 = 1

for i in index2:
    trialData1 = df['LEFT_PUPIL_SIZE'].ix[i-nSampPre:i+nSampPost].astype(numpy.float).tolist()

    trialData = interpolateBlinks(trialData1)

    if not trialData == []:

        if df['cond'].ix[i] == 'tft-focus':
            nTFTF2 += 1
            #print(df['cond'].ix[index[0]])
            if firstTFTF2:
                firstTFTF2 = 0
                tftFPupilData2 = numpy.array([trialData])
            else:
                tftFPupilData2 = numpy.concatenate([tftFPupilData2, [trialData]])
        elif df['cond'].ix[i] == 'not-focus':
            nOddF2 += 1
            #print(df['cond'].ix[index[0]])
            if firstOddF2:
                firstOddF2 = 0
                oddFPupilData2 = numpy.array([trialData])
            else:
                oddFPupilData2 = numpy.concatenate([oddFPupilData2, [trialData]])


# Mask invalid data (e.g., data missing due to blinks)
tftMasked = tftPupilData
oddMasked = oddballPupilData
tftFMasked = tftFPupilData
oddFMasked = oddFPupilData
tftFMasked2 = tftFPupilData2
oddFMasked2 = oddFPupilData2

# Baseline each trial

# Change this variable to alter how far "back" the 
# baseline period extends prestimulus
nBaselineSamps = 1000

for i in xrange(len(tftMasked)):
    baselineAvg = numpy.mean(tftMasked[i][1000-nBaselineSamps:1000])
    tftMasked[i] = tftMasked[i] - baselineAvg
for i in xrange(len(oddMasked)):
    baselineAvg = numpy.mean(oddMasked[i][1000-nBaselineSamps:1000])
    oddMasked[i] = oddMasked[i] - baselineAvg
for i in xrange(len(tftFMasked)):
    baselineAvg = numpy.mean(tftFMasked[i][1000-nBaselineSamps:1000])
    tftFMasked[i] = tftFMasked[i] - baselineAvg
for i in xrange(len(oddFMasked)):
    baselineAvg = numpy.mean(oddFMasked[i][1000-nBaselineSamps:1000])
    oddFMasked[i] = oddFMasked[i] - baselineAvg
for i in xrange(len(tftFMasked2)):
    baselineAvg = numpy.mean(tftFMasked2[i][1000-nBaselineSamps:1000])
    tftFMasked2[i] = tftFMasked2[i] - baselineAvg
for i in xrange(len(oddFMasked2)):
    baselineAvg = numpy.mean(oddFMasked2[i][1000-nBaselineSamps:1000])
    oddFMasked2[i] = oddFMasked2[i] - baselineAvg

# Average across trials
tftAvg = tftMasked.mean(axis=0)
oddAvg = oddMasked.mean(axis=0)
tftFAvg = tftFMasked.mean(axis=0)
oddFAvg = oddFMasked.mean(axis=0)
tftFAvg2 = tftFMasked2.mean(axis=0)
oddFAvg2 = oddFMasked2.mean(axis=0)

# Log data

# probably want to change the file name here
f = open('PD'+str(SN)+'-baseinterp.csv', 'w')
f.write('t,TFT,odd,tftF,oddF, tftF2, oddF2\n')
for x,t,o,v,u, m, n in zip(range(-1000,2000+1),tftAvg, oddAvg, tftFAvg, oddFAvg, tftFAvg2, oddFAvg2):
    f.write(str(x)+',')
    f.write(str(t)+',')
    f.write(str(o)+',')
    f.write(str(v)+',')
    f.write(str(u)+',')
    f.write(str(m)+',')
    f.write(str(n)+',')
    f.write('\n')


