class Node(object):
    def __str__(self):
        return self.printTree()

    def accept(self, visitor, sym_table):
        return visitor.visit(self, sym_table)


class Const(Node):
    def __init__(self, value, lineno):
        self.value = value
        self.lineno = lineno


class Integer(Const):
    pass


class Float(Const):
    pass


class String(Const):
    pass


class ConstDef(Node):
    def __init__(self, const, ident, lineno):
        self.const = const
        self.ident = ident
        self.lineno = lineno


class VarDec(Node):
    def __init__(self, type_specifier, id_list, lineno):
        self.type_specifier = type_specifier
        self.id_list = id_list
        self.lineno = lineno


class Variable(Node):
    def __init__(self, ident, lineno):
        self.ident = ident
        self.lineno = lineno


class ProcDec(Node):
    def __init__(self, header, declarations, body):
        self.header = header
        self.declarations = declarations
        self.body = body


class ProcHeader(Node):
    def __init__(self, ident, arguments, lineno):
        self.ident = ident
        self.arguments = arguments
        self.lineno = lineno


class FuncHeader(Node):
    def __init__(self, ident, arguments, return_type, lineno):
        self.ident = ident
        self.arguments = arguments
        self.return_type = return_type
        self.lineno = lineno


class Statement(Node):
    pass


class CompoundStatement(Statement):
    def __init__(self, statement_list):
        self.statement_list = statement_list


class AssignmentStatement(Statement):
    def __init__(self, variable, expression, lineno):
        self.variable = variable
        self.expression = expression
        self.lineno = lineno


class ProcedureCall(Statement):
    def __init__(self, procedure_name, expr_list, lineno):
        self.procedure_name = procedure_name
        self.expr_list = expr_list
        self.lineno = lineno


class FunctionCall(Statement):
    def __init__(self, function_name, expr_list, lineno):
        self.function_name = function_name
        self.expr_list = expr_list
        self.lineno = lineno


class ForStatement(Statement):
    def __init__(self, variable_name, for_type, initial_expr, termination_expr, statement):
        self.variable_name = variable_name
        self.for_type = for_type
        self.initial_expr = initial_expr
        self.final_expr = termination_expr
        self.statement = statement


class WhileStatement(Statement):
    def __init__(self, condition, while_body, lineno):
        self.condition = condition
        self.while_body = while_body
        self.lineno = lineno


class IfStatement(Statement):
    def __init__(self, lineno, condition, if_statement, else_statement=None):
        self.condition = condition
        self.if_statement = if_statement
        self.else_statement = else_statement
        self.lineno = lineno


class CaseStatement(Statement):
    pass


class RepeatStatement(Statement):
    def __init__(self, repeat_body, condition, lineno):
        self.repeat_body = repeat_body
        self.condition = condition
        self.lineno


class Expression(Node):
    pass


class BinaryExpression(Expression):
    def __init__(self, left_operand, operator, right_operand, lineno):
        self.left_operand = left_operand
        self.right_operand = right_operand
        self.operator = operator
        self.lineno = lineno


class UnaryExpression(Expression):
    def __init__(self, operand, operator):
        self.operand = operand
        self.operator = operator


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


class Argument(Node):
    def __init__(self, ident, arg_type, lineno):
        self.ident = ident
        self.type = arg_type
        self.lineno = lineno