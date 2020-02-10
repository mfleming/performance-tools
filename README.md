# performance-tools
A collection of performance-related tools and scripts

## schedtime - A better time(1)-like tool 

schedtime executes a program and prints the run time statistics. It
works like the time(1) command, only instead of printing high-level
details such as system and user time schedtime tells you whether the
program was waiting on userspace (sleep(), wait()), waiting in the
kernel (preemption, locking), or blocked on i/o (disk and network
accesses).

## pmucaps - Display Performance Monitoring Unit capabilities

PMU features vary from system to system, particularly in the cloud where
it's common for the absolute bare minimum of hardware-events to be
available. **pmucaps** prints which PMU capabilities are available on the
current system and includes details such as microarchitecture, Last
Branch Record support, and whether precise IPs can be reported with
PEBS.
