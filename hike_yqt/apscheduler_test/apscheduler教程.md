##apscheduler的四大组件  
- triggers 触发器 可以按照日期、时间间隔或者contab表达式三种方式触发 
- job stores 作业存储器 指定作业存放的位置，默认保存在内存，也可以保存在各种数据库中
- executors 执行器 将指定的作业提交到线程池或者进程池中运行
- schedulers 作业调度器 常用的有BackgroundScheduler（后台运行）和BlockingScheduler(阻塞式)