#include <stdio.h>

int find_size()
{
    unsigned int x = ~0;  // all bits = 1
    int count = 0;

    while (x)
    {
        count++;
        x >>= 1;
    }

    return count;
}

int main()
{
    printf("Size of unsigned int = %d bits\n", find_size());
    return 0;
}