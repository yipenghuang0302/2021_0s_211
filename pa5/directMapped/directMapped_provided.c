#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>

// Rutgers University 2021 Spring CS 211 Computer Architecture
// Assignment based on CS:APP Cache Lab

// 64-bit memory address
typedef unsigned long long int mem_addr_t;

// cache properties
unsigned char s = 4; // set index bits
unsigned short S = 1<<4; // set count

unsigned char b = 4; // block offset bits
// unsigned short B = 1<<4; // block size in bytes

// direct mapped cache set/line
typedef struct cache_set_line {
    bool valid;
    mem_addr_t tag;
} cache_set_line_t;

typedef cache_set_line_t* cache_t;

// accessData - Access data at memory address addr.
void accessData (
    mem_addr_t addr,
    cache_t cache,
    unsigned int* hit_count, // If it is already in cache, increase hit_count
    unsigned int* miss_count, // If it is not in cache, bring it in cache, increase miss_count
    unsigned int* eviction_count // Also increase eviction_count if a line is evicted
) {

    // Cache indices for this address
    /* ... */

    // Cache hit
    /* ... */

    // Otherwise, cache miss
    /* ... */

    // If cache set line already in use as indicated by the valid variable, then evict the existing cache set line
    /* ... */
}

int main(int argc, char* argv[]) {

    // path to memory trace
    if ( argc!= 2 ) {
        printf( "Usage: ./directMapped <mem_trace_file>" );
    }
    char* mem_trace_file = argv[1];
    FILE *fp = fopen(mem_trace_file, "r");
    if (!fp) {
        fprintf(stderr, "Error opening file '%s'\n", mem_trace_file);
        exit( EXIT_FAILURE );
    }

    // Allocate memory, write 0's for valid and tag and LRU
    cache_t cache = (cache_set_line_t*) calloc( S, sizeof(cache_set_line_t) );

    /* ... */
}
