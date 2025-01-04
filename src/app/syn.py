
# ! TO fix : the hard coded end values 
class SyntaxAnalyzer:
    def __init__(self, tokens=None):
        self.tokens = tokens
        self.current_token_index = 0
        self.aplyed_rules = []

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
    
    def save_REGLES(self, file_path="./logs/regles.txt"):
        with open(file_path, "w") as file:
            for rule in self.aplyed_rules:
                file.write(f"{rule}\n")
        return True
    
    
    def syntax_analyzer(self, file_path="output.txt"):
        tokens = self.read_file(file_path)
        self.tokens = tokens
        self.parse_ProgrammeAlgoLang()
        self.save_REGLES()
        return True
    
    def match(self, expected_token_type, type=0):
        if type == 1:
            current_token = self.tokens[self.current_token_index][1].split("_")[0]
        else :
            current_token = self.tokens[self.current_token_index][1]
        
        if self.current_token_index < len(self.tokens) and current_token == expected_token_type:
            self.current_token_index += 1
        else:
            raise SyntaxError(f"Expected {expected_token_type}, found {self.tokens[self.current_token_index][1]}")

    def parse_ProgrammeAlgoLang(self):
        self.aplyed_rules.append("<ProgrammeAlgoLang>::= programme <NomProgramme> ; <Corps> .")
        self.match("Keyword_programme")
        self.match("Name")
        self.match("Semicolon")
        self.parse_Corps()
        self.match("END")

    def parse_Corps(self):
        self.aplyed_rules.append("<Corps>::=[<PartieDéfinitionConstante>][<PartieDéfinitionVariable>] <InstrComp>")
        if self.current_token_index < len(self.tokens) and self.tokens[self.current_token_index][1] == "Keyword_constante":
            self.parse_PartieDéfinitionConstante()
        if self.current_token_index < len(self.tokens) and self.tokens[self.current_token_index][1] == "Keyword_variable":
            self.parse_PartieDéfinitionVariable()
        self.parse_InstrComp()

    def parse_PartieDéfinitionConstante(self):
        self.aplyed_rules.append("<PartieDéfinitionConstante>::= constante <DéfinitionConstante> {<DéfinitionConstante>}")
        self.match("Keyword_constante")
        self.parse_DéfinitionConstante()
        while self.current_token_index < len(self.tokens) and self.tokens[self.current_token_index][1] == "Name":
            self.parse_DéfinitionConstante()

    def parse_DéfinitionConstante(self):
        self.aplyed_rules.append("<DéfinitionConstante> ::=<NomConstante>=<Constante> ;")
        self.match("Name")
        self.match("RelOperator_E")
        self.parse_Constante()
        self.match("Semicolon")

    def parse_PartieDéfinitionVariable(self):
        self.aplyed_rules.append("<PartieDéfinitionVariable>::= variable <DéfinitionVariable> {<DéfinitionVariable>}")
        self.match("Keyword_variable")
        self.parse_DéfinitionVariable()
        while self.current_token_index < len(self.tokens) and self.tokens[self.current_token_index][1] == "Name":
            self.parse_DéfinitionVariable()

    def parse_DéfinitionVariable(self):
        self.aplyed_rules.append("<DéfinitionVariable>::=<GroupeVariable>;")
        self.parse_GroupeVariable()
        self.match("Semicolon")

    def parse_GroupeVariable(self):
        self.aplyed_rules.append("<GroupeVariable>::=<NomVariable>{,<NomVariable>}:<Type>")
        self.match("Name")
        while self.current_token_index < len(self.tokens) and self.tokens[self.current_token_index][1] == "COMMA":
            self.match("COMMA")
            self.match("Name")
        self.match("COLON")
        self.match("TypeName",1) # ! TOBE FIXED

    def parse_Constante(self):
        self.aplyed_rules.append("<Constante>::= <Nombre> | <NomConstante>")
        if self.current_token_index < len(self.tokens) and self.tokens[self.current_token_index][1] == "Number":
            self.match("Number")
        else:
            self.match("Name")

    def parse_InstrComp(self):
        self.aplyed_rules.append("<InstrComp>::= debut <Instruction> {;<Instruction>} fin")
        self.match("Keyword_debut")
        self.parse_Instruction()
        while self.current_token_index < len(self.tokens) and self.tokens[self.current_token_index][1] == "Semicolon":
            self.match("Semicolon")
            self.parse_Instruction()
        self.match("Keyword_fin")

    def parse_Instruction(self):
        self.aplyed_rules.append("<Instruction>::=<InstructionAffectation>|<InstructionRépéter>|<InstrComp>|<Vide>")
        if self.current_token_index < len(self.tokens) and self.tokens[self.current_token_index][1] == "Name":
            self.parse_InstructionAffectation()
        elif self.current_token_index < len(self.tokens) and self.tokens[self.current_token_index][1] == "Keyword_répéter":
            self.parse_InstructionRépéter()
        elif self.current_token_index < len(self.tokens) and self.tokens[self.current_token_index][1] in ("Keyword_debut", "Semicolon"):
            self.parse_InstrComp()
        else:
            self.parse_Vide()

    def parse_InstructionAffectation(self):
        self.aplyed_rules.append("<InstructionAffectation>::=<NomVariable>:=<Expression>")
        self.match("Name")
        self.match("ASSIGNMENT")
        self.parse_Expression()

    def parse_Expression(self):
        self.aplyed_rules.append("<Expression>::=<ExpressionSimple> [<OpRelExp> <ExpressionSimple>]")
        self.parse_ExpressionSimple()
        if self.current_token_index < len(self.tokens) and str(self.tokens[self.current_token_index][1]).startswith("RelOperator"):
            self.parse_OpRelExp()

    def parse_OpRelExp(self):
        self.match("RelOperator",1)
        self.parse_ExpressionSimple()

    def parse_ExpressionSimple(self):
        self.aplyed_rules.append("<ExpressionSimple>::=[<OperateurSigne>]<Terme> {<OpAdTerm> <Terme>}")
        if self.current_token_index < len(self.tokens) and str(self.tokens[self.current_token_index][1]).startswith("AddOperator") :
            self.match("AddOperator",1)
        self.parse_Terme()
        while self.current_token_index < len(self.tokens) and str(self.tokens[self.current_token_index][1]).startswith("AddOperator") :
            self.parse_OpAdTerm()

    def parse_OpAdTerm(self):
        self.match("AddOperator",1)
        self.parse_Terme()

    def parse_Terme(self):
        self.aplyed_rules.append("<Terme>::=<Facteur> {<OpMulFact> <Facteur>}")
        self.parse_Facteur()
        if self.current_token_index < len(self.tokens) and str(self.tokens[self.current_token_index][1]).startswith("MultOperator"):
            self.parse_OpMulFact()

    def parse_OpMulFact(self):
        self.match("MultOperator",1)
        self.parse_Facteur()

    def parse_Facteur(self):
        self.aplyed_rules.append("<Facteur>::=<Constante>|<NomVariable>|(<Expression>)")
        if self.current_token_index < len(self.tokens) and self.tokens[self.current_token_index][1] == "Number":
            self.parse_Constante()
        elif self.current_token_index < len(self.tokens) and self.tokens[self.current_token_index][1] == "Name":
            self.match("Name")
        else:
            self.match("left-parenthesis")
            self.parse_Expression()
            self.match("right-parenthesis")

    def parse_InstructionRépéter(self):
        self.aplyed_rules.append("<InstructionRépéter>::= répéter <Instruction> jusqua <Condition>")
        self.match("Keyword_répéter")
        self.parse_Instruction()
        self.match("Keyword_jusqua")
        self.parse_Condition()

    def parse_Condition(self):
        self.aplyed_rules.append("<Condition> ::= <Expression> <OperateurRelationnel> <Expression>/(<Condition>)")
        if self.current_token_index < len(self.tokens) and self.tokens[self.current_token_index][1] == "left-parenthesis":
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
        self.aplyed_rules.append("<Vide>::=''")
        pass

# Example usage
# analyzer = SyntaxAnalyzer(lex("programme x1; debut x2 := 2; fin."))
# analyzer.parse_ProgrammeAlgoLang()
# print("Parsing successful!")