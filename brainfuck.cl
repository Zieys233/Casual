/* 
 * This is Casual implementation of Brainfuck
 * Casual version: b1.0
 */

print("Please enter the Brainfuck code: ");
str::code = input();
int::length = strlen(code);

int[256]::byteArray = [0]*256;
int::ptr = 0;

int::loop = 0; int::jumping = 0;
int[256]::loopPosition = [];
int::_i = 0; while(_i < length)
{
    if (! jumping && code[_i] == '>') ptr += 1;
    else if (! jumping && code[_i] == '<') ptr -= 1;
    else if (! jumping && code[_i] == '+') byteArray[ptr] += 1;
    else if (! jumping && code[_i] == '-') byteArray[ptr] -= 1;
    else if (! jumping && code[_i] == '.') print(chr(byteArray[ptr]));
    else if (! jumping && code[_i] == ',') 
    {
        _c = input();
        if (strlen(c) == 1) byteArray[ptr] = ord(c);
        else 
        {
            print("error. please enter a char\n"); 
            break;
        }
    }
    else if (code[_i] == '[')  
    {
        loop += 1; loopPosition[loop] = _i;
        if (!byteArray[ptr]) jumping = 1;
    }
    else if (code[_i] == ']')
    {
        if (byteArray[ptr]) _i = loopPosition[loop]-1;
        jumping = 0; loop -= 1;
    }
    else {print("error. stop\n"); break;}
    _i += 1;
}
