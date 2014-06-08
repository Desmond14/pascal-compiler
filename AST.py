class Node(object):
    def __str__(self):
        return self.printTree()

    def accept(self, visitor, sym_table):
        return visitor.visit(self, sym_table)


class Const(Node):
    def __init__(self, value):
        self.value = value


class Integer(Const):
    pass


class Float(Const):
    pass


class String(Const):
    pass


class Statement(Node):
    pass


class CompoundStatement(Statement):
    def __init__(self, statement_list):
        self.statement_list = statement_list


class AssignmentStatement(Statement):
    def __init__(self, variable, expression):
        self.variable = variable
        self.expression = expression


class ProcedureCall(Statement):
    def __init__(self, procedure_name, expr_list = None):
        self.procedure_name = procedure_name
        self.expr_list = expr_list


class ForStatement(Statement):
    def __init__(self, variable_name, for_type, initial_expr, termination_expr, statement):
        self.variable_name = variable_name
        self.for_type = for_type
        self.initial_expr = initial_expr
        self.final_expr = termination_expr
        self.statement = statement


class WhileStatement(Statement):
    def __init__(self, condition, while_body):
        self.condition = condition
        self.while_body = while_body


class IfStatement(Statement):
    def __init__(self, condition, if_statement, else_statement = None):
        self.condition = condition
        self.if_statement = if_statement
        self.else_statement = else_statement

class CaseStatement(Statement):
    pass


class RepeatStatement(Statement):
    def __init__(self, repeat_body, condition):
        self.repeat_body = repeat_body
        self.condition = condition


class Expression(Node):
    pass


class BinaryExpression(Expression):
    pass


class Declarations(Node):
    def __init__(self, const_defs, type_defs, var_decls, proc_decls):
        self.const_defs = const_defs
        self.type_defs = type_defs
        self.var_decls = var_decls
        self.proc_decls = proc_decls


class ProgramHeader(Node):
    def __init__(self, program_name, parameters=None):
        self.program_name = program_name
        self.parameters = parameters


class Program(Node):
    def __init__(self, program_header, decls, body):
        self.program_header = program_header
        self.decls = decls
        self.body = body
