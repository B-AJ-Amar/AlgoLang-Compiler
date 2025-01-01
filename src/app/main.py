from lex import LexicalAnalizer
from syn import SyntaxAnalyzer


class Compiler:
    def __init__(self,input_path="input.txt", output_path="output.txt"):
        self.input_path = input_path
        self.output_path = output_path
        self.lexical_analyzer = LexicalAnalizer()
        self.syntax_analyzer = SyntaxAnalyzer()
        
    def compile(self):
        tokens = self.lexical_analyzer.lexical_analyzer(self.input_path, self.output_path)
        self.syntax_analyzer.tokens = tokens
        print(self.syntax_analyzer.tokens)
        resault = self.syntax_analyzer.parse_ProgrammeAlgoLang()
        return resault
    

if __name__ == "__main__":
    compiler = Compiler()
    compiler.compile()
    print("Compilation done successfully")
      






