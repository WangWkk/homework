import SM2
import random
import bitcoin
def gcd(a,b):
    if b==0:
        return 1,0,a 
    else:
        x,y,q=gcd(b,a%b)
        x,y=y,(x-(a//b)*y)
        return x,y,q
#拓展欧几里得算法求逆元
def inv(a,p):
    x,y,q=gcd(a,p)
    if q!=1:
        raise Exception("No solution!")
    else:
        return (x+p)%p
#进行签名的用户
class Certifiers:
    def __init__(self):
        self.d1=random.randint(1,(SM2.n)-1)
        #print("d1=",self.d1)
        self.Z=b'sduzt'#标识符
        self.k1=random.randint(1,SM2.n-1)
    def Certifiers_1(self):
        P1=SM2.Mulyipoint(inv(self.d1,SM2.p),SM2.G,SM2.a,SM2.p)
        #print('P1=',P1)
        return P1
    def Certifiers_2(self,M):
        e=bitcoin.hash_to_int(self.Z+M)
        #print('e=',e)
        #print('k1=',self.k1)
        Q1=SM2.Mulyipoint(self.k1,SM2.G,SM2.a,SM2.p)
        return Q1,e
    #生成签名
    def Certifiers_3(self,r,s2,s3):
        s=SM2.MOD(((self.d1*self.k1)*s2+self.d1*s3-r),SM2.n)
        if s!=0 and s!=(SM2.n-r):
            return [r,s]
    
#请求签名的一方
class Sender:
    def __init__(self):
        self.d2=random.randint(1,SM2.n-1)
        self.M=b"helloworld"
    def Sender_1(self,P1):
        #print("d2=",self.d2)
        P=SM2.Mulyipoint(inv(self.d2,SM2.p)-1,P1,SM2.a,SM2.p)
        print("public key=",P)
    #生成部分签名r
    def Sender_2(self,Q1,e):
        k2=random.randint(1,SM2.n-1)
        k3=random.randint(1,SM2.n-1)
        Q2=SM2.Mulyipoint(k2,SM2.G,SM2.a,SM2.p)
        T=[0,0]
        temp=SM2.Mulyipoint(k3,Q1,SM2.a,SM2.p)#k3*Q1
        T[0]=temp[0]+Q2[0]
        T[1]=temp[1]+Q2[1]
        r=SM2.MOD(T[0]+e,SM2.n)
        #print("生成的部分签名为:",r)
        s2=SM2.MOD(self.d2*k3,SM2.n)
        s3=SM2.MOD(self.d2*(r+k2),SM2.n)
        return r,s2,s3
#模拟交互过程
if __name__=='__main__':
    S=Sender()
    C=Certifiers()
    P1=C.Certifiers_1()
    S.Sender_1(P1)#将P1发送给请求签名的一方。
    Q1,e=C.Certifiers_2(S.M)
    r,s2,s3=S.Sender_2(Q1,e)
    sigma=C.Certifiers_3(r,s2,s3)
    print("签名为：",sigma)
