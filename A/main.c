#include <stdio.h>
#include "bit_utils.h"

int main()
{
    unsigned char num, n;

    printf("Enter a number (0-255): ");
    scanf("%hhu", &num);

    printf("Bit sequence: ");
    showbits(num);
    printf("\n");

    printf("Enter n-th position (0-7): ");
    scanf("%hhu", &n);

    printf("Bit at position %d: %d\n", n, get_bit(num, n));

    printf("After setting bit %d: ", n);
    showbits(set_bit(num, n));
    printf("\n");

    printf("After clearing bit %d: ", n);
    showbits(clear_bit(num, n));
    printf("\n");

    printf("After toggling bit %d: ", n);
    showbits(toggle_bit(num, n));
    printf("\n");

    printf("Number of 1s: %d\n", count_ones(num));

    return 0;
}