/**
 * Created by yun on 2/27/16.
 */
var NetworkYun = NetworkYun || {};

NetworkYun.Node = function(props,count){
    this.id = props.nid;
    this.label = props.nid;
    this.color = props.color;
    this.attributes = {
        indexInTree:0,
        patternId:0,
        active:1
    };
    this.attributes.indexInTree = props.index-1;
    this.attributes.patternId = props.pid;
    this.attributes.active = props.active;
    this.shape = 'ellipse';
    if(this.attributes.indexInTree==0) this.shape = 'box';
    //this.group = props.patternId;
    //this.group = count;
    if(count<8){
        var x;
        var y;
        if(this.attributes.indexInTree==0){
            x = 150;
            y = 100;
        }
        else if(this.attributes.indexInTree==1){
            x = 100;
            y = 150;
        }
        else if(this.attributes.indexInTree==2){
            x = 200;
            y = 150;
        }
        else if(this.attributes.indexInTree==3){
            x = 75;
            y = 200;
        }
        else if(this.attributes.indexInTree==4){
            x = 125;
            y = 200;
        }
        else if(this.attributes.indexInTree==5){
            x = 175;
            y = 200;
        }
        else if(this.attributes.indexInTree==6){
            x = 225;
            y = 200;
        }
        this.x = x + count%4 * 300 ;
        this.y = y + parseInt(count/4) * 300;
    }
    return this;
};

NetworkYun.Node.prototype.getId = function(){
    return this.id;
};

NetworkYun.Node.prototype.getIndex = function(){
    return this.attributes.indexInTree;
};

NetworkYun.Node.prototype.getColor = function(){
    return this.color;
};

NetworkYun.Node.prototype.getShape = function(){
    return this.shape;
};

NetworkYun.Node.prototype.getX = function(){
    return this.x;
};

NetworkYun.Node.prototype.getY = function(){
    return this.y;
};

NetworkYun.Node.prototype.getPatternId = function(){
    return this.attributes.patternId;
};

NetworkYun.Node.prototype.updatePos = function(x,y){
    this.x = x;
    this.y = y;
};

NetworkYun.Node.prototype.changeColor = function(whichColor){
    this.color = whichColor;
};

NetworkYun.Edge = function(props,connectOrNot){
    this.from = props.source;
    this.to = props.target;
    this.id = props.id;
    if(connectOrNot){
        this.smooth = {
            enabled:true,
            type:"curvedCCW",
            roundness:0.1
        };
    }
    return this;
};

NetworkYun.Edge.prototype.getFrom = function(){
    return this.from;
};

NetworkYun.Edge.prototype.getTo = function(){
    return this.to;
};

NetworkYun.Edge.prototype.getId = function(){
    return this.id;
};

NetworkYun.Pattern = function(props,count){
    this.patternId = props.id;
    this.nodes = [];
    for (var i in props.nodes){
        this.nodes.push(new NetworkYun.Node(props.nodes[i],count));
    }
    this.outEdges = [];
    for (var i in props.outEdges){
        this.outEdges.push(props.outEdges[i]);
    }
    this.edges = [];
    this.count = count;
    var node0 = this.getNodeByIndex(0);
    var node1 = this.getNodeByIndex(1);
    var node2 = this.getNodeByIndex(2);
    var node3 = this.getNodeByIndex(3);
    var node4 = this.getNodeByIndex(4);
    var node5 = this.getNodeByIndex(5);
    var node6 = this.getNodeByIndex(6);
    if(node0){
        if(node1){
            this.edges.push(new NetworkYun.Edge({
                source:node0.getId(),
                target:node1.getId(),
                id: node0.getId() + '-' + node1.getId()
            }));
            if(node3){
                this.edges.push(new NetworkYun.Edge({
                    source:node1.getId(),
                    target:node3.getId(),
                    id: node1.getId() + '-' + node3.getId()
                }));
            }
            if(node4){
                this.edges.push(new NetworkYun.Edge({
                    source:node1.getId(),
                    target:node4.getId(),
                    id: node1.getId() + '-' + node4.getId()
                }));
            }
        }
        if(node2){
            this.edges.push(new NetworkYun.Edge({
                source:node0.getId(),
                target:node2.getId(),
                id: node0.getId() + '-' + node2.getId()
            }));
            if(node5){
                this.edges.push(new NetworkYun.Edge({
                    source:node2.getId(),
                    target:node5.getId(),
                    id: node2.getId() + '-' + node5.getId()
                }));
            }
            if(node6){
                this.edges.push(new NetworkYun.Edge({
                    source:node2.getId(),
                    target:node6.getId(),
                    id: node2.getId() + '-' + node6.getId()
                }));
            }
        }
    }
    return this;
};

NetworkYun.Pattern.prototype.getId = function(){
    return this.patternId;
};


NetworkYun.Pattern.prototype.getNodeById = function(id){
    for (var i in this.nodes){
        if(this.nodes[i].getId()==parseInt(id)){
            return this.nodes[i];
        }
    }
    return null;
};

NetworkYun.Pattern.prototype.getNodeByIndex = function(index){
    for (var i in this.nodes){
        if(this.nodes[i].getIndex()==parseInt(index)){
            return this.nodes[i];
        }
    }
    return null;
};

NetworkYun.Pattern.prototype.getNodes = function(){
    return this.nodes;
};

NetworkYun.Pattern.prototype.getEdges = function(){
    return this.edges;
};

NetworkYun.Pattern.prototype.getOutEdges = function(){
    return this.outEdges;
};

NetworkYun.Pattern.prototype.getConnector = function(){
    return this.getNodeByIndex(0);
};

NetworkYun.Pattern.prototype.getConnectorId = function(){
    return this.getConnector().getId();
};


NetworkYun.Pattern.prototype.getCanBeAdded = function(){
    var canBeAdded = [];
    var left = this.getNodeByIndex(1);
    var right = this.getNodeByIndex(2);
    if(!left||!right) canBeAdded.push(this.getNodeByIndex(0).getId());
    if(left){
        if(!this.getNodeByIndex(3)||!this.getNodeByIndex(4)){
            canBeAdded.push(left.getId());
        }
    }
    if(right){
        if(!this.getNodeByIndex(5)||!this.getNodeByIndex(6)){
            canBeAdded.push(right.getId());
        }
    }
    return canBeAdded;
};

NetworkYun.Pattern.prototype.getCanBeAddedChild = function(whoseChild){
    var whichOne = this.getNodeById(whoseChild);
    if(whichOne){
        var left = this.getNodeByIndex(whichOne.getIndex()*2+1);
        var right = this.getNodeByIndex(whichOne.getIndex()*2+2);
        if(left&&right) return null;
        if(left) return (whichOne.getIndex()*2+2);
        return (whichOne.getIndex()*2+1);
    }
    return -1;
};

NetworkYun.Pattern.prototype.ToBeAddedOne = function(parentId,index){
    var parentNode = this.getNodeById(parentId);
    if(!parentNode) return null;
    var toSendNode = {
        nid: -1,
        x: -1,
        y: -1,
        color: parentNode.getColor(),
        shape: 'ellipse',
        active: 1,
        index: index+1,
        pid: this.patternId
    };
    console.log(toSendNode);
    return toSendNode;
};

NetworkYun.Pattern.prototype.addNode = function(toSendNode){
    var whichNode = new NetworkYun.Node(toSendNode,this.count);
    console.log(whichNode);
    var parentNodeId = this.getNodeByIndex((whichNode.getIndex() - 1) / 2).getId();
    var neList=[];
    this.nodes.push(whichNode);
    var whichEdge = new NetworkYun.Edge({
        source: parentNodeId,
        target: whichNode.getId(),
        id: parentNodeId +'-'+ whichNode.getId()
    });
    this.edges.push(whichEdge);
    neList.push(whichNode);
    neList.push(whichEdge);
    return  neList;
};

NetworkYun.Pattern.prototype.getCanBeDeleted = function(){
    var canBeDeleted = [];
    for (var i in this.nodes){
        if(this.nodes[i].getIndex()!=0) canBeDeleted.push(this.nodes[i].getId());
    }
    return canBeDeleted;
};

NetworkYun.Pattern.prototype.removeNode = function(id){
    var i=0;
    while(i<this.nodes.length){
        if(this.nodes[i].getId()==id){
            this.nodes.splice(i,1);
            break;
        }
        else i++;
    }
};

NetworkYun.Pattern.prototype.removeEdge = function(id){
    var i=0;
    while(i<this.edges.length){
        if(this.edges[i].getFrom()==id) this.edges.splice(i,1);
        else if(this.edges[i].getTo()==id) this.edges.splice(i,1);
        else i++;
    }
};

NetworkYun.Pattern.prototype.deleteNode1 = function(id){
    var whichNode = this.getNodeById(parseInt(id));
    var index= whichNode.getIndex();
    if(whichNode){
        var left = this.getNodeByIndex(index*2+1);
        var right = this.getNodeByIndex(index*2+2);
        if(left) this.removeNode(left.getId());
        if(right) this.removeNode(right.getId());
        this.removeNode(parseInt(id));
        this.removeEdge(parseInt(id));
    }
};

NetworkYun.Network = function(props){
    this.patterns=[];
    for (var i in props){
        this.patterns.push(new NetworkYun.Pattern(props[i],i));
    }
    this.nodes = [];
    for (var i in this.patterns){
        var pNodes = this.patterns[i].getNodes();
        for (var j in pNodes){
            this.nodes.push(pNodes[j]);
        }
    }
    this.edges = [];
    for (var i in this.patterns){
        var pEdges = this.patterns[i].getEdges();
        for (var j in pEdges){
            this.edges.push(pEdges[j]);
        }
        var pOutEdges = this.patterns[i].getOutEdges();
        for (var j in pOutEdges){
            var source = this.patterns[i].getConnectorId();
            var target = this.getPatternById(pOutEdges[j]).getConnectorId();
            this.edges.push(new NetworkYun.Edge({
                source:source,
                target: target,
                id: source + '-' + target
            },true));
        }
    }
    return this;
};

NetworkYun.Network.prototype.getPatternData = function(){
    return this.patterns;
};

NetworkYun.Network.prototype.getNodesData = function(){
    return this.nodes;
};

NetworkYun.Network.prototype.getEdgesData= function(){
    return this.edges;
};

NetworkYun.Network.prototype.getNodeById = function(id){
    for (var i in this.nodes){
        if(this.nodes[i].getId()==parseInt(id)){
            return this.nodes[i];
        }
    }
};

NetworkYun.Network.prototype.getEdgeByFrom = function(from){
    for (var i in this.edges){
        if(this.edges[i].getFrom()==parseInt(from)){
            return this.edges[i];
        }
    }
};

NetworkYun.Network.prototype.changeColor = function(whichId,whichColor){
    this.getNodeById(whichId).changeColor(whichColor);
    dataStore.nodes.update({id:parseInt(whichId),color:whichColor});
};

NetworkYun.Network.prototype.toggleColor = function(whichId,whichColor){
    var whichNode = this.getNodeById(whichId);
    var pcolor = whichNode.getColor();
    whichNode.changeColor(whichColor);
    dataStore.nodes.update({id:parseInt(whichId),color:whichColor});
    setTimeout(function(){
        whichNode.changeColor(pcolor);
    dataStore.nodes.update({id:parseInt(whichId),color:pcolor});
    },1000)
};

NetworkYun.Network.prototype.getPatternById = function(id){
    for (var i in this.patterns){
        if(this.patterns[i].getId()==parseInt(id)){
            return this.patterns[i];
        }
    }
    return null;
};

NetworkYun.Network.prototype.addNode = function(whichPattern,whichNode){
    var neList = this.getPatternById(whichPattern).addNode(whichNode);
    this.nodes.push(neList[0]);
    this.edges.push(neList[1]);
    dataStore.nodes.add(neList[0]);
    dataStore.edges.add(neList[1]);
};



NetworkYun.Network.prototype.ToBeAddedOnePattern = function(){
    var toSendNode = {
        nid: -1,
        x: -1,
        y: -1,
        color: 'rgb(255,168,7)',
        shape: 'box',
        active: 1,
        index: 1,
        pid: -1
    };
    return toSendNode;
};


NetworkYun.Network.prototype.addPattern = function(whichOne,whichList){
    var count = this.patterns.length;
    var newPattern = new NetworkYun.Pattern({
        id:whichOne.pid,
        nodes:[whichOne],
        outEdges:whichList
    },count);
    var whichNode = newPattern.getNodeByIndex(0);
    this.patterns.push(newPattern);
    this.nodes.push(whichNode);
    var outEdges = newPattern.getOutEdges();
    for (var i in outEdges){
        var source = newPattern.getConnectorId();
        var target = this.getPatternById(outEdges[i]).getConnectorId();
        var whichEdge = new NetworkYun.Edge({
            source:source,
            target: target,
            id: source + '-' + target
        },true);
        this.edges.push(whichEdge);
        dataStore.edges.add(whichEdge);
    }
    dataStore.nodes.add(whichNode);
};

NetworkYun.Network.prototype.removeNode = function(id){
    var i=0;
    while(i<this.nodes.length){
        if(this.nodes[i].getId()==id){
            this.nodes.splice(i,1);
            break;
        }
        else i++;
    }
};

NetworkYun.Network.prototype.removeEdge = function(id){
    var i=0;
    var deletedList = [];
    while(i<this.edges.length){
        if(this.edges[i].getFrom()==id){
            deletedList.push(this.edges[i].getId());
            this.edges.splice(i,1);
        }
        else if(this.edges[i].getTo()==id){
            deletedList.push(this.edges[i].getId());
            this.edges.splice(i,1);
        }
        else i++;
    }
    return deletedList;
};

NetworkYun.Network.prototype.deleteNode = function(whichPatternId,whichId){
    var returnList = [];
    var whichPattern = this.getPatternById(whichPatternId);
    var whichNode = whichPattern.getNodeById(parseInt(whichId));
    var index= whichNode.getIndex();
    var left = whichPattern.getNodeByIndex(index*2+1);
    var right = whichPattern.getNodeByIndex(index*2+2);
    if(left){
        var leftId = left.getId();
        this.removeNode(leftId);
        returnList.push(leftId);
        dataStore.nodes.remove(leftId);
    }
    if(right){
        var rightId = right.getId();
        this.removeNode(rightId);
        returnList.push(rightId);
        dataStore.nodes.remove(rightId);
    }
    this.removeNode(parseInt(whichId));
    returnList.push(parseInt(whichId));
    dataStore.nodes.remove(parseInt(whichId));
    var deletedList = this.removeEdge(parseInt(whichId));
    for (var i in deletedList){
        dataStore.edges.remove(deletedList[i]);
    }
    whichPattern.deleteNode1(whichId);
    return returnList;
};