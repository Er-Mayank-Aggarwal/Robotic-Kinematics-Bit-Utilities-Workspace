#include <stdio.h>

unsigned char get_bit(unsigned char num, int n){
    if (num & (1<<n)){
        return 0x01;
    }
    return 0x00;
}

void main(){
    unsigned char num;
    int n;
    printf("enter a number (0-255)");
    scanf("%hhu",&num);
    printf("enter n_th position (0-7)");
    scanf("%hhu",&n);
    printf("Bit sequence: ");
    showbits(num);

}