# Check running lab on eve

root@SP-eve-ng:~# t

Copy output to notepad++

replace .\*(-T \d+ ).\* with $1

use notepad++ to remove duplicate entry

Count the number device by UID

```text
show User ID on EVE
```
admin            admin 0

anhvu admin 6

hailuong        admin 3

hieuduong admin 18

hoangle admin 8

hoangminh admin 23

hungngo admin 19

hungnguyen admin 12

huynguyen admin 13

khangnguyen admin 10

khuongthai admin 14

linhnguyen admin 22

luandang admin 15

minhle admin 11

minhnguyen admin 1

ngocnd admin 9

paragon admin 21

quandinh admin 17

quyle admin 16

script-server admin 7

thinhduong admin 4

thuonghuynh        admin 5

tungnguyen         admin 2

vyman admin 24

mapping the lab and the user ID to check

https://www.man7.org/linux/man-pages/man1/ps.1p.html

## **STDOUT         [top](https://www.man7.org/linux/man-pages/man1/ps.1p.html#top_of_page)**

When the -o option is not specified, the standard output format is

unspecified.

On XSI-conformant systems, the output format shall be as follows.

The column headings and descriptions of the columns in a ps

listing are given below. The precise meanings of these fields are

implementation-defined. The letters 'f' and 'l' (below) indicate

the option (full or long) that shall cause the corresponding

heading to appear; all means that the heading always appears. Note

that these two options determine only what information is provided

for a process; they do not determine which processes are listed.

F      (l)    Flags (octal and additive) associated with

the process.

```text
S      (l)    The state of the process.
```
UID    (f,l)  The user ID number of the process owner;

the login name is printed under the -f

option.

PID    (all)  The process ID of the process; it is

possible to kill a process if this datum is

known.

PPID    (f,l)  The process ID of the parent process.

C      (f,l)  Processor utilization for scheduling.

PRI    (l)    The priority of the process; higher numbers

mean lower priority.

NI      (l)    Nice value; used in priority computation.

ADDR    (l)    The address of the process.

SZ      (l)    The size in blocks of the core image of the

process.

WCHAN  (l)    The event for which the process is waiting

or sleeping; if blank, the process is

running.

STIME  (f)    Starting time of the process.

TTY    (all)  The controlling terminal for the process.

TIME    (all)  The cumulative execution time for the

process.

CMD    (all)  The command name; the full command name and

its arguments are written under the -f

option.
