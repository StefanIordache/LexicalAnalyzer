keywords = ["auto", "break", "case", "char", "const", "continue", "default",
            "do", "double", "else", "enum", "extern", "float", "for", "goto",
            "if", "int", "long", "register", "return", "short", "signed", "sizeof",
            "static", "struct", "switch", "typedef", "union", "unsigned", "void",
            "volatile", "while", "asm", "bool", "catch", "class", "const_cast",
            "delete", "dynamic_cast", "explicit", "false", "friend", "inline",
            "mutable", "namespace", "new", "operator", "private", "protected",
            "public", "reinterpret_cast", "static_cast", "template", "this",
            "throw", "true", "try", "typeid", "typename", "virtual", "using", "whchar_t"]

code = None
current_line = 1
current_column = 0
current_char = 0
input_length = 0


def analyze_cpp(input_code):
    output = ''
    global input_length, current_char
    input_length = len(input_code)
    while current_char < input_length:
        ch = input_code[current_char]
        print(ch)
        current_char = current_char + 1
    return output
