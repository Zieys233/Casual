# Casual Programming Language
# For learning purposes only
# Author: Benjamin Tang

# Improved version for Tranquillity lang


from sys import argv, exit

def main(argv:list):
    # Read variablePool file
    from json import loads, JSONDecodeError
    import builtin

    try:
        if '\\' in argv[0]: path = '/'.join(argv[0].split('\\')[:-1])
        elif '/' in argv: path = '/'.join(argv[0].split('/')[:-1])
        else: path = './'

        with open(path+"/Lib/variablePool") as f:
            initalVariablePool = loads(f.read())
            # print(initalVariablePool)
            builtin.init(initalVariablePool)
            # print(initalVariablePool)
    except FileNotFoundError: print("OSError: Missing orginal varibale pool file"); exit(1)
    except JSONDecodeError: print("OSError: Fatal syntax in original variable pool file"); exit(1)
    
    # Read the source code and run it
    from runtime import run, deleteBlankPart

    try:
        with open(argv[1], 'r') as f:
            sourceCode = deleteBlankPart(f.read(), 1)
            # print(f"======code======\n{sourceCode}\n===============")
            try:
                run(sourceCode, False, False, initalVariablePool, "<runtime>")
            except KeyboardInterrupt: ...
    except FileNotFoundError: print("OSError: Can not find the source file"); exit(1)
    # except IndexError: print("OSError: Missing source file"); exit(1)

if __name__ == "__main__":
    main(argv)
