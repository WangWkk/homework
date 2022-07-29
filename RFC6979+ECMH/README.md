## project:

$\qquad$**1、Implement the above ECMH scheme**

$\qquad$**2、Impl sm2 with RFC6979**

## 语言环境

$\qquad$ python3

## 贡献说明

$\qquad$ 本项目全部由张天完成。

## 项目代码说明
- SM2.py文件中包含SM2算法密钥生成函数，利用二倍点运算实现的椭圆曲线上的加法函数，其中生成公钥时k是根据RFC6979生成。
- ECMH.py文件调用SM2.py中椭圆曲线上的加法函数，实现ECMH方案。
- 代码内容说明详见代码内注释。

## 代码运行过程截图

### 使用RFC6979代替随机生成k

![](%E5%9B%BE%E7%89%87/RFC6979.png)
$\qquad$ 当消息m为"helloworld"时，根据RFC6979生成k的情况下生成的公私钥。

### ECMH
![](%E5%9B%BE%E7%89%87/ECMH.png)
$\qquad$ 图片中第二、三行表明实现了hash加法的同态性，即：hash{a}=hash{b}。第三四行是表明同一个集合的hash值是相同的，即：hash({a,b})=hash({b,a})

## 参考资料：

1、[椭圆曲线](https://trapdoor-tech.github.io/halo2-book-chinese/background/curves.html)

2、[Tonelli-Shanks算法求二次剩余](https://blog.csdn.net/qq_51999772/article/details/122642868)

3、[RFC6979](https://rfc2cn.com/rfc6979.html)

4、[python中hmac模块的使用](https://www.cnblogs.com/eliwang/p/14308791.html)

5、山东大学网络空间安全学院创新创业课
