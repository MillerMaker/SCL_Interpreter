from enum import Enum
from Token import Token, Type

class Node :

    def __init__(self, type) :
        self.type = type
        self.value = ""
        self.children = []
    
    def getType(self) :
        return self.type
        
    def getValue(self) :
        return self.value
    
    def containsChild(self, query):
        for node in self.children:
            if node.getType == query:
                return True
        return False

    def getChild(self, query) :
        #Search the children for a node who's type matches the query
        for node in self.children : 
            if node.getType() == query:
                return node
        print("ERROR, Type not found!")
        return Node("TYPE NOT FOUND")
    
    def getChildren(self):
        return self.children
    
    def setValue(self, value) :
        self.value = value
    
    #Adds a child to the array of children nodes.
    def addChild(self, node) :
        self.children.append(node)

    #Adds an identifier to the array of children nodes.
    def addIdentifier(self, value) :
        child = Node("identifier")
        child.setValue(value)
        self.children.append(child)
    
    #Adds an operator to the array of children nodes.
    def addOperator(self, value) :
        child = Node("operator")
        child.setValue(value)
        self.children.append(child)

    #Adds a string to the array of children nodes.
    def addString(self, value) :
        child = Node("string")
        child.setValue(value)
        self.children.append(child)

    #Adds a number to the array of children nodes.
    def addNumber(self, value) :
        child = Node("number")
        child.setValue(value)
        self.children.append(child)
    
    def printNode(self, indent) :
        if self.type == "identifier" :
            print(indent + "found identifier: " + self.value)
        elif self.type == "operator" : 
            print(indent + "found operator: " + self.value)
        elif self.type == "string" : 
            print(indent + "found string: \"" + self.value + "\"")
        elif self.type == "number" : 
            print(indent + "found number: " + self.value + "")
        else:
            print(indent + "Parsed <" + str(self.type) + ">")
            for node in self.children: 
                node.printNode(indent + "\t")
            print(indent + "Exited <" + str(self.type) + ">")

    
class NodeType(Enum):
    #KEYWORDS
    start = "<start>"
    imports = "<imports>"
    implement = "<implementations>"
    func_main = "<func_main"
    const_var_struct = "<const_dec>"
    var_dec = "<var_dec>"
    