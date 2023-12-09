from Scanner import Scanner
from Token import Token, Type
from Node import Node


class Parser:

    def __init__ (self) :
        ################ VARIABLES ################
        scan = Scanner("src/scanner/sample.scl")
        self.parseTree = Node("start")
        ############# DEFINE FUNCTIONS #############
        def begin():
            while compare(Type.IMPORT):
                self.parseTree.addChild(imports())
            while scan.currentToken.getType() == Type.IMPLEMENTATIONS:
                self.parseTree.addChild(implement())

        def imports(): 
            node = Node("import")
            if compare(Type.QUOTES): 
                id = scan.next()
                if id.type == Type.IDENTIFIER and compare(Type.QUOTES):
                    node.addIdentifier(id.value)
            return node

        #parses Function declaration, calls <const_var_struct> and <pactions>
        def implement():
            node = Node("implement")
            if compare(Type.FUNCTION, Type.MAIN, Type.IS):
                node.addChild(constVarStruct())
                if scan.currentToken.getType() == Type.PBEGIN:
                    node.addChild(pactions())
            return node
        
        # Parses <var_dec>
        def constVarStruct():
            node = Node("const_var_struct")
            if compare(Type.VARIABLES):
                while compare(Type.DEFINE):
                    variable = Node("variable")
                    variable.addIdentifier(scan.next().getValue())
                    if compare(Type.OF, Type.TYPE):
                        type = Node("type")
                        type.setValue(scan.next().getType())
                        variable.addChild(type)
                    node.addChild(variable)
            return node

        #parses actions by creating a new action node until the end of the function 
        def pactions():
            node = Node("pactions")
            while not compare(Type.EXIT):
                #Create new action
                keyword = scan.currentToken.getType()
                #Depending on the first keyword, parse the appropriate action
                match keyword :
                    case Type.SET:
                        #The set statement has the form: SET IDENTIFIER EQUOP <expr>
                        action = Node("set")
                        action.addIdentifier(scan.next().getValue())
                        if compare(Type.EQUOP) : 
                            action.addChild(expr())
                        node.addChild(action)
                    case Type.DISPLAY:
                        #The Display statement has the form: DISPLAY <param_list>
                        action = Node("display")
                        action.addChild(paramList())
                        node.addChild(action)
            return node
        

        # paramList is an <exp>, or a set of <exp> separated by commas
        def paramList():
            node = Node("paramList")
            node.addChild(expr())
            while scan.next().getType() is Type.COMMA:
               node.addChild(expr())
            scan.previous()
            return node
        
        #The <expr> has the form: <term> PLUS/MINUS <term>
        def expr():
            node = Node("expr")
            node.addChild(term())
            #DEBUG CODE V  V  V 
            #print("currentToken " + str(scan.currentToken.getType()))
            if compare(Type.PLUS) :
                node.addOperator("+")
                node.addChild(term())
            elif scan.currentToken.getType() == Type.MINUS:
                node.addOperator("-")
                node.addChild(term())
            else:
                scan.previous()
            return node
        
        # like <expr>, but with * and /
        def term():
            node = Node("term")
            node.addChild(element())
            if compare(Type.STAR) :
                node.addOperator("*")
                node.addChild(element())
            elif scan.currentToken.getType() == Type.DIVOP:
                node.addOperator("/")
                node.addChild(element())
            else:
                #Since we checked for an operator and there was none, we will have to set the scanner back. 
                #This previous doesn't work when checking + 
                scan.previous()
            return node
        
        # An element can be a string, number or identifier. 
        def element():
            token = scan.next()
            match (token.getType()):
                case Type.QUOTES:
                    #If the next token is a quote, we know the element is a string
                    node = Node("string")
                    string = ""
                    while scan.next().getType() is not Type.QUOTES:
                        string += (scan.currentToken.getValue() + " ")
                    node.setValue(string)
                    return node
                case Type.IDENTIFIER:
                    #The scanner doesn't differentiate between numbers and identifiers
                    #If the first value of the token is a number we create a number instead of an identifier.
                    if token.getValue()[0].isdigit() :
                        node = Node("number")
                        node.setValue(token.getValue())
                        return node
                    else:
                        node = Node("identifier")
                        node.setValue(token.getValue())
                        return node
                case _: 
                    print("Tried checking for an element(), but I'm a terrible programmer")
        
        def evaluateString(): 
            pass

        # Helper function that condenses comparison calls
        def compare(*types):
            x = "false"
            for type in types :
                if scan.next().type == type : x = True 
                else:
                    x = False
                    #print("Hey, your comparison between " + str(scan.currentToken.getType()) + " and " + str(type) + " was false")
            return x

        #PARSER EXECUTION#
        begin()
        #DEBUG CODE V  V  V 
        #self.parseTree.printNode("")
    

    def getParseTree(self): 
        return self.parseTree
