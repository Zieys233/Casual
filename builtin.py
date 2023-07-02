import runtime

def init(initalVariablePool:dict):
    initalVariablePool["<runtime>"]["variablePool"]["print"]["internal"] = builtinPrint
    initalVariablePool["<runtime>"]["variablePool"]["str_to_int"]["internal"] = builtinInt
    initalVariablePool["<runtime>"]["variablePool"]["float_to_int"]["internal"] = builtinInt
    initalVariablePool["<runtime>"]["variablePool"]["str_to_float"]["internal"] = builtinFloat
    initalVariablePool["<runtime>"]["variablePool"]["int_to_float"]["internal"] = builtinFloat
    initalVariablePool["<runtime>"]["variablePool"]["to_str"]["internal"] = builtinStr

def builtinPrint(variablePool:dict, currentScope:str, content:str) -> int:
    if content == None: print("(null)", end=''); return 1
    print(content, end='')
    return len(content)

def builtinInt(variablePool:dict, currentScope:str, num):
    print("builtin int() function is worked")
    return None

def builtinFloat(variablePool:dict, currentScope:str, num):
    print("builtin float() function is worked")
    return None

def builtinStr(variablePool:dict, currentScope:str, num):
    if num == None: print("TypeError: Cannot pass in null type"); exit(1)
    return str(num)
