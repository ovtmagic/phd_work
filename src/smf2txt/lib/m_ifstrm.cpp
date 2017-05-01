/*
 * m_ifstrm.cpp
 *
 *
 * 03-Oct-1997 ATC Created
 * ATC = Ali Taylan Cemgil. cemgil@boun.edu.tr
 *
 */


#include <iostream>
#include <fstream>
#include "common.h"
#include "m_ifstrm.h"
#include "midieven.h"

using namespace std;

/* =================================================================== */
/*                               midi_ifstream                         */
/* =================================================================== */


/* These operators are used to make sure that the byte order of
 * the various data types remains constant between machines. This
 * helps make sure that the code will be portable from one system
 * to the next.  It is slightly dangerous that it assumes that longs
 * have at least 32 bits and ints have at least 16 bits, but this
 * has been true at least on PCs, UNIX machines, and Macintosh's.
 *
 */

midi_ifstream& midi_ifstream::operator >> (unsigned long& data)
{
    unsigned char c;

    data = 0;
    for (int i=0; i<4; i++)
    {
      c = get();
      data = (data << 8) + c;
    };
    return *this;
}

/* -------------------------------------------------------------------- */

midi_ifstream& midi_ifstream::operator >> (unsigned int& data)
{
    unsigned char c;
    data = 0;
    for (int i=0; i<2; i++)
    {
      c = get();
      data = (data << 8) + c;
    };

    return *this;
};

/* -------------------------------------------------------------------- */

midi_ifstream& midi_ifstream::read_varlen(unsigned long& value)
{
  unsigned char c;

  c = get(); 
  value = c; 
  if ( c & 0x80 )
  {
    value &= 0x7f;
    do
    {
      c = get();
      value = (value << 7) + (c & 0x7f);

    } while (c & 0x80);
  }

  return *this;
}

/* -------------------------------------------------------------------- */

midi_ifstream& midi_ifstream::operator >> (VarLen& v)
{
    return read_varlen(v.data);
}

/* -------------------------------------------------------------------- */

midi_ifstream& midi_ifstream::operator >> (MidiTime& t)
{
  unsigned long temp; 
  read_varlen(temp);
  CurrentTime.time += temp;
  t = CurrentTime;
  return *this;
}

/* -------------------------------------------------------------------- */

int midi_ifstream::operator != (char * s)
{
  char *p=s, c;
  
  while (*p)
  {
        c = get();
        if (*p != c) return 1;
        p++;
  };

  return 0;
};

/* -------------------------------------------------------------------- */

void midi_ifstream::open(char * fn)
{

#ifdef DOS
    ifstream::open(fn ,ios::binary | ios::in);
#else
    ifstream::open(fn , ios::in);
#endif
    if (!this) return;

    
    if (*this != (char*)"MThd")
    {
      // Set <not a midi file> status bit
      return;
    };


    *this >> ToBeRead;
    BytesRead = 0L;

    *this >> Format;
    *this >> nTracks;
    *this >> Division;

      //cout << ToBeRead << " " << Format << " " << nTracks << " " << Division << endl;

  /* flush any extra stuff, in case the length of header is not 6 */
  while ( BytesRead < ToBeRead ) get();

  return;

};

/* -------------------------------------------------------------------- */

void midi_ifstream::close(void)
{
      ifstream::close();
};

void midi_ifstream::putback(char c)
{
  ifstream::putback(c);
  BytesRead--;
}
/* -------------------------------------------------------------------- */

int midi_ifstream::eot()
{
	return BytesRead >= ToBeRead;
};

/* -------------------------------------------------------------------- */

void midi_ifstream::track_begin()
{

  if ( *this != (char*)"MTrk" )
  {
    // Set <not at the beginning of a track> bit
    return;
  }

  *this >> ToBeRead;

  /* Reset the time */
  CurrentTime = 0L;
  BytesRead = 0L;

};

/* -------------------------------------------------------------------- */

void midi_ifstream::track_end()
{
  //  cout << "tr" << ToBeRead << " br" << BytesRead << endl;
};

/* -------------------------------------------------------------------- */

int midi_ifstream::division()
{
    return Division;
};

/* -------------------------------------------------------------------- */

int midi_ifstream::format()
{
    return Format;
};

/* -------------------------------------------------------------------- */


midi_ifstream& midi_ifstream::operator >> (MessageBuffer& msg)

  /* Reads in the next message in the midi_ifstream into a message buffer.

     The Bytes in the message buffer are organized as in the following :

     |---------------|----------------|----------------------
     | Midi Messages |  Meta          |  SysEx
-----|---------------|----------------|----------------------
m[0] | Message Type  |  META_EVENT    |  SYSTEM_EXCLUSIVE
-----|---------------|----------------|----------------------
m[1] | Channel       |  Message Type  |  Data
-----|---------------|----------------|----------------------
m[2] | Data 1        |  Data          |  ....
-----|---------------|----------------|----------------------
m[3] | Data 2        |  ....          |  ....
-----|---------------|----------------|----------------------
...
-----|---------------|----------------|----------------------
m[N] |    ???        |  Data          |  EOX
-----|---------------|----------------|----------------------

 */
{
  /* This array is indexed by the high half of a status byte.  It's */
  /* value is either the number of bytes needed (1 or 2) for a channel */
  /* message, or 0 (meaning it's not  a channel message). */
  static int chantype[] =
  {
    0, 0, 0, 0, 0, 0, 0, 0,    /* 0x00 through 0x70 */
    2, 2, 2, 2, 1, 1, 2, 0     /* 0x80 through 0xf0 */
  };

  int sysexcontinue = 0;  /* 1 if last message was an unfinished sysex */
  int running = 0;  /* 1 when running status used */

  // PIERRE 20031021: Creo que lo he pillado. 'status' debe ser static
  // Sino el bucle que lee el mensaje se salta los bytes de los mensajes con running status

  static unsigned int status = 0;    /* status value (e.g. 0x90==note-on) */

  static unsigned char last_message = 0;
  int needed = 0;

  unsigned char c, temp;
  unsigned char type;
  VarLen Size;
  unsigned long i;


  msg.Reset();
  *this >> msg.Time;
  //!  cout << msg.Time.time << " ";

  c = get();
  
  
  while (!eot())
  {  
    if ( sysexcontinue && c != EOX )
      {
       	putback(c);
	return *this;
      };

    if ( (c & 0x80) == 0 )
      {   /* running status? */
	if ( status == 0 )
	  {
	    //        mferror("unexpected running status");
	    // cout << "rs " ;
	  }
        running = 1;
      }
    else
      {
	status = c;
	running = 0;
      }
    
    needed = chantype[ (status>>4) & 0x0f ];
    
    if ( needed )
      {    /* ie. is it a channel message? */
	
	temp = running ? c : get();
	last_message = (unsigned char)((status) & 0xf0);
	msg <<  last_message; // Message Type
	msg << (unsigned char)(status & 0x0f);      // Channel
	msg << temp;
	if (needed>1) msg << get();
	return *this;
      }

    switch ( c )
      {
      case META_EVENT:  
	
	msg << char(META_EVENT);
	type = get();
	*this >> Size;
	msg << type;
	
	for (i=0; i < Size.data; i++) msg << get();
	
	return *this;
      
	break;

      case SYSTEM_EXCLUSIVE:    /* start of system exclusive */

	*this >> Size;
	msg << char(SYSTEM_EXCLUSIVE);
       
	for (i=0; i < Size.data; i++) msg << ( c = get());

	//      if ( c==EOX || Mf_nomerge==0 ) return *this;
	if ( c==EOX ) return *this;
	else sysexcontinue = 1;  /* merge into next msg */

	break;

      case EOX:  /* sysex continuation or arbitrary stuff */
	*this >> Size;
	
	for (i=0; i < Size.data; i++) msg << ( c = get());      
	if ( ! sysexcontinue )
	  {
	    // Arbitrary Stuff
	    return *this;
	  }
	else if ( c == EOX )
	  {
	    sysexcontinue = 0;
	    return *this;
	  }
	
	break;

      default:
	switch(last_message)
	  {
	    /*
	      Some Midi Files contain continious Control Change Messages.
	      There is not a seperate 0xB0 for each message. 
	      Maybe there are other such messages but I saw any.
	     */
	  case CONTROL_CHANGE:
	    putback(c);
	    c = last_message;
	    break;
	  default:
	    //      badbyte(c);
	    c = get();
	    break;
	  };
	break;
      }
  } // while(1)
  return *this;
};





