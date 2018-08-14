num1 = 30
num2 = 192
c1 = 'good'
c2 = 'hello'
a = {'a':8, 'k':c2, 'c':3, 'b':5}
a['g'] = 56
a['jj'] = num2
a['89'] = 'asdfg'
a['u'] =42
a['d'] = c1
a['11'] = 40
a['0'] = num1
print(a)
for key in a:
    print(key, a[key])
