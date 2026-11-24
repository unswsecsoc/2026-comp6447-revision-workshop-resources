- `PROG_PATH`: Path to the chall binary
- `LIBC_PATH`: Path to the chall libc shared object (`linc.so.6`)
  - You can pass `LOCAL_LIBC` on the command line to use your local libc instead
  - I typically keep a standard libc in my scripts dir and use it for all challs except those that use different libc versions and need libc-specific exploitation.
- `REMOTE` and `REMOTE_PORT`: Self explanatory, only used when `REMOTE` is passed on the cmd line, otherwise the binary at `PROG_PATH` is executed locally.
- `ic()`: You can call this to log stuff for debugging, e.g. `ic(libc.address)` will print something like `libc.address: 0x12345678000 (1250999894016)`
- `context.terminal`: Used to open GDB in a new tmux (or zellij) pane. You'll need to be in a tmux (or zellij) session to use GDB with this script.
- GDB: if you pass `GDB` on the command line, it'll open a splitscreen pane with GDB on the right, and run `gdbscript` immediately. This is very very useful, it means you don't have to get the pid of the program and manually attach every time, and means you can run certain commands at the start every time if you want. It should automatically use pwndbg but if not you might need to change some stuff to get it working.

So e.g. to run against the remote you'd run `./solve.py REMOTE`, or to run with gdb you'd run `./solve.py GDB` from within tmux.
Also, the `DEBUG` and `NOASLR` options are often useful, you can look at the pwntools docs to see what all the different options do. 