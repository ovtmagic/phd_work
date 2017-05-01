/*
 * midieven.cpp
 *
 * Implementation of :
 *
 *   Event
 *
 *   MidiEvent
 *   MetaEvent
 *   CompositeEvent
 *
 *   Note
 *   Parameter
 *   Program
 *   PolyAfterTouch
 *   ChannelAfterTouch
 *   PitchBend
 *   SysEx
 *
 *   TimeSignature
 *   KeySignature
 *   TempoChange
 *   Smpte
 *   Text
 *
 *
 *  Chord
 */

/*
 * 23-Sep-1997 ATC Created
 * ATC = Ali Taylan Cemgil. cemgil@boun.edu.tr
 *
 */

#include <math.h>
#include "common.h"
#include "mididef.h"
#include "midieven.h"
#include <string>
#include <sstream>
using namespace std;


/* =================================================================== */
/*                             Event                                   */
/* =================================================================== */



/* =================================================================== */
/*                         MidiEvent                                   */
/* =================================================================== */

MidiEvent::MidiEvent(unsigned char ch) : Event()
{
  prev = NULL;
  next = NULL;
  chan = ch;
  trk=0;
  onsetS=0;
  durS=0;
};

/* -------------------------------------------------------------------- */

void MidiEvent::Write(midi_ofstream& midi_out)
{
  // Delta times are computed by the midi_out object
  midi_out << Time;
  
  /* all MIDI events start with the type in the first four bits,
     and the channel in the lower four bits */
  unsigned char c = Type()|chan;
	
  midi_out << c;
};

/* =================================================================== */
/*                              Note                                   */
/* =================================================================== */

Note::Note(unsigned char ch, unsigned char pit, unsigned char vl, unsigned long durp) :  MidiEvent(ch)
{
  pitch = pit; vol = vl; dur = durp;
};

Note::Note(unsigned char pit, unsigned long durp, unsigned char vl) :  MidiEvent(0)
{
  pitch = pit; vol = vl; dur = durp;
};

Note::Note(MessageBuffer& msg) : MidiEvent()
{
  // No comprueba el tipo de mensaje almacenado en msg
  unsigned char *p = &msg; // PIERRE apunta al Buffer del MessageBuffer
  Time = msg.Time; // Asignaci�n MidiTime
  chan = p[1];
  pitch = p[2];
  vol = p[3];
  dur = 0;
};

Note::Note(string pformat,string pnotes,int pDstart,int pDchan, int pDpitch, int pDvol, int pDdur,int pDtrk,int pResol, int pTempo) : MidiEvent()
{
  size_t pos=0,pos2=0,antPos;
  int cont=0,fin=0;
  int startC=0,chanC=0,pitchC=0,volC=0,durC=0,trkC=0;
  int datos[50];
  double datosD[50];
  string a;
  
//	 cout<< "pformat=" << pformat<< endl;
//	 cout << "Dentro creando nota" << endl;

  pos=pnotes.find(" ",pos);
  if(pos!=string::npos)	
  {	
	  a=pnotes.substr(0,pos);
  }else
	{
		a=pnotes;
		fin=1;
	}
  datos[cont]=atoi(a.c_str());
  datosD[cont]= strtod (a.c_str(),NULL);
 // cout<<"creando notas " << datos[cont] << endl;
  cont++;
  pos++;


  while(fin==0)
  {
	antPos=pos-1;
   	pos=pnotes.find(" ",pos);
//    int antPos=pos++;
//    pos=pformat.find(" ",pos);
	if(pos==string::npos)		
	{
		pos=pnotes.find("\n",antPos);		
//		cout<< "LLEGA A FINAL " << endl;
		fin=1;
	}
    a=pnotes.substr(antPos,pos-antPos);
	datos[cont]=atoi(a.c_str());
	datosD[cont]= strtod (a.c_str(),NULL);
   // cout<<"creando notas " << a.c_str() << " datos=" << datos[cont] << endl;
	cont++;
	pos++;
  }

//  cout<<"fin nota" << endl;
	int tamDatos=cont;
	
  pos=0;
  pos2=0;
  cont=0;
	//cout<< "AQUI pformat=" << pformat<< endl;
  int usedPos=1,usedPos2=1;
  double onsetS=-1.0;
  int changeDur=0;	
  while(pos<pformat.size() && pos2<pformat.size())
  {
	if(usedPos==1)
	{
		pos=pformat.find("%",pos);
		usedPos=0;	
	}
	if(usedPos2==1)
	{
		pos2=pformat.find("#",pos2);
		usedPos2=0;
	}

	if(pos==string::npos && pos2!=string::npos)
		pos=pformat.size()-1;
	else 	if(pos != string::npos && pos2==string::npos)
		pos2=pformat.size()-1;
	if((pos==pformat.size()-1) && (pos2==pformat.size()-1))
		break;

	//cout << "pos=" << pos << " pos2=" << pos2 << endl;    
	if(pos<=pos2)
	{
		usedPos=1;
		//cout << "cont=" << cont << " letra=" << pformat.at(pos+1) << endl;
		if(pos != string::npos)
		{

			if((pos+1)<pformat.size())
			switch((char) pformat.at(pos+1))
			{
				case 'p':
					pitch=datos[cont];
					if(datos[cont]>=128)
						cerr << "WARNING: " << "pitch out of range.  Value (" << datos[cont] << ") outside limits of 0 to 127" << "." <<endl;
					pitchC=1;
					break;
				case 'o':
					Time.time=datos[cont];
					if(changeDur)
					{
						dur=dur-Time.time;
					}
					startC=1;
					break;
				case 'd':
					dur=datos[cont];
					durC=1;
					break;
				case 'v':
					vol=datos[cont];
					// cout <<"vol=" << datos[cont]<<  " cont="<< cont << endl;
					if(datos[cont]>=128)
						cerr << "WARNING: " << "velocity out of range.  Value (" << datos[cont] << ") outside limits of 0 to 127" << "." <<endl;
					volC=1;
					break;
				case 'c':
					chan=datos[cont]-1;
					if(datos[cont]>16 && datos[cont]<1)
						cerr << "WARNING: " << "channel out of range.  Value (" << datos[cont] << ") outside limits of 1 to 16" << "." <<endl;

					chanC=1;
					break;
				case 't':   
					trk=datos[cont];
					trkC=1;
					break;	
				default :
					cerr<<"formato incorrecto"<<endl;
			}
			pos++;
			cont++;	
			if(cont> tamDatos)
				break;
	
	    }
	}
	else
	{
		usedPos2=1;
		if(pos2 != string::npos)
		{
			double sec2tick=(double) pResol*pTempo/60;
			//double pResol2=(double) pResol*2.0;
			//double pResol2=(double) pResol*108/60;
			if((pos2+1)<pformat.size())
			switch((char) pformat.at(pos2+1))
			{
				case 'p':   //pitch in HZ
				{
					double intfrec;
					double freq_ini= 440.0 ; 
					double pit=12.0*(log2(datosD[cont]/freq_ini))+69;
//					cout << "Pitch datos=" << datosD[cont] << " pit=" << pit << endl;
	        		double fracPit = modf ( pit , &intfrec);  
					if(fracPit<=0.5)
						fracPit=0;
					else
						fracPit=1;


					pitch=(int) floor(intfrec+fracPit);
					pitchC=1;
					break;
				}
				case 'o':		//onset in seconds
				{
					double intOnset;
					double onset=datosD[cont]*sec2tick;
					//double onset=datosD[cont]*pResol2;
	        		double fractOnset = modf ( onset , &intOnset);  
					if(fractOnset<=0.5)
						fractOnset=0;
					else
						fractOnset=1;
					Time.time=(int) floor(intOnset+fractOnset);
					onsetS=intOnset+fractOnset;
					if(changeDur)
					{
						dur=dur-Time.time;
					}
					
					//Time.time= datosD[cont]*pResol2;
					//cout << "On datos=" << datosD[cont] << " pResol2=" << pResol2 << " Onset=" << Time.time << endl;
					startC=1;
					break;
				}
				case 'd':		//duration in seconds
				{
					double intDur;
					double durAux=datosD[cont]*sec2tick;
					//double durAux=datosD[cont]*pResol2;
	        		double fractDur = modf ( durAux , &intDur);  
					if(fractDur<=0.5)
						fractDur=0;
					else
						fractDur=1;
					dur=(int) floor(intDur+fractDur);
					//cout << "Dur datos=" << datosD[cont] << " pResol2=" << pResol2 << " dur=" << dur<< endl;
					durC=1;
					break;
				}
				case 'e':		//end time in seconds
				{
					double intEnd;
					double endAux=datosD[cont]*sec2tick;
					//double endAux=datosD[cont]*pResol2;
	        		double fractEnd = modf ( endAux , &intEnd);  
					if(fractEnd<=0.5)
						fractEnd=0;
					else
						fractEnd=1;
					if(onsetS>=0)
					{
						dur=(int) floor(intEnd+fractEnd-onsetS);
						changeDur=0;
					}
					else
					{
						changeDur=1;   // change dur when onset changes
						dur=(int) floor(intEnd+fractEnd);
					}
//					cout << "Dur datos=" << datosD[cont] << " pResol2=" << pResol2 << " dur=" << dur<< endl;
					durC=1;
					break;
				}
			}
			pos2++;
			cont++;
			if(cont> tamDatos)
				break;

		}	
		

	}
  }
/*
  	pos=0;
    cont=0;
//	cout << "AQUI" << endl;
	double pResol2=(double) pResol*2.0;
	while(pos<pformat.size())
	{
		pos=pformat.find("#",pos);
		if(pos != string::npos)
		{
			if((pos+1)<pformat.size())
			switch((char) pformat.at(pos+1))
			{
				case 'p':   //pitch in HZ
				{
					double intfrec;
					double freq_ini= 440.0 ; 
					double pit=12.0*(log2(datosD[cont]/freq_ini))+69;
//					cout << "Pitch datos=" << datosD[cont] << " pit=" << pit << endl;
	        		double fracPit = modf ( pit , &intfrec);  
					if(fracPit<=0.5)
						fracPit=0;
					else
						fracPit=1;


					pitch=(int) floor(intfrec+fracPit);
					pitchC=1;
					break;
				}
				case 'o':		//onset in seconds
				{
					double intOnset;
					double onset=datosD[cont]*pResol2;
	        		double fractOnset = modf ( onset , &intOnset);  
					if(fractOnset<=0.5)
						fractOnset=0;
					else
						fractOnset=1;
					Time.time=(int) floor(intOnset+fractOnset);
					//Time.time= datosD[cont]*pResol2;
//					cout << "On datos=" << datosD[cont] << " pResol2=" << pResol2 << " Onset=" << Time.time << endl;
					startC=1;
					break;
				}
				case 'd':		//duration in seconds
				{
					double intDur;
					double durAux=datosD[cont]*pResol2;
	        		double fractDur = modf ( durAux , &intDur);  
					if(fractDur<=0.5)
						fractDur=0;
					else
						fractDur=1;
					dur=(int) floor(intDur+fractDur);
//					cout << "Dur datos=" << datosD[cont] << " pResol2=" << pResol2 << " dur=" << dur<< endl;
					durC=1;
					break;
				}
			}
			pos++;
			cont++;
			if(cont> tamDatos)
				break;

		}
	}
 
*/
 // cout << "nueva nota" << endl;	


//default values
	if(!startC)
	  Time.time = pDstart; 
	if(!chanC)
	  chan = pDchan;
	if(!pitchC)
	  pitch = pDpitch;
	if(!volC)
	  vol = pDvol;
	if(!durC)
	  dur = pDdur;
	if(!trkC)
	  trk = pDtrk;
	
};



Event* Note::Copy(void)
{
  Note* p = new Note;

  *p = *this;
  p-> next = p->prev = NULL;
  return (Event *)p;
};

void Note::Print(string pformat,ostringstream &pntuples)
{
	size_t pos=0;
	int valor=0;
	double valor2=0.0;

	//se recorre toda la cadena de formato en busca de % ..
	//y se cambian por el dato que se quiere.
	while(pos<pformat.size())
	{
		pos=pformat.find("%",pos);
		if(pos != string::npos)
		{
			if((pos+1)<pformat.size())
			switch((char) pformat.at(pos+1))
			{
				case 'p':
					valor=pitch;
					break;
				case 'o':
					valor=Time.time;
					break;
				case 'd':
					valor=dur;
					break;
				case 'v':
					valor=vol;
					break;
				case 'c':
					valor=chan+1;
					break;
				case 'e':   //end time
					valor=(Time.time)+dur;
					break;
				case 't':   //end time
					valor=trk;
					break;	
				default :
					cerr<<"formato incorrecto"<<endl;

			}
			char data[99];
			sprintf(data,"%i",valor);
			string  dato=data;
			pformat.replace(pos,2,dato,0,dato.size());
			pos++;
		}
	}
	//se mira si aparecen $* para poner en segundos los tiempos
	pos=0;
	while(pos<pformat.size())
	{
		pos=pformat.find("#",pos);
		if(pos != string::npos)
		{
			if((pos+1)<pformat.size())
			switch((char) pformat.at(pos+1))
			{
				case 'p':   //pitch in HZ
				{
					double freq_ini= 8.1757989156 ; 
					double p=pow(2,pitch/12.0);
					valor2=freq_ini*p;
					break;
				}
				case 'o':		//onset in seconds
					valor2=onsetS;
					break;
				case 'd':		//duration in seconds
					valor2=durS;
					break;
				case 'e':		//end time in seconds
					valor2=onsetS+durS;
					break;
								

			}
			char data[99];
			sprintf(data,"%f",valor2);
			string  dato=data;
			pformat.replace(pos,2,dato,0,dato.size());
			pos++;
		}
	}
	
	pntuples<< pformat <<endl;
}


 void Note::Quantize(double prel)
 {
	double onset;
	double dura;
	int duraI;
	double fractOnset,intOnset;
	double fractDur,intDur;

	onset=(double) (Time.time)*prel;
        fractOnset = modf (onset , &intOnset);  //se obtiene la parte entera y fraccionaria de onset
	if(fractOnset<=0.5)
		fractOnset=0;
	else
		fractOnset=1;
	Time.time=(int) floor(intOnset+fractOnset);

	
	dura=(double) dur*prel;
        fractDur = modf(dura , &intDur);  //se obtiene la parte entera y fraccionaria de duration
	if(fractDur<=0.5)
		fractDur=0;
	else
		fractDur=1;
	duraI=(int) floor(intDur+fractDur);
	dur=(unsigned long) duraI;  
	
	if(dur==0) dur=1;
 }

/* -------------------------------------------------------------------- */
/* -------------------------------------------------------------------- */
char* Note::Key[12]={(char*)" C",(char*)"Db",(char*)" D",(char*)"Eb",(char*)" E",(char*)" F",(char*)"F#",(char*)" G",(char*)"Ab",(char*)" A",(char*)"Bb",(char*)" B"};

ostream& Note::operator >> (ostream& ascii_out)
{
  // Key
  //   ascii_out << e.Time << "  ";
  ascii_out << Time.time << "  ";
  
  char fill_char = ascii_out.fill('0'); ascii_out.width(2);
  ascii_out << int(chan) << "  " << Key[pitch%12] << int(pitch)/12 <<"  "<< int(vol) <<"  "<< dur << endl;

  ascii_out.fill(fill_char);

  return ascii_out;
};

midi_ofstream& Note::operator >> (midi_ofstream& midi_out)
{
  Write(midi_out);
  midi_out << pitch << vol;
  return midi_out; 
};


/* =================================================================== */
/*                              Parameter                              */
/* =================================================================== */
ostream& Parameter::operator >> (ostream& ascii_out)
{
  ascii_out << Time <<" Parameter "<< int(chan) <<" "<< int(control) <<" "<< int(value) << endl;
  return ascii_out;
};

midi_ofstream& Parameter::operator >> (midi_ofstream& midi_out)
{
  Write(midi_out);
  midi_out << control << value;
  return midi_out; 
};


Event* Parameter::Copy(void)
{
  Parameter* p = new Parameter;

  *p = *this;
  p-> next = p->prev = NULL;
  return (Event *)p;
};



/* =================================================================== */
/*                              Program                                */
/* =================================================================== */

Event* Program::Copy(void)
{
  Program* p = new Program;

  *p = *this;
  p-> next = p->prev = NULL;
  return (Event *)p;
};

/* -------------------------------------------------------------------- */
/* -------------------------------------------------------------------- */
ostream& Program::operator >> (ostream& ascii_out)
{
  ascii_out << Time <<" Program "<< int(chan)+1 <<" "<< int(program)+1 << endl;
  return ascii_out;
};

midi_ofstream& Program::operator >> (midi_ofstream& midi_out)
{	
  Write(midi_out);
  midi_out << program;
  return midi_out; 
};

void Program :: Print(ostringstream &pProgram)
{
	//se incrementan el canal y el programa en 1 unidad
	//ya que estan codificados desde 0
	pProgram << "@Program " <<  Time.time << " " << (int)chan+1<< " " << (int)program+1<< endl;
};
/* =================================================================== */
/*                              PolyAfterTouch                         */
/* =================================================================== */

Event* PolyAfterTouch::Copy(void)
{
  PolyAfterTouch* p = new PolyAfterTouch;

  *p = *this;
  p-> next = p->prev = NULL;
  return (Event *)p;
};

/* -------------------------------------------------------------------- */


/* -------------------------------------------------------------------- */

ostream& PolyAfterTouch::operator >> (ostream& ascii_out)
{
  ascii_out << Time <<" PolyAfterTouch "<< int(chan) <<" "<< int(pitch) <<" " << int(press) << endl;
  return ascii_out;
};

midi_ofstream& PolyAfterTouch::operator >> (midi_ofstream& midi_out)
{
  Write(midi_out);
  midi_out << pitch << press;
  return midi_out; 
};


/* =================================================================== */
/*                              ChannelAfterTouch                      */
/* =================================================================== */
ChannelAfterTouch :: ChannelAfterTouch(MessageBuffer& msg) : MidiEvent()
{
  unsigned char *p = &msg;
  Time = msg.Time;
  
  chan = p[1];
  press = p[2];
};

/* -------------------------------------------------------------------- */

Event* ChannelAfterTouch::Copy(void)
{
  ChannelAfterTouch* p = new ChannelAfterTouch;

 *p = *this;
  p-> next = p->prev = NULL;
  return (Event *)p;
};

/* -------------------------------------------------------------------- */
ostream& ChannelAfterTouch::operator >> (ostream& ascii_out)
{
  ascii_out << Time <<" ChannelAfterTouch "<< int(chan) <<" "<< int(press) << endl;
  return ascii_out;
};
midi_ofstream& ChannelAfterTouch::operator >> (midi_ofstream& midi_out)
{
  Write(midi_out);
  midi_out <<  press;
  return midi_out; 
};



/* =================================================================== */
/*                              PitchBend                              */
/* =================================================================== */

PitchBend :: PitchBend(MessageBuffer& msg) : MidiEvent()
{
  unsigned char *p = &msg;
  Time = msg.Time;
  chan = p[1];
  msb = p[2];
  lsb = p[3];
};

Event* PitchBend::Copy(void)
{
  PitchBend* p = new PitchBend;

 *p = *this;
  p-> next = p->prev = NULL;
  return (Event *)p;
};

/* -------------------------------------------------------------------- */
/* -------------------------------------------------------------------- */
ostream& PitchBend::operator >> (ostream& ascii_out)
{
  ascii_out << Time << " PitchBend "<< int(chan) <<" "<< int(msb) << " " << int(lsb) <<endl;
  return ascii_out;
};
midi_ofstream& PitchBend::operator >> (midi_ofstream& midi_out)
{
  Write(midi_out);
  midi_out <<  msb << lsb;
  return midi_out; 
};


/* =================================================================== */
/*                              SysEx                                  */
/* =================================================================== */
SysEx::SysEx(int len, unsigned char *data) : MidiEvent(0)
{
  msg = NULL;
  Set(len, data);
  
};

SysEx :: SysEx(MessageBuffer& msgbuf) : MidiEvent()
{
  unsigned char *p = &msgbuf;
  Time = msgbuf.Time;
  msg = NULL;
  
  Set(msgbuf.Length()-1, p+1);
};

SysEx ::~SysEx()  { if (msg) delete [] msg;  };

/* -------------------------------------------------------------------- */

Event* SysEx::Copy(void)
{
  SysEx* p = new SysEx(Length(),msg);
  p->Time = Time;
  
  p-> next = p->prev = NULL;
  return (Event *)p;
};

/* -------------------------------------------------------------------- */

void SysEx::Set(int len, unsigned char *data)
{
  unsigned char *p, *q;

  if (msg) delete [] msg;
  
  msg = new unsigned char[len];
  if (msg)
    {
      length = len;
      p = msg; q = data;
      for (int i=0; i<length; i++) *p++ = *q++;
    }
  else
    {
      length = 0;
    };
  
};

/* -------------------------------------------------------------------- */
/* -------------------------------------------------------------------- */
ostream& SysEx::operator >> (ostream& ascii_out)
{
  ascii_out << Time << " SysEx " << Length() <<endl;
  return ascii_out;
};

midi_ofstream& SysEx::operator >> (midi_ofstream& midi_out)
{
  midi_out << Time << (unsigned char)(SYSTEM_EXCLUSIVE) << VarLen(Length());
  midi_out.write(msg, Length());
  //	midi_out <<  (unsigned char)(EOX);
  return midi_out; 
};



/* =================================================================== */
/*                         MetaEvent                                   */
/* =================================================================== */


/* =================================================================== */
/*                         TimeSignature                               */
/* =================================================================== */

TimeSignature :: TimeSignature( int nnp, int dd, int ccp, int bbp) : MetaEvent()
{
  denom = 1;
  while ( dd-- > 0 ) denom *= 2;
  // denom = 1<<dd;
  nn = nnp; cc = ccp; bb = bbp;
};

TimeSignature :: TimeSignature(MessageBuffer& msg) : MetaEvent()
{
  unsigned char *p = &msg;
  int dd;
  
  Time = msg.Time;
  
  denom = 1; dd = p[3]; 
  while ( dd-- > 0 ) denom *= 2;
  // denom = 1<<dd;
  nn = p[2]; cc = p[4]; bb = p[5];
  
};

void TimeSignature :: Print(ostringstream &pTimeSig)
{

	//pTimeSig<<"@TimeSignature "<<Time.time<<" "<<(int) nn<<" " << (int) denom <<endl;
	pTimeSig<<"@Meter "<<Time.time<<" "<< Length() << " " << (int) nn<<"/" << (int) denom <<endl;
}


/* -------------------------------------------------------------------- */

Event* TimeSignature::Copy(void)
{
  TimeSignature* p = new TimeSignature;

 *p = *this;
  p-> next = p->prev = NULL;
  return (Event *)p;
};

/* -------------------------------------------------------------------- */
/* -------------------------------------------------------------------- */
ostream& TimeSignature::operator >> (ostream& ascii_out)
{
  ascii_out << Time << " TimeSignature  : " << (unsigned int)nn << "/" << (unsigned  int)denom << endl;
  return ascii_out;
};
midi_ofstream& TimeSignature::operator >> (midi_ofstream& midi_out)
{
  int dd = 0, de = denom;
  
  while (de>1) { de>>=1; dd++; }
	
  Write(midi_out);
  midi_out << nn << (unsigned char)dd << cc << bb;
  return midi_out; 
};



/* =================================================================== */
/*                         KeySignature                                */
/* =================================================================== */

Event* KeySignature::Copy(void)
{
  KeySignature* p = new KeySignature;
  
 *p = *this;
 p-> next = p->prev = NULL;
 return (Event *)p;
};


/* -------------------------------------------------------------------- */

char * KeySignature::Key[]={(char*)"CbM",(char*)"GbM",(char*)"DbM",(char*)"AbM",(char*)"EbM",(char*)"BbM",(char*)"FM",(char*)"CM",(char*)"GM",(char*)"DM",(char*)"AM", (char*)"EM", (char*)"BM", (char*)"F#M",(char*)"C#M",
		(char*)"Abm",(char*)"Ebm",(char*)"Bbm",(char*)"Fm", (char*)"Cm", (char*)"Gm", (char*)"Dm",(char*)"Am",(char*)"Em",(char*)"Bm",(char*)"F#m",(char*)"C#m",(char*)"G#m",(char*)"D#m",(char*)"A#m"};

ostream& KeySignature::operator >> (ostream& ascii_out)
{
  //ascii_out << Time << " Key Signature  \t : " << Key[sf+7] << (mi ? " minor":" major") << endl;
  
  if(mi)
  {
  	ascii_out << Time << " Key Signature  \t : " << Key[sf+7+15] << endl;
  }
  else
  {
  	ascii_out << Time << " Key Signature  \t : " << Key[sf+7] << endl;
  }	
  
  return ascii_out;
};

midi_ofstream& KeySignature::operator >> (midi_ofstream& midi_out)
{
  Write(midi_out);
  midi_out << sf << mi;
  return midi_out; 
};

void KeySignature :: Print(ostringstream &pKeySig)
{
	int sfAux ; //sf is negative number but stored unsigned
	
	
	//cerr << "sf: " << (int)sf << endl;
	//cerr << "mi: " << (int)mi << endl;
	
	
	if((int)sf > 7 )
		sfAux=sf-256;
	else
		sfAux=sf;

	//pKeySig<<"@KeySignature "<< mi << endl;

	
	pKeySig << "@KeySignature ";
	pKeySig << Time.time << " ";
	pKeySig << Length() << " " ;

	if((int)mi)
	{
		pKeySig<< (char*) Key[sfAux+7+15];
	}
	else
	{
		pKeySig<< (char*) Key[sfAux+7];
	}

	pKeySig << endl;
  
	//pKeySig<<"@KeySignature "<< (char*) Key[sfAux+7] <<" " << mi << (mi ? "minor":"major") <<endl;
	
}


/* =================================================================== */
/*                         TempoChange                                 */
/* =================================================================== */

Event* TempoChange::Copy(void)
{
  TempoChange* p = new TempoChange;

  *p = *this;
  p-> next = p->prev = NULL;
  return (Event *)p;
};



/* -------------------------------------------------------------------- */
ostream& TempoChange::operator >> (ostream& ascii_out)
{
  ascii_out << Time << " TempoChange = ";
  
  ascii_out.width(4);
  ascii_out <<Time.time<<" H " <<(unsigned long)rint(metronome()) << endl;
  
  return ascii_out;
};

midi_ofstream& TempoChange::operator >> (midi_ofstream& midi_out)
{

  unsigned char data[3];
  data[2] = (unsigned char)(tempo & 0xff);
  data[1] = (unsigned char)((tempo >> 8) & 0xff);
  data[0] = (unsigned char)((tempo >> 16) & 0xff);

  Write(midi_out);
  
  midi_out.write(&data[0], 3);
  return midi_out; 

};

void TempoChange :: Print(ostringstream &pTempoSig)
{
	pTempoSig << "@Tempo " <<  Time.time << " " << Length() << " " << 60000000.0/tempo << endl;
}

/* =================================================================== */
/*                         Smpte                                       */
/* =================================================================== */

Event* Smpte::Copy(void)
{
  Smpte* p = new Smpte;

 *p = *this;
  p-> next = p->prev = NULL;
  return (Event *)p;
};

ostream& Smpte::operator >> (ostream& ascii_out)
{
  ascii_out << Time << " Smpte " <<endl;
  return ascii_out;
};
midi_ofstream& Smpte::operator >> (midi_ofstream& midi_out)
{
  unsigned char data[5];
  data[0] = hr;    data[1] = mn;
  data[2] = se;    data[3] = fr;    data[4] = ff;
  
  Write(midi_out);
  
  midi_out.write(&data[0], 5);
  return midi_out; 
};


/* =================================================================== */
/*                             Text                                    */
/* =================================================================== */

Text :: Text(int typep, int len,char *mess) : MetaEvent()
{
  str = NULL;
  type = typep;
  Set(len, mess);
    
};

Text :: Text(MessageBuffer& msg) : MetaEvent()
{
    char *p = (char *)&msg;
    Time = msg.Time;
    type = p[1];
    Set(msg.Length()-2, p+2);
};

Text ::~Text()  {    if (str) delete [] str;  };

/* -------------------------------------------------------------------- */

Event* Text::Copy(void)
{
  Text* p = new Text(type, length, str );
  p->Time = Time; 
  
  p-> next = p->prev = NULL;
  return (Event *)p;
};

void Text::Print(ostringstream &pTempo)
{
		pTempo << "@Text " << Time.time << " " << length << " \"" << str << "\"" << endl;
}


/* -------------------------------------------------------------------- */

void Text::Set(int len,char *mess)
{
  char *p, *q;
  str = new char[len+1];
  if (str)
    {
      length = len;
      p = str; q = mess;
      for (int i=0; i<length; i++) *p++ = *q++;
      str[length] = '\0';
    }
  else
    {
      length = 0;
    };
};

/* -------------------------------------------------------------------- */
/* -------------------------------------------------------------------- */
ostream& Text::operator >> (ostream& ascii_out)
{
  ascii_out << Time << " Text : type = " << type << " " << str << endl;
  return ascii_out;
};
midi_ofstream& Text::operator >> (midi_ofstream& midi_out)
{
  midi_out << Time << (unsigned char)(META_EVENT) << (unsigned char)(type) << VarLen(Length());

  midi_out.write((unsigned char *)str, Length());
  return midi_out; 

};




