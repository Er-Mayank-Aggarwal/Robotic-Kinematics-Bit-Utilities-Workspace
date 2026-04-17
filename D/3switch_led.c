/************************************************************************************
         File:    switch_led.c
         Date:    March 23, 2015
	   Target:	  ATmega8
     Compiler:    avr-gcc (AVR Studio 5)
       Author:    Excel Technologies Pvt. Ltd.
 
 ************************************************************************************/

/******************************* Program Notes **************************************
	This program is used to show that a press at switch turns ON a LED connected 
	to PORTD pins. The four data lines are connected to LEDs as shown below:
				 -----------
				|  atmega8  |
				|           |
				|		 PD7|-----------------> LED1
				|		 PD6|-----------------> LED2
				|        PD5|-----------------> LED3
				|        PD4|-----------------> LED4
				|			|
				 -----------
	
	Following switches are used to make the corresponding LED to glow:
				Switch						LED
				  S1    PD2                     1
				  S2    PD3                  2
				  S3    PB3                  3
				  S4    PB2                  4
	
	Output on LED remains high as long as the switch is pressed.
*************************************************************************************/

#define F_CPU 1000000UL					//define CPU clock frequency as 1MHz.
#include <avr/io.h>						//this header file includes appropriate IO definitions for the device.
#include <util/delay.h>					//this header file includes busy-wait functions.
int main (void)
{
	DDRD  = 0b11110000;					//1 = output, 0 = input, set PD7 to PD4 as an output pin and, PD2 and PD3 as an input pin.
	PORTD = 0b11111100;					//enable PORTD pin 2 and pin 3 internal pullup.
	DDRB &= ~(1<<PB2);					//set PB2 as an output pin.
	DDRB &= ~(1<<PB3);					//set PB3 as an output pin.
	PORTB = 0b00001100;					//enable PORTB pin2 and pin3 internal pullup.
	while(1)							//infinite loop.
	{
		if (bit_is_clear(PIND, 2))		//check if switch S1 is pressed.
		{
			PORTD &= ~_BV(PD7);			//turn ON LED connected to PD7.
			for(int i=0;i<100;i++)		//give a delay of 1 second.
			_delay_ms(10);
			PORTD |= _BV(PD7);			//turn OFF LED connected to PD7.
		}
		else
		if(bit_is_clear(PIND, 3))		//check if switch S2 is pressed.
		{
			PORTD &= ~_BV(PD6);			//turn ON LED connected to PD6.
			for(int i=0;i<100;i++)		//give a delay of 1 second.
			_delay_ms(10);
			PORTD |= _BV(PD6);			//turn OFF LED connected to PD6.
		   
		}
		else
		if (bit_is_clear(PINB, 3))		//check if switch S3 is pressed.
		{
			PORTD &= ~_BV(PD5);			//turn ON LED connected to PD5.
			for(int i=0;i<100;i++)		//give a delay of 1 second.
			_delay_ms(10);
			PORTD |= _BV(PD5);			//turn OFF LED connected to PD5.
		}
		else
		if(bit_is_clear(PINB, 2))		//check if switch S4 is pressed.
		{
			PORTD &= ~_BV(PD4);			//turn ON LED connected to PD4.
			for(int i=0;i<100;i++)		//give a delay of 1 second.
			_delay_ms(10);
			PORTD |= _BV(PD4);			//turn OFF LED connected to PD4.
		}
	}
	return 0;
}		

