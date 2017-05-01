/* common.cpp

*/
#include "common.h"
#include <iostream>
#include "midieven.h"

using namespace std;

/* =================================================================== */
/*                             MidiTime                                */
/* =================================================================== */

unsigned long MidiTime::Division = 192UL;
int MidiTime::DivisionFormat = MIDITIME_BEAT;

double MidiTime::Second(unsigned long tempo)
{
  double smpte_format, smpte_resolution;

  switch (DivisionFormat)
    {
    case MIDITIME_BEAT:
	return double(time) * double(tempo) / (double(Division) * 1000000.0);
	break;
    case MIDITIME_SMPTE:
     smpte_format = upperbyte(Division);
     smpte_resolution = lowerbyte(Division);
     return ( double(time) / (smpte_format * smpte_resolution * 1000000.0));
     break;
    default:
	return(0.0);
	break;
    }
}

// ostream& operator << (ostream& ost, const MidiTime &t)
// {
//   int wi = ost.width(3);  int fi = ost.fill('0');
//   ost <<  t.Measure()+1 << "-";
//   ost.width(2);
//   ost <<  t.Beat()+1 << ":";
//   ost <<  2*t.Fraction()/t.Division+1 ;
//   ost.width(wi);  ost.fill(fi);
//   return ost;
// };


ostream& operator << (ostream& ost, const MidiTime &t)
{
  int wi = ost.width(10);  int fi = ost.fill(' ');
  ost <<  t.time;
  ost.width(wi);  ost.fill(fi);
  return ost;
};



/* =================================================================== */
/*                             VarLen                                  */
/* =================================================================== */

VarLen::VarLen(const MidiTime& t) : data(t.time) {};


/* =================================================================== */
/*                             MessageBuffer                           */
/* =================================================================== */

MessageBuffer :: MessageBuffer(int MaxLen)
{
  BufferLength = 0;

  Buffer = new unsigned char [MaxLen];
  if (Buffer)
    {
      BufferLength = MaxLen;
      length = 0;
    }
}

MessageBuffer ::~MessageBuffer()  
{ 
  if (Buffer) delete [] Buffer; 
}

/* -------------------------------------------------------------------- */

MessageBuffer& MessageBuffer::operator << (unsigned char c)
{
  unsigned int i;
  if (!Buffer) return *this;
  
  if (length == BufferLength)
    {
      unsigned char *p = new unsigned char[BufferLength*2];
      unsigned char *q, *r;
      
      for (q = Buffer, r=p, i=0; i<BufferLength; i++) *r++=*q++;
      delete [] Buffer;
      Buffer = p;
      BufferLength*=2;
    }

  Buffer[length++] = c;
  return *this;
};

/* -------------------------------------------------------------------- */

void MessageBuffer::operator >> (Event* &ep)
{
  ep = NULL;
  if (length == 0 || Buffer==NULL)
    {
      cerr << "Bad Message Buffer...\n"<<" length=" << length << " buffer=" << (unsigned) Buffer[0] << endl;
      return;
    };

  switch (unsigned (Buffer[0]))
    {
    case NOTE_OFF:
      Buffer[0] = NOTE_ON;
      Buffer[3] = 0;
      ep = new Note(*this);
      break;
    case NOTE_ON:
      ep = new Note(*this);
      break;
    case POLY_AFTERTOUCH:
      ep = new PolyAfterTouch(*this);
      break;
    case CONTROL_CHANGE:
      ep = new Parameter(*this);
      break;
    case PITCH_BEND:
      ep = new PitchBend(*this);
      break;
    case PROGRAM_CHANGE:
      ep = new Program(*this);
      break;
    case CHANNEL_AFTERTOUCH:
      ep = new ChannelAfterTouch(*this);
      break;
    case SYSTEM_EXCLUSIVE:
      ep = new SysEx(*this);
      break;
    case META_EVENT:

      switch  (unsigned (Buffer[1]))
	{
	case SEQUENCE_NUMBER:
	  //      this->Mf_seqnum(to16bit(m[0],m[1]));
	  break;
	case TEXT_EVENT:  
	case COPYRIGHT_NOTICE:  
	case SEQUENCE_NAME:  
	case INSTRUMENT_NAME:  
	case LYRIC:  
	case MARKER:
	case CUE_POINT:
	case 0x08:
	case 0x09:
	case 0x0a:
	case 0x0b:
	case 0x0c:
	case 0x0d:
	case 0x0e:
	case 0x0f:
	  /* These are all text events */
	  ep = new Text(*this);
	  break;
	case END_OF_TRACK:  /* End of Track */
	  //      this->Mf_eot();
	  break;
	case TEMPO_CHANGE:  /* Set tempo */
	  ep = new TempoChange(*this);
	  break;
	case SMPTE_OFFSET:
	  ep = new Smpte(*this);
	  break;
	case TIME_SIGNATURE:
	  ep = new TimeSignature(*this);
	  break;
	case KEY_SIGNATURE:
	  ep = new KeySignature(*this);
	  break;
	case SEQUENCER_SPECIFIC:
	  break;
	case CHANNEL_PREFIX:
	  break;
	default:
	  break;
	}
      break;
    }
  return;
}

/* -------------------------------------------------------------------- */


















