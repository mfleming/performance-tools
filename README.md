# performance-tools
A collection of performance-related tools and scripts

## schedtime - A better time(1)-like tool 

schedtime executes a program and prints the run time statistics. It
works like the time(1) command, only instead of printing high-level
details such as system and user time schedtime tells you whether the
program was waiting on userspace (sleep(), wait()), waiting in the
kernel (preemption, locking), or blocked on i/o (disk and network
accesses).
