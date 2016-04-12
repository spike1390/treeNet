/**
 * Created by yun on 2/27/16.
 */
var NetworkYun = NetworkYun || {};

NetworkYun.Node = function(props,wide,left,height,top,domainId){
    this.id = props.nid;
    this.color = 'rgb(255,168,7)';
    this.attributes = {
        indexInTree:props.index - 1,
        patternId:props.pid,
        active:props.active,
        domainId:domainId
    };
    this.shape = 'ellipse';
    this.label = this.id;
    if(this.attributes.active==0){
        this.color='rgb(192,192,192)';
    }
    if(this.attributes.indexInTree==0){
        this.shape = 'box';
        this.label = 'P'+ this.attributes.patternId + "--" + this.id;
    }
    //this.group = props.patternId;
    //this.group = count;
    var x;
    var y;
    if(this.attributes.indexInTree != -2){
        if(this.attributes.indexInTree==0){
            x = wide/2;
            y = height/3;
        }
        else if(this.attributes.indexInTree==1){
            x = wide/3;
            y = height/2;
        }
        else if(this.attributes.indexInTree==2){
            x = wide/3 *2;
            y = height/2;
        }
        else if(this.attributes.indexInTree==3){
            x = wide/4;
            y = height/3 *2;
        }
        else if(this.attributes.indexInTree==4){
            x = wide/12 *5;
            y = height/3 * 2;
        }
        else if(this.attributes.indexInTree==5){
            x = wide/12 *7;
            y = height/3 * 2;
        }
        else if(this.attributes.indexInTree==6){
            x = wide/4 *3;
            y = height/3 * 2;
        }
        this.x = x + left;
        this.y = y + top;
    }
    else{
        this.x = left+wide;
        this.y = 300;
        this.shape = 'database';
        this.label = 'D'+ this.attributes.domainId + "--" + this.id;
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

NetworkYun.Node.prototype.getActive = function(){
    return this.attributes.active;
};

NetworkYun.Node.prototype.getDomainId = function(){
    return this.attributes.domainId;
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


NetworkYun.Node.prototype.changeColor = function(whichColor){
    this.color = whichColor;
};

NetworkYun.Node.prototype.changeActive = function(){
    this.attributes.active = 1;
};

NetworkYun.Node.prototype.changeInActive = function(){
    this.attributes.active = 0;
};

NetworkYun.Edge = function(props,connectOrNot){
    this.from = props.source;
    this.to = props.target;
    this.id = props.id;
    if(connectOrNot){
        this.smooth = {
            enabled:true,
            type:"curvedCCW",
            roundness:0.2
        };
    }
    this.color = 'rgb(255,168,7)';
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



NetworkYun.Pattern = function(props,wide,left,height,top){
    this.patternId = props.id;
    this.domainId = props.did;
    this.nodes = [];
    for (var i in props.nodes){
        this.nodes.push(new NetworkYun.Node(props.nodes[i],wide,left,height,top,this.domainId));
    }
    this.outEdges = [];
    for (var i in props.outEdges){
        this.outEdges.push(props.outEdges[i]);
    }
    this.edges = [];
    this.wide = wide;
    this.left = left;
    this.height = height;
    this.top = top;
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

NetworkYun.Pattern.prototype.getDomainId = function(){
    return this.domainId;
};

NetworkYun.Pattern.prototype.getConnector = function(){
    return this.getNodeByIndex(0);
};

NetworkYun.Pattern.prototype.getConnectorId = function(){
    return this.getConnector().getId();
};


NetworkYun.Pattern.prototype.getCanBeAddedChild = function(whoseChild){
    var whichOne = this.getNodeById(whoseChild);
    if(whichOne){
        if(whichOne.getIndex()>2) return -1;
        var left = this.getNodeByIndex(whichOne.getIndex()*2+1);
        var right = this.getNodeByIndex(whichOne.getIndex()*2+2);
        if(left&&right) return -1;
        if(left) return (whichOne.getIndex()*2+2);
        return (whichOne.getIndex()*2+1);
    }
    return -1;
};

NetworkYun.Pattern.prototype.addNode = function(toSendNode){
    var whichNode = new NetworkYun.Node(toSendNode,this.wide,this.left,this.height,this.top,this.domainId);
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

NetworkYun.Pattern.prototype.deleteOutEdge = function(id){
    for(var i in this.outEdges){
        if(this.outEdges[i]==id){
            this.outEdges.splice(i,1);
            break;
        }
    }
};


NetworkYun.Pattern.prototype.addOutEdge = function(id){
    this.outEdges.push(id);
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

NetworkYun.Domain = function(props,wide,left){
    this.domainId = props.did;
    this.patterns = [];
    var plen = props.patterns.length;
    var height = 600/plen;
    this.wide = wide;
    this.left = left;
    for (var i in props.patterns){
        this.patterns.push(new NetworkYun.Pattern(props.patterns[i],wide,left,height,height*i));
    }
    this.domainEdges = [];
    for (var i in props.domain_edges){
        this.domainEdges.push(props.domain_edges[i]);
    }
    this.domainNode = new NetworkYun.Node(props.domain_node,wide,left,height,300,this.domainId);
};

NetworkYun.Domain.prototype.removePattern = function(id){
    var i=0;
    while(i<this.patterns.length){
        if(this.patterns[i].getId()==id){
            this.patterns.splice(i,1);
            break;
        }
        else i++;
    }
};

NetworkYun.Domain.prototype.addPattern = function(pattern){
    this.patterns.push(pattern);
};


NetworkYun.Domain.prototype.delDomainEdge = function(id){
    var edge ;
    for(var i in this.domainEdges){
        if(this.domainEdges[i]==id){
            edge = this.domainEdges[i];
            this.domainEdges.splice(i,1);
            break;
        }
    }
    return edge;
};

NetworkYun.Domain.prototype.addDomainEdge = function(id){
    this.domainEdges.push(parseInt(id));
};

NetworkYun.Network = function(props){
    this.domains = [];
    var dlen = props.length;
    var wide = 1200/dlen;
    for (var i in props){
        this.domains.push(new NetworkYun.Domain(props[i],wide,wide*i));
    }
    this.patterns=[];
    for(var i in this.domains){
        for(var j in this.domains[i].patterns){
            this.patterns.push(this.domains[i].patterns[j]);
        }
    }
    this.nodes = [];
    for (var i in this.patterns){
        var pNodes = this.patterns[i].getNodes();
        for (var j in pNodes){
            this.nodes.push(pNodes[j]);
        }
    }
    for(var i in this.domains){
        this.nodes.push(this.domains[i].domainNode);
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
    for(var i in this.domains){
        var source = this.domains[i].domainNode.getId();
        for (var j in this.domains[i].patterns){
            var target = this.domains[i].patterns[j].getConnectorId();
            this.edges.push(new NetworkYun.Edge({
                source:source,
                target: target,
                id: source + '-' + target
            },true));
        }
        for (var j in this.domains[i].domainEdges){
            var target = this.getDomainById(this.domains[i].domainEdges[j]).domainNode.getId();
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

NetworkYun.Network.prototype.getEdgeById = function(id){
    for (var i in this.edges){
        if(this.edges[i].getId()==id){
            return this.edges[i];
        }
    }
};

NetworkYun.Network.prototype.getPatternById = function(id){
    for (var i in this.patterns){
        if(this.patterns[i].getId()==parseInt(id)){
            return this.patterns[i];
        }
    }
    return null;
};


NetworkYun.Network.prototype.changeColor = function(whichId,whichColor){
    this.getNodeById(whichId).changeColor(whichColor);
    dataStore.nodes.update({id:parseInt(whichId),color:whichColor});
};


NetworkYun.Network.prototype.toggleColor = function(path,count){
    var tt= 1000;
    if(path.length==0) return false;
    var pcolor = networkPY.getNodeById(path[0]).getColor();
    if(networkPY.getNodeById(path[0]).getActive()==0){
        return false;
    }
    setTimeout(function(){
        networkPY.changeColor(path[0],'red');
    },tt);
    var j=0;
    var interrupt = false;
    var i =0 ;
    while(i<path.length-1){
        if(interrupt) return;
        setTimeout(function(){
            if(interrupt) return false;
            //if(j>0) networkPY.changeEdgeColor(path[j-1],path[j],pcolor);
            networkPY.changeColor(path[j],pcolor);
            if(!sendJson(path[j],path[j+1],count)){
                interrupt = true;
                return false;
            }
            //networkPY.changeEdgeColor(path[j],path[j+1],'red');
            networkPY.changeColor(path[j+1],'red');
            j+=1;
        },tt+1000*(i+1));
        i++;
    }
    setTimeout(function(){
        //networkPY.changeEdgeColor(path[path.length-2],path[path.length-1],pcolor);
        if(interrupt) return;
        networkPY.changeColor(path[path.length-1],pcolor);
    },tt+1000*(i+1));
};


NetworkYun.Network.prototype.getCanBeAdded = function(nodeId){
    var node = this.getNodeById(nodeId);
    if(node.getIndex()==-2) return -1;
    return this.getPatternById(node.getPatternId()).getCanBeAddedChild(nodeId);
};

NetworkYun.Network.prototype.ToBeAddedOne = function(nodeId){
    var index = this.getCanBeAdded(nodeId);
    if(index==-1) return;
    var parentNode = this.getNodeById(nodeId).getPatternId();
    if(!parentNode) return;
    var toSendNode = {
        nid: -1,
        x: -1,
        y: -1,
        color:  'rgb(255,168,7)',
        shape: 'ellipse',
        active: 1,
        index: index+1,
        pid: parentNode
    };
    return toSendNode;
};


NetworkYun.Network.prototype.getCanBeDeleted = function(nodeId){
    if(this.getNodeById(nodeId).getIndex()==-2) return -1;
    return (this.getNodeById(nodeId).getIndex()!=0);
};

NetworkYun.Network.prototype.addNode = function(whichPattern,whichNode){
    var neList = this.getPatternById(whichPattern).addNode(whichNode);
    this.nodes.push(neList[0]);
    this.edges.push(neList[1]);
    dataStore.nodes.add(neList[0]);
    dataStore.edges.add(neList[1]);
};


NetworkYun.Network.prototype.getDomainById = function(id){
    for(var i in this.domains){
        if(this.domains[i].domainId==parseInt(id)){
            return this.domains[i];
        }
    }
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

NetworkYun.Network.prototype.exDomainNode = function(){
    var toSendNode = {
        nid: -1,
        x: -1,
        y: -1,
        color: 'rgb(255,168,7)',
        shape: 'database',
        active: 1,
        index: -1,
        pid: -1
    };
    return toSendNode;
};

NetworkYun.Network.prototype.addPattern = function(whichOne,whichList,domainId){
    var whichDomain = this.getDomainById(domainId);
    var newPattern = new NetworkYun.Pattern({
        id:whichOne.pid,
        nodes:[whichOne],
        outEdges:whichList,
        did:domainId
    },whichDomain.wide,whichDomain.left,600/whichDomain.patterns.length,600);
    var whichNode = newPattern.getNodeByIndex(0);
    this.patterns.push(newPattern);
    whichDomain.addPattern(newPattern);
    this.nodes.push(whichNode);
    var outEdges = newPattern.getOutEdges();
    var source = newPattern.getConnectorId();
    for (var i in outEdges){
        var target = this.getPatternById(outEdges[i]).getConnectorId();
        var whichEdge = new NetworkYun.Edge({
            source:source,
            target: target,
            id: source + '-' + target
        },true);
        this.edges.push(whichEdge);
        dataStore.edges.add(whichEdge);
    }
    var dedge = new NetworkYun.Edge({
        source:whichDomain.domainNode.getId(),
        target:source,
        id:whichDomain.domainNode.getId() + '-' + source
    },true);
    this.edges.push(dedge);
    dataStore.edges.add(dedge);
    dataStore.nodes.add(whichNode);
};

NetworkYun.Network.prototype.newDomain = function(whichOne,domainId,domainNode,domainList){
    var whichDomain =new NetworkYun.Domain({
        did:domainId,
        patterns:[{
            id:whichOne.pid,
            nodes:[whichOne],
            outEdges:[],
            did:domainId
        }],
        domain_node:domainNode,
        domain_edges:domainList
    },1200,1200/this.domains.length);
    this.domains.push(whichDomain);
    var newPattern = whichDomain.patterns[0];
    var whichNode = newPattern.getNodeByIndex(0);
    this.patterns.push(newPattern);
    this.nodes.push(whichNode);
    this.nodes.push(whichDomain.domainNode);
    var source = whichDomain.domainNode.getId();
    var connector = newPattern.getConnectorId();
    for (var i in domainList){
        var target = this.getDomainById(domainList[i]).domainNode.getId();
        var whichEdge = new NetworkYun.Edge({
            source:source,
            target: target,
            id: source + '-' + target
        },true);
        this.edges.push(whichEdge);
        dataStore.edges.add(whichEdge);
    }
    var dedge = new NetworkYun.Edge({
        source:source,
        target:connector,
        id: source + '-' + connector
    },true);
    this.edges.push(dedge);
    dataStore.nodes.add(whichNode);
    dataStore.nodes.add(whichDomain.domainNode);
    dataStore.edges.add(dedge);
};

NetworkYun.Network.prototype.removeDomain = function(id){
    var i=0;
    while(i<this.domains.length){
        if(this.domains[i].domainId==id){
            var domain = this.domains[i];
            this.domains.splice(i,1);
            return domain
        }
        else i++;
    }
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
            deletedList.push(this.edges[i]);
            this.edges.splice(i,1);
        }
        else if(this.edges[i].getTo()==id){
            deletedList.push(this.edges[i]);
            this.edges.splice(i,1);
        }
        else i++;
    }
    return deletedList;
};

NetworkYun.Network.prototype.removeEdgeById = function(id){
    for(var i in this.edges){
        if(this.edges[i].getId()==id){
            var edge = this.edges[i];
            this.edges.splice(i,1);
            return edge;
        }
    }
};

NetworkYun.Network.prototype.removePattern = function(id){
    var i=0;
    while(i<this.patterns.length){
        if(this.patterns[i].getId()==id){
            var whichDomain = this.patterns[i].getDomainId();
            this.patterns.splice(i,1);
            break;
        }
        else i++;
    }
    whichDomain = this.getDomainById(whichDomain);
    whichDomain.removePattern(id);
};

NetworkYun.Network.prototype.deleteNode = function(whichId){
    var returnList = [];
    var whichNode = this.getNodeById(parseInt(whichId));
    var whichPatternId = whichNode.getPatternId();
    var whichPattern = this.getPatternById(whichPatternId);
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
        dataStore.edges.remove(deletedList[i].getId());
    }
    whichPattern.deleteNode1(whichId);
    return returnList;
};


NetworkYun.Network.prototype.getOutEdgeList= function(whichPatternId){
    var outEdgeL = [];
    var whichPattern =this.getPatternById(whichPatternId);
    if(whichPattern){
        for (var i in whichPattern.getOutEdges()){
            outEdgeL.push(whichPattern.getOutEdges()[i]);
        }
        for (var i in this.patterns){
            var outEdges = this.patterns[i].getOutEdges();
            for (var j in outEdges){
                if(outEdges[j]==parseInt(whichPatternId)){
                    outEdgeL.push(this.patterns[i].getId());
                }
            }
        }
    }
    return outEdgeL;
};


NetworkYun.Network.prototype.getOutdomainList= function(whichDomainId){
    var outEdgeL = [];
    var whichDomain =this.getDomainById(whichDomainId);
    if(whichDomain){
        for (var i in whichDomain.domainEdges){
            outEdgeL.push(whichDomain.domainEdges[i]);
        }
        for (var i in this.domains){
            var outEdges = this.domains[i].domainEdges;
            for (var j in outEdges){
                if(outEdges[j]==parseInt(whichDomainId)){
                    outEdgeL.push(this.domains[i].domainId);
                }
            }
        }
    }
    return outEdgeL;
};

NetworkYun.Network.prototype.checkpushList = function(dlist,id){
    for(var i in dlist){
        if(dlist[i]==id) return true
    }
    dlist.push(id);
    return false
};


NetworkYun.Network.prototype.getDomainConn = function(domainList,dlist){
    for(var i in domainList){
        if(!this.checkpushList(dlist,domainList[i])){
            var outList = this.getOutdomainList(domainList[i]);
            this.getDomainConn(outList,dlist);
        }
    }
};

NetworkYun.Network.prototype.judgeDomainConn = function(whichDomainId,whichDomainId2){
    var domain = this.getDomainById(whichDomainId);
    var oneOR = false;
    var edge;
    for(var i in domain.domainEdges){
        if(domain.domainEdges[i]==whichDomainId2){
            edge = domain.delDomainEdge(whichDomainId2);
            oneOR=true;
            break;
        }
    }
    if(!oneOR) edge = this.getDomainById(whichDomainId2).delDomainEdge(whichDomainId);
    var dlist =[];
    this.getDomainConn([whichDomainId],dlist);
    if(oneOR) this.getDomainById(whichDomainId).addDomainEdge(edge);
    else this.getDomainById(whichDomainId2).addDomainEdge(edge);
    if(dlist.length==this.domains.length) return true;
    return false;
};



NetworkYun.Network.prototype.judgeDomainConn2 = function(whichDomainId){
    var domain = this.getDomainById(whichDomainId);
    var domainList = this.getOutdomainList(whichDomainId);
    for(var i in domainList){
        this.getDomainById(domainList[i]).delDomainEdge(whichDomainId);
    }
    var domainEdges = [];
    for(var i in domain.domainEdges){
        domainEdges.push(domain.domainEdges[i]);
        this.getDomainById(whichDomainId).delDomainEdge(domain.domainEdges[i]);
    }
    if(this.domains.length==0) return true;
    var dlist =[];
    var p=0;
    while(this.domains[p].domainId==whichDomainId){
        p++;
        if(p==this.domains.length) p=0;
    }
    this.getDomainConn([this.domains[p].domainId],dlist);
    for(var i in domainList){
        var oneOr = false;
        for(var j in domainEdges){
            if(domainEdges[j]==domainList[i]){
                oneOr=true;
                this.getDomainById(whichDomainId).addDomainEdge(domainList[i]);
                break;
            }
        }
        if(!oneOr) this.getDomainById(domainList[i]).addDomainEdge(whichDomainId);
    }
    if(dlist.length==this.domains.length-1) return true;
    return false;
};


NetworkYun.Network.prototype.getCanBeDelPattern = function(){
    var canBeDel = [];
    for (var i in this.patterns){
        if(this.patterns[i].getNodes().length==1&&this.patterns[i].getNodes()[0].getIndex()==0){
            var checkOrNot =false;
            for(var j in this.getOutEdgeList(this.patterns[i].getId())){
                var ll = this.getOutEdgeList(this.patterns[i].getId())[j];
                if(this.getOutEdgeList(ll).length==1){
                    checkOrNot = true;
                    break;
                }
            }
            if(!checkOrNot) canBeDel.push("pattern "+this.patterns[i].getId());
        }
    }
    return canBeDel;
};

NetworkYun.Network.prototype.getCanBeDelPattern2 = function(){
    var canBeDel = [];
    for(var i in this.domains){
        var whichDomain = this.domains[i];
            if(whichDomain.patterns.length==1&&whichDomain.patterns[0].getNodes().length==1){
            var checkOrNot =false;
            var domainList = this.getOutdomainList(whichDomain.domainId);
            for(var j in domainList){
                var ll = domainList[j];
                if(this.getOutdomainList(ll).length==1){
                    checkOrNot = true;
                    break;
                }
            }
            if(!this.judgeDomainConn2(whichDomain.domainId)){
                checkOrNot=true;
            }
            if(!checkOrNot) canBeDel.push("pattern "+whichDomain.patterns[0].getId());
        }
        else{
            for(var j in whichDomain.patterns){
                if(whichDomain.patterns[j].getNodes().length==1){
                    canBeDel.push("pattern "+whichDomain.patterns[j].getId());
                }
            }
        }
    }
    return canBeDel;
};


NetworkYun.Network.prototype.deletePattern = function(whichPatternId){
    var whichPattern = this.getPatternById(whichPatternId);
    var returnList=[];
    if(whichPattern){
        var rid = whichPattern.getConnectorId();
        this.removeNode(rid);
        dataStore.nodes.remove(rid);
        var deletedList = this.removeEdge(rid);
        for (var i in deletedList){
            dataStore.edges.remove(deletedList[i].getId());
            returnList.push({
                source:deletedList[i].from,
                target:deletedList[i].to
            });
        }
        this.removePattern(parseInt(whichPatternId));
        for(var i in this.patterns){
            this.patterns[i].deleteOutEdge(parseInt(whichPatternId));
        }
        var ll = {
            nodeId: {
                nid:rid,
                pid:parseInt(whichPatternId),
                did:-1
            }
        };
        return ll;
    }
};



NetworkYun.Network.prototype.deletePatternLast = function(whichPatternId){
    var whichPattern = this.getPatternById(whichPatternId);
    var domainId = whichPattern.getDomainId();
    var returnList=[];
    if(whichPattern){
        var rid = whichPattern.getConnectorId();
        this.removeNode(rid);
        dataStore.nodes.remove(rid);
        var deletedList = this.removeEdge(rid);
        for (var i in deletedList){
            dataStore.edges.remove(deletedList[i].getId());
            returnList.push({
                source:deletedList[i].from,
                target:deletedList[i].to
            });
        }
        var domainNode = this.getDomainById(domainId).domainNode.getId();
        this.removeNode(domainNode);
        dataStore.nodes.remove(domainNode);
        var deletedList = this.removeEdge(domainNode);
        for (var i in deletedList){
            dataStore.edges.remove(deletedList[i].getId());
            returnList.push({
                source:deletedList[i].from,
                target:deletedList[i].to
            });
        }
        this.removePattern(parseInt(whichPatternId));
        this.removeDomain(domainId);
        for(var i in this.domains){
            this.domains[i].delDomainEdge(domainId);
        }
        var ll = {
            nodeId: {
                nid:rid,
                pid:parseInt(whichPatternId),
                did:domainId
            }
        };
        return ll;
    }
};

NetworkYun.Network.prototype.getAllNodeId = function(){
    var returnList=[];
    for (var i in this.nodes){
        if(this.nodes[i].getIndex()!=-2){
            returnList.push(this.nodes[i].getId());
        }
    }
    returnList=returnList.sort(function(a,b){
        return a-b;
    });
    for(var i in returnList){
        returnList[i] ='node '+returnList[i];
    }
    return returnList;
};

NetworkYun.Network.prototype.getAllDomainId = function(){
    var returnList=[];
    for (var i in this.domains){
        returnList.push("domain "+this.domains[i].domainId);
    }
    return returnList;
};

NetworkYun.Network.prototype.getAllPatInDomain = function(id){
    var returnList =[];
    var domain = this.getDomainById(id);
    for (var i in domain.patterns){
        returnList.push("pattern "+domain.patterns[i].getId());
    }
    return returnList;
};

NetworkYun.Network.prototype.getAllPatId = function(id){
    var returnList =[];
    for (var i in this.patterns){
        returnList.push("pattern "+this.patterns[i].getId());
    }
    return returnList;
};

NetworkYun.Network.prototype.Activate = function(id){
    this.getNodeById(id).changeActive();
    this.changeColor(id,'rgb(255,168,7)');
};

NetworkYun.Network.prototype.Inactive = function(idlist){
    for(var i in this.nodes){
        var checkOrNot = false;
        for(var j in idlist){
            if(this.nodes[i].getId()==idlist[j]){
                checkOrNot=true;
                break;
            }
        }
        if(!checkOrNot){
            this.nodes[i].changeActive();
            this.changeColor(this.nodes[i].getId(),'rgb(255,168,7)');
        }
        else{
            this.nodes[i].changeInActive();
            this.changeColor(this.nodes[i].getId(),'rgb(192,192,192)');
        }
    }
};

NetworkYun.Network.prototype.getaddEdgeData = function(){
    var returnList =[];
    for(var i in this.nodes){
        var index = this.nodes[i].getIndex();
        if(index==-2||index==0){
            var id = this.nodes[i].getId();
            if(this.getaddEdgeData2(id).length>0) returnList.push("node "+id);
        }
    }
    return returnList;
};

NetworkYun.Network.prototype.judgeEdge = function(node1Id,node2Id){
    for(var i in this.edges){
        if( (this.edges[i].getFrom()==node1Id&&this.edges[i].getTo()==node2Id) ||
            (this.edges[i].getFrom()==node2Id&&this.edges[i].getTo()==node1Id)){
            return this.edges[i];
        }
    }
};

NetworkYun.Network.prototype.getaddEdgeData2 = function(nodeId){
    var node = this.getNodeById(nodeId);
    var index = node.getIndex();
    var domain = this.getDomainById(node.getDomainId());
    var returnList = [];
    if(index==0){
        for(var i in domain.patterns){
            var cnode = domain.patterns[i].getConnectorId();
            if(cnode!=nodeId){
                if(!this.judgeEdge(nodeId,cnode)){
                    returnList.push("node "+cnode);
                }
            }
        }
    }
    else if(index == -2){
        for(var i in this.domains){
            var cnode = this.domains[i].domainNode.getId();
            if(cnode!=nodeId){
                if(!this.judgeEdge(nodeId,cnode)){
                    returnList.push("node "+cnode);
                }
            }
        }
    }
    return returnList;
};

NetworkYun.Network.prototype.addEdge = function(nodeId1,nodeId2){
    var node1 =this.getNodeById(nodeId1);
    var node2 =this.getNodeById(nodeId2);
    if(node1.getIndex()==0&&node2.getIndex()==0){
        this.getPatternById(node1.getPatternId()).addOutEdge(node2.getPatternId());
        var newEdge = new NetworkYun.Edge({
            source:nodeId1,
            target:nodeId2,
            id:nodeId1+'-'+nodeId2
        },true);
        this.edges.push(newEdge);
        dataStore.edges.add(newEdge);
    }
    else if(node1.getIndex()==-2&&node2.getIndex()==-2){
        this.getDomainById(node1.getDomainId()).domainEdges.push(node2.getDomainId());
        var newEdge = new NetworkYun.Edge({
            source:nodeId1,
            target:nodeId2,
            id:nodeId1+'-'+nodeId2
        },true);
        this.edges.push(newEdge);
        dataStore.edges.add(newEdge);
    }
};

NetworkYun.Network.prototype.judgeEdgeToDel = function(edgeId){
    var edge = this.getEdgeById(edgeId);
    var from = this.getNodeById(edge.getFrom());
    var to = this.getNodeById(edge.getTo());
    console.log(from);
    console.log(to);
    if(from.getIndex()==0&&to.getIndex()==0){
        return true;
    }
    else if(from.getIndex()==-2&&to.getIndex()==-2){
        if(this.getOutdomainList(from.getDomainId()).length>1&&this.getOutdomainList(to.getDomainId()).length>1){
            if(this.judgeDomainConn(from.getDomainId(),to.getDomainId())) return true;
        }
        else return false;
    }
    return false;
};

NetworkYun.Network.prototype.deleteEdge = function(edgeId){
    var edge = this.getEdgeById(edgeId);
    var from = this.getNodeById(edge.getFrom());
    var to = this.getNodeById(edge.getTo());
    if(from.getIndex()==0&&to.getIndex()==0){
        this.getPatternById(from.getPatternId()).deleteOutEdge(to.getPatternId());
        this.getPatternById(to.getPatternId()).deleteOutEdge(from.getPatternId());
        this.removeEdgeById(edgeId);
        dataStore.edges.remove(edgeId);
    }
    else if(from.getIndex()==-2&&to.getIndex()==-2){
        this.getDomainById(from.getDomainId()).delDomainEdge(to.getDomainId());
        this.getDomainById(to.getDomainId()).delDomainEdge(from.getDomainId());
        this.removeEdgeById(edgeId);
        dataStore.edges.remove(edgeId);
    }
};



NetworkYun.Message = function(props){
    this.from = props._from;
    this.to = props._to;
    this.msg = props.msg;
    this.sender = props.sender;
    this.msgId = props.msgId;
    this.blocked = props.blockedAt;
    this.ctime = props.createdAt;
    return this;
};
