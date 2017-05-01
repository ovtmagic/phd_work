/* mididef.h

   Standart Code Definitions

*/

/* definitions for MIDI file parsing code */

#if !defined(__MIDIDEF_H)
#define __MIDIDEF_H

/* MIDI status commands most significant bit is 1 */
#define NOTE_OFF         	0x80
#define NOTE_ON          	0x90
#define POLY_AFTERTOUCH  	0xA0
#define CONTROL_CHANGE    	0xB0
#define PROGRAM_CHANGE     	0xC0
#define CHANNEL_AFTERTOUCH      0xD0
#define PITCH_BEND      	0xE0
#define SYSTEM_EXCLUSIVE      	0xF0
#define EOX			0xF7
#define DELAY_PACKET	 	(1111)

/* 7 bit controllers */
#define DAMPER_PEDAL            0x40
#define PORTAMENTO	        0x41 	
#define SOSTENUTO	        0x42
#define SOFT_PEDAL	        0x43
#define GENERAL_4               0x44
#define HOLD_2		        0x45
#define GENERAL_5	        0x50
#define GENERAL_6	        0x51
#define GENERAL_7	        0x52
#define GENERAL_8	        0x53
#define TREMOLO_DEPTH	        0x5C
#define CHORUS_DEPTH	        0x5D
#define DETUNE		        0x5E
#define PHASER_DEPTH	        0x5F

/* parameter values */
#define DATA_INC	        0x60
#define DATA_DEC	        0x61

/* parameter selection */
#define NON_REG_LSB	        0x62
#define NON_REG_MSB	        0x63
#define REG_LSB		        0x64
#define REG_MSB		        0x65

/* Standard MIDI Files meta event definitions */
#define META_EVENT		0xFF
#define SEQUENCE_NUMBER 	0x00
#define TEXT_EVENT		0x01
#define COPYRIGHT_NOTICE 	0x02
#define SEQUENCE_NAME    	0x03
#define INSTRUMENT_NAME 	0x04
#define LYRIC	        	0x05
#define MARKER			0x06
#define CUE_POINT		0x07
#define CHANNEL_PREFIX		0x20
#define END_OF_TRACK		0x2F
#define TEMPO_CHANGE		0x51
#define SMPTE_OFFSET		0x54
#define TIME_SIGNATURE		0x58
#define KEY_SIGNATURE		0x59
#define SEQUENCER_SPECIFIC	0x74

/* Composite Event Definitions */
#define COMPOSITE_EVENT		0x01
#define CHORD_EVENT	        0x75

/* Manufacturer's ID number */
#define Seq_Circuits (0x01) /* Sequential Circuits Inc.*/
#define Big_Briar    (0x02) /* Big Briar Inc.          */
#define Octave       (0x03) /* Octave/Plateau          */
#define Moog         (0x04) /* Moog Music              */
#define Passport     (0x05) /* Passport Designs        */
#define Lexicon      (0x06) /* Lexicon 			*/
#define Tempi        (0x20) /* Bon Tempi               */
#define Siel         (0x21) /* S.I.E.L.                */
#define Kawai        (0x41) 
#define Roland       (0x42)
#define Korg         (0x42)
#define Yamaha       (0x43)

/* Midi Note (MN) codes and Octave Offsets */
#define MN_C(o) (0+12*o)
#define MN_Cs(o) (1+12*o)
#define MN_Db(o) (1+12*o)
#define MN_D(o) (2+12*o)
#define MN_Ds(o) (3+12*o)
#define MN_Eb(o) (3+12*o)
#define MN_E(o) (4+12*o)
#define MN_F(o) (5+12*o)
#define MN_Fs(o) (6+12*o)
#define MN_Gb(o) (6+12*o)
#define MN_G(o) (7+12*o)
#define MN_Gs(o) (8+12*o)
#define MN_Ab(o) (8+12*o)
#define MN_A(o) (9+12*o)
#define MN_As(o) (10+12*o)
#define MN_Bb(o) (10+12*o)
#define MN_B(o) (11+12*o)


/* miscellaneous definitions */
#define MThd 0x4d546864UL
#define MTrk 0x4d54726bUL
#define lowerbyte(x) ((unsigned char)(x & 0xff))
#define upperbyte(x) ((unsigned char)((x & 0xff00)>>8))




#endif
