
# ! TO fix : the hard coded end values 
class SyntaxAnalyzer:
    def __init__(self, tokens=None):
        self.tokens = tokens
        self.current_token_index = 0

    def read_file(self, file_path):
        "this should pass line by line get the tokens and put them in array of lists [(1,2,3),(4,5,6)...]"
        # read line by line python
        tokens = []
        file = open(file_path, "r")
        while True:
            line = file.readline()
            if not line: break
            tokens.append(line.split("|"))
        file.close()
        return tokens
    
    
    def syntax_analyzer(self, file_path="output.txt"):
        tokens = self.read_file(file_path)
        self.tokens = tokens
        self.parse_ProgrammeAlgoLang()
        return True
    
    def match(self, expected_token_type, type=0):
        print(f"    Matching {expected_token_type} with {self.tokens[self.current_token_index]}")
        if type == 1:
            current_token = self.tokens[self.current_token_index][1].split("_")[0]
        else :
            current_token = self.tokens[self.current_token_index][1]
        
        if self.current_token_index < len(self.tokens) and current_token == expected_token_type:
            self.current_token_index += 1
        else:
            raise SyntaxError(f"Expected {expected_token_type}, found {self.tokens[self.current_token_index][1]}")

    def parse_ProgrammeAlgoLang(self):
        self.match("Keyword_programme")
        self.match("Name")
        self.match("Semicolon")
        self.parse_Corps()
        self.match("END")

    def parse_Corps(self):
        if self.current_token_index < len(self.tokens) and self.tokens[self.current_token_index][1] == "Keyword_constante":
            self.parse_PartieDéfinitionConstante()
        if self.current_token_index < len(self.tokens) and self.tokens[self.current_token_index][1] == "Keyword_variable":
            self.parse_PartieDéfinitionVariable()
        self.parse_InstrComp()

    def parse_PartieDéfinitionConstante(self):
        self.match("Keyword_constante")
        self.parse_DéfinitionConstante()
        while self.current_token_index < len(self.tokens) and self.tokens[self.current_token_index][1] == "Name":
            self.parse_DéfinitionConstante()

    def parse_DéfinitionConstante(self):
        self.match("Name")
        self.match("RelOperator_E")
        self.parse_Constante()
        self.match("Semicolon")

    def parse_PartieDéfinitionVariable(self):
        self.match("Keyword_variable")
        self.parse_DéfinitionVariable()
        while self.current_token_index < len(self.tokens) and self.tokens[self.current_token_index][1] == "Name":
            self.parse_DéfinitionVariable()

    def parse_DéfinitionVariable(self):
        self.parse_GroupeVariable()
        self.match("Semicolon")

    def parse_GroupeVariable(self):
        self.match("Name")
        while self.current_token_index < len(self.tokens) and self.tokens[self.current_token_index][1] == "COMMA":
            self.match("COMMA")
            self.match("Name")
        self.match("COLON")
        self.match("TypeName",1) # ! TOBE FIXED

    def parse_Constante(self):
        if self.current_token_index < len(self.tokens) and self.tokens[self.current_token_index][1] == "Number":
            self.match("Number")
        else:
            self.match("Name")

    def parse_InstrComp(self):
        self.match("Keyword_debut")
        self.parse_Instruction()
        while self.current_token_index < len(self.tokens) and self.tokens[self.current_token_index][1] == "Semicolon":
            self.match("Semicolon")
            self.parse_Instruction()
        self.match("Keyword_fin")

    def parse_Instruction(self):
        if self.current_token_index < len(self.tokens) and self.tokens[self.current_token_index][1] == "Name":
            self.parse_InstructionAffectation()
        elif self.current_token_index < len(self.tokens) and self.tokens[self.current_token_index][1] == "Keyword_répéter":
            self.parse_InstructionRépéter()
        elif self.current_token_index < len(self.tokens) and self.tokens[self.current_token_index][1] == "Keyword_debut":
            self.parse_InstrComp()
        else:
            self.parse_Vide()

    def parse_InstructionAffectation(self):
        self.match("Name")
        self.match("ASSIGNMENT")
        self.parse_Expression()

    def parse_Expression(self):
        self.parse_ExpressionSimple()
        if self.current_token_index < len(self.tokens) and str(self.tokens[self.current_token_index][1]).startswith("RelOperator"):
            print("PARSING : ",self.tokens[self.current_token_index])
            self.parse_OpRelExp()

    def parse_OpRelExp(self):
        self.match("RelOperator",1) # ! TOFIX
        self.parse_ExpressionSimple()

    def parse_ExpressionSimple(self):
        if self.current_token_index < len(self.tokens) and str(self.tokens[self.current_token_index][1]).startswith("AddOperator") :
            self.match("AddOperator",1)
        self.parse_Terme()
        while self.current_token_index < len(self.tokens) and str(self.tokens[self.current_token_index][1]).startswith("AddOperator") :
            self.parse_OpAdTerm()

    def parse_OpAdTerm(self):
        self.match("AddOperator",1)
        self.parse_Terme()

    def parse_Terme(self):
        self.parse_Facteur()
        if self.current_token_index < len(self.tokens) and str(self.tokens[self.current_token_index][1]).startswith("MultOperator"):
            self.parse_OpMulFact()

    def parse_OpMulFact(self):
        self.match("MultOperator",1)
        self.parse_Facteur()

    def parse_Facteur(self):
        if self.current_token_index < len(self.tokens) and self.tokens[self.current_token_index][1] == "Number":
            self.parse_Constante()
        elif self.current_token_index < len(self.tokens) and self.tokens[self.current_token_index][1] == "Name":
            self.match("Name")
        else:
            self.match("left-parenthesis")
            self.parse_Expression()
            self.match("right-parenthesis")

    def parse_InstructionRépéter(self):
        self.match("Keyword_répéter")
        self.parse_Instruction()
        self.match("Keyword_jusqua")
        self.parse_Condition()

    def parse_Condition(self):
        if self.current_token_index < len(self.tokens) and self.tokens[self.current_token_index][1] == "left-parenthesis":
            print(f">PARSING CONDITION (CON) : {self.tokens[self.current_token_index]}")
            self.match("left-parenthesis")
            self.parse_Condition()
            self.match("right-parenthesis")
        else: #! TO FIX
            temp_curent_index = self.current_token_index
            self.parse_Expression()
            try:
                self.match("RelOperator",1)
            except:
                self.current_token_index = temp_curent_index
                self.parse_ExpressionSimple()
            self.match("RelOperator",1)
            self.parse_Expression()
            
    def parse_Vide(self):
        pass

# Example usage
# analyzer = SyntaxAnalyzer(lex("programme x1; debut x2 := 2; fin."))
# analyzer.parse_ProgrammeAlgoLang()
# print("Parsing successful!")