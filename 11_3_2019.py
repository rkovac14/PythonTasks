#sample input file:

#id1 -> id2
#abc 256
#def 123
#id2 -> id3
#256 A
#123 B

#Imports needed for the code to function. ctypes enables you to interface with windows DLL files
#which output integers compatible with C language. os.path enables you to check for a directory
#or a file like out.txt and verify if it exists. sys allows you to exit the script before its
#finished, for example when you receive an error
import ctypes
import os.path
import sys

#These are for the popup windows, you can use a combination of these to achieve the desired popup
#windows style and functionality:
MB_OKCXL = 0x01 #this one tells the window to include OK and Cancel buttons
STOP_ICO = 0x030 #this one includes a STOP icon
EXCL_ICO = 0x040 #this one includes an exclamation mark icon

#this block of code tries to open the input file and if it does not exist (or in coding language
#you get an exception) it calls a popup window and terminates the code
try:
    with open("in.txt", "r") as f:
        data = f.read().splitlines()
except IOError:
    ctypes.windll.user32.MessageBoxW(0, "Aborting ...", "Input file does not exist !",STOP_ICO)
    sys.exit()

#this function checks if the file out.txt exists and if it does, it calls a popup window with an
#option to either abort or continue
def checkOut():
    if os.path.isfile("out.txt") is True:
        out = ctypes.windll.user32.MessageBoxW(0, "Press OK to append or Cancel to abort.", "out.txt already exists!",
                                               MB_OKCXL | STOP_ICO)
        if out is 2:
            sys.exit()
        else:
            writeOut("\n")

#a very simple function that writes its calling variable (inString) into the output file
def writeOut(inString):
    with open("out.txt", "a") as f:
        f.write(inString)

#another very simple function that counts and returns the number of entries we will be looking
#a pair for (i.e. the id1 -> id2 group)
def parsAm(dataIn):
    counter = 0
    for x in dataIn:
        if x == 'id1 -> id2':
            continue
        if x == 'id2 -> id3':
            break
        else:counter +=1
    return counter

#this function is fed the global input file (the variable "data") and the number of entries
#that need a pair-searching. It basically counts the characters of every line until it finds
#a free space and feeds everything before said free space into the next function for content
#checking plus it takes everything *after* the free space and feeds that into the next
#function so it can be written into the output file later. It also keeps track of how many
#entries have been written to the output file.
def parsFin(dataIn, dataLenLoc):
    track1 =-1
    locNum =0
    for x in dataIn:
        track2 =0
        track1 +=1
        if track1 == dataLenLoc+1:
            break
        if track1 == 0:
             continue
        for i in x:
            track2 +=1
            if i == ' ':
                break
        locNum += checkForContents(x[track2:], data, x[:track2])
    return locNum

#the main function that receives the main dataset, the string that has to be looked for and
#a passthrough value for later use. First it goes entry by entry in the input list to look
#for the "id2 -> id3" string. This it the position from which the looking up needs to be
#done. Next it goes through all the entries that come after the afformentioned string and looks for one
#that contains a match of a string that has to be looked for. Then it isolates the position of the entry
#that has to be matched to the said string and prints the passthrough file as well as the entry it was
#searching for. It also keeps track of many matches occured. This value is passed over to the previous
#function
def checkForContents(dataIn, dataSet, LookedUp):
    dostuff = False
    entriesPrinted =0
    for x in dataSet:
        if x == 'id2 -> id3':
            dostuff = True
            continue
        if dostuff is True:
            track3 = 0
            if x[:len(dataIn)] == dataIn:
                for i in x:
                    track3 += 1
                    if i == ' ':
                        break
                writeOut(LookedUp)
                writeOut(x[track3:])
                writeOut("\n")
                entriesPrinted +=1

    return entriesPrinted

#call for the checkout function
checkOut()

#call for the writeout function
writeOut("id1 -> id3\n")

#calls for the parsAm() and parsFin() function
dataLen = parsAm(data)
val = parsFin(data, dataLen)

#a simple pop-up call that informs the user about how many entries have been written to the output file
ctypes.windll.user32.MessageBoxW(0, str(val) + " entries have been written", "Done processing", EXCL_ICO)

