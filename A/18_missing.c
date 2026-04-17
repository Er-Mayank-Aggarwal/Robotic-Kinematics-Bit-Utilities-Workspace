#include <stdio.h>

int main()
{
    int n;
    scanf("%d", &n);

    int arr[n];
    for(int i=0;i<n;i++)
        scanf("%d", &arr[i]);

    int xor_all=0, xor_arr=0;

    for(int i=0;i<=n;i++)
        xor_all ^= i;

    for(int i=0;i<n;i++)
        xor_arr ^= arr[i];

    printf("Missing number: %d\n", xor_all ^ xor_arr);

    return 0;
}