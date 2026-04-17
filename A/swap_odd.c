#include <stdio.h>
#include "bit_utils.h"

unsigned int swap_bits(unsigned int x)
{
    return ((x & 0xAAAAAAAA) >> 1) | ((x & 0x55555555) << 1);
}

int main()
{
    unsigned int x;
    scanf("%u", &x);
    showbits(x);

    printf("Result: %u\n", swap_bits(x));
    showbits(swap_bits(x));
    return 0;
}

// to run
// gcc swap_odd.c bits_utils.c -o program 
