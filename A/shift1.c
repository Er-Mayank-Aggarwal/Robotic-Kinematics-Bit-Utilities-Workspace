#include <stdio.h>

unsigned char shift_ones_left(unsigned char byte)
{
    int ones = 0;
    for(int i = 0; i < 8; i++)
        if(byte & (1 << i)) ones++;

    return (0xFF << (8 - ones));
}

void showbits(unsigned char byte)
{
    for(int i = 7; i >= 0; i--)
        printf("%d", (byte >> i) & 1);
}

int main()
{
    unsigned char num;
    printf("Enter number: ");
    scanf("%hhu", &num);

    printf("Original: ");
    showbits(num);

    printf("\nShifted:  ");
    showbits(shift_ones_left(num));

    return 0;
}