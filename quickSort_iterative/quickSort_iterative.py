import random
import time

def genRandInt(interval) -> int:
    return random.randint(0, interval)


def getRandList(interval) -> list:
    return [genRandInt(interval) for _ in range(0, interval)]


# pivot partitioning
def partition(inputList, low, high):
    pivot = inputList[high]
    i = low - 1
    
    for j in range(low, high):
        if inputList[j] <= pivot:
            i += 1
            inputList[i], inputList[j] = inputList[j], inputList[i]
    
    inputList[i + 1], inputList[high] = inputList[high], inputList[i + 1]
    return i + 1


# QS
def quickSort(inputList):
    if len(inputList) <= 1:
        return inputList
    
    tmpList = [(0, len(inputList) - 1)]
    
    while tmpList:
        low, high = tmpList.pop()
        pivot = partition(inputList, low, high)
        if pivot - low > 1:
            tmpList.append((low, pivot - 1))
        if high - pivot > 1:
            tmpList.append((pivot + 1, high))
    return inputList


length = 50
unorderedList = getRandList(length)
left = length - length
right = length - 1


#print(f"\n### Unordered list:\n{unorderedList}\n")
startTime = time.time()

### QUICKSORT ###
#print(f"Running quicksort on {length} items.")
#quickSort(unorderedList)
print(f"\n### Sorted list:\n{quickSort(unorderedList)}")

endTime = time.time()
print(f"\nSorting duration: {round(endTime - startTime, 3)} [seconds]")
