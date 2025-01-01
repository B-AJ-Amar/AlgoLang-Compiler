
import string

final_states = {
    9:  "Keyword_programme",
    18: "Keyword_constante",
    34: "Keyword_variable",
    39: "Keyword_debut",
    42: "Keyword_fin",
    49: "Keyword_répéter",
    58: "Keyword_jusqua",
    
    26: "TypeName_caractere",
    51: "TypeName_réel",
    64: "TypeName_entier",
    
    65: "MultOperator_et",
    68: "MultOperator_mod",
    71: "MultOperator_div",
    69: "MultOperator_mult",
    
    73: "AddOperator_ou",
    78: "AddOperator_plus",
    79: "AddOperator_minus",
    80: "RelOperator_L",
    81: "RelOperator_LE",
    82: "RelOperator_NE",
    83: "RelOperator_G",
    84: "RelOperator_GE",
    85: "RelOperator_E",
    
    86: "Semicolon",
    
    75: "Name",
    
    77: "Number",
    
    88: "Float",
    
    89: "END",
    90: "COMMA",
    91: "COLON",
    92: "ASSIGNMENT",
    
    93: "left-parenthesis",
    94: "right-parenthesis",
    
    
}


# the states should be referred only by numbers 
rules = {
    0: {
        # Keywords
        "p": 1, "c": 10, "v": 27, "d": 35, "f": 40, "r": 43, "j": 52, ";": 86,
        ".": 89, ",": 90, ":": 91,
        
        # Relational Operators
        "<": 80, ">": 83, "=": 85,
        
        # Addition Operators
        "+": 78, 
        "-": 79,  
        "o": 72,
        
        # Multiplication Operators
        "e": 59, "m": 66, "*": 69, 
        
        # Parenthesis
        "(": 93, ")": 94,
        
        # Name
        **{x: 74 for x in string.ascii_letters if x not in "pcvdfrjome"},
        
        # Numbers
        **{x: 77 for x in string.digits},
    },
    
    # Keywords
    1: {"r": 2,**{x: 75 for x in string.digits}},
    2: {"o": 3},
    3: {"g": 4},
    4: {"r": 5},
    5: {"a": 6},
    6: {"m": 7},
    7: {"m": 8},
    8: {"e": 9},  # programme_FOUND
    
    10: {"o": 11, "a": 19,**{x: 75 for x in string.digits}},
    11: {"n": 12},
    12: {"s": 13},
    13: {"t": 14},
    14: {"a": 15},
    15: {"n": 16},
    16: {"t": 17},
    17: {"e": 18},  # constante_FOUND
    
    19: {"r": 20},
    20: {"a": 21},
    21: {"c": 22},
    22: {"t": 23},
    23: {"è": 24,"e":24},
    24: {"r": 25},
    25: {"e": 26},  # caractère_FOUND
    
    27: {"a": 28,**{x: 75 for x in string.digits}},
    28: {"r": 29},
    29: {"i": 30},
    30: {"a": 31},
    31: {"b": 32},
    32: {"l": 33},
    33: {"e": 34},  # variable_FOUND
    
    35: {"e": 36, "i": 70,**{x: 75 for x in string.digits}},
    36: {"b": 37},
    37: {"u": 38},
    38: {"t": 39},  # debut_FOUND
    70: {"v": 71},
    
    40: {"i": 41,**{x: 75 for x in string.digits}},
    41: {"n": 42},  # fin_FOUND
    
    43: {"é": 44, "e": 44,**{x: 75 for x in string.digits}},
    44: {"p": 45, "é": 50, "e": 50},
    45: {"é": 46, "e": 46},
    46: {"t": 47},
    47: {"e": 48},
    48: {"r": 49},  # répéter_FOUND
    
    50: {"l": 51},  # reel_FOUND
    
    52: {"u": 53,**{x: 75 for x in string.digits}},
    53: {"s": 54},
    54: {"q": 55},
    55: {"u": 56},
    56: {"'": 57,"’":57},
    57: {"a": 58, "à": 58},  # jusqua_FOUND
    
    59: {"n": 60, "t": 65,**{x: 75 for x in string.digits}},
    60: {"t": 61},
    61: {"i": 62},
    62: {"e": 63},
    63: {"r": 64},  # entier_FOUND
    
    66: {"o": 67,**{x: 75 for x in string.digits}},
    67: {"d": 68},  # mod_FOUND
    
    72: {"u": 73,**{x: 75 for x in string.digits}},  # ou_FOUND
    
    87 :{**{x: 88 for x in string.digits}},
    
    
    
    # Final states
    **{i: {} for i in final_states.keys()},
    
    # overide the final states with other states
    74: {**{x: 75 for x in string.digits}},
    75: {**{x: 76 for x in string.ascii_lowercase}},
    76: {**{x: 75 for x in string.digits}},
    77: {**{x: 77 for x in string.digits}, ".": 87},
    80: {">": 82, "=": 81},
    83: {"=": 84},
    88: {**{x: 88 for x in string.digits}},
    91: {"=": 92},
}


class LexicalAnalizer:
    def __init__(self, rules=rules, final_states=final_states):
        self.rules = rules
        self.final_states = final_states
        
        
        
        
    def lexical_analyzer(self, file_path="input.txt",output_path="output.txt", save=True):
        code = self.read_file(file_path)
        tokens =  self.run(code)  
        if save: self.save_tokens(tokens, output_path)
        return tokens
    
    def read_file(self, file_path):
        with open(file_path, "r") as file:
            return file.read()
        
      
    def save_tokens(self, tokens, file_path="./output.txt"):
        with open(file_path, "w") as file:
            for token in tokens:
                file.write(f"{token[0]}|{token[1]}|{token[2]}\n")
                
                
    def run(self, code):
        code = code.lower()
        tokens = []
        state = 0
        buffer = ""
        position = 0

        while position < len(code):
            char = code[position]
            next_state = self.rules.get(state, {}).get(char)
            if char.isspace():
                if state in self.final_states:
                    tokens.append((buffer, self.final_states[state], position - len(buffer)))
                state = 0
                buffer = ""
            elif next_state is not None:
                state = next_state
                buffer += char

            else:
                if state in self.final_states:
                    tokens.append((buffer, self.final_states[state], position - len(buffer)))
                    state, buffer = 0, ""
                    if char != " ":
                        position -= 1
                elif state != 0:
                    raise Exception(f"Lexical Error: Unexpected character '{char}' after `{buffer}` at position {position}")
                else:
                    raise Exception(f"Lexical Error: Unexpected character '{char}' at position {position}")

            position += 1
        if state in self.final_states:
            tokens.append((buffer, self.final_states[state], position - len(buffer)))
        return tokens

# test
if __name__ == "__main__":  
    lexer = LexicalAnalizer(rules, final_states)
    tokens = lexer.run("programme a1; variable b1; constante c1; debut répéter jusqu'a; fin.")
    print(tokens)