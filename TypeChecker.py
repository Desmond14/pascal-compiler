from SymbolTable import *
from AST import *


class NodeVisitor(object):
    def visit(self, node, sym_table):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node, sym_table)


    def generic_visit(self, node):  # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, Node):
                            self.visit(item)
                elif isinstance(child, Node):
                    self.visit(child)


class TypeChecker(NodeVisitor):
    def __init__(self):
        self.ttype = self.init_ttype()
        self.correct = True

    def init_ttype(self):
        res = {}
        for op in ['+', '-', '*', '/']:
            res[op] = {}
            res[op]['int'] = {}
            res[op]['float'] = {}
            res[op]['int']['int'] = 'int'
            res[op]['float']['float'] = 'float'

        res['+']['string'] = {}
        res['*']['string'] = {}
        res['+']['string'] = {}

        for op in ['>', '>=', '<=', '=', '<>', '<']:
            res[op] = {}
            res[op]['int'] = {}
            res[op]['int']['int'] = 'bool'
            res[op]['float'] = {}
            res[op]['float']['float'] = 'bool'

        return res


    def get_ttype(self, op, l_operand, r_operand):
        if op not in self.ttype:
            return None
        elif l_operand not in self.ttype[op]:
            return None
        elif r_operand not in self.ttype[op][l_operand]:
            return None
        else:
            return self.ttype[op][l_operand][r_operand]


    def visit_Integer(self, node, sym_table):
        return 'int'


    def visit_String(self, node, sym_table):
        return 'string'


    def visit_Float(self, node, sym_table):
        return 'float'


    def visit_Program(self, node, sym_table):
        # print "Program"
        #program header variables not supported
        node.decls.accept(self, sym_table)
        node.body.accept(self, sym_table)


    def visit_Declarations(self, node, sym_table):
        for const_def in node.const_defs:
            const_def.accept(self, sym_table)
        # node.type_defs.accept(self, sym_table)
        for var_decl in node.var_decls:
            var_decl.accept(self, sym_table)
        for proc_decl in node.proc_decls:
            proc_decl.accept(self, sym_table)


    def visit_ConstDef(self, node, sym_table):
        if sym_table.get(node.ident) is not None:
            print "Linia %d. Nazwa %s juz w uzyciu!" % (node.lineno, node.ident)
            self.correct = False
            return None

        if isinstance(node.const, Float):
            sym_table.put(node.ident, VariableSymbol(node.ident, "float"))
        elif isinstance(node.const, String):
            sym_table.put(node.ident, VariableSymbol(node.ident, "string"))
        else:
            sym_table.put(node.ident, VariableSymbol(node.ident, "int"))


    def visit_VarDec(self, node, sym_table):
        if node.type_specifier == 'char':
            type_specifier = 'string'
        elif node.type_specifier == 'integer':
            type_specifier = 'int'
        elif node.type_specifier == 'real':
            type_specifier = 'float'
        else:
            print "Linia: %d. Niedozwolony typ zmiennej: %s" % (node.lineno, node.type_specifier)
            self.correct = False
            return None  # TODO: think how to handle such situations

        for ident in node.id_list:
            if sym_table.get(ident) is not None:
                print "Linia: %d. Zmienna o nazwie %s juz istnieje." % (node.lineno, ident)
                self.correct = False
            else:
                sym_table.put(ident, VariableSymbol(ident, type_specifier))


    def visit_ProcDec(self, node, sym_table):
        if sym_table.get(node.header.ident) is not None:
            print "Linia: %d. Nazwa procedury %s jest juz w uzyciu."(node.lineno, node.ident)
            self.correct = False
        else:
            local_sym_table = SymbolTable(sym_table)
            arg_types = node.header.accept(self, local_sym_table)
            node.declarations.accept(self, local_sym_table)
            if isinstance(node.header, ProcHeader):
                sym_table.put(node.header.ident, FunctionSymbol(node.header.ident, "void", arg_types))
            else:
                sym_table.put(node.header.ident, FunctionSymbol(node.header.ident, node.header.return_type, arg_types))
                last_statement = node.body.statement_list[-1]
                if not isinstance(last_statement,
                                  AssignmentStatement) or last_statement.variable.ident != node.header.ident:
                    print "Funkcja %s. Ostatnia operacja w funkcji powinno byc zwrocenie wartosci!" % (
                    node.header.ident)
                    self.correct = False


    def visit_ProcHeader(self, node, sym_table):
        arg_types = list()
        for arg in node.arguments:
            arg_types.append(arg.accept(self, sym_table))
        return arg_types


    def visit_FuncHeader(self, node, sym_table):
        arg_types = list()
        for arg in node.arguments:
            arg_types.append(arg.accept(self, sym_table))
        sym_table.put(node.ident, FunctionSymbol(node.ident, node.return_type, arg_types))
        return arg_types


    def visit_Argument(self, node, sym_table):
        if sym_table.get(node.ident) is not None:
            print "Linia: %d. Nazwa zmiennej z sygnatury funkcji %s juz w uzyciu!" % (node.lineno, node.arg_name)
            self.correct = False
        else:
            sym_table.put(node.ident, VariableSymbol(node.ident, node.type))
        return node.type


    def visit_CompoundStatement(self, node, sym_table):
        for statement in node.statement_list:
            statement.accept(self, sym_table)


    def visit_AssignmentStatement(self, node, sym_table):
        type1 = node.expression.accept(self, sym_table)
        symbol = sym_table.get(node.variable.ident)
        if symbol is None:
            print "Linia: %d. Przypisanie do nieistniejacej zmiennej - %s!" % (node.lineno, node.var_name)
            self.correct = False
            return None
        elif isinstance(symbol, FunctionSymbol) and symbol.return_type != type1:
            print "Linia: %d. Niezgodnosc typow. Proba zwrocenia z funkcji %s wartosci typu %s" % (
                node.lineno, symbol.name, type1)
            self.correct = False
            return None
        elif isinstance(symbol, ProcedureCall):
            print "Linia: %d. Proba zwrocenia wartosci z procedury!"
            self.correct = False
            return None
        elif symbol.type != type1:
            print "Linia: %d. Niezgodnosc typow. Proba przypisania do zmiennej %s typu %s wartosci typu: %s" % (
                node.lineno, symbol.name, symbol.type, type1)
        else:
            return symbol.type


    def visit_IfStatement(self, node, sym_table):
        condition_type = node.condition.accept(self, sym_table)
        if condition_type != "bool":
            print "Linia: %d. Warunek instrukcji warunkowej nie jest wartoscia logiczna! Oczekiwano: bool. Otrzymano: %s" % (
            node.lineno, condition_type)
        node.if_statement.accept(self, sym_table)
        if node.else_statement is not None:
            node.else_statement.accept(self, sym_table)


    def visit_ProcedureCall(self, node, sym_table):
        if sym_table.get(node.procedure_name, ) is None:
            print "Linia: %d. Proba wywolania procedury lub funkcji, ktora nie zostala wczesniej zadeklarowana." % node.lineno
            self.correct = False
            return None
        fun_symbol = sym_table.get(node.procedure_name)
        if not isinstance(fun_symbol, FunctionSymbol):
            print "Linia: %d. %s nie jest procedura" % (node.lineno, node.procedure_name)
            self.correct = False
            return None
        if len(node.expr_list) != len(fun_symbol.arg_types):
            print "Linia: %d. Blad w wywolaniu procedury %s. Liczba argumentow niezgodna z deklaracja!" % (
                node.lineno, node.procedure_name)
            self.correct = False
            return None
        arg_no = 0
        for expr in node.expr_list:
            arg_no += 1
            type1 = expr.accept(self, sym_table)
            if type1 != fun_symbol.arg_types[arg_no - 1]:
                print "Linia: %d. Niezgodny typ dla %d argumentu w wywolaniu funkcji %s." % (
                    node.lineno, arg_no, node.procedure_name)
                print "Znaleziono: %s. Powinien byc: %s." % (type1, fun_symbol.arg_types[arg_no - 1])
                self.correct = False
        return fun_symbol.type


    def visit_FunctionCall(self, node, sym_table):
        return self.visit_ProcedureCall(node, sym_table)


    # def visit_ForStatement(self, node, sym_table):


    def visit_WhileStatement(self, node, sym_table):
        condition_type = node.condition.accept(self, sym_table)
        if condition_type != "bool":
            print "Linia: %d. Warunek petli nie jest wartoscia logiczna! Oczekiwano: bool. Otrzymano: %s" % (
            node.lineno, condition_type)
        node.while_body.accept(self, sym_table)


    def visit_RepeatStatement(self, node, sym_table):
        condition_type = node.condition.accept(self, sym_table)
        if condition_type != "bool":
            print "Linia: %d. Warunek petli nie jest wartoscia logiczna! Oczekiwano: bool. Otrzymano: %s" % (
            node.lineno, condition_type)
        for statement in node.repeat_body:
            statement.accept(self, sym_table)


    def visit_BinaryExpression(self, node, sym_table):
        type1 = node.left_operand.accept(self, sym_table)
        type2 = node.right_operand.accept(self, sym_table)

        op = node.operator;
        result_type = self.get_ttype(op, type1, type2)
        if result_type is None:
            print "Linia: %d. Operacja %s %s %s niedozwolona!" % (node.lineno, type1, op, type2)
            self.correct = False
        return result_type


    def visit_Variable(self, node, sym_table):
        var_symbol = sym_table.get(node.ident)
        if var_symbol is None:
            print "Linia: %d. Zmienna %s nie zostala wczesniej zadeklarowana!" % (node.lineno, node.value)
            self.correct = False
            return None
        return var_symbol.type


    def visit_Const(self, node, sym_table):
        try:
            float(node.value)
            return "float"
        except ValueError:
            try:
                int(node.value)
                return "int"
            except ValueError:
                return "string"