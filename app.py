from flask import Flask, request, jsonify, render_template
import re

app = Flask(__name__)

# Tokens para el analizador léxico
tokens = {
    'FOR': r'for',
    'INT_TYPE': r'int',
    'ID': r'[a-zA-Z_][a-zA-Z_0-9]*',
    'NUM': r'\d+',
    'OP': r'[+\-*/]',
    'ASSIGN': r'=',
    'RELOP': r'[<>]=?|==|!=',
    'LPAREN': r'\(',
    'RPAREN': r'\)',
    'LBRACE': r'\{',
    'RBRACE': r'\}',
    'SEMICOLON': r';',
    'DOT': r'\.',
    'STRING': r'".*?"',
    'WHITESPACE': r'\s+',
    'OTHER': r'.'
}

# Función para el análisis léxico
def lexical_analysis(code):
    lexemes = []
    while code:
        for token_name, token_regex in tokens.items():
            match = re.match(token_regex, code)
            if match:
                lexeme = match.group(0)
                if token_name != 'WHITESPACE':
                    lexemes.append((token_name, lexeme))
                code = code[len(lexeme):]
                break
    return lexemes

# Función para el análisis sintáctico
def syntax_analysis(lexemes):
    tokens_iter = iter(lexemes)
    current_token = None

    def next_token():
        nonlocal current_token
        try:
            current_token = next(tokens_iter)
        except StopIteration:
            current_token = None

    def match(expected_token):
        if current_token and current_token[0] == expected_token:
            next_token()
        else:
            raise SyntaxError(f"Expected {expected_token} but got {current_token}")

    def parse_for_statement():
        match('FOR')
        match('LPAREN')
        parse_initialization()
        match('SEMICOLON')
        parse_condition()
        match('SEMICOLON')
        parse_update()
        match('RPAREN')
        match('LBRACE')
        parse_body()
        match('RBRACE')

    def parse_initialization():
        match('INT_TYPE')
        match('ID')
        match('ASSIGN')
        match('NUM')

    def parse_condition():
        match('ID')
        match('RELOP')
        match('NUM')

    def parse_update():
        match('ID')
        match('OP')
        match('OP')

    def parse_body():
        match('ID')
        match('DOT')
        match('ID')
        match('DOT')
        match('ID')
        match('LPAREN')
        match('STRING')
        match('OP')
        match('ID')
        match('RPAREN')
        match('SEMICOLON')

    try:
        next_token()
        parse_for_statement()
        return "Sintaxis válida"
    except SyntaxError as e:
        return f"Error de sintaxis: {e}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    code = data['code']

    lexemes = lexical_analysis(code)
    lexical_output = '\n'.join([f"{token}: {lexeme}" for token, lexeme in lexemes])

    syntax_output = syntax_analysis(lexemes)

    return jsonify({
        'lexical': lexical_output,
        'syntax': syntax_output
    })

if __name__ == '__main__':
    app.run(debug=True)
