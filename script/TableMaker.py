# class to create and update tables. 
# 1 table instance represents 1 cable assembly
#   | ROW LABEL |   COL 1   |   COL 2   |  COL 3    |
#   ---------------------------------------------------------------------
#   |   HEADER  |   Label   |  Housing  | Position  |
#   ---------------------------------------------------------------------
#   |   PATHX   |    J2     |JST PH MALE|     1     |
#   ---------------------------------------------------------------------
#   |   PATHX   |           |           |     2     |  
#   ---------------------------------------------------------------------

class TableMaker():
    def __init__(self, ComponentList, Paths, NetList):
        self.table = [['HEADER']]
        self.ComponentList = ComponentList
        self.Paths = Paths
        self.NetList = NetList

    def getNumRows(self):
        return len(self.table)

    def addPath(self, pathName):
        rowToAdd = [pathName]
        for i, _ in enumerate(self.table[0]):
            if(i != 0):
                rowToAdd.append('')
        self.table.append(rowToAdd)

    def getNumColumns(self):
        return len(self.table[0])

    def addHeader(self, header):
        for i, row in enumerate(self.table):
            if(i==0):
                row.append(header)
            else:
                row.append('')

    def updateCell(self, newValue, header, path):
        # remove "KICABLE_HEADER:" from header
        if 'KICABLE_HEADER:' in header:
            header = header.replace('KICABLE_HEADER:', '')

        # find column the "header" is in
        column = -1
        for col, Header in enumerate(self.table[0]):
            if(header == Header):
                column = col
        
        # find the row the representing the "path"
        row = -1
        for r, ROWLABEL in enumerate(self.table):
            if(path == ROWLABEL[0]):
                row = r
        # update the cell in the "row" and the "column"
        if(column >= 0 & row >= 0):
            self.table[row][column] = newValue

    def addComponent(self, component, path=None):
        # ADD HEADERS
        KiCadComponent = component['KiCadComponent']
        fields = []
        import copy
        currentHeaders = copy.copy(self.table[0])
        if(component['ref'].startswith("HOUSING")):
            fields = self.makeHousingHeaders(len(currentHeaders))
        elif(component['ref'].startswith("TERMINAL")):
            fields = self.makeTerminalHeaders(component, currentHeaders)
        else:
            fields = component['KiCadComponent'].getFieldNames()
        # if fields does not contain 'Anchor' field, it is a standard component
        if not 'KICABLE_INFO:Anchor' in component['KiCadComponent'].getFieldNames():
            component['Standard Component'] = True
            fields.append('KICABLE_HEADER:Position')
            fields.append('KICABLE_HEADER:Component')
            
        # remove any "INFO" Fields and fields NOT containing KICABLE, string 'KICABLE_HEADER'
        cleanFields = [];
        for field in fields:
            if not 'INFO' in field and 'KICABLE' in field:
                if 'KICABLE_HEADER:' in field:
                    newField = field.replace('KICABLE_HEADER:', '')
                    cleanFields.append(newField)
        
        # check to make sure the new headers are not the same as the last headers
        if( set(cleanFields) != set(currentHeaders[-len(cleanFields):]) ):
            for header in cleanFields:
                self.addHeader(header)
            
        # ADD CELL VALUES
        cellValues = []
        if(component['ref'].startswith("HOUSING")):
            self.populateHousingCells(component)
        elif(component['ref'].startswith('TERMINAL')):
            self.populateTerminalCells(component, fields, path)
        elif('Standard Component' in component):
            self._populateStandardComponentCells(component, fields)
        else:
            for field in fields:
                cellValues.append({'fieldName': field, 'value': component['KiCadComponent'].getField(field)})
            for cell in cellValues:
                self.updateCell(cell['value'], cell['fieldName'], path['name'])

    def makeHousingHeaders(self, len):
        fields = []
        if(len < 3):
            fields = ['KICABLE_HEADER:Label', 'KICABLE_HEADER:Housing', 'KICABLE_HEADER:Position']
        else:
            fields = ['KICABLE_HEADER:Position', 'KICABLE_HEADER:Housing', 'KICABLE_HEADER:Label']
        return fields

    def makeTerminalHeaders(self, component, currentHeaders):
        fields = []
        if 'Terminal' not in currentHeaders:
            fields = ['KICABLE_HEADER:Terminal']
            for field in component['KiCadComponent'].getFieldNames():
                fields.append(field)
        else:
            for field in component['KiCadComponent'].getFieldNames():
                fields.append(field)
            fields.append('KICABLE_HEADER:Terminal')
        return fields

    def populateHousingCells(self, component):
        Paths = self.Paths.getPaths()
        cellValues = []
        from componentList import getPosition
        remainingPositions = []
        unusedPaths = []
        for connection in component['connections']:
            remainingPositions.append(connection['pin'])
        for i, path in enumerate(Paths):
            #if 'component' contains 'path' position will NOT be NONE
            position = getPosition(component['ref'], path['nets'][-1], self.NetList)
            if(position):
                cellValues.append({ 'fieldName': 'Label', 'value': component['KiCadComponent'].getField('KICABLE_HEADER:Label') })
                cellValues.append({ 'fieldName': 'Housing', 'value': component['KiCadComponent'].getValue() })
                cellValues.append({ 'fieldName': 'Position', 'value': position })
                remainingPositions.remove(position)
            else:
                unusedPaths.append(path['name'])
            for cell in cellValues:
                self.updateCell(cell['value'], cell['fieldName'], path['name'])
            cellValues = []
        for position in remainingPositions:
            cellValues.append({ 'fieldName': 'Position', 'value': position })
            self.updateCell(position, 'Position', unusedPaths.pop(0))s

    def _populateStandardComponentCells(self, component, fields):
        from componentList import getPosition
                
        for connection in component['connections']:
            cells = []
            
            for field in fields:
                if(field == 'KICABLE_HEADER:Component'):
                    cells.append({ 'fieldName': field, 'value': component['KiCadComponent'].getValue() })
                else:
                    cells.append({'fieldName': field, 'value': component['KiCadComponent'].getField(field)})

            pathName = self.Paths.getPathName(connection['net'])
            path = self.Paths.getPath(pathName)
            if path :
                position = getPosition(component['ref'], path['nets'][-1], self.NetList)
                if(position):
                    cells.append({ 'fieldName': 'Position', 'value': position })

                for cell in cells:
                    self.updateCell(cell['value'], cell['fieldName'], path['name'])
            elif 'MECH' in connection['pin']:
                # get the connected component
                from netList import getNetRefs
                refs = getNetRefs(connection['net'], component['ref'], self.NetList)

                for ref in refs:
                    pathName = self.Paths.addPath(connection['pin'], ref, connection['net'])
                    self.addPath(pathName)

                    from componentList import getComponent
                    self.addComponent(getComponent(ref, self.ComponentList), pathName)

            else:
                print 'FOUND PIN BUT NO PATH ASSOCIATED'
        

    def populateTerminalCells(self, component, fields, path):
        cellValues = []
        for field in fields:
            if(field == 'KICABLE_HEADER:Terminal'):
                cellValues.append({'fieldName': field, 'value': component['KiCadComponent'].getValue()})
            elif(field != "Anchor" and 'INFO' not in field):
                cellValues.append({'fieldName': field, 'value': component['KiCadComponent'].getField(field)})
        for cell in cellValues:
            self.updateCell(cell['value'], cell['fieldName'], path['name'])

    def formatCSV(self):
        # sort table by Row Label
        self.smartSort()
        # strip ROW LABELS
        import copy
        formattedTable = copy.deepcopy(self.table)
        for row in formattedTable:
            row.pop(0)
        return formattedTable
    
    def sortTable(self):
        # sort rows by path name, leave HEADER row at top
        self.table.sort()

    # Smart sort groups the rows by the labels on either side and 
    # orders by pin number, left side priority
    def smartSort(self):


        # find the 'Label' and 'Position' columns
        labelColumns = []
        positionColumns = []
        for i, col in enumerate(self.table[0]):
            if col == 'Label':
                labelColumns.append(i)
            elif col == 'Position':
                positionColumns.append(i)

        if labelColumns and positionColumns:

            # get number and label of groups on both sides
            groups = []
            for i, col in enumerate(labelColumns):
                groups.append([])
                for row in self.table:
                    if row[col] and row[col] != 'Label':
                        if not row[col] in groups[i]:
                            groups[i].append(row[col])

            print groups

            # determine which label/position set has priority
            prioritySet = 0
            numLabels = 1
            for i, group in enumerate(groups):
                if len(group) > 1 and len(group) > numLabels:
                    prioritySet = i
                    numLabels = len(group)

            print prioritySet, numLabels

            # split content from headers and into groups by label sets
            labelSets = []
            for i, label in enumerate(groups[prioritySet]):
                print groups[prioritySet]
                print label
                labelSets.append([])
                for j, row in enumerate(self.table):
                    if(j>0 and row[labelColumns[prioritySet]] == label):
                        labelSets[i].append(row)

            # convert position columns to number
            for group in labelSets:
                for row in group:
                    for col in positionColumns:
                        try:
                            number = int(row[col])
                            row[col] = number
                        except ValueError:
                            #Handle the exception
                            True

            # sort each labelSet
            from operator import itemgetter
            for i, group in enumerate(labelSets):
                labelSets[i] = sorted(group, key=itemgetter(positionColumns[0]))

            # recombine headerRow and labelSets
            rowCount = 0
            for i, group in enumerate(labelSets):
                for j, row in enumerate(group):
                    self.table[rowCount+1] = row
                    rowCount += 1

    def printTable(self):
        for row in self.table:
            print(row)