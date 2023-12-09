from Parser import Parser
from Node import Node
    
class Executor():
    def __init__(self):
        ################ VARIABLES ################
        p = Parser()
        head = p.getParseTree()
        memory = {}

        ############# DEFINE FUNCTIONS #############
        def start():
            imports(head)
            implement(head)
            
        def imports(parent):
            #Import each child of the import node
            for child in parent.getChild("import").getChildren():
                print("Imported " + child.getValue())
        
        def implement(parent):
            variables(parent.getChild("implement").getChild("const_var_struct"))
            actions(parent.getChild("implement").getChild("pactions"))

        def variables(parent):
            #For each variable node, create a new memory entry. 
            for child in parent.getChildren() :
                var = {
                    "value" : "",
                    "type" : child.getChild("type").getValue().value
                }
                memory.update({child.getChild("identifier").getValue() : var})
    
        def actions(parent):
            #Call the appropriate action for each node in pactions
            for child in parent.getChildren():
                match (child.getType()):
                    case "set":
                        setAction(child)
                    case "display":
                        displayAction(child)
        
        def setAction(parent):
            #Parent node has two children, identifier, and expression. 
            variable = memory[parent.getChild("identifier").getValue()]
            value = expr(parent.getChild("expr"))
            memory[parent.getChild("identifier").getValue()]["value"] = value

            #print("Set the value of " + parent.getChild("identifier").getValue() +" to: "+ str(value))

        def displayAction(parent):
            #Parent node has one child, param list.
            value = ""
            for child in parent.getChild("paramList").getChildren():
                value += str(expr(child))
            print(str(value))

        def expr(parent): 
            #If the parent node contains an operator, then it must contain two terms. Otherwise,
            #There's only one term in the node.
            children = parent.getChildren()

            
            if len(children) == 3:
                return operation(term(children[0]), term(children[2]), children[1].getValue()).getValue()
            return term(children[0]).getValue()
        
        def term(parent):
            #If the parent node contains an operator, then it must contain two values. Otherwise,
            #There's only one value in the node
            children = parent.getChildren()

            #First, if the children are variable names, load the values into the nodes
            for child in children:
                if child.getType() == "identifier":
                    child.setValue(memory[child.getValue()]["value"])

            if len(children) == 3:
                return operation(children[0], children[2], children[1].getValue())
            return children[0]
        
        #When given two value nodes and an operator, this function completes the operation based on the 
        #Type of the value, whether string, number, or variable. 
        def operation(value1, value2, operator):
            result = value1
            match (operator):
                case "+":
                    #Check if value is string or number. 
                    if value1.getType() == "string" :
                       result.setValue(value1.getValue() + value2.getValue()) 
                    else:
                        result.setValue(float(value1.getValue()) + float(value2.getValue()))
                case "-":
                    if value1.getType() == "string" :
                       result.setValue(value1.getValue() + value2.getValue())
                    else:
                        result.setValue(float(value1.getValue()) + float(value2.getValue()))
                case "*":
                    if value1.getType() == "string" :
                       print("Error, can't multiply strings")
                       result.setValue("Error, can't multiply strings")
                    else:
                        result.setValue(float(value1.getValue()) * float(value2.getValue()))
                case "/":
                    if value1.getType() == "string" :
                       print("Error, can't divide strings")
                       result.setValue("Error, can't divide strings")
                    else:
                        result.setValue(float(value1.getValue()) / float(value2.getValue()))
                case __: 
                    print("invalid operator")
            return result
        ############# BEGIN EXECUTION #############
        start()
        #print(memory.items())
    

ex = Executor() 