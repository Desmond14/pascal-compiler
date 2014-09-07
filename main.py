import sys
import ply.lex as lex
import ply.yacc as yacc
from Cparser import Cparser
from Translator import Translator
from TypeChecker import *


def append_data_segment(code, symbol_table):
    code.append("data	segment")
    for symbol in symbol_table.symbols:
        if isinstance(symbol_table.symbols[symbol], VariableSymbol) and symbol_table.symbols[symbol].type == "int":
            code.append(symbol_table.symbols[symbol].name + " dw ?")

    code.append("data ends")


def append_prefix(code):
    code.append(".model small")
    code.append(".186")
    code.append("stos1 segment STACK")
    code.append("dw	512 dup(?)")
    code.append("top dw	?")
    code.append("stos1 ends")


if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    Cparser = Cparser()
    parser = yacc.yacc(module=Cparser) #(debug = True)
    text = file.read()
    program = parser.parse(text, lexer=Cparser.scanner)
    symbol_table = SymbolTable(None)
    symbol_table.put("print", FunctionSymbol("print", "void", ["int"]))
    type_checker= TypeChecker()
    program.accept(type_checker, symbol_table)
    if not type_checker.correct:
        exit()

    translator = Translator()
    append_prefix(translator.code)
    append_data_segment(translator.code, symbol_table)
    program.accept(translator, None)
    with open('result.asm', 'w') as the_file:
        for line in translator.code:
            the_file.write(line + "\n")


