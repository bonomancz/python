import random
import time

def genRandInt(interval) -> int:
    return random.randint(0, interval)


def getRandList(interval) -> list:
    return [genRandInt(interval) for _ in range(0, interval)]


def quickSort(sortList) -> list:
    if len(sortList) <= 1:
        return sortList
    pivot = sortList[len(sortList) - 1]
    left = [x for x in sortList if x < pivot]
    right = [x for x in sortList if x > pivot]
    middle = [x for x in sortList if x == pivot]
    return quickSort(left) + middle + quickSort(right)


length = 20
unorderedList = getRandList(length)
left = length - length
right = length - 1


print(f"\n### Unordered list:\n{unorderedList}\n")
startTime = time.time()

### QUICKSORT ###
print(f"\n### Sorted list:\n{quickSort(unorderedList)}")

endTime = time.time()
print(f"\nSorting duration: {round(endTime - startTime, 3)} [seconds]")
