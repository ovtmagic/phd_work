/*
 * m_ofstrm.cpp
 *
 *
 * 23-Sep-1997 ATC Created
 * ATC = Ali Taylan Cemgil. cemgil@boun.edu.tr
 *
 */


#include "common.h"
#include <iostream>
#include <fstream>
#include "m_ofstrm.h"

using namespace std;

/* =================================================================== */
/*                             midi_ofstream                           */
/* =================================================================== */

/* These operators are used to make sure that the byte order of
 * the various data types remains constant between machines. This
 * helps make sure that the code will be portable from one system
 * to the next.  It is slightly dangerous that it assumes that longs
 * have at least 32 bits and ints have at least 16 bits, but this
 * has been true at least on PCs, UNIX machines, and Macintosh's.
 *
 */

midi_ofstream& midi_ofstream::operator << (unsigned long data)
{
  put((unsigned)((data >> 24) & 0xff));
  put((unsigned)((data >> 16) & 0xff));
  put((unsigned)((data >> 8) & 0xff));
  put((unsigned)(data & 0xff));
  return *this;
}

/* -------------------------------------------------------------------- */

midi_ofstream& midi_ofstream::operator << (int data)
{
  put((unsigned)((data & 0xff00) >> 8));
  put((unsigned)(data & 0xff));
  return *this;
};

/* -------------------------------------------------------------------- */

  //WriteVarLen
midi_ofstream& midi_ofstream::write_varlen(unsigned long value)
{
  unsigned long buffer;

  buffer = value & 0x7f;
  while((value >>= 7) > 0)
    {
      buffer <<= 8;
      buffer |= 0x80;
      buffer += (value & 0x7f);
    }
  while(1)
    {
      put((unsigned char)(buffer & 0xff));
      if(buffer & 0x80) buffer >>= 8;
      else return *this;
    }

};

/* -------------------------------------------------------------------- */

midi_ofstream& midi_ofstream::operator << (VarLen v)
{
    return write_varlen(v.data);
}

/* -------------------------------------------------------------------- */

midi_ofstream& midi_ofstream::operator << (MidiTime t)
{
  //   cout << t << endl;
  write_varlen(t.time - LastTime.time);
  LastTime = t;
  return *this;
}

/* -------------------------------------------------------------------- */

void midi_ofstream::open(char * fn)
{
#ifdef DOS
  ofstream::open(fn ,ios::binary | ios::out);
#else
  ofstream::open(fn , ios::out);
#endif
  if (!this) return;
  
  unsigned long ident,length;

  // Will update this information when closed
  Format = 1;
  nTracks = 0;
  Division = 0;
  
  ident = MThd;           /* Head chunk identifier                    */
  length = 6;             /* Chunk length                             */

  /* individual bytes of the header must be written separately
     to preserve byte order across cpu types :-( */
  *this << ident << length << Format << nTracks << Division; 
};

/* -------------------------------------------------------------------- */

void midi_ofstream::close(void)
{
  unsigned long ident,length;
  ident = MThd;           /* Head chunk identifier                    */
  length = 6;             /* Chunk length                             */
  
  if ((void *)this)
    {
      seekp(0, ios::beg);
      *this << ident << length << Format << nTracks << Division;
      ofstream::close();
    }
};

/* -------------------------------------------------------------------- */

void midi_ofstream::track_begin()
{

  /* Reset the time */
  LastTime = 0L;
  nTracks++;

  /* Remember where the length was written, because we don't
     know how long it will be until we've finished writing */
  Place_Marker = tellp(); 

#ifdef DEBUG
  cout << offset;
#endif


  /* Write the track chunk header */
  *this << (unsigned long)MTrk << BytesWritten;
  
  BytesWritten = 0L; /* the header's length doesn't count */

};

/* -------------------------------------------------------------------- */

void midi_ofstream::track_end()
{
  unsigned long offset, saveBytesWritten;


  /* mf_write End of track meta event */
  put(0);
  put(META_EVENT);
  put(END_OF_TRACK);
  
  put(0);
  
  /* It's impossible to know how long the track chunk will be beforehand,
     so the position of the track length data is kept so that it can
     be written after the chunk has been generated */
  offset = tellp();
  
  
  seekp(Place_Marker, ios::beg);
  
  saveBytesWritten = BytesWritten;

  /* Re-write the track chunk header with right length */
  *this << (unsigned long)MTrk << saveBytesWritten;

  seekp(offset,ios::beg);

};

/* -------------------------------------------------------------------- */

/**
  
 */
int midi_ofstream::division(int new_division)
{
    int old_division = Division;
    Division = new_division;
    return old_division;
};

/* -------------------------------------------------------------------- */

/**
  
 */
int midi_ofstream::format(int new_format)
{
    int old_format = Format;
    Format = new_format;
    return old_format;
};
