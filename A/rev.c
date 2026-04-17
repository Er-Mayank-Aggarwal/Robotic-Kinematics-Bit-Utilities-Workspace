#include <stdio.h>

unsigned char reverse_bits(unsigned char byte)
{
    unsigned char rev = 0;
    for(int i = 0; i < 8; i++)
    {
        rev <<= 1;
        rev |= (byte & 1);
        byte >>= 1;
    }
    return rev;
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

    printf("\nReversed: ");
    showbits(reverse_bits(num));

    return 0;
}