def find(item, mylist):
    for i,x in enumerate(mylist):
        if item == mylist[i]:
            return i
    return 