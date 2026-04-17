#include <stdio.h>

int main()
{
    unsigned char byte;
    scanf("%hhu", &byte);

    int odd1=0, even1=0, odd0=0, even0=0;

    for(int i=0;i<8;i++)
    {
        if(i%2==0)
            (byte&(1<<i)) ? even1++ : even0++;
        else
            (byte&(1<<i)) ? odd1++ : odd0++;
    }

    printf("Even 1s=%d Even 0s=%d\n", even1, even0);
    printf("Odd 1s=%d Odd 0s=%d\n", odd1, odd0);

    return 0;
}