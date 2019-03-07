from Analyzer.utils.analyzer_c import analyze_c
from Analyzer.utils.analyzer_cpp import analyze_cpp
from Analyzer.utils.analyzer_csharp import analyze_csharp


def analyze_input(selected_language, input_code):
    output = ''

    if selected_language == 'C':
        output = analyze_c(input_code)
    elif selected_language == 'C++':
        output = analyze_cpp(input_code)
    elif selected_language == 'C#':
        output = analyze_csharp(input_code)
    else:
        output = 'Please selected a valid language from the pick list!'

    return output


