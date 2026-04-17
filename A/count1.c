#include <stdio.h>

int count_ones(unsigned char byte)
{
    int count = 0;
    while(byte)
    {
        count += (byte & 1);
        byte >>= 1;
    }
    return count;
}

int main()
{
    unsigned char num;
    printf("Enter number (0-255): ");
    scanf("%hhu", &num);

    printf("Number of 1 bits: %d\n", count_ones(num));
    return 0;
}