class CablePaths:
    def __init__(self):
        self.paths=[];

    def getPaths(self):
        return self.paths;

    def getPath(self, pathName):
        pathToReturn = {};
        for path in self.paths:
            if path['name'] == pathName:
                pathToReturn = path;
        return pathToReturn

    def addPath(self, position, ref, net):
        name = "Path"+str(position);
        self._createPath(name, ref, net);
        return name;

    def updatePath(self, pathName, ref, nextNet):
        pathToUpdate = {};
        for path in self.paths:
            if(path['name'] == pathName): 
                pathToUpdate = path;
                break;
        pathToUpdate['refs'].append(ref);

        # check to make sure nextNet is not already registered to another Path
        netInAPath = False;
        for path in self.paths:
            if nextNet in path['nets']:
                netInAPath = True;
                
        if not netInAPath:
            pathToUpdate['nets'].append(nextNet);

    def branchPath(self, pathName, newRefs, newNets):
        print('Branching: ',pathName);
        newPaths = [];
        # get the path object
        branchedPath = {};
        for path in self.paths:
            if(path['name'] == pathName):
                branchedPath = path;
        print(branchedPath);

        # first ref goes to 'branchedPath' additional refs go to new paths
        newName = '';
        for i, ref in enumerate(newRefs):
            if(i==0):
                self.updatePath(branchedPath['name'], ref, newNets[i][0]);
            else:
                if 'branches' in branchedPath:
                    newName = branchedPath['name'] + '.' + str(branchedPath['branches']+1);
                    branchedPath['branches'] += 1;
                else:
                    newName = branchedPath['name'] + '.1'
                    branchedPath['branches'] = 1;
                newPaths.append(self._createPath(newName, ref, newNets[i][0]));
        return newPaths;

    def _createPath(self, name, ref, net):
        path = {};
        path['name'] = name;
        path['refs'] = [ref];
        path['nets'] = [net];
        path['complete'] = False;
        self.paths.append(path);
        return path;

    def anyPathIncomplete(self):
        for path in self.paths:
            if(path['complete'] == False):
                return True;
        return False;


    def printPaths(self):
        print("PATHS");
        print("-------------");
        for path in self.paths:
            # name, refs, nets, complete
            print('Name: ',path['name']);
            print('Refs: ',path['refs']);
            print('Nets: ',path['nets']);
            print('complete',path['complete']);
            print('---------------');