/************************************************************************************
         File:    Running_Pattern_leds.c
         Date:    March 23, 2015
	   Target:	  ATmega8
    
     Compiler:    avr-gcc (AVR Studio 5)
       Author:    Excel Technologies Pvt. Ltd.
 
 ************************************************************************************/

/******************************* Program Notes **************************************
	This program is used to run a pattern on LEDs connected to PORTD pins.
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
	A pattern will run continuously on LEDs which is defined as:
				
				LED1 LED2 LED3 LED4
				 0    0    0    1
				 0    0    1    0
				 0    1    0    0
				 1    0    0    0
	
*************************************************************************************/

#define F_CPU 1000000UL			//define CPU clock frequency as 1MHz.
#include <avr/io.h>				//this header file includes appropriate IO definitions for the device.
#include <util/delay.h>			//this header file includes busy-wait functions.
int main(void)
{
   int i,j;
   DDRD=0xF0;					//set PD7, PD6, PD5, PD4 pins as an output pin.
   PORTD=0xEF;					//write data 0b11101111 on PORTD pins.
   while(1)
   {
		for(i=4;i>0;i--)
		{
			for(j=50;j>0;j--)	//give a delay of 5 seconds.
			_delay_ms(100);
			PORTD=PORTD<<1;		//shift PORTD bits to left by 1.
		}
		for(i=0;i<200;i++)		//give a delay of 2 seconds.
		_delay_ms(10);
		PORTD=0xEF;
   }	
   return 0;
}