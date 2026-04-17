#include <stdio.h>

unsigned int next_larger(unsigned int n)
{
    unsigned int c = n;
    int c0 = 0, c1 = 0;

    while(((c & 1) == 0) && c) { c0++; c >>= 1; }
    while(c & 1) { c1++; c >>= 1; }

    int p = c0 + c1;

    n |= (1 << p);
    n &= ~((1 << p) - 1);
    n |= (1 << (c1 - 1)) - 1;

    return n;
}

unsigned int next_smaller(unsigned int n)
{
    unsigned int temp = n;
    int c0 = 0, c1 = 0;

    while (temp & 1) { c1++; temp >>= 1; }   // count 1s
    if (temp == 0) return 0;

    while ((temp & 1) == 0 && temp) { c0++; temp >>= 1; } // count 0s

    int p = c0 + c1;

    n &= (~0) << (p + 1);                 // clear bits
    n |= ((1 << (c1 + 1)) - 1) << (c0 - 1); // add ones

    return n;
}

int main()
{
    unsigned int n;
    printf("Enter number: ");
    scanf("%u", &n);

    printf("Next larger: %u\n", next_larger(n));
    printf("Next smaller : %u\n", next_smaller(n));
    return 0;
}