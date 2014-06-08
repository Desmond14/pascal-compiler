# !/usr/bin/python

from scanner import Scanner


class Cparser(object):
    def __init__(self):
        self.scanner = Scanner()
        self.scanner.build()

    tokens = Scanner.tokens

    precedence = (
        ("nonassoc", 'IFX'),
        ("nonassoc", 'ELSE'),
        ("right", '='),
        ("left", 'OR'),
        ("left", 'AND'),
        ("left", '^'),
        ("nonassoc", '<', '>', 'EQ', 'NEQ', 'LE', 'GE'),
        ("left", '+', '-'),
        ("left", '*', '/', '%'),
    )

    error_encountered = False


    def p_error(self, p):
        if p:
            print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno,
                                                                                      self.scanner.find_tok_column(p),
                                                                                      p.type, p.value))
        else:
            print('At end of input')


    def p_program(self, p):
        """program : program_header declarations compound_statement"""


        def p_program_header(self, p):
            """program_header : PROGRAM_LITERAL ID ';'
                              | PROGRAM_LITERAL ID '(' id_list ')' ';' """
            pass

    def p_declarations(self, p):
        """declarations : constant_definitions type_definitions variable_declarations procedure_declarations"""
        pass

        def p_constant_definitions(self, p):
            """constant_definitions : CONST constant_definition_list
                                    | """
            pass

        def p_constant_definition_list(self, p):
            """constant_definition_list : constant_definition_list const_def
                                        | const_def """
            pass

        def p_const_def(self, p):
            """const_def : ID '=' CONSTANT ';'"""
            pass

        def p_type_definitions(self, p):
            """type_definitions : TYPE type_definition_list
                                | """
            pass

        def p_type_definition_list(self, p):
            """type_definition_list : type_definition_list type_def
                                    | type_def"""
            pass

        def p_type_def(self, p):
            """type_def : ID '=' type_specifier ';'"""
            pass

        def p_variable_declarations(self, p):
            """variable_declarations : VAR variable_declaration_list
                                     | """
            pass

        def p_variable_declaration_list(self, p):
            """variable_declaration_list : variable_declaration_list var_dec
                                         | var_dec"""
            pass

        def p_var_dec(self, p):
            """var_dec : id_list ':' type_specifier ';' """
            pass

        def p_procedure_declarations(self, p):
            """procedure_declarations : procedure_declarations proc_dec
                                      | """
            pass

        def p_proc_dec(self, p):
            """proc_dec : proc_header FORWARD ';'
                        | proc_header declarations compound_statement ';'
                        | func_header FORWARD ';'
                        | func_header declarations compound_statement ';' """
            pass

        def p_proc_header(self, p):
            """proc_header : PROCEDURE ID arguments ';' """
            pass

        def p_func_header(self, p):
            """func_header : FUNCTION ID arguments ':' type_specifier ';' """
            pass

        def p_arguments(self, p):
            """arguments : '(' argument_list ')'
                         | """
            pass

        def p_argument_list(self, p):
            """argument_list : argument_list ';' args
                             | arg """
            pass

        def p_arg(self, p):
            """arg : VAR id_list ':' type_specifier
                   | id_list ':' type_specifier """
            pass

        def p_compound_statement(self, p):
            """compound_statement : BEGIN statement_list END"""
            pass

        def p_statement_list(self, p):
            """statement_list : statement_list ';' statement
                              | statement """
            pass

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
            pass

        def p_assignment_statement(self, p):
            """assignment_statement : variable ASSIGN expression"""
            pass

        def p_procedure_call(self, p):
            """procedure_call : ID actuals"""
            pass

        def p_for_statement(self, p):
            """for_statement : FOR ID ASSIGN expression TO expression DO statement
                             | FOR ID ASSIGN expression DOWNTO expression DO statement"""
            pass

        def p_while_statement(self, p):
            """while_statement : WHILE expression DO statement"""
            pass

        def p_if_statement(self, p):
            """if_statement : IF expression THEN statement
                            | IF expression THEN statement ELSE statement"""
            pass

        def p_repeat_statement(self, p):
            """repeat_statement : REPEAT statement_list UNTIL expression"""
            pass

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
            pass

        def p_simple_expression(self, p):
            """simple_expression : term
                                 | simple_expression '+' term
                                 | simple_expression '-' term
                                 | simple_expression OR term
                                 """
            pass

        def p_term(self, p):
            """term : factor
                    | term '*' factor
                    | term '/' factor
                    | term DIV factor
                    | term MOD factor
                    | term AND factor
                    """
            pass

        def p_factor(self, p):
            """factor : '(' expression ')'
                      | '+' factor
                      | '-' factor
                      | NOT factor
                      | function_call
                      | CONSTANT
                      | variable
                      """
            pass

        def p_function_call(self, p):
            """function_call : ID actuals"""
            pass

        def p_actuals(self, p):
            """actuals : '(' expression_list ')'
                       | """
            pass

        def p_expression_list(self, p):
            """expression_list : expression_list ',' expression
                               | expression"""
            pass

        def p_variable(self, p):
            """variable : ID
                        | variable '.' ID
                        | variable '^'
                        | variable '[' expression_list ']'
                        """
            pass

        def p_type_specifier(self, p):
            """type_specifier : ID
                              | '^' type_specifier
                              | '(' id_list ')'
                              | CONSTANT DOUBLE_DOT CONSTANT
                              | ARRAY '[' dimension_list ']' OF type_specifier
                              | RECORD field_list END
                              | FILE OF type_specifier """
            pass

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
            """id_list : id_list ',' id
                       | id"""
            pass