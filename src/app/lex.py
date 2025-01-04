from automate import rules, final_states

class LexicalAnalizer:
    def __init__(self, rules=rules, final_states=final_states):
        self.rules = rules
        self.final_states = final_states   
    
        
    def lexical_analyzer(self, file_path="./input.txt",output_path="./token.txt", save=True):
        code = self.read_file(file_path)
        tokens =  self.run(code)  
        if save: self.save_tokens(tokens, output_path)
        return tokens
    
    
    def read_file(self, file_path):
        with open(file_path, "r") as file:
            return file.read()
              
      
    def save_tokens(self, tokens, file_path="./token.txt"):
        with open(file_path, "w") as file:
            for token in tokens:
                file.write(f"{token[0]}|{token[1]}\n")
                
                
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
                    tokens.append((buffer, self.final_states[state]))
                state = 0
                buffer = ""
            elif next_state is not None:
                state = next_state
                buffer += char

            else:
                if state in self.final_states:
                    tokens.append((buffer, self.final_states[state]))
                    state, buffer = 0, ""
                    if char != " ":
                        position -= 1
                elif state != 0:
                    raise Exception(f"Lexical Error: Unexpected character '{char}' after `{buffer}` at position {position}")
                else:
                    raise Exception(f"Lexical Error: Unexpected character '{char}' at position {position}")

            position += 1
        if state in self.final_states:
            tokens.append((buffer, self.final_states[state]))
        return tokens

# test
if __name__ == "__main__":  
    lexer = LexicalAnalizer(rules, final_states)
    tokens = lexer.run("programme a1; variable b1; constante c1; debut répéter jusqu'a; fin.")
    print(tokens)