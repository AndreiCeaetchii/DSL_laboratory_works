from ply import yacc
from lexer import tokens, lexer
from ast_definitions import *

start = 'start_command'


def p_start_command(p):
    """start_command : START_COMMAND target_flag command_sequence"""
    p[0] = StartCommand(p[1], p[2], p[3])


def p_target_flag_img(p):
    """target_flag : FLAG EQUALS IMAGE_PATH"""
    p[0] = TargetFlag(p[1], p[3])


def p_target_flag_folder(p):
    """target_flag : FLAG EQUALS FOLDER_PATH"""
    p[0] = TargetFlag(p[1], p[3])


def p_command_sequence_single(p):
    """command_sequence : command"""
    p[0] = p[1]


def p_command_sequence_pipe(p):
    """command_sequence : command PIPELINE command_sequence"""
    p[0] = p[1]
    p[0].next_command = p[3]


def p_command_plain(p):
    """command : COMMAND"""
    p[0] = Command(p[1])


def p_command_with_flags(p):
    """command : COMMAND flag_sequence"""
    p[0] = Command(p[1], p[2])


def p_flag_sequence_single(p):
    """flag_sequence : flag"""
    p[0] = [p[1]]


def p_flag_sequence_collect(p):
    """flag_sequence : flag flag_sequence"""
    p[0] = [p[1]] + p[2]


def p_flag(p):
    """flag : FLAG EQUALS value"""
    p[0] = Flag(p[1], p[3])


def p_value(p):
    """value : NUMBER
             | IMG_FORMAT
             | IMAGE_PATH"""
    p[0] = p[1]


def p_error(p):
    if p is not None:
        print(f"Syntax error at token '{p.value}'")
    else:
        print("Syntax error at EOF")


parser1 = yacc.yacc()
