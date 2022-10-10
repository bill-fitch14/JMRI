class NestedListFunctions:
    
    pegs = ([])
    
    def __init__(self, pegs):
        self.pegs = pegs

    #find location of item_in_pegs in pegs
    def firstIndex(self, item_in_pegs):
        for n in self.pegs:
            for i in n:
                if i == item_in_pegs:
                    secondIndexInNestedList = str(a.index(n))
                    return secondIndexInNestedList[0]

    def secondIndex(self, item_in_pegs):
        for n in self.pegs:
            for i in n:
                if i == item_in_pegs:
                    secondIndexInNestedList = str(n.index(i))
                    return secondIndexInNestedList[0]

    #find value of nth item
    def itemLocation(self,nthItem):
        count = 0
        for n in self.pegs:
            for i in n:
                count = count+1
                if count == nthItem:
                    return i
        return 0

a =  [[4, 1], [3], [5], [0], [], [], [2]] 
##index2 = [str(n.index(i))
##          for n in a
##          for i in n
##          if i == 5]
##index1 = [str(a.index(n))
##          for n in a
##          for i in n
##          if i == 5]
##print index1[0]
##print index2[0]

g = NestedListFunctions(a)

nthItem = g.itemLocation(1)
print ("nthItem= ",nthItem)
#get it's indices
rp1 = g.firstIndex(1)
print("8" + str(rp1))
rp1 = g.firstIndex(nthItem)
print("8" + str(rp1))
rp2 = g.secondIndex(nthItem)
print("9" + str(rp1))
rp2 = g.secondIndex(nthItem)
print(rp2)
print("1" + str(g.firstIndex(8)))
print("2" + g.secondIndex(8))
print("3" + g.itemLocation(3))
print("4" + g.itemLocation(4))
