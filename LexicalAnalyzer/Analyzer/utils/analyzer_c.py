from __future__ import print_function
import sys

keywords = ["auto", "break", "case", "char", "const", "continue", "default",
            "do", "double", "else", "enum", "extern", "float", "for", "goto",
            "if", "int", "long", "register", "return", "short", "signed", "sizeof",
            "static", "struct", "switch", "typedef", "union", "unsigned", "void",
            "volatile", "while", "printf", "scanf", "print"]

symbols = ['{', '}', '(', ')', '[', ']', ';', ',', '+', '-', '*', '%']

code = None
current_line = 1
current_column = 0
current_char_index = 0
current_char = " "
input_length = 0
error_message = ""


def error_alert(line, column, message):
    global error_message
    error_message = "ERROR - " + str(line) + " - " + str(column) + " - " + message + "\n"
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


def try_string(starting_char, line, column):
    text = ""

    while get_next_char() != starting_char:
        if len(current_char) == 0:
            error_alert(line, column, "Invalid string. EOF found while trying to parse string")
        if current_char == '\n':
            error_alert(line, column, "End of line found while parsing a string")
        text += current_char

    get_next_char()
    return "STRING" , line, column, text


def try_identifier_or_number(line, column):
    is_number = True
    text = ""
    is_int = True
    is_float = True

    while current_char.isalnum() or current_char == "_" or current_char == '.':
        text += current_char
        if not current_char.isdigit():
            is_number = False
        get_next_char()

    if len(text) == 0:
        error_alert(line, column, "Invalid character: (%d) '%c'" % (ord(current_char), current_char))

    if text[0].isdigit():
        # if not is_number:
            # error_alert(line, column, "Invalid number: %s" %(text))
        try:
            number = int(text)
            return "INT", line, column, number
        except ValueError:
            is_int = False
        if not is_int:
            try:
                number = float(text)
                return "FLOAT", line, column, number
            except ValueError:
                is_float = False
        if not is_float:
            return error_alert(line, column, "Invalid number: %s" % (text))

    if text in keywords:
        return "KEYWORD", line, column, text

    return "IDENTIFIER", line, column, text


def check_pattern(expected_character, if_yes, if_no, line, column):
    if get_next_char() == expected_character:
        get_next_char()
        return if_yes, line, column

    if if_no == "End of Input":
        error_alert(line, column, "Unrecognized character: (%d) '%c'" % (ord(current_char), current_char))

    return if_no, line, column


def get_token():
    if current_char_index < len(code):
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
    elif current_char == '<':
        return check_pattern('=', "<=", "<", line, column)
    elif current_char == '>':
        return check_pattern('=', '>=', ">", line, column)
    elif current_char == '=':
        return check_pattern('=', '==', '=', line, column)
    elif current_char == '!':
        return check_pattern('=', '!=', '!', line, column)
    elif current_char == '&':
        return check_pattern('&', '&&', 'End of Input', line, column)
    elif current_char == '|':
        return check_pattern('|', '||', "End of Input", line, column)
    elif current_char == '"':
        return try_string(current_char, line, column)
    elif current_char in symbols:
        sym = current_char
        if current_char_index < len(code):
            get_next_char()
        return sym, line, column
    else:
        return try_identifier_or_number(line, column)


def analyze_c(input_code):
    global code, current_line, current_column, current_char_index, current_char, input_length
    code = None
    current_line = 1
    current_column = 0
    current_char_index = 0
    current_char = " "
    input_length = 0
    output = ""
    code = input_code

    while True and current_char_index <= len(code):
        t = get_token()
        if t is not None:
            # t = get_token()
            token = t[0]
            token_line = t[1]
            token_column = t[2]

            output += str(token_line) + " - " + str(token_column) + " - " + str(token)

            print("%7d   %7d   %-60s" % (token_line, token_column, token), end='')

            if token == "INT":
                print("   %7d" % (t[3]))
                output += "    " + str(t[3])
            if token == 'FLOAT':
                print(t[3])
                output += "    " + str(t[3])
            elif token == "IDENTIFIER":
                print("   %s" % (t[3]))
                output += "    " + str(t[3])
            elif token == "STRING":
                print('   "%s"' % (t[3]))
                output += '    "' + str(t[3]) + '"'
            elif token == "KEYWORD":
                print('   "%s"' % (t[3]))
                output += '    "' + str(t[3]) + '"'
            else:
                print('')
                output += ''

            output += '\n'

            if token == "End of Input" or current_char_index == len(code):
                break
        else:
            output += error_message
            print('')

    return output
