#include <stdio.h>

unsigned int insert_bits(unsigned int N, unsigned int M, int i, int j)
{
    unsigned int mask = ((1 << (j - i + 1)) - 1) << i;
    N &= ~mask;
    N |= (M << i);
    return N;
}

int main()
{
    unsigned int N, M;
    int i, j;

    printf("Enter N, M, i, j: ");
    scanf("%u %u %d %d", &N, &M, &i, &j);

    printf("Result: %u\n", insert_bits(N, M, i, j));
    return 0;
}