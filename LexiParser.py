import re

class LexicalAnalyzer:
    def __init__(self, code):
        self.code = code
        self.tokens = []

    def tokenize(self):
        code = self.code
        code = code.replace("(", " ( ")
        code = code.replace(")", " ) ")
        code = code.replace("{", " { ")
        code = code.replace("}", " } ")
        code = code.replace("then", " then ")
        code = code.replace("else", " else ")
        code = code.replace("==", " == ")
        code = code.replace("!=", " != ")
        code = code.replace("<=", " <= ")
        code = code.replace(">=", " >= ")
        code = code.replace("=", " = ")
        code = code.replace("<", " < ")
        code = code.replace(">", " > ")
        tokens = code.split()

        # Remove extra whitespaces
        tokens = [token.strip() for token in tokens]

        # Remove empty tokens
        tokens = list(filter(None, tokens))

        self.tokens = tokens

    def get_tokens(self):
        return self.tokens

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.token_index = -1
        self.parse_tree = {}

    def advance(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        else:
            self.current_token = None

    def parse(self):
        self.advance()
        self.parse_tree = self.parse_if_statement()

    def parse_if_statement(self):
        if self.current_token == "if":
            self.advance()
            if self.current_token == "(":
                self.advance()
                condition = self.parse_condition()
                if self.current_token == ")":
                    self.advance()
                    if self.current_token == "then":
                        self.advance()
                        then_action = self.parse_action()
                        if self.current_token == "else":
                            self.advance()
                            else_action = self.parse_action()
                            return {
                                "if": condition,
                                "then": then_action,
                                "else": else_action
                            }
                        else:
                            raise SyntaxError("Expected 'else'")
                    else:
                        raise SyntaxError("Expected 'then'")
                else:
                    raise SyntaxError("Expected ')'")
            else:
                raise SyntaxError("Expected '('")
        else:
            raise SyntaxError("Expected 'if'")

    def parse_condition(self):
        if self.current_token in ["a", "b", "c"]:
            identifier1 = self.current_token
            self.advance()
            comparison_operator = self.parse_comparison_operator()
            if self.current_token in ["a", "b", "c"]:
                identifier2 = self.current_token
                self.advance()
                return {
                    "condition": {
                        "identifier1": identifier1,
                        "operator": comparison_operator,
                        "identifier2": identifier2
                    }
                }
            else:
                raise SyntaxError("Expected identifier")
        else:
            raise SyntaxError("Expected identifier")

    def parse_comparison_operator(self):
        if self.current_token in ["==", "!=", "<", ">", "<=", ">="]:
            operator = self.current_token
            self.advance()
            return operator
        else:
            raise SyntaxError("Expected comparison operator")

    def parse_action(self):
        if self.current_token == "{":
            self.advance()
            statement = self.parse_statement()
            if self.current_token == "}":
                self.advance()
                return {
                    "action": statement
                }
            else:
                raise SyntaxError("Expected '}'")
        else:
            raise SyntaxError("Expected '{'")

    def parse_statement(self):
        if self.current_token in ["a", "b", "c"]:
            identifier1 = self.current_token
            self.advance()
            if self.current_token == "=":
                self.advance()
                if self.current_token in ["a", "b", "c"]:
                    identifier2 = self.current_token
                    self.advance()
                    return {
                        "identifier1": identifier1,
                        "identifier2": identifier2
                    }
                else:
                    raise SyntaxError("Expected identifier")
            else:
                raise SyntaxError("Expected '='")
        else:
            raise SyntaxError("Expected identifier")

    def get_parse_tree(self):
        return self.parse_tree

def main():
    input_string = input("Masukkan if-else statement yang ingin diuji: ")

    try:
        tokens = LexicalAnalyzer(input_string)
        result = Parser(tokens)
        print("Analisis Leksikal dan Grammar berhasil:")
        print(result)
    except SyntaxError as e:
        print("Error:", str(e))


if __name__ == "__main__":
    main()
