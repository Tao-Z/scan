def merge_by_x(a, b, begin, middle, end):  #merge (begin~middle-1) and (middle~end-1) in list x to list y
    i=begin
    j=middle
    for k in range(begin, end):
        if i<middle and (j>=end or a[i][0]<a[j][0] or (a[i][0]==a[j][0] and a[i][1]<a[j][1])):
            b[k][0]=a[i][0]
            b[k][1]=a[i][1]
            i=i+1
        else:
            b[k][0]=a[j][0]
            b[k][1]=a[j][1]
            j=j+1
def merge_by_y(a, b, begin, middle, end):  #merge (begin~middle-1) and (middle~end-1) in list x to list y
    i=begin
    j=middle
    for k in range(begin, end):
        if i<middle and (j>=end or a[i][1]<a[j][1] or (a[i][1]==a[j][1] and a[i][0]<a[j][0])):
            b[k][0]=a[i][0]
            b[k][1]=a[i][1]
            i=i+1
        else:
            b[k][0]=a[j][0]
            b[k][1]=a[j][1]
            j=j+1
def copy(x,y):
    for i in range(len(y)):
        x[i][0]=y[i][0]
        x[i][1]=y[i][1]
def sort(a,coord):
    b=[[0,0] for i in range(len(a))]  #work list b
    width=1
    while width<len(a):
        for i in range(0,len(a),2*width):
            if coord=='x':
                merge_by_x(a,b,i,min(i+width,len(a)),min(i+2*width,len(a)))
            elif coord=='y':
                merge_by_y(a,b,i,min(i+width,len(a)),min(i+2*width,len(a)))
        copy(a,b)
        width=width*2
