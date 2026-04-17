/******************************************************************************
         File:    ADC.c
         Date:    MARCH 04, 2015
       Target:    ATmega8
     Compiler:    avr-gcc (AVR Studio 5)
       Author:    Excel Technologies Pvt. Ltd.
*******************************************************************************/
/******************************* Program Notes ********************************
		This program is used to show that ADC converts analog input voltage
		to a 10-bit number of range 0-1023 through successive approximation. 
		ADC is multiplexed with PORTC giving 6 channels. PC2 (ADC2) is used
		as an analog input channel. ATmega8 reads 10k POT connected to PORTC, 
		by turning the POT, the resulting value (decimal) gets displays on LCD.
		
		The four data lines of PORTD as well as the two control lines may be
        implemented on any available I/O pin of any port. These are
        the connections used for this program:
 
                 -----------                   ----------
                |  atmega8  |                 |   LCD    |
                |           |                 |          |
                |        PD7|---------------->|D7        |
                |        PD6|---------------->|D6        |
                |        PD5|---------------->|D5        |
                |        PD4|---------------->|D4        |
                |           |                 |D3        |
                |           |                 |D2        |
10K POT ------->|PC2        |                 |D1        |
(Variable-      |           |                 |D0        |
 Resistance)    |           |                 |          |
                |        PB4|---------------->|E         |
                |           |         GND --->|RW        |
                |        PB5|---------------->|RS        |
                 -----------                   ----------
		
*****************************************************************************/

#define F_CPU 16000000UL						//define CPU clock frequency as 16MHz.
#include <avr/io.h>								//this header file includes appropriate IO definitions for the device.
#include <util/delay.h>							//this header file includes busy-wait functions.
#include <avr/interrupt.h>						//this header file defines interrupt handling routines.
#include <inttypes.h>							//this header file defines for different int data types.
#define lcd_D7_port     PORTD                   //LCD D7 connection
#define lcd_D7_bit      PORTD7
#define lcd_D7_ddr      DDRD

#define lcd_D6_port     PORTD                   //LCD D6 connection
#define lcd_D6_bit      PORTD6
#define lcd_D6_ddr      DDRD

#define lcd_D5_port     PORTD                   //LCD D5 connection
#define lcd_D5_bit      PORTD5
#define lcd_D5_ddr      DDRD

#define lcd_D4_port     PORTD                   //LCD D4 connection
#define lcd_D4_bit      PORTD4
#define lcd_D4_ddr      DDRD

#define lcd_E_port      PORTB                   //LCD Enable pin
#define lcd_E_bit       PORTB4
#define lcd_E_ddr       DDRB

#define lcd_RS_port     PORTB                   //LCD Register Select pin
#define lcd_RS_bit      PORTB5
#define lcd_RS_ddr      DDRB

// LCD module information
#define lcd_LineOne     0x00                    //start of line 1.
#define lcd_LineTwo     0x40					//start of line 2.       
// LCD instructions
#define lcd_Clear           0b00000001          //clear display.
#define lcd_Home            0b00000010          //return cursor to first position on first line.
#define lcd_EntryMode       0b00000110          //shift cursor from left to right on read/write.
#define lcd_DisplayOff      0b00001000          //turn display off.
#define lcd_DisplayOn       0b00001100          //display on, cursor off, don't blink character.
#define lcd_FunctionReset   0b00110000          //reset the LCD.
#define lcd_FunctionSet4bit 0b00101000          //4-bit data, 2-line display, 5 x 7 font.
#define lcd_SetCursor       0b10000000			//set cursor position.   
#define lcd_SetCursor1		0x81
#define lcd_SetCursor2		0x86

// Program ID
uint8_t program_firstline[]= "in decimal";

// Function Prototypes
void lcd_write_4(uint8_t);
void lcd_write_instruction_4d(uint8_t);
void lcd_write_character_4d(uint8_t);
void lcd_write_string_4d(uint8_t *);
void lcd_init_4d(void);

void initadc()  
 {  
      ADMUX=(1<<REFS0);		//for ARef=AVcc.	
	  //ADEN: set to turn ON ADC.									
      //Set ADCSRA Register with division factor 128.
	  ADCSRA=(1<<ADEN)|(1<<ADPS2)|(1<<ADPS1)|(1<<ADPS0);	  
 }  
 uint16_t readadc(uint8_t ch)  
 {  
      ch=ch&0b00000010;								//select ADC channel.  
      ADMUX|=ch;									 
      ADCSRA|=(1<<ADSC);							//start single conversion.  
      while(!(ADCSRA&(1<<ADSC)));					//wait for conversion to complete.  
      ADCSRA|=(1<<ADIF);							//clear ADIF by writing 1 to it.  
      return(ADC);
	  	 
 } 
int main(void)
{
	int adc_result, a1, a2, a3, a4,a5,a6;					//variables to hold ADC result.
    
	//configure the microprocessor pins for the data lines.
    
	lcd_D7_ddr |= (1<<lcd_D7_bit);                  //4 data lines - output.
    lcd_D6_ddr |= (1<<lcd_D6_bit);
    lcd_D5_ddr |= (1<<lcd_D5_bit);
    lcd_D4_ddr |= (1<<lcd_D4_bit);

	//configure the microprocessor pins for the control lines.
    
	lcd_E_ddr |= (1<<lcd_E_bit);                    //E line - output.
    lcd_RS_ddr |= (1<<lcd_RS_bit);                  //RS line - output.
	lcd_init_4d();                                  //initialize the LCD display for a 4-bit interface.
	lcd_write_instruction_4d(lcd_SetCursor2);		//set cursor.
	lcd_write_string_4d(program_firstline);			//display the first line of information.
	initadc();										//initialize ADC.
	_delay_ms(10);									//10mS delay.
	while(1)
	{
		lcd_write_instruction_4d(lcd_SetCursor);	//set cursor.
		adc_result=readadc(2);						//read value from channel 2.
		a1=(adc_result/1000)+48;					//converting into decimal value.
		a2=(adc_result%1000);
		a3=(a2/100)+48;
		a4=(a2%100);
		a5=(a4/10)+48;
		a6=(a4%10)+48;
		_delay_ms(10);								//10mS delay.	
		lcd_write_character_4d(a1);					//display a decimal digit.
		_delay_ms(1);								//1mS delay.
		lcd_write_character_4d(a3);					//display a decimal digit.
		_delay_ms(1);								//1mS delay.
		lcd_write_character_4d(a5);					//display a decimal digit.
		_delay_ms(1);								//1mS delay.
		lcd_write_character_4d(a6);					//display a decimal digit.
		_delay_ms(1);								//1mS delay.
				
	}
	while(1)
	return 0;
}
/*============================== 4-bit LCD Functions ======================*/
/*-------------------------------------------------------------------------
  Name:     lcd_init_4d
  Purpose:  initialize the LCD module for a 4-bit data interface.
  Entry:    equates (LCD instructions) set up for the desired operation.
  Notes:    uses time delays rather than checking the busy flag.
---------------------------------------------------------------------------*/
void lcd_init_4d(void)
{
	_delay_ms(100);											//100mS delay.                                 

/*IMPORTANT - At this point the LCD module is in the 8-bit mode and it is expecting to receive  
8 bits of data, one bit on each of its 8 data lines, each time the 'E' line is pulsed.
Since the LCD module is wired for the 4-bit mode, only the upper four data lines are connected 
and the lower four data lines are typically left open. Therefore, when the 'E' line is pulsed, 
the LCD controller will read whatever data has been set up on the upper 
four data lines and the lower four data lines will be high (due to internal pull-up circuitry).
Fortunately the 'FunctionReset' instruction does not care about what is on the lower four bits so  
this instruction can be sent on just the four available data lines and it will be interpreted 
properly by the LCD controller. The 'lcd_write_4' subroutine will accomplish this if the 
control lines have previously been configured properly.*/

// Set up the RS and E lines for the 'lcd_write_4' subroutine.
    lcd_RS_port &= ~(1<<lcd_RS_bit);						//select the Instruction Register(RS low).
    lcd_E_port &= ~(1<<lcd_E_bit);							//make sure E is initially low.

// Reset the LCD controller
    lcd_write_4(lcd_FunctionReset);							//first part of reset sequence.
    _delay_ms(10);											//10 mS delay.

    lcd_write_4(lcd_FunctionReset);							//second part of reset sequence.
    _delay_us(200);											//100uS delay.

    lcd_write_4(lcd_FunctionReset);							//third part of reset sequence.
    _delay_us(200);											//200uS delay.

/*Preliminary Function Set instruction - used only to set the 4-bit mode.
The number of lines or the font cannot be set at this time since the controller is still in the
8-bit mode, but the data transfer mode can be changed since this parameter is determined by one 
of the upper four bits of the instruction.*/
 
    lcd_write_4(lcd_FunctionSet4bit);						//set 4-bit mode.
    _delay_us(80);											//40uS delay.

    lcd_write_instruction_4d(lcd_FunctionSet4bit);			//set mode, lines, and font.
    _delay_us(80);											//40uS delay.

//The next three instructions are specified as part of the initialization routine.

//Display On/Off Control instruction
    lcd_write_instruction_4d(lcd_DisplayOff);				//turn display OFF.
    _delay_us(80);											//80uS delay.

//Clear Display instruction
    lcd_write_instruction_4d(lcd_Clear);					//clear display RAM.
    _delay_ms(4);											//4mS delay. 

//Entry Mode Set instruction
    lcd_write_instruction_4d(lcd_EntryMode);				//set desired shift characteristics.
    _delay_us(80);											//40uS delay. 

/*This is the end of the LCD controller initialization, but the display
has been left in the OFF condition. This is a good time to turn the display back ON*/
 
// Display On/Off Control instruction
    lcd_write_instruction_4d(lcd_DisplayOn);				//turn the display ON.
    _delay_us(80);											//80uS delay.
}
/*---------------------------------------------------------------------------
  Name:     lcd_write_string_4d
  Purpose:  display a string of characters on the LCD.
  Entry:    (theString) is the string to be displayed.
  Notes:    uses time delays rather than checking the busy flag.
----------------------------------------------------------------------------*/
void lcd_write_string_4d(uint8_t theString[])
{
    volatile int i = 0;										//character counter.
    while (theString[i] != 0)
    {
        lcd_write_character_4d(theString[i]);
        i++;
        _delay_us(80);										//80 uS delay.
    }
}
/*---------------------------------------------------------------------------
  Name:     lcd_write_character_4d
  Purpose:  send a byte of information to the LCD data register.
  Entry:    (theData) is the information to be sent to the data register.
  Notes:    does not deal with RW (busy flag is not implemented).
-----------------------------------------------------------------------------*/
void lcd_write_character_4d(uint8_t theData)
{
    lcd_RS_port |= (1<<lcd_RS_bit);							//select the Data Register (RS high).
    lcd_E_port &= ~(1<<lcd_E_bit);							//make sure E is initially low.
    lcd_write_4(theData);									//write the upper 4-bits of the data.
    lcd_write_4(theData << 4);								//write the lower 4-bits of the data.
}
/*----------------------------------------------------------------------------
  Name:     lcd_write_instruction_4d
  Purpose:  send a byte of information to the LCD instruction register.
  Entry:    (theInstruction) is the information to be sent to the instruction register.
  Notes:    does not deal with RW (busy flag is not implemented).
------------------------------------------------------------------------------*/
void lcd_write_instruction_4d(uint8_t theInstruction)
{
    lcd_RS_port &= ~(1<<lcd_RS_bit);						//select the Instruction Register (RS low).
    lcd_E_port &= ~(1<<lcd_E_bit);							//make sure E is initially low.
    lcd_write_4(theInstruction);							//write the upper 4-bits of the data.
    lcd_write_4(theInstruction << 4);						//write the lower 4-bits of the data.
}
/*----------------------------------------------------------------------------
  Name:     lcd_write_4
  Purpose:  send a byte of information to the LCD module.
  Entry:    (theByte) is the information to be sent to the desired LCD register.
            RS is configured for the desired LCD register.
            E is low.
            RW is low.
  Notes:    use either time delays or the busy flag.
------------------------------------------------------------------------------*/
void lcd_write_4(uint8_t theByte)
{
    lcd_D7_port &= ~(1<<lcd_D7_bit);						//assume that data is '0'.
    if (theByte & 1<<7) lcd_D7_port |= (1<<lcd_D7_bit);     //make data = '1' if necessary.

    lcd_D6_port &= ~(1<<lcd_D6_bit);                        //repeat for each data bit.
    if (theByte & 1<<6) lcd_D6_port |= (1<<lcd_D6_bit);

    lcd_D5_port &= ~(1<<lcd_D5_bit);
    if (theByte & 1<<5) lcd_D5_port |= (1<<lcd_D5_bit);

    lcd_D4_port &= ~(1<<lcd_D4_bit);
    if (theByte & 1<<4) lcd_D4_port |= (1<<lcd_D4_bit);
//write data
    lcd_E_port |= (1<<lcd_E_bit);							//Enable pin high.
    _delay_us(1);										
    lcd_E_port &= ~(1<<lcd_E_bit);							//Enable pin low.
    _delay_us(1);									
}
