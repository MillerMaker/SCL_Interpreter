from Token import Token, Type

class Scanner():
    # Instantiated by parser, creates a token list
    # Constructor
    def __init__(self, path) :

        #Index used by next()
        self.i = 0

        self.currentToken = Token("")

        #init path
        self.path = path
        self.file = open(path, "r")
        self.text = self.file.read()

    #Given a string file, scan each lexeme one at a time. This function also eliminates comments. 
    def next(self) :
        tokenList = []
        lexeme = ""
        while self.i < len(self.text): 
            char = self.text[self.i]
            #DEBUG CODE V  V  V 
            #print(lexeme)
            match char:
                    case " ": 
                        break
                    case "\n":
                        break
                    case "/" :
                        #Check for comments. If the next character is "/" or "*", skip
                        #characters until we get to a new line or "*/". 
                        if self.text[self.i + 1] == "/":
                            while not self.text[self.i] == "\n": self.i += 1
                            self.i += 1
                        elif self.text[self.i +1] == "*":
                            while not (self.text[self.i] == "*" and self.text[self.i + 1] == "/"): self.i += 1
                            self.i += 1
                        else : lexeme += char
                    case "\"" :
                        # Remove Quotations
                        if lexeme == "" :
                            lexeme = char
                            break
                        else : 
                            self.i = self.i - 1
                            break
                    case "+" :
                        # Remove Addition
                        #If lexeme is empty, add +. otherwise, return the current lexeme, and break. 
                        if lexeme == "" :
                            lexeme = char
                            break
                        else : 
                            self.i = self.i - 1
                            break
                    case "-" :
                        # Remove subtraction
                        if lexeme == "" :
                            lexeme = char
                            break
                        else : 
                            self.i = self.i - 1
                            break
                    case "," :
                        # Remove subtraction
                        if lexeme == "" :
                            lexeme =  char
                            break
                        else : 
                            self.i = self.i - 1
                            break                    
                    case _:
                        lexeme += char
            self.i += 1
        self.i += 1

        # we don't want empty lexemes, so call next again if this is the case.
        if lexeme == "":
            return self.next()
        else : 
            # Now that we have a lexeme, tokenize and return. 
            #print(str(self.currentToken.getType()))
            self.currentToken = Token(lexeme)
            #DEBUG CODE V  V  V 
            #print("Token Value: " + str(self.currentToken.getType()))
            return self.currentToken
    
    # Makes Next() call the previous token. 
    def previous(self) :
        #print("We are about to call previous. the current token: "  + self.currentToken.getType().value)
        if self.currentToken.getType() is Type.PLUS or self.currentToken.getType() is Type.COMMA or self.currentToken.getType() is Type.MINUS or self.currentToken.getType() is Type.STAR or self.currentToken.getType() is Type.DIVOP  or self.currentToken.getType() is Type.QUOTES:
            self.i = self.i - (len(self.currentToken.getType().value))
        else :
            self.i = self.i - (len(self.currentToken.getType().value)+1)
    # Used by parser to get the current token object
    def getCurrentToken(self) :
        return self.currentToken



