/*
 * m_ifstrm.h
 *
 * Declarations for midi_ifstream, an object which provides
 * MIDI stream input services.
 *
 * 03-Oct-1997 ATC Created
 * ATC = Ali Taylan Cemgil. cemgil@boun.edu.tr
 *
 */

#if !defined(__M_IFSTRM_H)
#define __M_IFSTRM_H

#include "common.h"
#include <iostream>
#include <fstream>
#include "midieven.h"

using namespace std;

/* =================================================================== */
/*                               midi_ifstream                         */
/* =================================================================== */

/**
  Provides MIDI stream input.
 */
class midi_ifstream : public ifstream
{

  unsigned int Format;
  unsigned int nTracks;
  unsigned int Division;

  unsigned long BytesRead;
  unsigned long ToBeRead;

  MidiTime CurrentTime;

  unsigned char get() 
    {
      /* unsigned */ char c; 
      ifstream::read(&c, 1); 
      BytesRead++; return c;
    };

  public:

  midi_ifstream(void)  { };
  midi_ifstream(char * fn)  {    open(fn);  };
 ~midi_ifstream()  { close(); };


  midi_ifstream& operator >> (unsigned char& c) {c = get(); return *this;};
  midi_ifstream& operator >> (unsigned long& data);
  midi_ifstream& operator >> (unsigned int& data);
  midi_ifstream& operator >> (VarLen& v);
  midi_ifstream& operator >> (MidiTime& t);
  midi_ifstream& operator >> (MessageBuffer& msg);

  int operator != (char * s);

  midi_ifstream& read_varlen(unsigned long& value);
  void read(unsigned char* p, int n) {ifstream::read((char *)p, n); BytesRead+=n; };

  void close(void);
  void open(char * fn);
  void putback(char c);
  int eot(void);

  void track_begin();

  /**
    Noop
   */
  void track_end();

  /** 
    Division of a quarter-note represented by
    the delta-times in the file..

    (If division is negative, it represents
    the division of a second represented by the delta-times in the file, so
    that the track can represent events occurring in actual time instead of
    metrical time.  It is represented in the following way:  the upper byte
    is one of the four values -24, -25, -29, or -30, corresponding to the
    four standard SMPTE and MIDI time code formats, and represents the
    number of frames per second.  The second byte (stored positive) is the
    resolution within a frame:  typical values may be 4 (MIDI time code
    resolution), 8, 10, 80 (bit resolution), or 100.  This system allows
    exact specification of time-code-based tracks, but also allows
    millisecond-based tracks by specifying 25 frames/sec and a resolution of
    40 units per frame.)   

    @see Song
   */
  int division();

  /** 
    Format of the Midifile.

    
    @return
    0      if the file contains a single multi-channel track.
    1      if the file contains one or more simultaneous tracks (or MIDI outputs) of a sequence.
    2      if the file contains one or more sequentially independent single-track patterns.  
    Note : for a format 1 file, the tempo map must be stored as the first track.

    */
  int format();

  /**
    Number of Tracks.

    */
  int ntracks() {return nTracks;};

};

#endif
