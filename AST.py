class Node(object):
    def __str__(self):
        return self.printTree()

    def accept(self, visitor, sym_table):
        return visitor.visit(self, sym_table)


class Const(Node):
    pass


class Integer(Const):
    pass


class Float(Const):
    pass


class String(Const):
    pass


class Statement(Node):
    pass


class CompoundStatement(Statement):
    pass


class AssignmentStatement(Statement):
    pass


class ProcedureCall(Statement):
    pass


class ForStatement(Statement):
    pass


class WhileStatement(Statement):
    pass


class IfStatement(Statement):
    pass


class CaseStatement(Statement):
    pass


class RepeatStatement(Statement):
    pass


class Expression(Node):
    pass


class BinaryExpression(Expression):
    pass


class Declarations(Node):
    pass


class Program(Node):
    pass

