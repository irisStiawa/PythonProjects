# from randomlist import myList10k as myList  #randomlist.py in discord oder .txt in murad-community
from time import time
myList = [12, 5, 18, 17, 12, 16, 3, 1, 3, 19, 19, 8, 20, 20, 6, 8, 2, 18, 18, 6]

def bubbleSort(myList):
    for k in range(len(myList)-2):
        for i in range(len(myList)-k-1):
            if myList[i] > myList[i+1]:
                myList[i], myList[i+1] = myList[i+1], myList[i]            
    return myList

def selectionSort(myList):
    for staticIndex in range(len(myList)-1):
        minimum = staticIndex
        for movingIndex in range(staticIndex+1, len(myList)):
            if myList[movingIndex] < myList[minimum]:
                minimum = movingIndex
        myList[staticIndex], myList[minimum] = myList[minimum], myList[staticIndex]         
    return myList

def insertionSort(myList):
    for movingIndex in range(1,len(myList)):        
        poppedElement = myList.pop(movingIndex)
        indexToCompare = movingIndex - 1        
        while poppedElement < myList[indexToCompare] and indexToCompare >= 0:
            indexToCompare -= 1        
        myList.insert(indexToCompare + 1, poppedElement)    
    return myList

def mergeSort(myList):
    if len(myList) > 1:
        middle = len(myList)//2
        leftHalf = myList[:middle] 
        rightHalf = myList[middle:]
 
        mergeSort(leftHalf)
        mergeSort(rightHalf)
 
        leftIndex = rightIndex = indexToFill = 0
        
        while leftIndex < len(leftHalf) or rightIndex < len(rightHalf):
            if leftIndex < len(leftHalf) and rightIndex < len(rightHalf): 
                if leftHalf[leftIndex] < rightHalf[rightIndex]:
                    myList[indexToFill] = leftHalf[leftIndex]
                    leftIndex  += 1
                else:
                    myList[indexToFill] = rightHalf[rightIndex]
                    rightIndex += 1
            elif leftIndex < len(leftHalf):
                myList[indexToFill] = leftHalf[leftIndex]
                leftIndex  += 1
            else:
                myList[indexToFill] = rightHalf[rightIndex]
                rightIndex += 1
            indexToFill += 1
        
        return myList

def quickSort_iterative(myList):
    pivot = 0
    store = pivot + 1
    right = len(myList)
    new = 0    
    while True:       
        for index in range(pivot + 1,right):
            if myList[index] < myList[pivot]:
                myList[index], myList[store] = myList[store], myList[index]
                store += 1        
        if new < store: new = store
        if store - 1 == pivot:
            pivot = pivot + 1
            if new > pivot + 2:
                right = new
            else:
                pivot = new
                right = len(myList)
                new = 0
        else:
            myList[pivot], myList[store-1] = myList[store-1], myList[pivot]
            right = store - 1        
        store = pivot + 1
        if store > len(myList):
            break
    return myList

def partitionForQuickSort_recursive(myList, start, end):
    global passes
    pivot = myList[start]
    left = start + 1
    right = end
    done = False
    while not done:
        while left <= right and myList[left] <= pivot:
            left += 1
        while myList[right] >= pivot and right >=left:
            right -= 1
        if right < left:
            done= True
        else:
            myList[left], myList[right] = myList[right], myList[left]
    myList[start], myList[right] = myList[right], myList[start]
    return right
    
def quickSort_recursive(myList, start=0, end=len(myList)-1):
    if start < end:
        pivot = partitionForQuickSort_recursive(myList, start, end)
        quickSort_recursive(myList, start, pivot-1)
        quickSort_recursive(myList, pivot+1, end)
    return myList

def quickSort_listcomprehension(myList):
    if len(myList) <= 1:
        return myList
    pivot = myList[0]
    leftOfPivot = [x for x in myList if x < pivot]
    insertPivot = [x for x in myList if x == pivot]
    rightOfPivot = [x for x in myList if x > pivot]
    return quickSort_listcomprehension(leftOfPivot) + insertPivot + quickSort_listcomprehension(rightOfPivot)

def mySort(myList, myMethod):
    sortingMethods = {1: bubbleSort,
                      2: selectionSort,
                      3: insertionSort,
                      4: mergeSort,
                      5: quickSort_iterative,
                      6: quickSort_recursive,
                      7: quickSort_listcomprehension}
    start = time()
    orderedList = sortingMethods[myMethod](myList)   
    end = time()
    runtime = end - start
    return orderedList, runtime
    
def printOut(orderedList,runtime,myMethod):
    print (f'  sorted: {orderedList}')
    print(f'M{myMethod}: {runtime:.1f} sec runtime')
    print(orderedList == sorted(orderedList))
    
def selection():
    print (f'unsorted: {myList}')
    print (''
    'Wie soll sortiert werden?\n'
    '    | (0) compare all methods    |\n'
    '    | (1) bubble sort            |\n'
    '    | (2) selection sort         |\n'
    '    | (3) insertion sort         |\n'
    '    | (4) merge sort (recursive) |\n'
    '    | (5) quicksort (iterative)  |\n'
    '    | (6) quicksort (recursive)  |\n'
    '    | (7) quicksort (recursive*) | *(implemented with list comprehension)')
    myMethod = int(input ('    |  '))
    return myMethod
    
def main():    
    myMethod = selection()
    
    if myMethod == 0:
        for m in range (1,8):
            unorderedList = myList[:]
            orderedList, runtime = mySort(unorderedList, m)
            print(f'M{m}: {runtime:.1f} sec runtime')
    else:
        unorderedList = myList[:]
        orderedList, runtime = mySort(unorderedList, myMethod)
        printOut(orderedList, runtime,myMethod)
    
if __name__ == '__main__':
    main()
