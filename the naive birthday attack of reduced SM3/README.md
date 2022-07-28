### Project：implement the naïve birthday attack of reduced SM3（16 bits）
#### 项目代码说明
该项目有一个名为 **birthday_attack.cpp** 的源代码文件，内容主要是详细的优化过的SM3代码和实施birthday attack的代码，SM3代码使用的是在另一个project中使用宏函数和SIMD指令优化过的代码。
#### 运行指导
将代码复制到visual studio中，直接运行即可。
#### 代码运行过程截图
直接运行程序，输出的两行字符串即为经过哈希后，前16bits相同的原像。<br>
截图：
![image](https://user-images.githubusercontent.com/105151081/181529976-b1f750dc-8daa-405a-a8d7-71a3a771452e.png)
#### 贡献说明：
本项目全部由王文凯同学完成。
