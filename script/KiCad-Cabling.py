from __future__ import print_function
import kicad_netlist_reader
import sys
import csv

from netList import *
from componentList import *
from TableMaker import *
from Pathing import *

# Generate an instance of a generic netlist, and load the netlist tree from
# the command line option. If the file doesn't exist, execution will stop
net = kicad_netlist_reader.netlist(sys.argv[1])
Components = net.getInterestingComponents();

# Create the NetList and componentList lists
NetList = getNetList(net);
componentList = getComponentList(net);

# printNetList(NetList);
# printComponentList(componentList);

# Get an Anchor component and start Paths
Tables = []
tableCount = 0;
iterations = 0;
while(len(componentList) > 0 and iterations < 1000):
    iterations += 1;
    Tables.append(TableMaker());
    table = Tables[tableCount];
    Paths = CablePaths();
    for component in componentList:
        if(component['isAnchor'] == True):
            # start Paths
            for i, connection in enumerate(component['connections']):
                position = connection['pin'];
                pathName = Paths.addPath(position, component['ref'], connection['net'])
                table.addPath(pathName);
            table.sortTable();
            # Add Headers
            for path in Paths.getPaths():
                table.addComponent(component, path, Components, Paths.getPaths(), NetList);
            # Remove Component
            componentList = removeComponent(component['ref'], componentList);
            break;


    # For each path that is incomplete:  
    # Get next component, by looking up last net in path.nets in NetList, 
    # then lookup the next net for that component by looking in componentList, 
    # then remove component from componentList
    while Paths.anyPathIncomplete():
        for path in Paths.getPaths():
            if(path['complete'] == False):
                lastNet = path['nets'][-1];
                lastRef = path['refs'][-1];
                refs = getNetRefs(lastNet, lastRef, NetList);
                if(len(refs) == 1):
                    ref = refs[0];
                    nextNets = getNextNets(ref, componentList, lastNet);
                    component = getComponent(ref, componentList);
                    if(nextNets):
                        if(len(nextNets) == 1):
                            Paths.updatePath(path['name'], ref, nextNets[0]);
                        table.addComponent(component, path, Components, Paths.getPaths(), NetList);
                        componentList = removeComponent(ref, componentList);
                    else:
                        path['complete'] = True;
                elif(len(refs) > 1):
                    print(refs);
                    nextNets = [];
                    for ref in refs:
                        nextNets.append(getNextNets(ref, componentList, lastNet));
                    print(nextNets);
                    newPaths = Paths.branchPath(path['name'], refs, nextNets);
                    # update newly branched paths
                    for newPath in newPaths:
                        ref = newPath['refs'][-1]
                        component = getComponent(ref, componentList);
                        table.addPath(newPath['name']);
                        table.addComponent(component, newPath, Components, Paths.getPaths(), NetList);
                        componentList = removeComponent(ref, componentList)
                    # update old path
                    ref = refs[0];
                    component = getComponent(ref, componentList);
                    table.addComponent(component, path, Components, Paths.getPaths(), NetList);
                    componentList = removeComponent(ref, componentList)
                else:
                    path['complete'] = True;
    tableCount += 1;
    print("**********************************************");
    print('Tables');
    table.printTable();
    print("**********************************************");
    Paths.printPaths();

    Paths = [];

# Write Tables to CSV
# Open a file to write to, if the file cannot be opened output to stdout
# instead
try:
    f = open(sys.argv[2], 'wb')
    writer = csv.writer(f, quotechar="\"", quoting=csv.QUOTE_ALL);
    for table in Tables:
        writer.writerows(table.formatCSV());
        writer.writerows([[]]);
except IOError:
    e = "Can't open output file for writing: " + sys.argv[2]
    print( __file__, ":", e, sys.stderr )
    f = sys.stdout

    
print("**********************************************");
print('Tables');
table.printTable();
print("**********************************************");
printComponentList(componentList);
print("**********************************************");
print("ALL DONE");