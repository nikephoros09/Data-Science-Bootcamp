def data_types():
    a = 1
    b = 'Hello'
    c = 1.0
    d = True
    e = [1,2,3]
    f = {a:1, b:2}
    g = (1,2)
    h = {1,2}
    all_vars = [a,b,c,d,e,f,g,h]
    all_types =  [type(i).__name__ for i in all_vars]
    res = "[" + ", ".join(all_types) + "]"
    print(res)
if __name__ == '__main__':
     data_types()
