CC := gcc

COMMON_FLAGS := -O0 -fno-stack-protector -no-pie -Wno-stringop-overflow

.PHONY: all clean

all: chal1

chal1: chal1.c
	$(CC) $(COMMON_FLAGS) $< -o $@

clean:
	rm -f chal1
