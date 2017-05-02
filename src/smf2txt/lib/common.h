/*
 * common.h
 *
 * Declaration of :
 *
 *  Varlen
 *  MidiTime
 *  MessageBuffer
 *
 */

/*
 * 23-Sep-1997 ATC Created
 * ATC = Ali Taylan Cemgil. cemgil@boun.edu.tr
 *
 */

#if !defined(__COMMON_H)
#define __COMMON_H

#include "mididef.h"
#include <iostream>
//#include "iomanip.h"

using namespace std;

// Forward Declarations
class MidiTime;
class Event;


/* =================================================================== */
/*                             VarLen                                  */
/* =================================================================== */

class VarLen
{
  public:
  unsigned long data;

  VarLen(unsigned long l=0) : data(l) {};
  VarLen(const MidiTime& t);

};


/* =================================================================== */
/*                             MidiTime                                */
/* =================================================================== */

#define MIDITIME_BEAT 1
#define MIDITIME_SMPTE 0

class MidiTime
{
  public:
  static int DivisionFormat;
  static unsigned long Division;
  unsigned long time;

  MidiTime(unsigned long tp = 0) : time(tp) {};
  MidiTime(const VarLen& v) : time(v.data) {};

  // PIERRE 20031021 : FALTA CONSTRUCTOR DE COPIA y oper. = (se usa p. ej. en Event::Event(MidiTime))
  MidiTime(const MidiTime& mt) : time(mt.time) {};
  MidiTime& operator = (const MidiTime& mt) { time = mt.time; return *this; }
  MidiTime& operator = (unsigned long t) { time = t; return *this; }

  MidiTime& operator ++ (void) {time++; return *this;};
  MidiTime& operator += (const MidiTime &mt) {time+=mt.time; return *this;};
  MidiTime& operator -= (const MidiTime &mt) {time-=mt.time; return *this;};
  MidiTime  operator -  (const MidiTime &mt)  { return MidiTime(time-mt.time);};
  MidiTime  operator +  (const MidiTime &mt)  { return MidiTime(time+mt.time);};

  int operator > (MidiTime &mt) {return time > mt.time; };
  int operator >=(MidiTime &mt) {return time >= mt.time; };
  int operator < (MidiTime &mt) {return time < mt.time; };
  int operator <=(MidiTime &mt) {return time <= mt.time; };

  unsigned long Measure() const { return time/Division/8;  };
  unsigned long Beat() const  { return (time - Measure()*Division*8)/Division/2;};
  unsigned long Fraction() const { return time - (Measure()*Division*8 + Beat()*Division*2);};

  /**
   * Converts delta times (in ticks) to seconds. 
   *
   * 
   * Note : the formula is different for tracks based on beats and tracks based on SMPTE times.
   *
   */
  double Second(unsigned long tempo = 500000L);

};


ostream& operator << (ostream& ost, const MidiTime &t);

/* =================================================================== */
/*                             MessageBuffer                           */
/* =================================================================== */

class MessageBuffer
{
  unsigned char *Buffer;
  unsigned int BufferLength;
  unsigned int length;

  public:
  MidiTime Time;

  MessageBuffer(int MaxLen = 80);
 ~MessageBuffer();

  MessageBuffer& operator << (unsigned char c);
  unsigned char* operator &  () {return Buffer;};
  void           operator >> (Event* &ep);

  unsigned int   Length() {return length;};
  void           Reset()  {length = 0;};
  void		 Print() { cout << Time; for (unsigned int i=0;i<length;i++) {cout  << " " << hex << int(Buffer[i]) << " ";} cout << endl; }

};



// Old stuff :   ------------------------------------------------

// extern long Mf_currtime;		/* current time in delta-time units */

inline unsigned long mf_sec2ticks(float secs, int division, unsigned int tempo)
{    
     return (long)(((secs * 1000.0) / 4.0 * division) / tempo);
}


#endif
