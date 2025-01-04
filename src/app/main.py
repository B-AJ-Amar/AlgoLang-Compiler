from lex import LexicalAnalizer
from syn import SyntaxAnalyzer
import argparse

class Compiler:
    def __init__(self,input_path="input.txt", output_path="token.txt"):
        self.input_path = input_path or "input.txt"
        self.output_path = output_path or "token.txt"
        self.lexical_analyzer = LexicalAnalizer()
        self.syntax_analyzer = SyntaxAnalyzer()
        
    def compile(self):
        tokens = self.lexical_analyzer.lexical_analyzer(self.input_path, self.output_path)
        self.syntax_analyzer.tokens = tokens
        resault = self.syntax_analyzer.parse_ProgrammeAlgoLang()
        return resault
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compiler for AlgoLang")
    parser.add_argument("-i", "--input", required=False, help="Path to the input file")
    parser.add_argument("-o", "--output", required=False, help="Path to the output file")
    # add help to the parser
    args = parser.parse_args()
    print(args)
    
    compiler = Compiler(input_path=args.input, output_path=args.output)
    compiler.compile()
    
    print("Compilation done successfully")
      






