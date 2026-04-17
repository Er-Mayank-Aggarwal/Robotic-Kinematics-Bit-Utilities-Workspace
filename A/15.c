#include <stdio.h>

int main()
{
    int n;
    printf("Enter number: ");
    scanf("%d", &n);

    if((n & (n - 1)) == 0)
        printf("Power of 2\n");
    else
        printf("Not power of 2\n");

    return 0;
}