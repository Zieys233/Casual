from sys import exit
from unicodedata import category
from sys import maxunicode

invalidSymbol = [c for _i in range(maxunicode+1) if category(c:=chr(_i)).startswith('P')]; invalidSymbol.remove('_')

def deleteBlankPart(code:str, remainingBlankCount:int):
    _tmp, stringMode, annotationMode, i = '', False, 0, 0
    while i < len(code):
        if (code[i] == '"' or code[i] == '\'') and not annotationMode: 
            if not stringMode: stringMode = code[i]
            elif stringMode == code[i]: stringMode = False
        if not stringMode and not annotationMode and code[i] == '/' and code[i+1] == '/': annotationMode = 1
        if not stringMode and not annotationMode and code[i] == '/' and code[i+1] == '*': annotationMode = 2
        if annotationMode == 1 and not stringMode and code[i] == '\n': annotationMode = 0
        elif annotationMode == 2 and not stringMode and code[i] == '*' and code[i+1] == '/': annotationMode = 0; i += 1
        elif annotationMode == 0: _tmp += code[i]
        i += 1
    if stringMode: print("SyntaxError: incomplete input of string"); exit(1)

    code = _tmp.replace("\t", '').replace("\n", '').replace("\r", '')
    _tmp, blank, stringMode = '', False, False
    for _c in code :
        if _c == ' ' and not stringMode:
            if not blank: blank = True
        else:
            if blank and not stringMode: _tmp += ' '*remainingBlankCount; blank = False
            _tmp += _c
        if _c == '"' or _c == '\'': 
            if not stringMode: stringMode = _c
            else: stringMode = False
    if stringMode: print("SyntaxError: incomplete input of string"); exit(1)

    return _tmp

def createVariable(variablePool:dict, currentScope:str, variableName:str, variableType:str, internal) -> list:
    currentScopeArray = currentScope.split('.')
    accessWidth = len(currentScopeArray)
    _tmp = variablePool
    for _l in range(accessWidth):
        _tmp = _tmp[currentScopeArray[_l]]["variablePool"]

    _tmp[variableName] = {"type": variableType, "internal": internal, "variablePool": {}}

    return _tmp[variableName]

def getValue(variablePool:dict, currentScope:str, variableName:str):
    currentScopeArray = currentScope.split('.')
    accessWidth = len(currentScopeArray)
    for _i in range(accessWidth):
        _tmp = variablePool
        for _l in range(accessWidth-_i):
            _tmp = _tmp[currentScopeArray[_l]]["variablePool"]
        if variableName in _tmp: return _tmp[variableName]
    
    return None

def tupleParsing(parameterCode:str) -> list:
    if parameterCode == '': return []

    elementArray, element, stringMode, parenthesisLevel = [], '', False, 0
    for _i in range(len(parameterCode)):
        if parameterCode[_i] == '"' or parameterCode[_i] == '\'':
            if stringMode and parameterCode[_i] == stringMode: stringMode = False
            else: stringMode = parameterCode[_i]
        if not stringMode:
            if parameterCode[_i] == '(': parenthesisLevel += 1
            elif parameterCode[_i] == ')':
                if parenthesisLevel == 0: print("SyntaxError: Cannot match closing parenthesis ')'"); exit(1)
                else: parenthesisLevel -= 1
        if not stringMode and not parenthesisLevel and parameterCode[_i] == ',': 
            elementArray.append(element)
            element = ''
        else: element += parameterCode[_i]
    elementArray.append(element)

    return elementArray

def stringCodeRestoration(code:str, stringCodeTable:dict):
    for _i in stringCodeTable.keys():
        code = code.replace(f"${_i}", stringCodeTable[_i])
    return code

def assignmentSentence(code:str, stringCodeTable:dict, variablePool:dict, currentScope:str):
    _value = singleCommandParsing(stringCodeRestoration(code[code.find('=')+1:len(code)], stringCodeTable), variablePool, currentScope)
    _element = stringCodeRestoration(code[0:code.find('=')], stringCodeTable)

    try:
        typeName, variableName = _element.split("::")
    except ValueError: 
        variableValue = getValue(variablePool, currentScope, _element)
        if not variableValue: print("SyntaxError: Type definition required"); exit(1)
        variableValue["variablePool"]["__value"] = _value
        return _value

    # Invalid symbol or invalid variable name
    for _i in ["while", "function", "str", "int", "float", "if", "else", "return", "break", "continue"]:
        if variableName == _i: print("SyntaxError: invalid syntax"); exit(1)
    for _i in invalidSymbol:
        if _i in variableName: print("SyntaxError: invalid syntax"); exit(1)
    if '[' in typeName and typeName[-1] == ']':
        typeName, index = typeName[0:typeName.find('[')], singleCommandParsing(typeName[typeName.find('[')+1:-1], variablePool, currentScope)
        if len(_value) > index: print("IndexError: The actual element quality cannot exceed the array index"); exit(1)
        print(typeName, index)
        createVariable(variablePool, currentScope, variableName, typeName+"[]", None)["variablePool"]["__value"] = _value
    elif typeName == type(_value).__name__ or type(_value).__name__=="NoneType" or \
        (typeName == "float" and type(_value).__name__ == "int"):
        createVariable(variablePool, currentScope, variableName, typeName, None)["variablePool"]["__value"] = _value
    else:
        print("TypeError: Cannot assign values to variables of different types"); exit(1)

    return _value

def functionCall(code:str, stringCodeTable:dict, variablePool:dict, currentScope:str):
    functionName = stringCodeRestoration(code[0:code.find('(')], stringCodeTable) # function name obtained from the code

    functionInformation = getValue(variablePool, currentScope, functionName)
    if not functionInformation: print(f"NameError: name '{functionName}' is not defined"); exit(1)
    if not functionInformation["type"] == "function": 
        print(f"TypeError: '{functionInformation['type']}' object is not callable"); exit(1)
    
    from copy import deepcopy
    originFunctionVariablePool = deepcopy(functionInformation["variablePool"])

    parameterCode = stringCodeRestoration(code[code.find('(')+1:-1], stringCodeTable)
    elementArray = tupleParsing(parameterCode)

    _valueArray = []
    for _i in elementArray: _valueArray.append(singleCommandParsing(_i, variablePool, currentScope))   
    
    returnValueType = functionInformation["variablePool"]["__returnValueType"]
    functionParameterArray = functionInformation["variablePool"]["__parameterList"]
    if len(_valueArray) < len(functionParameterArray): 
        print(f"TypeError: {functionName}() missing {len(functionParameterArray)-len(_valueArray)} required argument"); exit(1)
    elif len(_valueArray) > len(functionParameterArray): 
        print(f"TypeError: Only {len(_valueArray)-len(functionParameterArray)} parameters are required for {functionName}() "); exit(3)
    
    for _i in range(len(_valueArray)):
        _valueType = type(_valueArray[_i]).__name__
        _parameterType = functionInformation["variablePool"][functionParameterArray[_i]]["type"]
        if not (_valueType == _parameterType or _valueType == "NoneType" or (_valueType == "int" and _parameterType == "float")):
            print("TypeError: The formal and actual parameter types must be consistent"); exit(1)

    if functionInformation["internal"]:
        try:
            _value = functionInformation["internal"](variablePool, currentScope+'.'+functionName, *_valueArray)
        except: print("RuntimeError: faulty internal function functionality"); exit(1)
    else:
        _value = run(functionInformation["variablePool"]["__code"], variablePool, currentScope+'.'+functionName)
    functionInformation["variablePool"] = originFunctionVariablePool

    if returnValueType  == type(_value).__name__ or type(_value).__name__=="NoneType" or \
        (returnValueType == "float" and type(_value).__name__ == "int"): return _value
    else: print("TypeError: The return value defined by the function does not match the actual return value"); exit(1)

def operationSentence(code:str, stringCodeTable:dict, variablePool:dict, currentScope:str): 
    # Divide symbols into different groups
    # Different groups represent different priorities
    # The higher the priority of the group, the higher the priority
    symbolArray = [["||", "&&", '!'], ["==", ">=", "<=", '>', '<'], ['+', '-', '*', '/', '%']]
    # Divide the sentence into multiple blocks based on symbols
    if code[0] == '(' and code[-1] == ')': code = code[1:-1]

    sentence = stringCodeRestoration(code[0:len(code)], stringCodeTable)
    element, stringMode, parenthesisLevel, whetherAddingElement, elementArray = '', False, 0, False, []
    for _group in symbolArray:
        _groupBeLocked, _i = False, 0
        while _i < len(sentence):
            if sentence[_i] == '"' or sentence[_i] == '\'': 
                if not stringMode: stringMode = sentence[_i]
                elif stringMode == sentence[_i]: stringMode = False
            
            if not stringMode:
                if sentence[_i] == '(': parenthesisLevel += 1
                elif sentence[_i] == ')':
                    if parenthesisLevel == 0: print("SyntaxError: Cannot match closing parenthesis ')'"); exit(1)
                    else: parenthesisLevel -= 1
                if parenthesisLevel == 0:
                    for _symbol in _group:
                        if not sentence[_i] == _symbol[0]: continue
                        for _l in range(len(_symbol)): 
                            if sentence[_i+_l] != _symbol[_l]: break
                        else:
                            elementArray.extend([element, _symbol])
                            _groupBeLocked, whetherAddingElement, element = True, True, ''
                            _i += len(_symbol)
                            break
            if not whetherAddingElement: element += sentence[_i]; _i += 1
            else: whetherAddingElement = False
        if _groupBeLocked == True: break
        element = '' # Clear the legacy value of the previous group
    else: element = sentence
    if stringMode: print("SyntaxError: incomplete input of string"); exit(1)
    elif parenthesisLevel: print("SyntaxError: Cannot match opening parenthesis '('"); exit(1)
    elementArray.append(element)

    if '' in elementArray: 
        _i, _tmp = 0, []
        while _i < len(elementArray):
            if elementArray[_i] == '' and elementArray[_i+1] == '-':
                _tmp.append(elementArray[_i+1]+elementArray[_i+2])
                _i += 3; continue
            _tmp.append(elementArray[_i])
            _i += 1
        if '' in _tmp: print("SyntaxError: invalid syntax"); exit(1)
        elementArray = _tmp

    # Perform arithmetic operations
    elementParsing = lambda element: singleCommandParsing(element, variablePool, currentScope)

    symbolArray = ["||", "&&", "==", ">=", "<=", '>', '<', '+', '-', '*', '/', '%']
    if elementArray[0] in symbolArray: print("SyntaxError: invalid syntax"); exit(1)
    elif elementArray[0] == '!':
        if elementArray[0] in symbolArray: print("SyntaxError: invalid syntax"); exit(1)
    else:
        _value = elementParsing(elementArray[0])
    for _i in range(len(elementArray)):
        if elementArray[_i] in symbolArray:
            try:
                if elementArray[_i+1] in symbolArray: print("SyntaxError: invalid syntax"); exit(1)

                _anotherValue = elementParsing(elementArray[_i+1])
                if elementArray[_i] == "||": _value = _value or _anotherValue
                elif elementArray[_i] == "&&": _value = _value and _anotherValue
                elif elementArray[_i] == '!': _value = not _anotherValue
                elif elementArray[_i] == "==": _value = int(_value == _anotherValue)
                elif elementArray[_i] == ">=": _value = int(_value >= _anotherValue)
                elif elementArray[_i] == "<=": _value = int(_value <= _anotherValue)
                elif elementArray[_i] == '>': _value = int(_value > _anotherValue)
                elif elementArray[_i] == '<': _value = int(_value < _anotherValue)
                elif elementArray[_i] == '+': _value = _value + _anotherValue
                elif elementArray[_i] == '-': _value = _value - _anotherValue
                elif elementArray[_i] == '*': _value = _value * _anotherValue
                elif elementArray[_i] == '/': _value = _value / _anotherValue
                elif elementArray[_i] == '%': _value = _value % _anotherValue
            except IndexError: print("SyntaxError: invalid syntax"); exit(1)
            except TypeError: 
                print("TypeError: Different types of values cannot be operated on directly")
                if type(_value).__name__ == "NoneType" or type(_anotherValue).__name__ == "NoneType":
                    print(" └─ Warning: type `null` cannot be operated on with any type")
                exit(1)
    return _value

def singleCommandParsing(code:str, variablePool:dict, currentScope:str):
    code = deleteBlankPart(code, 0)
    symbolTable = ['=', '>', '<', '!', '(', '+', '-', '*', '/', '%', '|', '&']
    
    index, _stringMode, mainCode, _stringCode, _count, stringCodeTable = 0, False, '', '', 0, {}
    while index < len(code):
        if code[index] == '"' or code[index] == '\'': 
            if not _stringMode: _stringMode = code[index]; _count += 1
            elif _stringMode == code[index]: 
                _stringMode = False
                while f"${_count}" in code: _count += 1
                stringCodeTable[_count] = _stringCode+code[index]; _stringCode = ''; mainCode += f"${_count}"
                index += 1; continue
        
        if _stringMode: _stringCode += code[index]
        else: mainCode += code[index]
        index += 1
    if _stringMode: print("SyntaxError: incomplete input of string"); exit(1)

    # assignment
    if '=' in mainCode and mainCode[mainCode.find('=')+1] != '=': 
        return assignmentSentence(mainCode, stringCodeTable, variablePool, currentScope)
    
    # function call
    if mainCode[0] != '(' and '(' in mainCode and mainCode[-1] == ')' and mainCode[mainCode.find('(')-1] not in symbolTable:
        for _i in symbolTable:
            if _i in mainCode[0:mainCode.find('(')]: break
        else:
            return functionCall(mainCode, stringCodeTable, variablePool, currentScope)

    # judgment (operation)
    for _i in symbolTable: 
        if _i in mainCode and ('[' not in mainCode or ']' not in mainCode): 
            if mainCode.count('-'):
                # negative number 
                try: 
                    _tmp = stringCodeRestoration(mainCode, stringCodeTable)
                    if int(_tmp) == float(_tmp): return int(_tmp)
                    return float(_tmp)
                except: ...
            return operationSentence(mainCode, stringCodeTable, variablePool, currentScope)

    # Obtain value normally, whether it is in variable pool
    _value = getValue(variablePool, currentScope, stringCodeRestoration(mainCode, stringCodeTable))
    if _value != None: return _value['variablePool']["__value"]
    # whether it is a regular value, such as int, float etc.
    if mainCode == "null": return None
    if (code[0] == '"' or code[0] == '\'') and code[-1] == code[0]: 
        # it is a string
        return code[1:-1].replace("\\t", '\t').replace("\\n", '\n').replace("\\r", '\r')
    elif mainCode[0] == '[' and mainCode[-1] == ']': 
        # it is an array
        _tmp, elementArray = '', []
        for _i in range(1, len(mainCode)-1): 
            if mainCode[_i] == ',': elementArray.append(_tmp); _tmp = ''; continue
            _tmp += mainCode[_i]
        elementArray.append(_tmp)

        elementType = "NoneType"; _tmp = []
        for _i in elementArray: 
            if elementType == type(_i).__name__ or elementType == "NoneType" or type(_i).__name__ == "NoneType" or \
                (elementType == "float" and type(_i).__name__ == "int"): elementType = type(_i).__name__; 
            else: print(f"TypeError: The types of each element in the array must be consistent"); exit(1)
            _tmp.append(singleCommandParsing(_i, variablePool, currentScope))

        return _tmp
    try:
        if float(code) == int(float(code)): return int(code)
        else: return float(code)
    except ValueError: 
        if '[' in mainCode and mainCode[-1] == ']':
            _variable = getValue(variablePool, currentScope, mainCode[0:mainCode.find('[')])
            if not _variable: print(f"NameError: name '{mainCode[0:mainCode.find('[')]}' is not defined"); exit(1)
            _index = singleCommandParsing(stringCodeRestoration(mainCode[mainCode.find('[')+1:-1], stringCodeTable), variablePool, currentScope)
            try:
                return _variable["variablePool"]["__value"][_index]
            except: print(f"SyntaxError: invalid array operation."); exit(1)
        print(f"NameError: name '{code}' is not defined"); exit(1)

def keywordComparison(code:str, index:int, keyword:str) -> int:
    if code[index] == ' ': 
        while True:
            if index == len(code): return None
            if code[index] == ' ': index += 1
            else: break
    
    comparison = ''
    while True:
        if index == len(code): return None
        if code[index] == ' ': break
        comparison += code[index]; index += 1
    
    if comparison == keyword: return index
    else: return None

def run(code:str, variablePool:dict, currentScope:str):
    keywordArray = [
        "function", "while", "if", "else"
    ]

    index = 0
    while index < len(code):
        # Find keywords that match the requirements
        keyword = None
        comparsionResult = None
        for _k in keywordArray:
            comparsionResult = keywordComparison(code, index, _k)
            if comparsionResult: keyword = _k; break
        print("found:", keyword, comparsionResult)

        # No keywords match
        if keyword == None: 
            # Read a single element
            element, stringMode = '', False
            while True:
                if index == len(code): print("EOFError: incomplete input"); exit(1)
                if code[index] == '"' or code[index] == '\'': 
                    if not stringMode: stringMode = code[index]
                    else: stringMode = False
                if code[index] == ';' and not stringMode: break
                element += code[index]
                index += 1

            _result = singleCommandParsing(element, variablePool, currentScope)
            print(f"result: `{_result}`, type: {type(_result)}\n"+'='*25)
            # print(variablePool)
            index += 1; continue
        
        index = comparsionResult
        if keyword == "if":
            ...