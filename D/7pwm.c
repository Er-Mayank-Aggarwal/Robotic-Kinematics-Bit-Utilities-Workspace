/************************************************************************************
         File:    bright.c
         Date:    March 04, 2015
	   Target:	  ATmega8
     Compiler:    avr-gcc (AVR Studio 5)
       Author:    Excel Technologies Pvt. Ltd.
 
 ************************************************************************************/

/******************************* Program Notes **************************************
	This program is used to produce a Pulse Width modulated output of varying width
	on PORTB pin PB1 and check the output at pin 15 i.e. on PB1.
*************************************************************************************/

#define F_CPU 16000000UL							//define CPU clock frequency as 16MHz.		
#include <avr/io.h>									//this header file includes appropriate IO definitions for the device.
#include <util/delay.h>								//this header file includes busy-wait functions.

void InitPWM()
{
   /*
   TCCR1A - Timer/Counter1 Control Register A.
   -----------------------------------------------------------------
   BITS DESCRIPTION
   NO:      NAME   DESCRIPTION
   -----------------------------------------------------------------
   BIT 7 : COM1A1  Compare Output Mode for channel A   [SET to 1].  
   BIT 6 : COM1A0  Compare Output Mode for channel A   [SET to 0].
   BIT 5 : COM1B1  Compare Output Mode for channel B   [SET to 0].
   BIT 4 : COM1B0  Compare Output Mode for channel B   [SET to 0].

   BIT 3 : FOC1A   Force output compare for channel A  [SET to 0].
   BIT 2 : FOC1B   Force output compare for channel B  [SET to 0].
   BIT 1 : WGM11  Wave form generation mode            [SET to 1].
   BIT 0 : WGM10  Wave form generation mode            [SET to 1].

   The above settings are for
   --------------------------
   Mode        = PWM Phase correct.
   PWM Output  = Non Inverted

   */
	TCCR1A|=(1<<WGM10)|(1<<WGM11)|(1<<COM1A1);
	TCCR1B|=(1<<CS11);								//set prescaler to 8.
	DDRB|=(1<<PB1);
}

/******************************************************************
Sets the duty cycle of output. 

Arguments
---------
duty: Between 0 - 255

0= 0%

255= 100%

The Function sets the duty cycle of pwm output generated.
The average voltage on this output pin will be

         duty
 Vout=  ------ x 5v
         255 

This can be used to control the width.
*********************************************************************/

void SetPWMOutput(uint8_t duty)
{
	OCR1A=duty;
}
void Wait()										//simple wait loop.
{
	_delay_loop_2(3200);
}
void main()
{
	uint8_t width=0;
	InitPWM();
	while(1)									//infinite loop.
	{
		for(width=0;width<255;width++)			//Now Loop with increasing width.
		{
			SetPWMOutput(width);				//Set the width using PWM.
			Wait();								//Wait for some time.
		}
		for(width=255;width>0;width--)			//Loop with decreasing width.
		{
			SetPWMOutput(width);				//Set the width using PWM.
			Wait();								//wait for some time.
		}
   }
}