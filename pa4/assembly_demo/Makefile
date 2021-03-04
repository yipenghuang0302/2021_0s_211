OUTPUT=greater_than
CC=gcc
CFLAGS=-Os -Wall -Werror -std=c99
ASM = swap.s

%.s: %.c
	$(CC) $(CFLAGS) -S $^ -o $@

$(OUTPUT): $(OUTPUT).s
	$(CC) $(CFLAGS) $^ -o $@

all: $(OUTPUT)

clean:
	rm -f *.s *.o $(OUTPUT)
