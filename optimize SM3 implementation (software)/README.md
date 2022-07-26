### 项目名称：do your best to optimize SM3 implementation (software)
#### 项目代码说明
    项目共有三个源代码文件`SM3_宏函数_SIMD.cpp`<br> ，其中代码**SM3_without_optimization.cpp**是没有做任何优化的SM3的简单实现，代码**SM3_宏函数优化.cpp**是在**SM3_without_optimization.cpp**的基础上进行宏函数优化，将自己定义的函数修改为宏函数，减少因为函数调用产生的大量时间开销
