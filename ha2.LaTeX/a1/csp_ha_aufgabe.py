#csp
#set of variables, domain of each variable, constraints
#can have only inequality constraints (sufficient for map coloring problems)
class CSP():

    def __init__(self,domains,constraints):
        self.domains=domains
        self.constraints=constraints
        self.assignments={}
        for k in domains.keys():
            self.assignments[k]=None
        self.adjacentDictionary = self.makeAdjacentMatrix()

    def getNVar(self):
        return len(self.domains.keys())

    def isConsistent(self):
        consistent = True
        for k in self.constraints.keys():
            co = self.constraints[k]
            for c in co:
                if (self.assignments[k] is not None) and (self.assignments[c] is not None):
                    consistent = consistent and (self.assignments[k] != self.assignments[c])
        return consistent

    def getDomain(self,var):
        return self.domains[var]

    def assign(self,var,value):
        self.assignments[var]=value

    def unassign(self,var):
        self.assignments[var]=None

    def getAssignments(self):
        return self.assignments

    def makeAdjacentMatrix(self):
        adjacentMatrixAsDictionary = {}
        for node in self.assignments.keys():
          #print("considered node is : " + node)
          adjacentMatrix=[]
              #take for each node it knowen adjacent from contrains
          if(self.assignments[node] is None) and self.domains[node] != []:
            try:
             for v in self.constraints[node]:
               adjacentMatrix.append(v)
            except KeyError as keyErr:
                print("node: " + node + " has no adjacent list of its neigthbors")
              #consider other nodes for there adjacent list, if this node is in it 
              #Start for-loop "otherNodes"
            for otherNode in self.assignments.keys():
               if otherNode == node:
                  continue
               else:
                  try:
                    tempAdjacent = self.constraints[otherNode]
                          #print("tempAdjacentList is " +str(tempAdjacent))
                  except KeyError as keyErr1:
                          #print("")
                    continue
               if node in tempAdjacent and not(node in adjacentMatrix) :
                  adjacentMatrix.append(otherNode)
                  #End of for-loop "otherNodes", adjacentMatrix has now all connection to this note              
          adjacentMatrixAsDictionary[node] = adjacentMatrix
        return adjacentMatrixAsDictionary    

    def getNextAssignableVar(self,heuristics):
        if heuristics=="MRV":
            #TODO: make adjacent matrix for each node            
            #catch an empty list
            try:
              #sort the dictionary by the length of their values and bring it into a list of tupels (t_0,...t_n),
              #where t_n = (x_0,x_1) | x_1 := {List of adjacent nodes to x_0}
              sortedList = sorted(self.adjacentDictionary.items(), key=lambda kv: (len(kv[1]),kv[0])) 
              firstNode = sortedList[0][0]
              #remove first node
              sortedList.pop(0)
              print(str("node with less adjacent nodes: " +firstNode))
              #remove node as key
              del self.adjacentDictionary[firstNode]
              #remove all entries in the values for this key
              newAdjacentDict = {}
              for kv in sortedList:
                if firstNode in kv[1]:
                  kv[1].remove(firstNode)                  
                newAdjacentDict[kv[0]] = kv[1]

              print(str(newAdjacentDict))
              #reset adjacent dictionary
              self.adjacentDictionary = newAdjacentDict


              print(str(self.adjacentDictionary))
            except IndexError as iErr:
              firstNode = None
            return firstNode
            pass
        else:
            #get the next var that is unassigned AND has non-empty domain
            for u in self.assignments.keys():
                if (self.assignments[u] is None) and self.domains[u] != []:
                    return u

    def isSolved(self):
        solved=True
        for a in self.assignments.values():
            solved = solved and (a is not None)
        return (solved and self.isConsistent())


#backtracking search algorithm
def backtrackcsp(csp,depth,heuristics):
    #select d-th variable. iterate over domain. for each element, iteratively call backtrackscp
    #return None when no solution possible, or the csp with the solution    
    if not (csp.getNVar() > depth):
        return None
    else:
        #iterate over domain of d-th variable
        var = csp.getNextAssignableVar(heuristics)
        dom = csp.getDomain(var)
        for d in dom:
            #bind var to d
            csp.assign(var,d)
            #test whether this is a solution (then return solution), or go deeper
            if csp.isSolved():
                return csp
            #when this is consistent, go deeper. if not consistent, we do not need to consider this
            #any further
            if csp.isConsistent():
                #go deeper
                print("increase depth; depth is: " + str(depth+1))
                ret = backtrackcsp(csp,depth+1,heuristics)
                #if ret is a solution, return this, if not, go to next iteration
                print(str(ret))
                if ret is not None:
                    return ret
            #else: (this is not a valid assignment, we do not need to test this any further)
        #when we get here, no assignment lead to a solution, i.e. there is no solution
        #remove the assignments of var
        csp.unassign(var)
        return None

#definition of map
places = {'LUP':[1,2,3],'MSE':[1,2,3],'NWM':[1,2,3],'HRO':[1,2,3],'LRO':[1,2,3],'SN':[1,2,3],'VG':[1,2,3],'VR':[1,2,3]}
borders = {'NWM':['SN','LUP','LRO'], 'SN':['LUP'], 'LUP':['LRO','MSE'], 'LRO':['MSE','HRO','VR'],'MSE':['VR','VG'], 'VG':['VR']}

mvmap = CSP(places,borders)

print(backtrackcsp(mvmap,0,'MRV').getAssignments())
