#include "bit_utils.h"

void showbits(unsigned char byte)
{
    for(int bit_number = 7; bit_number >= 0; bit_number--)
    {
        if(byte & (1 << bit_number))
            printf("1");
        else
            printf("0");
    }
}

unsigned char get_bit(unsigned char num, unsigned char n)
{
    return (num & (0x01 << n)) ? 0x01 : 0x00;
}

unsigned char set_bit(unsigned char byte, unsigned char bit_no)
{
    return byte | (0x01 << bit_no);
}

unsigned char clear_bit(unsigned char byte , unsigned char bit_no)
{
    return byte & ~(0x01 << bit_no);
}

unsigned char toggle_bit(unsigned char byte, unsigned char bit_no)
{
    return byte ^ (0x01 << bit_no);
}

unsigned char count_ones(unsigned char byte)
{
    int count = 0;
    for(int i = 0; i < 8; i++)
    {
        if(byte & (0x01 << i))
            count++;
    }
    return count;
}