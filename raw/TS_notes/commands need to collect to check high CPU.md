# commands need to collect to check high CPU

For further investigation, please collect when high CPU is seen.

1.Collect from both RE:

> show mpls lsp extensive | save /var/tmp/lsp\_ext.txt

>show mpls lsp | count

2. collect 4-6 iterations of the below commands from both RE:

> show route summary

> show system processes extensive | save /var/tmp/SYS1.txt

> set task accounting on

-- wait for 30 sec --

> show task accounting detail | save /var/tmp/TAD1.txt

> show task accounting extensive | save /var/tmp/TAE1.txt

> set task accounting off

> show task jobs

> show task io

> show task memory detail

> show task memory summary

> show task history

> show task statistics

> show task job

> show krt queue

> show krt state

3. get rpd live core from backup RE.

> start shell user root

# ps -aux | grep rpd (to get RPD pid)

# gcore -c /var/tmp/rpdlive-core.0.gz

4. get rtsockmon from both RE:

> start shell user root

# rtsockmon -nrt
