#ifndef BIT_UTILS_H
#define BIT_UTILS_H

#include <stdio.h>

void showbits(unsigned char byte);

unsigned char get_bit(unsigned char num, unsigned char n);
unsigned char set_bit(unsigned char byte, unsigned char bit_no);
unsigned char clear_bit(unsigned char byte, unsigned char bit_no);
unsigned char toggle_bit(unsigned char byte, unsigned char bit_no);
unsigned char count_ones(unsigned char byte);

#endif