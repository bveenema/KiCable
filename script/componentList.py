def getComponentList(net):
    nets = net.nets;
    components = net.getInterestingComponents()

    componentList = [];
    # [
    #     {
    #         ref: "HOUSING1",
    #         Connections:   [
    #                           {pin: 3, net: "Net-(HOUSING1-Pad3)"},
    #                           {pin: 2, net: "Net-(HOUSING1-Pad2)"},
    #                           {pin: 1, net: "Net-(HOUSING1-Pad1)"}
    #                        ],
    #         isAnchor: True,
    #         KiCadComponent: <comp>,
    #     },
    #     ...
    # ]

    # initialize componentList with refs
    for component in components:
        newComponent = {};
        newComponent['ref'] = component.getRef();
        newComponent['connections'] = [];
        newComponent['isAnchor'] = (str.lower(component.getField("Anchor")) == "yes");
        newComponent['KiCadComponent'] = component;
        componentList.append(newComponent);

    # add nets to components
    for thisNet in nets:
        netName = thisNet.attributes["name"];

        nodes = thisNet.getChildren();

        for node in nodes:
            ref = node.attributes["ref"];
            pin = node.attributes['pin'];
            for component in componentList:
                if(component['ref'] == ref):
                    component['connections'].append({'net': netName, 'pin': pin});
            
        for component in componentList:
            component['connections'] = sorted(component['connections'], key=lambda k: k['net'])

    return componentList;

def printComponentList(componentList):
    print("COMPONENT LIST");
    print("-------------");
    for component in componentList:
        print("Ref: ", component['ref']);
        print('Nets', component['connections']);
        print('isAnchor', component['isAnchor']);
        print("-------------");

def removeComponent(component, componentList):
    # theList = [{'id': 1, 'name': 'paul'},{'id': 2, 'name': 'john'}]
    # thelist[:] = [d for d in thelist if d.get('id') != 2]
    componentList[:] = [d for d in componentList if d.get('ref') != component];
    return componentList;

def getComponent(ref, componentList):
    for component in componentList:
        if(ref == component['ref']):
            return component;
    return None;

def getKiCadComponent(ref, components):
    for component in components:
        if(ref == component.getRef()):
            return component;
    return None;

def getPosition(ref, netName, netList):
    for net in netList:
        if(netName == net['netName']):
            for node in net['nodes']:
                if(ref == node['ref']):
                    return node['pin'];
    return None;