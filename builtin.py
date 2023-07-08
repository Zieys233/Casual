import runtime


def init(initalVariablePool:dict):
    initalVariablePool["<runtime>"]["variablePool"]["print"]["internal"] = builtinPrint
    initalVariablePool["<runtime>"]["variablePool"]["str_to_int"]["internal"] = builtinInt
    initalVariablePool["<runtime>"]["variablePool"]["float_to_int"]["internal"] = builtinInt
    initalVariablePool["<runtime>"]["variablePool"]["str_to_float"]["internal"] = builtinFloat
    initalVariablePool["<runtime>"]["variablePool"]["int_to_float"]["internal"] = builtinFloat
    initalVariablePool["<runtime>"]["variablePool"]["to_str"]["internal"] = builtinStr

def builtinPrint(variablePool:dict, currentScope:str) -> int:
    content = runtime.getValue(variablePool, currentScope, "content")[0]['variablePool']['__value']
    if content == None: print("(null)", end=''); return 1
    print(content, end='')
    return len(content)

def builtinInt(variablePool:dict, currentScope:str):
    num = runtime.getValue(variablePool, currentScope, "num")[0]["variablePool"]["__value"]
    if num == None: print("TypeError: Cannot pass in null type"); exit(1)
    return int(float(num))

def builtinFloat(variablePool:dict, currentScope:str):
    num = runtime.getValue(variablePool, currentScope, "num")[0]["variablePool"]["__value"]
    if num == None: print("TypeError: Cannot pass in null type"); exit(1)
    return float(num)

def builtinStr(variablePool:dict, currentScope:str):
    num = runtime.getValue(variablePool, currentScope, "num")[0]["variablePool"]["__value"]
    if num == None: print("TypeError: Cannot pass in null type"); exit(1)
    return str(num)
