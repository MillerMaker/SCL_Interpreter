from enum import Enum

# These two classes outline the list of keywords, operators and literals defined in the file
# "Cohen's SCL Grammar" Stored in the program folder

class Token : 
    def __init__(self, lexeme):
        self.type = Type.getType(lexeme)
        self.value = lexeme
    
    def getType(self): 
        return self.type
    
    def getValue(self):
        return self.value
    
    def printToken(self):
        print("Token of type " + str(self.type.name))

class Type(Enum):
    
    #KEYWORDS
    IMPORT = "import"
    QUOTES = "\""
    IMPLEMENTATIONS = "implementations"
    FUNCTION = "function"
    MAIN = "main"
    IS = "is"
    VARIABLES = "variables"
    DEFINE = "define"
    OF = "of"
    TYPE = "type"
    CHAR = "char"
    COMMA = ","
    INTEGER = "integer"
    DOUBLE = "double"
    FLOAT = "float"
    TSTRING = "string"
    TBOOL = "boolean"
    PBEGIN = "begin"
    SET = "set"
    INPUT = "input"
    DISPLAY = "display"
    RETURN = "return"
    IF = "if"
    THEN = "then"
    EXIT = "exit"
    ENDIF = "endif"
    ENDFUN = "endfun"

    #OPERATORS
    EQUOP = "="
    PLUS = "+"
    MINUS = "-"
    STAR = "*"
    DIVOP = "/"
    EQUALS = "=="
    GREATERT = ">"
    LESST = "<"
    OR = "||"
    AND = "&&"
    NOT = "!"

    #SPECIAL CHARACTERS
    IDENTIFIER = ""
    LP = "("
    RP = ")"

    def getType(lexeme) : 
        for type in Type:
            if type.value == lexeme : 
                return type
            
        return Type.IDENTIFIER