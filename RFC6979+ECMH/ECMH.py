import SM2#加载预先写好的SM2.py文件
from gmssl import sm3,func
#[2]
#Tonelli-Shanks算法求二次剩余
def Legendre(n,p):
    return pow(n,(p-1)>>1,p)
def Tonelli_Shanks(n,p):
    assert Legendre(n,p)==1
    if p%4==3:
        return pow(n,(p + 1)>>2,p)
    q=p-1
    s=0
    while q%2==0:
        q=q/2
        s+=1
    for z in range(2,p):
        if Legendre(z,p)==p-1:
            c=pow(z,q,p)
            break
    r=pow(n,(q+1)>>1,p)
    t=pow(n,q,p)
    m=s
    if t%p==1:
        return r
    else:
        i=0
        while t%p!=1:
            temp=pow(t,2**(i+1),p)#这里写作i+1是为了确保之后内层循环用到i值是与这里的i+1的值是相等的
            i+=1
            if temp%p==1:
                b=pow(c,2**(m-i-1),p)
                r=r*b%p
                c=b*b%p
                t=t*c%p
                m=i
                i=0
        return r
def MultiSetHash(Set):
    x=[float("inf"),float("inf")]
    for i in Set:
        y=int(sm3.sm3_hash(func.bytes_to_list(i)),16)
        temp=SM2.MOD(y**2+(SM2.a)*y+(SM2.b),SM2.p)
        z=Tonelli_Shanks(temp,SM2.p)
        x=SM2.Pluspoint(x,[y,z],SM2.a,SM2.p)
    return x
if __name__=='__main__':
    set1=(b'1234',)
    set2=(b'12345',)
    set3=(b'1234',b'12345')
    set4=(b'12345',b'1234')
    result1=MultiSetHash(set1)
    result2=MultiSetHash(set2)
    result3=MultiSetHash(set3)
    result4=MultiSetHash(set4)
    Result=SM2.Pluspoint(result1,result2,SM2.a,SM2.p)
    #print("hash({b'1234'})=",result1)
    #print("hash({b'12345'})=",result2)
    print("hash({b'1234'}+hash(b'12345'))=",Result)
    print("hash({b'1234',b'12345'})=",result3)
    print("hash({b'12345',b'1234'})=",result4)