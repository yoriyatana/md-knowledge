# commands need to collect to check high CPU

For further investigation, please collect when high CPU is seen.

1. Collect from both RE:

```text
> show mpls lsp extensive | save /var/tmp/lsp\_ext.txt
```

```text
>show mpls lsp | count
```

2. collect 4-6 iterations of the below commands from both RE:

```text
> show route summary
```

```text
> show system processes extensive | save /var/tmp/SYS1.txt
```

```text
> set task accounting on
```

- - wait for 30 sec --

```text
> show task accounting detail | save /var/tmp/TAD1.txt
```

```text
> show task accounting extensive | save /var/tmp/TAE1.txt
```

```text
> set task accounting off
```

```text
> show task jobs
```

```text
> show task io
```

```text
> show task memory detail
```

```text
> show task memory summary
```

```text
> show task history
```

```text
> show task statistics
```

```text
> show task job
```

```text
> show krt queue
```

```text
> show krt state
```

3. get rpd live core from backup RE.

```text
> start shell user root
```

# ps -aux | grep rpd (to get RPD pid)

# gcore -c /var/tmp/rpdlive-core.0.gz

4. get rtsockmon from both RE:

```text
> start shell user root
```

# rtsockmon -nrt
