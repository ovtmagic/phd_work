/*
 * m_ofstrm.h
 *
 * Declerations for midi_ofstream, an object which provides
 * MIDI stream output services.
 *
 * 30-Sep-1997 ATC Created
 * ATC = Ali Taylan Cemgil. cemgil@boun.edu.tr
 *
 */

#if !defined(__M_OFSTRM_H)
#define __M_OFSTRM_H

#include "common.h"
#include <iostream>
#include <fstream>

using namespace std;

/* =================================================================== */
/*                             midi_ofstream                           */
/* =================================================================== */

class midi_ofstream : public ofstream
{
  unsigned long Place_Marker;

  int Format;
  int nTracks;
  int Division;

  unsigned long BytesWritten;
  MidiTime LastTime;

  void put(unsigned char c)  { ofstream::write((const char *)&c, 1); BytesWritten++;};

  public:

  midi_ofstream(void)  { };
  midi_ofstream(char * fn)  {    open(fn);  };
 ~midi_ofstream()  { close(); };


  midi_ofstream& operator << (unsigned char c) {put(c); return *this;};
  midi_ofstream& operator << (unsigned long data);
  midi_ofstream& operator << (int data);
  midi_ofstream& operator << (VarLen v);
  midi_ofstream& operator << (MidiTime t);

  midi_ofstream& write_varlen(unsigned long value);
  void write(unsigned char* p, int n) {ofstream::write((const char *)p, n); BytesWritten+=n; };

  void close(void);
  void open(char * fn);

  void track_begin();
  void track_end();

  int division(int new_division);
  int format(int new_format);

};

#endif

























