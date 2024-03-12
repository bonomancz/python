import random
import time

def genRandInt(interval) -> int:
    return random.randint(0, interval)


def getRandList(interval) -> list:
    return [genRandInt(interval) for _ in range(0, interval)]


def selectionSort(sortList) -> list:
    '''returns sorted list according selection sort algorithm'''
    listLen = len(sortList)
    insertionIndex = 0
    while insertionIndex <= listLen -1:
        minItem = sortList[insertionIndex]
        selectionIndex = insertionIndex
        for i in range(insertionIndex, listLen):
            if sortList[i] < minItem: # selection of smallest item
                minItem = sortList[i]
                selectionIndex = i
        sortList.insert(insertionIndex, sortList.pop(selectionIndex)) # insertion, sorting
        insertionIndex += 1
    return sortList


length = 500
unorderedList = getRandList(length)

#print(f"\n### Unordered list:\n{unorderedList}\n") 

startTime = time.time()
print(f"\n### Sorted list:\n{selectionSort(unorderedList)}")
endTime = time.time()
print(f"\nSorting duration: {round(endTime - startTime, 3)} [seconds]")
