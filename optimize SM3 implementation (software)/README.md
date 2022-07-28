### Project：do your best to optimize SM3 implementation (software)
#### 项目代码说明
* 项目共有三个源代码文件**SM3_without_optimization.cpp**、**SM3_宏函数优化.cpp**与**SM3_宏函数_SIMD.cpp**。
* 代码**SM3_without_optimization.cpp**是没有做任何优化的SM3的简单实现。
* 代码**SM3_宏函数优化.cpp**是在**SM3_without_optimization.cpp**的基础上进行宏函数优化，将自己定义的函数修改为宏函数，减少因为函数调用产生的大量时间开销。
* 代码**SM3_宏函数_SIMD.cpp**是在**SM3_宏函数优化.cpp**的基础上将部分代码改为SIMD形式，也是我们代码的最终形式。
* 运行代码即可实现测试过程，测试过程中使用 **“abc”** 作为输入，外循环执行5次，内循环执行1000000次，计算出来每1000000次执行所花费时间，再计算出每秒可以计算多少次。

#### 运行指导
直接将代码复制到visual studio中，点击运行即可。
#### 代码运行过程及其截图
* **SM3_without_optimization.cpp**
点击运行即可，此代码未经过优化，执行时间较长。<br>
运行结果：<br>
![image](https://user-images.githubusercontent.com/105151081/181038427-f583301d-fa2a-4a17-80ee-6963c786a97e.png)

* **SM3_宏函数优化.cpp**
直接点击运行。<br>
运行结果：<br>
![image](https://user-images.githubusercontent.com/105151081/181040503-9ca6299c-d080-4ffb-8062-3e84b3bbb39f.png)

* **SM3_宏函数_SIMD.cpp**
直接点击运行。<br>
运行结果：<br>
![image](https://user-images.githubusercontent.com/105151081/181041164-97368bc5-a2ef-4f9f-bc5b-5c857e01ebe6.png)

#### 贡献说明
本项目全部由王文凯同学完成。
