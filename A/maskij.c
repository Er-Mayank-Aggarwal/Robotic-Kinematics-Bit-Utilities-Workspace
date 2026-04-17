#include <stdio.h>

unsigned int create_mask(int i, int j)
{
    unsigned int mask = 0;
    for(int k = i; k <= j; k++)
        mask |= (1 << k);

    return mask;
}

void showbits(unsigned int num)
{
    for(int i = 31; i >= 0; i--)
        printf("%d", (num >> i) & 1);
}

int main()
{
    int i, j;
    printf("Enter i and j: ");
    scanf("%d %d", &i, &j);

    unsigned int mask = create_mask(i, j);

    printf("Mask: ");
    showbits(mask);

    return 0;
}