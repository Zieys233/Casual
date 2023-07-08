float[5]::a = [1.414, 2.236, 3.141];
a[-1+print("a\n")+2] = 233;
float::b = 1;
float::b = a[-1+2];
str::string = to_str(b);

if (b <= 20) 
    print(string+'\n'); 
else if (b == 5) {
    print("i ya da\n");
    b  = b + 255;
    print("a[1]: "+to_str(a[1])+", b:"+to_str(b)+'\n');
} else {
    print("ha?\n");
}

b = 1;
while(b<10){
    if (b == 6) {
        b = b + 2;
        continue;
    }
    print("b-value: "+to_str(b)+'\n');
    b = b + 1;
}


function int[3]::abc(str::content, int::_awa)
{
    content = content + " wtf!!";

    function str::__text(str::content){
        return content + '(end)';
    }
    content = __text(content);

    int[3]::a = [0, 0 ,0];
    int::_tmp = 0;
    while (_tmp < 3)
    {
        a[_tmp] = print(content+'\n')+_awa+_tmp;
        _tmp = _tmp + 1;
    }

    return a;
}

float[3]::_res = abc("hello", 3);

int::_tmp = 0;
while (_tmp < 3)
{
    print(to_str(_res[_tmp])+'\n');
    _tmp = _tmp + 1;
}

