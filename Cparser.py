# !/usr/bin/python
from AST import Program, ProgramHeader, Declarations, Integer, Float, ConstDef, String, VarDec, ProcDec, ProcHeader, \
    FuncHeader, Argument, CompoundStatement, AssignmentStatement, ProcedureCall, WhileStatement, IfStatement, \
    BinaryExpression, UnaryExpression, Variable, FunctionCall, RepeatStatement

from scanner import Scanner


class Cparser(object):
    def __init__(self):
        self.scanner = Scanner()
        self.scanner.build()

    tokens = Scanner.tokens

    precedence = (
        ("nonassoc", 'IF'),
        ("nonassoc", 'ELSE'),
        ("right", '='),
        ("left", 'OR'),
        ("left", 'AND'),
        ("left", '^'),
        ("nonassoc", '<', '>', '=', 'NEQ', 'LE', 'GE'),
        ("left", '+', '-'),
        ("left", '*', '/', 'MOD', 'DIV'),
    )

    error_encountered = False


    def convert_from_string(self, value, lineno):
        try:
            return Integer(int(value), lineno)
        except ValueError:
            try:
                return Float(float(value), lineno)
            except ValueError:
                return String(value, lineno)

    def p_error(self, p):
        self.error_encountered = True
        if p:
            print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno,
                                                                                      self.scanner.find_tok_column(p),
                                                                                      p.type, p.value))
        else:
            print('At end of input')


    def p_program(self, p):
        """program : program_header declarations compound_statement '.'"""
        p[0] = Program(p[1], p[2], p[3])


    def p_program_header(self, p):
        """program_header : PROGRAM_LITERAL ID ';'
                          | PROGRAM_LITERAL ID '(' id_list ')' ';' """
        if len(p) == 4:
            p[0] = ProgramHeader(p[2])
        else:
            p[0] = ProgramHeader(p[2], p[4])

    def p_declarations(self, p):
        """declarations : constant_definitions type_definitions variable_declarations procedure_declarations"""
        p[0] = Declarations(p[1], p[2], p[3], p[4])

    def p_constant_definitions(self, p):
        """constant_definitions : CONST constant_definition_list
                                | """
        if len(p) == 1:
            p[0] = list()
        else:
            p[0] = p[2]


    def p_constant_definition_list(self, p):
        """constant_definition_list : constant_definition_list const_def
                                    | const_def """
        if len(p) == 2:
            p[0] = list()
            p[0].append(p[1])
        else:
            p[1].append(p[2])
            p[0] = p[1]


    def p_const_def(self, p):
        """const_def : ID '=' CONSTANT ';'"""
        const_value = self.convert_from_string(p[3], p.lineno(1))
        p[0] = ConstDef(const_value, p[1], p.lineno(1))


    def p_type_definitions(self, p):
        """type_definitions : TYPE type_definition_list
                            | """
        if len(p) == 1:
            p[0] = list()
        else:
            p[0] = p[2]


    def p_type_definition_list(self, p):
        """type_definition_list : type_definition_list type_def
                                | type_def"""
        if len(p) == 2:
            p[0] = list()
            p[0].append(p[1])
        else:
            p[1].append(p[2])
            p[0] = p[1]

    def p_type_def(self, p):
        """type_def : ID '=' type_specifier ';'"""
        pass

    def p_variable_declarations(self, p):
        """variable_declarations : VAR variable_declaration_list
                                 | """
        if len(p) == 1:
            p[0] = list()
        else:
            p[0] = p[2]

    def p_variable_declaration_list(self, p):
        """variable_declaration_list : variable_declaration_list var_dec
                                     | var_dec"""
        if len(p) == 2:
            p[0] = list()
            p[0].append(p[1])
        else:
            p[1].append(p[2])
            p[0] = p[1]

    # def p_variable_declaration_list_error(self, p):
    #     """variable_declaration_list : error"""
    #     print "Bad declaration at line ", p.lineno(1)
    #     self.error_encountered = True

    def p_var_dec(self, p):
        """var_dec : id_list ':' type_specifier ';' """
        p[0] = VarDec(p[3], p[1], p.lineno(3))

    def p_procedure_declarations(self, p):
        """procedure_declarations : procedure_declarations proc_dec
                                  | """
        if len(p) == 1:
            p[0] = list()
        else:
            p[1].append(p[2])
            p[0] = p[1]

    def p_proc_dec(self, p):
        """proc_dec :  proc_header declarations compound_statement ';'
                    | func_header declarations compound_statement ';' """
        if len(p) == 5:
            p[0] = ProcDec(p[1], p[2], p[3])

    def p_proc_header(self, p):
        """proc_header : PROCEDURE ID arguments ';' """
        p[0] = ProcHeader(p[2], p[3], p.lineno(1))

    def p_func_header(self, p):
        """func_header : FUNCTION ID arguments ':' type_specifier ';' """
        if p[5] == "integer":
            p[0] = FuncHeader(p[2], p[3], "int", p.lineno(1))
        else:
             p[0] = FuncHeader(p[2], p[3], p[5], p.lineno(1))

    def p_arguments(self, p):
        """arguments : '(' argument_list ')'
                     | """
        if len(p) == 4:
            p[0] = p[2]
        else:
            p[0] = list()

    def p_argument_list(self, p):
        """argument_list : argument_list ';' arg
                         | arg """
        if len(p) == 4:
            p[1].extend(p[3])
            p[0] = p[1]
        else:
            p[0] = p[1]

    # def p_argument_list_error(self, p):
    #     """argument_list : error"""
    #     print "Syntax error in argument at line ", p.lineno(1)
    #     self.error_encountered = True

    def p_arg(self, p):
        """arg : id_list ':' type_specifier """
        id_list = None
        type_specifier = None
        result = list()
        id_list = p[1]
        type_specifier = p[3]
        if type_specifier == "integer":
            type_specifier = "int"
        elif type_specifier == "real":
            type_specifier = "float"
        for id in id_list:
            #print id
            result.append(Argument(id, type_specifier, p.lineno(1)))
        p[0] = result


    def p_compound_statement(self, p):
        """compound_statement : BEGIN statement_list END"""
        p[0] = CompoundStatement(p[2])


    def p_compound_statement_error(self, p):
        """compound_statement : BEGIN error END"""
        print "Linia: %d. Blad syntaktyczny w instrukcji zlozonej." % p.lineno(1)
        self.error_encountered = True


    def p_statement_list(self, p):
        """statement_list : statement_list ';' statement
                          | statement """
        if len(p) == 2:
            p[0] = list()
            p[0].append(p[1])
        else:
            p[1].append(p[3])
            p[0] = p[1]

    def p_statement(self, p):
        """statement : compound_statement
                     | assignment_statement
                     | procedure_call
                     | for_statement
                     | while_statement
                     | if_statement
                     | case_statement
                     | repeat_statement
                     | """
        p[0] = p[1]


    def p_assignment_statement(self, p):
        """assignment_statement : variable ASSIGN expression"""
        p[0] = AssignmentStatement(p[1], p[3], p.lineno(1))

    def p_procedure_call(self, p):
        """procedure_call : ID actuals"""
        p[0] = ProcedureCall(p[1], p[2], p.lineno(1))

    def p_for_statement(self, p):
        """for_statement : FOR ID ASSIGN expression TO expression DO statement
                         | FOR ID ASSIGN expression DOWNTO expression DO statement"""
        pass

    def p_while_statement(self, p):
        """while_statement : WHILE expression DO statement"""
        p[0] = WhileStatement(p[2], p[4], p.lineno(1))


    def p_while_statement_error(self, p):
        """while_statement : WHILE error DO statement"""
        print "Linia: %d. Blad syntaktyczny w w warunku petli while." % p.lineno(1)
        self.error_encountered = True

    def p_if_statement(self, p):
        """if_statement : IF expression THEN statement
                        | IF expression THEN statement ELSE statement"""
        if len(p) == 5:
            p[0] = IfStatement(p.lineno(1), p[2], p[4])
        else:
            p[0] = IfStatement(p.lineno(1), p[2], p[4], p[6])

    def p_if_statement_error(self, p):
        """if_statement : IF error THEN statement
                        | IF error THEN statement ELSE statement"""
        print "Linia: %d. Blad syntaktyczny w warunku instrukcji warunkowej." % p.lineno(1)
        self.error_encountered = True

    def p_repeat_statement(self, p):
        """repeat_statement : REPEAT statement_list UNTIL expression"""
        p[0] = RepeatStatement(p[2], p[4], p.lineno(1))

    def p_repeat_statement_error(self, p):
        """repeat_statement : REPEAT error UNTIL expression"""
        print "Linia: %d. Blad syntaktyczny w ciele instrukcji repeat." % p.lineno(1)
        self.error_encountered = True


    def p_case_statement(self, p):
        """case_statement : CASE expression OF  case_list END"""
        pass


    def p_case_list(self, p):
        """case_list : case_list ';' case
                     | case"""
        pass


    def p_case(self, p):
        """case : constant_list ':' statement"""
        pass


    def p_constant_list(self, p):
        """constant_list : constant_list ',' CONSTANT
                         | CONSTANT"""
        pass


    def p_expression(self, p):
        """expression : simple_expression
                      | simple_expression '=' simple_expression
                      | simple_expression NEQ simple_expression
                      | simple_expression '<' simple_expression
                      | simple_expression LE simple_expression
                      | simple_expression '>' simple_expression
                      | simple_expression GE simple_expression
                      """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = BinaryExpression(p[1], p[2], p[3], p.lineno(1))


    def p_simple_expression(self, p):
        """simple_expression : term
                             | simple_expression '+' term
                             | simple_expression '-' term
                             | simple_expression OR term
                            """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = BinaryExpression(p[1], p[2], p[3], p.lineno(1))

    def p_term(self, p):
        """term : factor
                | term '*' factor
                | term '/' factor
                | term DIV factor
                | term MOD factor
                | term AND factor
                   """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = BinaryExpression(p[1], p[2], p[3], p.lineno(1))

    def p_factor(self, p):
        """factor : '(' expression ')'
                  | '+' factor
                  | '-' factor
                  | NOT factor
                  | function_call
                  | CONSTANT
                  | variable
                  """
        if len(p) == 4:
            p[0] = p[2]
        elif len(p) == 3:
            p[0] = UnaryExpression(p[2, p[1]])
        elif isinstance(p[1], ProcedureCall) or isinstance(p[1], Variable) or isinstance(p[1], FunctionCall):
            p[0] = p[1]
        else:
            p[0] = self.convert_from_string(p[1], p.lineno(1))

    def p_function_call(self, p):
        """function_call : ID actuals"""
        p[0] = FunctionCall(p[1], p[2], p.lineno(1))


    def p_actuals(self, p):
        """actuals : '(' expression_list ')'
                   | '(' ')'"""
        if len(p) == 4:
            p[0] = p[2]
        else:
            p[0] = list()
        for i in p[0]:
            if isinstance(i, str):
                print i

    def p_actuals_error(self, p):
        """actuals : '(' error ')' """
        print "Linia: %d. Blad w liscie argumentow." % (p.lineno(1))


    def p_expression_list(self, p):
        """expression_list : expression_list ',' expression
                           | expression"""
        if len(p) == 2:
            p[0] = list()
            p[0].append(p[1])
        else:
            p[1].append(p[3])
            p[0] = p[1]


    def p_variable(self, p):
        """variable : ID
                    | variable '.' ID
                    | variable '^'
                    | variable '[' expression_list ']'
                    """
        if len(p) == 2:
            p[0] = Variable(p[1], p.lineno(1))

    # TODO: other types of variables

    def p_type_specifier(self, p):
        """type_specifier : TYPE
                          | '^' type_specifier
                          | '(' id_list ')'
                          | CONSTANT DOUBLE_DOT CONSTANT
                          | ARRAY '[' dimension_list ']' OF type_specifier
                          | RECORD field_list END
                          | FILE OF type_specifier """
        if len(p) == 2:
            p[0] = p[1]

    def p_dimension_list(self, p):
        """dimension_list : dimension_list ',' dimension
                          | dimension"""
        pass

    def p_dimension(self, p):
        """dimension : CONSTANT DOUBLE_DOT CONSTANT
                     | ID"""
        pass

    def p_field_list(self, p):
        """field_list : field_list ';' field
                      | field"""
        pass

    def p_field(self, p):
        """field : id_list ':' type_specifier"""
        pass

    def p_id_list(self, p):
        """id_list : id_list ',' ID
                   | ID"""
        if len(p) == 2:
            p[0] = list()
            p[0].append(p[1])
        else:
            p[1].append(p[3])
            p[0] = p[1]


