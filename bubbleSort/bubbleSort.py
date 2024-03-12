import random
import time

def genRandInt(interval) -> int:
    return random.randint(0, interval)


def getRandList(interval) -> list:
    return [genRandInt(interval) for _ in range(0, interval)]


def getMax(first, second):
    retVal = second
    if first > second:
        retVal = first
    return retVal


def bubbleSort(sortList) -> list:
    '''returns sorted list according bubble sort algorithm'''
    lstLen = len(sortList)
    haveToSort = True
    while haveToSort == True:
        nextIndex = 1
        haveToSort = False
        for currentIndex in range(0, lstLen - 1):
            if nextIndex <= (lstLen - 2):
                nextIndex = currentIndex + 1
                if(sortList[currentIndex] > sortList[nextIndex]): # sorting
                    haveToSort = True
                    sortList.insert(nextIndex, sortList.pop(currentIndex))
    return sortList


length = 100
unorderedList = getRandList(length)

#print(f"\n### Unordered list:\n\n{unorderedList}") 

startTime = time.time()
print(f"\n### Sorted list:\n{bubbleSort(unorderedList)}")
endTime = time.time()
print(f"\nSorting duration: {round(endTime - startTime, 3)} [seconds]")
