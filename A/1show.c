// Show bits of a number entered
#include <stdio.h>

void showbits(unsigned char byte)
{
    int bit_number;

    for(bit_number = 7; bit_number >= 0; bit_number--)
    {
        if(byte & (1 << bit_number))
            printf("1");
        else
            printf("0");
    }
}

unsigned char get_bit(unsigned char num, unsigned char n){
    if (num & (0x01<<n)){
        return 0x01;
    }
    return 0x00;
}

unsigned char set_bit(unsigned char byte, unsigned char bit_no){
    return byte|(0x01<<bit_no);
}


unsigned char clean_bit(unsigned char byte , unsigned char bit_no){
    return byte & ( ~(0x01 << bit_no));
}

unsigned char toggle_bit(unsigned char byte, unsigned char bit_no){
    return byte ^ (0x01 << bit_no);
}

unsigned char count_ones(unsigned char byte)
{
    int i =0, count =0;
    for (i;i<=7;i++){
        if (byte & (0x01 << i))
        count++;
    }
    return count;
}


int main(){
    unsigned char num;
    unsigned char n;
    printf("enter a number (0-255)");
    scanf("%hhu",&num);
    printf("Bit sequence: ");
    showbits(num);

    printf("enter n_th position (0-7)");
    scanf("%hhu",&n);

    return 0;
}