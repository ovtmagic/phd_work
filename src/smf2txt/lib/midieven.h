/*
 * midievent.h
 * 
 * Interface Definition for Event Objects
 */

#if !defined(__MIDIEVEN_H)
#define __MIDIEVEN_H

//#include <stdio.h>
#include <stdlib.h>
#include "mididef.h"
#include "common.h"
#include "m_ofstrm.h"
#include "m_ifstrm.h"
#include <string>
#include <sstream>

using namespace std;


#define MIDI_EVENT		0x0

/* =================================================================== */
/*                             Event                                   */
/* =================================================================== */

class Event
{
  protected:

  public:
  Event *prev;
  Event *next;
  MidiTime Time;
  

  Event(MidiTime TimeP = MidiTime(0)) { Time = TimeP; next = prev = NULL; };

  virtual int Length() {return 0;};
  virtual int Type(void) = 0;
  virtual Event* Copy(void) = 0;

  virtual ostream& operator >> (ostream& ascii_out) = 0;
  virtual midi_ofstream& operator >> (midi_ofstream& midi_out) = 0;

//  friend midi_ofstream& operator << (midi_ofstream& midi_out, Event& e); 
//  friend midi_ofstream& operator << (midi_ofstream& midi_out, Event* e);
//  friend ostream& operator << (ostream& ascii_out, Event& e);
//  friend ostream& operator << (ostream& ascii_out, Event* ep);

// friend class Track;

};


/* =================================================================== */
/*                         MidiEvent                                   */
/* =================================================================== */

class MidiEvent : public Event
{
protected:
  void Write(midi_ofstream& midi_out);

public:
  ostream& operator >> (ostream& ascii_out) {return ascii_out;};
  midi_ofstream& operator >> (midi_ofstream& midi_out) {return midi_out;};

  unsigned char chan;
  unsigned char trk;
  double onsetS;  //onset time in seconds
  double durS;    // duration in seconds
  
  unsigned char getTrk(){return trk;};


  MidiEvent(unsigned char ch = 0);
  virtual int Type(void) {return MIDI_EVENT;};

};

/* =================================================================== */
/*                              Note                                   */
/* =================================================================== */

/**
The basic musical unit which keeps pitch, channel, velocity and duration information. Note that the MIDI protocol specification
defines seperate messages (Note Off or equivalently Note On with zero velocity) for implicit representation of duration information.
This is a reasonable choice for a transmission protocol but not very suitable to the way humans think. MidiSong++ does not
implement separate Noteoff events. Instead the duration is stored on an additional field ('Note::dur'). Since the vast amount of
events on a MIDI file are Note events and our notion of a note ultimately includes its duration, this choice makes both processing
and storage more efficient. 
 */
class Note : public MidiEvent
{
  public:
  static char *Key[];
  unsigned char pitch;
  unsigned char vol;
  unsigned long dur;

  Note(unsigned char ch=0, unsigned char pit=0, unsigned char vl=0, unsigned long dur=0);
  Note(unsigned char pit, unsigned long durp, unsigned char vl = 64 );
  Note(MessageBuffer& msg);
  Note(string format,string notes,int pDstart,int pDchan, int pDpitch, int pDvol, int pDdur,int pDtrk,int pResol, int pTempo);

  

  int Type() {return vol ? NOTE_ON : NOTE_OFF;}

  Event* Copy(void);

  /**
    Ascii Stream Output. 
   */
  ostream& operator >> (ostream& ascii_out);

  /**
    MIDI Stream Output. 
   */
  midi_ofstream& operator >> (midi_ofstream& midi_out);
  
  void Print(string pformato,ostringstream &pntuples);
  void Quantize(double prel);
};

/* =================================================================== */
/*                              Parameter                              */
/* =================================================================== */

/**
  Parameter Change.
 */
class Parameter : public MidiEvent
{
  public:
  unsigned char control;
  unsigned char value;

  Parameter(unsigned char ch=0, int cnt=0, int vl=0) : MidiEvent(ch), control(cnt), value(vl)  {};
  Parameter(MessageBuffer& msg): MidiEvent()
  {
    unsigned char *p = &msg;
    Time = msg.Time;

    chan = p[1];
    control = p[2];
    value = p[3];
  };

  int Type() {return CONTROL_CHANGE;}

  Event* Copy(void);

  /**
    Ascii Stream Output. 
   */
  ostream& operator >> (ostream& ascii_out);

  /**
    MIDI Stream Output. 
   */
  midi_ofstream& operator >> (midi_ofstream& midi_out);
};

/* =================================================================== */
/*                              Program                                */
/* =================================================================== */

/**
  Program Change.
 */
class Program : public MidiEvent
{
  public:
  unsigned char program;

  //Program(unsigned char ch=0, int prog=0) : MidiEvent(ch), program(prog)  {};
  Program(unsigned char ch=0, int prog=0) : MidiEvent(ch), program(prog)  {};
  Program(MessageBuffer& msg) : MidiEvent()
  {
    unsigned char *p = &msg;
    Time = msg.Time;

    chan = p[1];
    program = p[2];
  };

  int Type() {return PROGRAM_CHANGE;}

  Event* Copy(void);

  /**
    Ascii Stream Output. 
   */
  ostream& operator >> (ostream& ascii_out);

  /**
    MIDI Stream Output. 
   */
  midi_ofstream& operator >> (midi_ofstream& midi_out);
  
  void Print(ostringstream &pProgram);
};


/* =================================================================== */
/*                              PolyAfterTouch                         */
/* =================================================================== */

/**
Polyphonic After Touch.
 */
class PolyAfterTouch : public MidiEvent
{
  public:
  unsigned char pitch;
  unsigned char press;

  PolyAfterTouch(unsigned char ch = 0, unsigned char pip = 0, int ps = 0) : MidiEvent(ch), pitch(pip), press(ps) {};
  PolyAfterTouch(MessageBuffer& msg) : MidiEvent()
  {
    unsigned char *p = &msg;
    Time = msg.Time;

    chan = p[1];

    pitch = p[2]; press = p[3];
  };

  int Type() {return POLY_AFTERTOUCH;}

  Event* Copy(void);

  /**
    Ascii Stream Output. 
   */
  ostream& operator >> (ostream& ascii_out);

  /**
    MIDI Stream Output. 
   */
  midi_ofstream& operator >> (midi_ofstream& midi_out);
};

/* =================================================================== */
/*                              ChannelAfterTouch                      */
/* =================================================================== */

/**
Channel After Touch
 */
class ChannelAfterTouch : public MidiEvent
{
  public:
  unsigned char press;

  ChannelAfterTouch(unsigned char ch=0, int pressp=0) : MidiEvent(ch), press(pressp) {};
  ChannelAfterTouch(MessageBuffer& msg);

  int Type() {return CHANNEL_AFTERTOUCH;}

  Event* Copy(void);

  /**
    Ascii Stream Output. 
   */
  ostream& operator >> (ostream& ascii_out);

  /**
    MIDI Stream Output. 
   */
  midi_ofstream& operator >> (midi_ofstream& midi_out);
};

/* =================================================================== */
/*                              PitchBend                              */
/* =================================================================== */

/**
Pitch Bend.
 */
class PitchBend : public MidiEvent
{
  public:
  unsigned char msb;
  unsigned char lsb;

  PitchBend(unsigned char ch=0, int msbp = 0, int lsbp = 0) : MidiEvent(ch), msb(msbp), lsb(lsbp) {};
  PitchBend(MessageBuffer& msg);

  int Type() {return PITCH_BEND;}

  Event* Copy(void);

  /**
    Ascii Stream Output. 
   */
  ostream& operator >> (ostream& ascii_out);

  /**
    MIDI Stream Output. 
   */
  midi_ofstream& operator >> (midi_ofstream& midi_out);
};

/* =================================================================== */
/*                              SysEx                                  */
/* =================================================================== */

/* Note:
     It would a better idea to put SysEx under MetaEvent, because
     the channel is not defined for SysEx Messages. However we do
     not so here to conform with the standard.
*/

/**
  System Exclusive Messages.

 */
class SysEx : public MidiEvent
{
  
public:
  int length;
  unsigned char *msg;
  
  SysEx(int len, unsigned char *data);
  SysEx(MessageBuffer& msg);

  ~SysEx();

  int Type() {return SYSTEM_EXCLUSIVE;}
  int Length() {return length;};
  void Set(int len, unsigned char *data);

  Event* Copy(void);

  /**
    Ascii Stream Output. 
   */
  ostream& operator >> (ostream& ascii_out);

  /**
    MIDI Stream Output. 
   */
  midi_ofstream& operator >> (midi_ofstream& midi_out);
};


/* =================================================================== */
/*                         MetaEvent                                   */
/* =================================================================== */

class MetaEvent : public Event
{
  protected:
  void Write(midi_ofstream& midi_out)
  {
	  midi_out << Time << (unsigned char)(META_EVENT) << (unsigned char)(Type()) << VarLen(Length());
  };

  public:

  MetaEvent(void) {};
  virtual int Type(void) {return META_EVENT;};

};


/* =================================================================== */
/*                         TimeSignature                               */
/* =================================================================== */

/**
 */
class TimeSignature : public MetaEvent
{
  public:
  unsigned char nn;    /* Numerator.*/
  unsigned char  denom; /* Denominator */
  unsigned char cc;    /* # of Midi Clocks in a Metronome Click */
  unsigned char bb;    /* the number of notated 32nd-notes in a MIDI quarter-note (24 MIDI Clocks) */

  TimeSignature( int nnp=4, int dd=2, int ccp=192*4, int bbp=8);
  TimeSignature(MessageBuffer& msg);

  int Type() {return TIME_SIGNATURE;};
  int Length() {return 4;};

  void Print(ostringstream &pTimeSig);

  Event* Copy(void);

  /**
    Ascii Stream Output. 
   */
  ostream& operator >> (ostream& ascii_out);

  /**
    MIDI Stream Output. 
   */
  midi_ofstream& operator >> (midi_ofstream& midi_out);
};

/* =================================================================== */
/*                         KeySignature                                */
/* =================================================================== */

/**
 */
class KeySignature : public MetaEvent
{
  public:
  static char *Key[];
  unsigned char sf; /*Sharp/Flat*/
  unsigned char mi;
  //int mi;

  KeySignature(int sfp = 0, int mip = 0) : MetaEvent(), sf((unsigned char)sfp), mi(mip) {};
  KeySignature(MessageBuffer& msg) : MetaEvent()
  {
    unsigned char *p = &msg;
    Time = msg.Time;

    sf = p[2];
    mi = p[3];
  };

  void Print(ostringstream &pKeySig);

  int Type() {return KEY_SIGNATURE;};
  int Length() {return 2;};

  Event* Copy(void);

  /**
    Ascii Stream Output. 
   */
  ostream& operator >> (ostream& ascii_out);

  /**
    MIDI Stream Output. 
   */
  midi_ofstream& operator >> (midi_ofstream& midi_out);
};

/* =================================================================== */
/*                         TempoChange                                 */
/* =================================================================== */

/**
Tempo Change mesured in microseconds per MIDI quarter-note. 
This is equivalent to 24ths of a microsecond per MIDI clock. 
Ideally, these events should only occur where MIDI clocks would be located. 
 */
class TempoChange : public MetaEvent
{

  public:
  unsigned long tempo; // in microseconds per MIDI quarter-note (=24 Midi Clocks)

  TempoChange(unsigned long ltempo = 500000L) : MetaEvent() {tempo = ltempo;};
  TempoChange(unsigned int metronome) : MetaEvent() {tempo = metronome2tempo(metronome);};
  TempoChange(MessageBuffer& msg) : MetaEvent()
  {
    unsigned char *p = &msg;
    Time = msg.Time;

    tempo = unsigned(p[2]);
    tempo = (tempo<<8) + unsigned(p[3]);
    tempo = (tempo<<8) + unsigned(p[4]);
  };

  void Print(ostringstream &pTempo);

  /**
    Converts metronome to Midi Tempo.

    Metronome is measured in quarter_note/min.
   */
  unsigned long metronome2tempo(unsigned int metronome) 
    {
      // 1 min = 60 x 1000 x 1000 microseconds.
      return (60UL*1000UL*1000UL)/metronome;
    }

  /**
    Converts MIDI Tempo to metronome.

    Midi Tempo is measured in microseconds/quarter_note.
   */
  double metronome() 
    {
      return double(60000000.0)/tempo;
    }


  int Type() {return TEMPO_CHANGE;};
  int Length() {return 3;};

  Event* Copy(void);

  /**
    Ascii Stream Output. 
   */
  ostream& operator >> (ostream& ascii_out);

  /**
    MIDI Stream Output. 
   */
  midi_ofstream& operator >> (midi_ofstream& midi_out);
};

/* =================================================================== */
/*                         Smpte                                       */
/* =================================================================== */

/**
 */
class Smpte : public MetaEvent
{
  public:
  int hr, mn, se, fr, ff;

  Smpte( int hrp = 0, int mnp = 0, int sep = 0, int frp = 0, int ffp = 0) : MetaEvent()
  {
    hr = hrp;    mn = mnp;
    se = sep;    fr = frp;    ff = ffp;
  };
  Smpte(MessageBuffer& msg) : MetaEvent()
  {
    unsigned char *p = &msg;
    Time = msg.Time;

    hr = p[2]; mn = p[3];
    se = p[4]; fr = p[5]; ff = p[6];
  };

  int Type() {return SMPTE_OFFSET;};
  int Length() {return 5;};

  Event* Copy(void);

  /**
    Ascii Stream Output. 
   */
  ostream& operator >> (ostream& ascii_out);

  /**
    MIDI Stream Output. 
   */
  midi_ofstream& operator >> (midi_ofstream& midi_out);
};

/* =================================================================== */
/*                             Text                                    */
/* =================================================================== */

/**
 */
class Text : public MetaEvent
{
  public:
  unsigned int type;
  int length;
  char* str;

  Text(int typep, int len,char *mess);
  Text(MessageBuffer& msg);

 ~Text();

  int Type() {return TEXT_EVENT ;};
  int Length() {return length;};
  void Set(int len,char *mess);

  Event* Copy(void);
  void Print(ostringstream &pText);

  
  /**
    Ascii Stream Output. 
   */
  ostream& operator >> (ostream& ascii_out);

  /**
    MIDI Stream Output. 
   */
  midi_ofstream& operator >> (midi_ofstream& midi_out);
};



#endif
