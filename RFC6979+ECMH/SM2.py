import hashlib
import random
import math
import hmac
import bitcoin

def MOD_f(n,a,b):
    if a==0:
        x=0
    elif n==0:
        x=float('inf')
    else:
        t=bin(b-2).replace('0b','')
        y=1
        i=0
        while i<len(t):
            y=(y**2)%b
            if t[i]=='1':
                y=(y*a)%b
            i+=1
        x=(y*n)%b
    return x
#求模
def MOD(a,b):
    if math.isinf(a):
        return float('inf')
    else:
        return a%b
#[1]
#椭圆曲线上加法的实现(无穷远点设为零点O)
def Pluspoint(P,Q,a,p):
    if (math.isinf(P[0]) or math.isinf(P[1])) and (~math.isinf(Q[0]) and ~math.isinf(Q[1])):#O+Q=Q
        R=Q
    elif (~math.isinf(P[0]) and ~math.isinf(P[1])) and (math.isinf(Q[0]) or math.isinf(Q[1])):#O+P=P
        R=P
    elif((math.isinf(P[0]) or math.isinf(P[1])) and (math.isinf(Q[0]) or math.isinf(Q[1])) or ((P[1]+Q[1])==0 and P[0]==Q[0])):#O+O=O or P=-Q
        R=[float('inf'),float('inf')]
    else:
        if P!=Q:
            k=MOD_f(Q[1]-P[1],Q[0]-P[0],p)
        else:#二倍点运算
            k=MOD_f(3*P[0]**2+a,2*P[1],p)#该点处切线的斜率：dy/dx=(3x^2+a)/2y
        x=MOD(k**2-P[0]-Q[0],p)
        y=MOD(k*(P[0]-x)-P[1],p)
        R=[x,y]
    return R
#计算利用二倍点实现椭圆曲线上的乘法
def Mulyipoint(k,G,a,p):
    k_b=bin(k).replace('0b','')#转变为2进制
    l=len(k_b)-1
    R=G
    if l!=0:
        k=k-2**l
        while l!=0:
            R=Pluspoint(R,R,a,p)
            l-=1
        if k>0:
            R=Pluspoint(R,Mulyipoint(k,G,a,p),a,p)
    return R  
#[3]、[4]
#密钥生成函数
def key_Gen(n,P,a,p,m):
    sk=random.randint(1,n-2)
    V=b'\x01'*32
    K=b'\x00'*32
    mhash=bitcoin.encode(bitcoin.hash_to_int(m),256,32)#实现bits2octets变换
    iv=bitcoin.encode(sk, 256, 32)#进行int2otets变换
    K=hmac.new(K,V+b'\x00'+iv+mhash,digestmod='sha256').digest()#使用K对数据进行HMAC算法
    V=hmac.new(K,V,hashlib.sha256).digest()
    K=hmac.new(K,V+b'\x01'+iv+mhash,digestmod='sha256').digest()
    V=hmac.new(K,V,hashlib.sha256).digest()
    k=bitcoin.decode(hmac.new(K,V,digestmod='sha256').digest(),256)
    #k=random.randint(1,n-1)
    pk=Mulyipoint(k,P,a,p)
    return sk,pk

a=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
b=0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
p=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
n=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
Gx=0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7
Gy=0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0
G=[Gx,Gy]

if __name__=='__main__':
    m=b'helloworld'
    sk,pk=key_Gen(n,G,a,p,m)
    print("sk=",sk)
    print('pk=',pk)
