/************************************************************************************
         File:    led_flashing.c
         Date:    September 16, 2015
	   Target:	  ATmega8
    
     Compiler:    avr-gcc (AVR Studio 5)
       Author:    Excel Technologies Pvt. Ltd.
 
 ************************************************************************************/

/******************************* Program Notes **************************************
	This program is used to flash the LEDs connected to PORTD pins.
	The four data lines are connected to LEDs as shown below:
				 -----------
				|  atmega8  |
				|           |
				|		 PD7|-----------------> LED1
				|		 PD6|-----------------> LED2
				|        PD5|-----------------> LED3
				|        PD4|-----------------> LED4
				|			|
				 -----------
	
	Output on LEDs is high and then after a delay of 2 seconds the output is low.
*************************************************************************************/

#define F_CPU 1000000UL			//define CPU clock frequency as 1MHz.
#include <avr/io.h>				//this header file includes appropriate IO definitions for the device.
#include <util/delay.h>			//this header file includes busy-wait functions.

int main(void)
{
    int i;
    DDRD=0xF0;					//set PD7, PD6, PD5, PD4 pins as an output pin.
	while(1)
    {	
		
		PORTD=0xFF;				//write data 0b11111111 on PORTD pins.
		for(i=20;i>0;i--)		//give a delay of 2 seconds.
		_delay_ms(100);		
		PORTD=0x00;				//write data 0b00000000 on PORTD pins.
		for(i=20;i>0;i--)		//give a delay of 2 seconds.
		_delay_ms(100);			
	}
	return 0;
}