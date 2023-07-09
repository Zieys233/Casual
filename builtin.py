import runtime


def init(initalVariablePool:dict):
    initalVariablePool["<runtime>"]["variablePool"]["print"]["internal"] = builtinPrint
    initalVariablePool["<runtime>"]["variablePool"]["str_to_int"]["internal"] = builtinInt
    initalVariablePool["<runtime>"]["variablePool"]["float_to_int"]["internal"] = builtinInt
    initalVariablePool["<runtime>"]["variablePool"]["str_to_float"]["internal"] = builtinFloat
    initalVariablePool["<runtime>"]["variablePool"]["int_to_float"]["internal"] = builtinFloat
    initalVariablePool["<runtime>"]["variablePool"]["to_str"]["internal"] = builtinStr
    initalVariablePool["<runtime>"]["variablePool"]["strlen"]["internal"] = strlen
    initalVariablePool["<runtime>"]["variablePool"]["chr"]["internal"] = numToChar
    initalVariablePool["<runtime>"]["variablePool"]["ord"]["internal"] = getUnicode

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

def strlen(variablePool:dict, currentScope:str):
    content = runtime.getValue(variablePool, currentScope, "content")[0]["variablePool"]["__value"]
    if content == None: print("TypeError: Cannot pass in null type"); exit(1)
    return len(content)

def numToChar(variablePool:dict, currentScope:str):
    num = runtime.getValue(variablePool, currentScope, "num")[0]["variablePool"]["__value"]
    if num == None: print("TypeError: Cannot pass in null type"); exit(1)
    return chr(num)

def getUnicode(variablePool:dict, currentScope:str):
    char = runtime.getValue(variablePool, currentScope, "char")[0]["variablePool"]["__value"]
    if char == None: print("TypeError: Cannot pass in null type"); exit(1)
    return ord(char)
