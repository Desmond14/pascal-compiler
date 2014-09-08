from SymbolTable import *
from AST import *


class NodeVisitor(object):
    def visit(self, node, sym_table):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node, sym_table)


    def generic_visit(self, node, sym_table):  # Called if no explicit visitor function exists for a node.
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


class Translator(NodeVisitor):
    def __init__(self):
        self.ttype = self.init_ttype()
        self.code = list()
        self.values_on_stack = 0
        self.cmp_counter = 0
        self.if_counter = 0
        self.loops_counter = 0

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
        res['+']['string']['string'] = 'string'

        for op in ['>', '>=', '<=', '==', '!=', '<']:
            res[op] = {}
            res[op]['int'] = {}
            res[op]['int']['int'] = 'int'

        res['='] = {}
        res['=']['int'] = {}
        res['=']['float'] = {}
        res['=']['int']['int'] = 'int'
        res['=']['float']['int'] = 'float'
        res['=']['float']['float'] = 'float'

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
        self.code.append("mov ax, %d" %(node.value))
        self.code.append("push ax")

    def visit_String(self, node, sym_table):
        pass

    def visit_Float(self, node, sym_table):
        pass


    def visit_Program(self, node, sym_table):
        self.code.append("code segment")
        self.code.append("assume	cs:code")
        self.code.append("start:")

        node.decls.accept(self, None)
        node.body.accept(self, None)
        self.code.append("mov	ax, 4c00h")
        self.code.append("int	21h")
        self.append_builtin()
        self.code.append("code ends")
        self.code.append("END start")


    def append_builtin(self):
        self.code.append("print	proc near")
        self.code.append("mov cx, 0")
        self.code.append("mov bx, 10")  # bx sluzy jako podstawa dzielenia

        self.code.append("divloop:")
        self.code.append("mov dx, 0")
        self.code.append("div bx")  # dx - zawiera reszte z dzielenia, ax - iloraz
        self.code.append("push dx")
        self.code.append("inc cx")
        self.code.append("cmp ax, 0")
        self.code.append("jnz divloop")

        self.code.append("printloop:")
        self.code.append("pop ax")
        self.code.append("mov dl, al")  # copy integer value to dl
        self.code.append("add dl, 30h")  # convert to ASCII character
        self.code.append("mov ah, 02h")
        self.code.append("int 21h")  # print character to sdtout
        self.code.append("dec cx")
        self.code.append("cmp cx, 0")
        self.code.append("jne printloop")
        self.code.append("ret")
        self.code.append("print	endp")


    def visit_Declarations(self, node, sym_table):
        pass
        # for const_def in node.const_defs:
        # const_def.accept(self, sym_table)
        # #node.type_defs.accept(self, sym_table)
        # for var_decl in node.var_decls:
        #     var_decl.accept(self, sym_table)
        # for proc_decl in node.proc_decls:
        #     proc_decl.accept(self, sym_table)


    def visit_ConstDef(self, node, sym_table):
        pass


    def visit_VarDec(self, node, sym_table):
        pass


    def visit_ProcDec(self, node, sym_table):
        # not yet implemented!
        local_sym_table = SymbolTable(sym_table)
        node.proc_header.accept(self, local_sym_table)
        for argument in node.declarations:
            argument.accept(self, local_sym_table)
        node.body.accept(self, local_sym_table)


    def visit_ProcHeader(self, node, sym_table):
        # not yet implemented!
        if sym_table.get(node.ident) is not None:
            print "Linia: %d. Nazwa procedury %s jest juz w uzyciu."(node.lineno, node.ident)
        else:
            arg_types = list()
            for arg in node.arguments:
                arg_types.append(arg.accept(self, sym_table))
            sym_table.put(node.ident, FunctionSymbol(node.ident, "void", arg_types))


    def visit_FuncHeader(self, node, sym_table):
        # not yet implemented!
        if sym_table.get(node.ident) is not None:
            print "Linia: %d. Nazwa funkcji %s jest juz w uzyciu."(node.lineno, node.ident)
        else:
            arg_types = list()
            for arg in node.arguments:
                arg_types.append(arg.accept(self, sym_table))
            sym_table.put(node.ident, FunctionSymbol(node.ident, node.return_type, arg_types))


    def visit_Argument(self, node, sym_table):
        # not yet implemented!
        if sym_table.get(node.arg_name) is not None:
            print "Linia: %d. Nazwa zmiennej z sygnatury funkcji %s juz w uzyciu!" % (node.lineno, node.arg_name)
        else:
            sym_table.put(node.arg_name, VariableSymbol(node.arg_name, node.arg_type))
        return node.arg_type


    def visit_CompoundStatement(self, node, sym_table):
        for statement in node.statement_list:
            statement.accept(self, None)


    def visit_AssignmentStatement(self, node, sym_table):
        node.expression.accept(self, None)
        self.code.append("pop ax")  # get expression value to ax
        self.code.append("mov " + node.variable.ident + ", ax")


    def visit_IfStatement(self, node, sym_table):
        node.condition.accept(self, sym_table)
        self.code.append("pop ax")
        self.code.append("cmp ax, 0")
        etiquette = "af_if" + str(self.if_counter)
        etiquette2 = "af_else" + str(self.if_counter)
        self.if_counter += 1
        self.code.append("jne " + etiquette)
        node.if_statement.accept(self, sym_table)
        if node.else_statement:
            self.code.append("jmp " + etiquette2)
        self.code.append(etiquette + ":")
        if node.else_statement:
            node.else_statement.accept(self, sym_table)
            self.code.append(etiquette2 + ":")


    def visit_ProcedureCall(self, node, sym_table):
        # simplified implementation for print, which assumes number to print is in ax
        #should push current procedure values on stack
        #currently handles passing only one argument
        if node.expr_list:
            node.expr_list[0].accept(self, sym_table)
            self.code.append("pop ax")
        self.code.append("call " + node.procedure_name)
        #should pop local procedure values from stack


    # def visit_FunctionCall


    #def visit_ForStatement(self, node, sym_table):


    def visit_WhileStatement(self, node, sym_table):
        loop_start = "loops" + str(self.loops_counter)
        loop_end = "loope" + str(self.loops_counter)
        self.loops_counter += 1

        self.code.append(loop_start + ":")
        node.condition.accept(self, sym_table)
        self.code.append("pop ax")
        self.code.append("cmp ax, 0")
        self.code.append("jne " + loop_end)
        node.while_body.accept(self, sym_table)
        self.code.append("jmp " + loop_start)
        self.code.append(loop_end + ":")


    def visit_RepeatStatement(self, node, sym_table):
        #not yet implemented!
        node.condition.accept(self, sym_table)
        node.repeat_body.accept(self, sym_table)


    def visit_BinaryExpression(self, node, sym_table):
        before_values_on_stack = self.values_on_stack
        node.right_operand.accept(self, None)
        node.left_operand.accept(self, None)
        # if (before_values_on_stack + 2) != self.values_on_stack:
        #     print "Error! More variables on stack than expected in BinaryExpression"

        if node.operator == "*":
            self.code.append("pop ax")
            self.code.append("pop bx")
            self.code.append("mul bx")
            self.values_on_stack -= 2
            self.code.append("push ax")  #push result to stack
            self.values_on_stack += 1
        elif node.operator == "/":
            self.code.append("mov dx, 0")
            self.code.append("pop ax")
            self.code.append("pop bx")
            self.code.append("div bx")
            self.values_on_stack -= 2
            self.code.append("push ax")  #push result to stack
            self.values_on_stack += 1
        elif node.operator == "+":
            self.code.append("pop ax")
            self.code.append("pop bx")
            self.values_on_stack -= 2
            self.code.append("add ax, bx")
            self.code.append("push ax")  #push result to stack
            self.values_on_stack += 1
        elif node.operator == "-":
            self.code.append("pop ax")
            self.code.append("pop bx")
            self.values_on_stack -= 2
            self.code.append("sub ax, bx")
            self.code.append("push ax")  #push result to stack
            self.values_on_stack += 1
        elif node.operator == ">":
            self.code.append("pop ax")
            self.code.append("pop bx")
            self.values_on_stack -= 2
            self.code.append("cmp ax, bx")
            self.code.append("mov ax, 0") #assume it will be true
            etiquette = "af_cmp" + str(self.cmp_counter)
            self.cmp_counter += 1
            self.code.append("jg " + etiquette)
            self.code.append("mov ax, 1") #if we didn't jump, it's false
            self.code.append(etiquette + ":")
            self.code.append("push ax")
        elif node.operator == ">=":
            self.code.append("pop ax")
            self.code.append("pop bx")
            self.values_on_stack -= 2
            self.code.append("cmp ax, bx")
            self.code.append("mov ax, 0") #assume it will be true
            etiquette = "af_cmp" + str(self.cmp_counter)
            self.cmp_counter += 1
            self.code.append("jge " + etiquette)
            self.code.append("mov ax, 1") #if we didn't jump, it's false
            self.code.append(etiquette + ":")
            self.code.append("push ax")
        elif node.operator == "<":
            self.code.append("pop ax")
            self.code.append("pop bx")
            self.values_on_stack -= 2
            self.code.append("cmp ax, bx")
            self.code.append("mov ax, 0") #assume it will be true
            etiquette = "af_cmp" + str(self.cmp_counter)
            self.cmp_counter += 1
            self.code.append("jl " + etiquette)
            self.code.append("mov ax, 1") #if we didn't jump, it's false
            self.code.append(etiquette + ":")
            self.code.append("push ax")
        elif node.operator == "=<":
            self.code.append("pop ax")
            self.code.append("pop bx")
            self.values_on_stack -= 2
            self.code.append("cmp ax, bx")
            self.code.append("mov ax, 0") #assume it will be true
            etiquette = "af_cmp" + str(self.cmp_counter)
            self.cmp_counter += 1
            self.code.append("jle " + etiquette)
            self.code.append("mov ax, 1") #if we didn't jump, it's false
            self.code.append(etiquette + ":")
            self.code.append("push ax")
        elif node.operator == "<>":
            self.code.append("pop ax")
            self.code.append("pop bx")
            self.values_on_stack -= 2
            self.code.append("cmp ax, bx")
            self.code.append("mov ax, 0") #assume it will be true
            etiquette = "af_cmp" + str(self.cmp_counter)
            self.cmp_counter += 1
            self.code.append("jne " + etiquette)
            self.code.append("mov ax, 1") #if we didn't jump, it's false
            self.code.append(etiquette + ":")
            self.code.append("push ax")
        elif node.operator == "=":
            self.code.append("pop ax")
            self.code.append("pop bx")
            self.values_on_stack -= 2
            self.code.append("cmp ax, bx")
            self.code.append("mov ax, 0") #assume it will be true
            etiquette = "af_cmp" + str(self.cmp_counter)
            self.cmp_counter += 1
            self.code.append("je " + etiquette)
            self.code.append("mov ax, 1") #if we didn't jump, it's false
            self.code.append(etiquette + ":")
            self.code.append("push ax")


    def visit_Variable(self, node, sym_table):
        self.code.append("mov ax, " + node.ident)
        self.code.append("push ax")
        self.values_on_stack += 1


    def visit_Const(self, node, sym_table):
        if isinstance(node, Integer):
            self.code.append("push " + node.value)
            self.values_on_stack += 1



