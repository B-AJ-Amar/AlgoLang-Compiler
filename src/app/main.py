from lex import LexicalAnalizer
from syn import SyntaxAnalyzer
import argparse

class Compiler:
    def __init__(self,input_path="input.txt", output_path="./logs/token.txt", verbose=True):
        self.input_path = input_path or "input.txt"
        self.output_path = output_path or "./logs/token.txt"
        self.verbose = False if str(verbose) in ["false","f","0"] else True
        self.lexical_analyzer = LexicalAnalizer()
        self.syntax_analyzer = SyntaxAnalyzer()
        
    def compile(self):
        tokens = self.lexical_analyzer.lexical_analyzer(self.input_path, self.output_path)
        self.syntax_analyzer.tokens = tokens
        resault = self.syntax_analyzer.parse_ProgrammeAlgoLang()
        self.syntax_analyzer.save_REGLES()
        
                
        if self.verbose:
            print("="*50)
            print(f"Lexical Analyzer Table des symboles : ")
            print("="*50)
            print(f"{'Value':10}| {'Type'}")
            print('-'*25)
            for token in self.lexical_analyzer.jeton:
                print(f"{token[0]:10}| {token[1]}")
            print("="*50)
            print("Syntax Analyzer stack call:")
            print("="*50)
            for rule in self.syntax_analyzer.aplyed_rules: print(rule)
            print("Compilation done successfully")
        return resault
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compiler for AlgoLang")
    parser.add_argument("-i", "--input", required=False, help="Path to the input file", default="./input.txt")
    parser.add_argument("-o", "--output", required=False, help="Path to the output file", default="./logs/token.txt")
    parser.add_argument("-v", "--verbose", required=False, help="Verbose mode", default=True)
    # add help to the parser
    args = parser.parse_args()
    
    compiler = Compiler(input_path=args.input, output_path=args.output, verbose=args.verbose)
    compiler.compile()
      






