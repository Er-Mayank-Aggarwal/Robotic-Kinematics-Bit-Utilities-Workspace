#include <stdio.h>

int count_zeros(unsigned char byte)
{
    int ones = 0;
    while(byte)
    {
        ones += (byte & 1);
        byte >>= 1;
    }
    return 8 - ones;
}

int main()
{
    unsigned char num;
    printf("Enter number (0-255): ");
    scanf("%hhu", &num);

    printf("Number of 0 bits: %d\n", count_zeros(num));
    return 0;
}
