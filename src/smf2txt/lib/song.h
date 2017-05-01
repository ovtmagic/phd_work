/*
 * song.h
 * 
 * Definition of the Song Object
 */

#if !defined(__SONG_H)
#define __SONG_H

#include "mididef.h"
#include "midieven.h"
#include "m_ofstrm.h"
#include "m_ifstrm.h"
#include <string>
#include <sstream>
#include <vector>

using namespace std;


/* =================================================================== */
/*                             Sequence                                */
/* =================================================================== */

/**
  A doubly linked list of Events.
 */
class Sequence
{
  protected:
  Event *head, *tail;

  public:
  /**
    Constructor.

    Creates an empty sequence.
   */
  Sequence();

  /**
    Copy Constructor.

    Copies the Events in seq. Deletes Events in *this.
   */
  Sequence( Sequence &seq);

  /**
    Destructor.

    Deletes all Events in the Sequence.
   */
 ~Sequence();

  /**
    Copy.

    Copies the Events in seq. Deletes Events in *this.
   */
  Sequence* Copy(void);

  /**
    Appends Event e to the tail.

    @param	e	Event Pointer
    @return	void
   */
  void Attach(Event *e);

  /**
    Remove an Event from Head.

    @return	Event Pointer
   */
  Event* Detach();

  /**
    Deletes all Events in the Sequence.

    @return	void
   */
  void Delete_All();

  friend ostream& operator << (ostream& ascii_out, Sequence& e);
  friend class tune_ifstream;

};

/* =================================================================== */
/*                             Track                                   */
/* =================================================================== */

#define kCutPer 0.1	//cut percentage for note 
#define kMIN_DURATION 0.025	//deletes a note if the duration is lower than this


/**
  A Sequence with restricted access (the basic unit of a Song object)
 */
class Track : public Sequence
{
  protected:
  Event *current;

  public:

  Track();
//  Track( Track &);
  Track( Sequence &);
 ~Track();

  char* Name(void);

  Track* Copy();

  /** 
    Insert Event into correct location starting from head.
   */
  void Insert(Event *e);


	/**
	 Remove the given  Event 
	*/
	void Delete(Event *e);

  /**
    Seek Track Cursor.
    Seek starting from head (tail) if start = 0 (1)
    */
  void Seek(unsigned long seek_time = 0L, int start = 0);

  /**
    Advances the Event cursor and returns its new value. 
    
   */
  Event* NextEvent();

  /**
    Returns Number of Events in the track.
   */
  unsigned long GetEventCount(void);

  /**
	Returns a string with note events in the given format
   */
   int PrintNotes(char *pformat,ostringstream &pntuples, int optMetadata);

   
   /**
   	Returns a string with note events (of the channel) in the given format
   */
   void printByChannel(char *pformat,int pcchannel,ostringstream &pntuples);
   
   /**
    * Write metadata events in this track to the text stream
    */
   void PrintMetadata(ostringstream &pntuples);

   /**
   	Returns a string with time signature events
   */
   int PrintTimeSig(ostringstream &pTimeSig);   		
   
	
/**
   	Returns a string with key signature events
   */
   int PrintKeySig(ostringstream &pTKeySig, int onlyfirst);   		
   

	  
    /**
  	modification of the notes with pedal events
   */
  void pedal();
  
   /**
  	modification of the notes with tempo events
  */
 void tempo(vector<unsigned long> changeTick, vector<unsigned long> tempoValue,int Division);


    
   
/**
	polyphony reduction
			poption: 1-> highest note
				 2-> lowest note
				 3-> both
*/
void polyphonyRed(int poption);   

   /**
   	Delete the notes out of the rank
   */
      
   void rank(double pBegin,double pEnd,int inSeconds) ; 


void setNumber(unsigned int pnum);

  /**
    Returns Number of Events of specified type.
   */
  unsigned long GetEventCount(int EVENT_TYPE);

  friend midi_ofstream& operator << (midi_ofstream& midi_out, Track& e);
  friend ostream& operator << (ostream& ascii_out, Track& e);

};

midi_ifstream& operator >> (midi_ifstream& midi_in, Track& track);
midi_ifstream& operator >> (midi_ifstream& midi_in, Track* & pTrk);



/* =================================================================== */
/*                             InputQueue                             */
/* =================================================================== */

/**
  Object used to match NoteOn's with NoteOff's.

  The Midi specification does not specify the length of a note directly,
  but rather by two messages NoteOn and NoteOff (=NoteOn with velocity 0).
  MidiSong uses a separate field to store the duration. So for any NoteOn
  Message, actually two messages are read from the file. The Note's
  must be delayed until their duration can be calculated. 
  InputQueue is actually a FIFO queue which stores those delayed messages.
 */
class InputQueue : public Track
{
  public:

  /**
    True if queue is empty.

    @return	TRUE if the queue is empty, FALSE otherwise.
   */
  int operator ! () {return head == NULL;}

  /**
    Appends an Event to the end of the queue, if it is not a NoteOff event,
    else the corresponding Note Message is found and the duration is calculated.

    @return void
   */
  void Insert(Event *e);

  /**
    True if Next Event in the Queue can be passed to a track.

    @return TRUE if the head is not a Note Event or is a Note Event with its duration already calculated. FALSE if the queue is empty or duration is not calculated.
   */
  int OK();

};

/* =================================================================== */
/*                             Song                                    */
/* =================================================================== */

/**
  Data structure which keeps events and other relevant information 
  about a musical piece in an easly accesible form.
 */
class Song
{
  /// Pointer to array of Track Pointers
  Track** track; 

  /// Number of Tracks
  int nTracks;       
  int Format;
  int Division;
  int DivisionFormat;

  void NewTracks(int Tracksp);

  public:

  /**
    Copy Constructor.
    */
  Song ( Song &);

  /**
    Creates a new Song object and allocates empty tracks.

    @param	Tracksp		Number of Tracks to be allocated
    @see Track
  */
  Song ( int Tracksp = 0);

  /**
    Destructor.

    Destroys all tracks. 
   */
 ~Song();

  Song* Copy();

  /**
    Assignment Operator. Makes a copy of s. Deletes the tracks of *this.

   */
  Song& operator = ( Song& s); 

  /**
    Number of Tracks.

    */
  int ntracks() {return nTracks; };
  
  /**
  	changes the track number
  */
  void setNtracks(int pnt);
  

  /**
	Generates a string with all the note events in the given format
   */

  int printAllNotes(char *pformat,ostringstream &pntuples, int optMetadata);
  int printSelTracksNotes(char *pformat, int plist[],int psizeLista,ostringstream &pntuples, int optMetadata);
  void printTracksByChannel(char *pformat,int pchannel,ostringstream &pntuples);
  
  /**
  	modification of the notes with pedal events
  */
  void pedalEvents();
  
   /**
  	modification of the notes with tempo events
  */
  void tempoEvents();
  void printTempoEvents(ostringstream &pTempoSig);
  
	/**
	quantize all the song events
		*/
   void Quantize(double prel);

	/**
	polyphony reduction
			poption: 1-> highest note
					 2-> lowest	note
					 3-> both
		*/
   void polyphonyRed(int poption); 
   
   /**
   	Delete the notes out of the rank
   */
      
   void rank(double pBegin,double pEnd,int inSeconds) ; 

		   
   /**
   	puts the number of the track to the note events
   */
   void setTrkNumber();
   
   
   /**
   	joins the new notes in the fisrt track
   */
   void mergeTrack(Track *ptr);

   /**
		adds the given track to the song
   */
   void addTrack(int pTrkNumber,char *pTrkName);
   
   

  /**
	Generates a string with the note events by tracks in the given format
   */

//  string printNotesOfTracks(char *pformat);


   /**
    * Write metadata in the selected track to the stream
    * (track index begins at 0)
    */
   void printMetadata(int tridx, ostringstream& stream);

  /**
  	returns the time signature events data
  */
    int printTimeSignature(ostringstream &pTimeSig);
  

/**
  	returns the key signature events data
  */
    int printKeySignature(ostringstream &pKeySig, int onlyfirst);

	

  /** 
    Format of the Midifile.

    
    @return
    0      if the file contains a single multi-channel track.
    1      if the file contains one or more simultaneous tracks (or MIDI outputs) of a sequence.
    2      if the file contains one or more sequentially independent single-track patterns.  
    Note : for a format 1 file, the tempo map must be stored as the first track.

    */
  int format()     {return Format;};
  void setFormat(int pfor)     {Format=pfor;};

  /** 
    Division.

    Division of a quarter-note represented by
    the delta-times in the file.  (If division is negative, it represents
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

    @see midi_ifstream
   */
  int division()   
    {
      if (DivisionFormat == MIDITIME_BEAT) return Division;
      else return ((-upperbyte(Division))<<8) | lowerbyte(Division);
    };

	void setDivision(int pdiv)
	{
		Division=pdiv;
	}
    
    
  /**
    Saves Song object in a MIDI file.

    @param	midi_out	Midi Output Stream
    @param	song		Song Object
   */
  friend midi_ofstream& operator << (midi_ofstream& midi_out, Song& song);

  /**
    Writes information to an output stream.

    @param	ascii_out	An Output Stream
    @param	song		Song Object
    */
  friend ostream&       operator << (ostream& ascii_out, Song& song);

  /**
    Reads a Song object from a MIDI input stream.

    @param	midi_in		Midi Input Stream
    @param	song		Song Object
   */
  friend midi_ifstream& operator >> (midi_ifstream& midi_in, Song& song);

  /**
    Track Indexing Operator.
    
    @return pointer to the i'th Track. If index is out of range, returns pointer to Track 0.
    
    @param	i	Index of the Track
  */
  Track*& operator [] (int i);

};

midi_ifstream& operator >> (midi_ifstream& midi_in, Song* &song_ptr);

// Operator Prototypes
template <class T>
midi_ofstream& operator << (midi_ofstream& midi_out, T* tp)
{
   if (!tp) return midi_out;
   else midi_out << *tp;

   return midi_out;
};

//template <class T>
//ostream& operator << (ostream& ascii_out, T* tp)
//{
//   if (!tp) return ascii_out;
//   else ascii_out << *tp;
//
//   return ascii_out;
//};

/* template <class T> */
/* ostream_withassign& operator << (ostream_withassign& ascii_out, T* tp) */
/* { */
/*    if (!tp) return ascii_out; */
/*    else ascii_out << *tp; */

/*    return ascii_out; */
/* }; */



#endif






