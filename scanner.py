import ply.lex as lex


class Scanner(object):
    def find_tok_column(self, token):
        last_cr = self.lexer.lexdata.rfind('\n', 0, token.lexpos)
        if last_cr < 0:
            last_cr = 0
        return token.lexpos - last_cr


    def build(self):
        self.lexer = lex.lex(object=self)

    def input(self, text):
        self.lexer.input(text)

    def token(self):
        return self.lexer.token()


    literals = "{}()<>=;:,+-*^."

    reserved = {
        'if': 'IF',
        'then': 'THEN',
        'else': 'ELSE',
        'repeat': 'REPEAT',
        'while': 'WHILE',
        'until': 'UNTIL',
        'for': 'FOR',
        'to': 'TO',
        'downto': 'DOWNTO',
        'do': 'DO',
        'var': 'VAR',
        'program': 'PROGRAM_LITERAL',
        'function': 'FUNCTION',
        'procedure': 'PROCEDURE',
        'begin': 'BEGIN',
        'end': 'END',
        'array': 'ARRAY',
        'record': 'RECORD',
        'div': 'DIV',
        'mod': 'MOD',
        'or': 'OR',
        'and': 'AND',
        'not': 'NOT',
        'file': 'FILE',
        'of': 'OF',
        'forward': 'FORWARD',
        'case': 'CASE',
        'const': 'CONST'
    }

    tokens = ["GE", "ID", "LE", "NEQ", "TYPE", "CONSTANT", "ASSIGN", "DOUBLE_DOT"] + list(reserved.values())

    t_ignore = ' \t\f'

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_newline2(self, t):
        r'(\r\n)+'
        t.lexer.lineno += len(t.value) / 2


    def t_error(self, t):
        print("Illegal character '{0}' ({1}) in line {2}".format(t.value[0], hex(ord(t.value[0])), t.lexer.lineno))
        t.lexer.skip(1)


    def t_LINE_COMMENT(self, t):
        r'\#.*'
        pass

    def t_BLOCK_COMMENT(self, t):
        r'/\*(.|\n)*?\*/'
        t.lexer.lineno += t.value.count('\n')


    def t_CONSTANT(self, t):
        r"(\d+(\.\d*)|\.\d+)|(\d+)|('(?:[^']+|'')*')"
        return t

    t_LE = r"<="

    t_GE = r">="

    t_NEQ = r"<>"

    t_ASSIGN = r":="

    def t_TYPE(self, t):
        r"\b(integer|real|char)\b"
        return t

    def t_ID(self, t):
        r"[a-zA-Z_]\w*"
        t.type = Scanner.reserved.get(t.value, 'ID')
        return t


    def t_DOUBLE_DOT(self, t):
        r"\.\."
        return t