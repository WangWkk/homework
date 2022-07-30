## Project:

$\qquad$**implement sm2 2P sign with real network communicatione**

## 语言环境

$\qquad$ python3

## 贡献说明

$\qquad$ 本项目全部由张天完成

## 项目代码说明

- 2P_sign.py文件模拟了实际网络中2P签名过程。
- 需将2P_sign.py和SM2.py文件放于同一文件夹下运行，签名时间较长，请耐心等待。
- 代码内容说明详见代码内注释。

## 代码运行过程截图
$\qquad$ 签名方随机生成d1，并计算出P1。
![](../%E5%9B%BE%E7%89%87/d1P1.png)
将P1发送给请求签名的一方，
![](../%E5%9B%BE%E7%89%87/P1.png)
请求方随机选择d2，利用P1计算公钥P,
![](../%E5%9B%BE%E7%89%87/d2publick.png)
签名方将消息m=“helloworld”与标识码Z级联，哈希运算得到e，并随机选取k1，计算Q1。
![](../%E5%9B%BE%E7%89%87/k1.png)
将Q1,e发送给请求方，请求方根据算法计算部分签名r，并将r,s2,s3发送给签名方，
![](../%E5%9B%BE%E7%89%87/r.png)
![](../%E5%9B%BE%E7%89%87/rs2s3.png)
签名方以此计算并输出签名$\sigma$:
![](../%E5%9B%BE%E7%89%87/sigma.png)