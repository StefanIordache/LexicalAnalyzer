from __future__ import print_function
import sys

keywords = ["auto", "break", "case", "char", "const", "continue", "default",
            "do", "double", "else", "enum", "extern", "float", "for", "goto",
            "if", "int", "long", "register", "return", "short", "signed", "sizeof",
            "static", "struct", "switch", "typedef", "union", "unsigned", "void",
            "volatile", "while"]

operators = ["+", "-", "*", "/", ">", "<", "="]

code = None
current_line = 1
current_column = 0
current_char_index = 0
current_char = " "
input_length = 0


def error_alert(line, column, message):
    print("ERROR   %5d   %5d   %-30s" % (line, column, message), end='')


def get_next_char():
    global current_char, current_column, \
        current_line, current_char_index

    current_char = code[current_char_index]
    current_char_index += 1
    current_column += 1

    if current_char == '\n':
        current_line += 1
        current_column = 0

    return current_char


def try_character_constant(line, column):
    ascii_code = ord(get_next_char())

    if current_char == '\'':
        error_alert(line, column, "Empty character constants are not valid")
    elif current_char == '\\':
        get_next_char()
        if current_char == 'n':
            ascii_code = 10
        elif current_char == '\\':
            ascii_code = ord('\\')
        else:
            error_alert(line, column, "Escape sequence not defined \\%c" % (current_char))
    if get_next_char() != '\'':
        error_alert(line, column, "Multi-chracter constants are not defined for C language")

    get_next_char()

    return "integer", line, column, ascii_code


def try_divide_or_comment(line, column):
    if get_next_char() != '*':
        return "divide", line, column

    # If comment was found
    get_next_char()
    while True:
        if current_char == '*':
            if get_next_char() == '/':
                get_next_char()
                return get_token()
            elif len(current_char) == 0:
                error_alert(line, column, "End of Input in comment")
            else:
                get_next_char()


def get_token():
    while current_char.isspace():
        get_next_char()

    line = current_line
    column = current_column

    if len(current_char) == 0:
        return "End of Input", line, column
    elif current_char == '/':
        return try_divide_or_comment(line, column)
    elif current_char == '\'':
        return try_character_constant(line, column)


def analyze_c(input_code):
    output = " "
    code = input_code

    while True:
        t = get_token()
        token = t[0]
        token_line = t[1]
        token_column = t[2]

        print("%5d   %5d   %-30s" % (token_line, token_column, token), end='')

    return output
