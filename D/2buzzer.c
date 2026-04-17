/************************************************************************************
         File:    buzzer.c
         Date:    March 23, 2015
	   Target:	  ATmega8
     Compiler:    avr-gcc (AVR Studio 5)
       Author:    Excel Technologies Pvt. Ltd.
 ************************************************************************************/

/******************************* Program Notes **************************************
	This program is used to interface a buzzer to atmega8 microcontroller. Buzzer
	is connected to PORTB PB1 pin, it gets ON making a sound then after a delay 
	it gets OFF and this process runs continuously. 
*************************************************************************************/
	
#define F_CPU 1000000UL					//define CPU clock frequency as 1MHz.
#include <avr/io.h>						//this header file includes appropriate IO definitions for the device.
#include <util/delay.h>					//this header file includes busy-wait functions.
int main(void)
{
	int i;
	DDRB=0x02;							//set PB1 as an output pin.
    while(1)					
	{
		PORTB=0b00000010;				//turn ON buzzer connected to PB1.
		for(i=0;i<500;i++)				//give a delay of 5 seconds.
		_delay_ms(10);
		PORTB=0b00000000;				//turn OFF buzzer connected to PB1.
		for(i=0;i<500;i++)				//give a delay of 5 seconds.
		_delay_ms(10);
	}	
	return 0;
}