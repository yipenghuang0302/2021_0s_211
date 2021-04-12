OUTPUT=cacheBlocking
CFLAGS=-Wall -Werror -m64
# -fsanitize=address

%: %.c %.h
	gcc $(CFLAGS) -O0 -o $@ $<

%: %.c
	gcc $(CFLAGS) -O0 -o $@ $<

all: $(OUTPUT)

clean:
	rm -f *.o $(OUTPUT)
