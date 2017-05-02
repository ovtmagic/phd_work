/*
 * song.cpp
 * 
 * Implements the Song Object
 */

#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include "mididef.h"
#include "midieven.h"
#include "song.h"
#include <sstream>
#include <vector>


using namespace std;

/* =================================================================== */
/*                             Sequence                                */
/* =================================================================== */

Sequence :: Sequence() {  head = tail = NULL; };
Sequence :: Sequence(Sequence &s2)
{
  Event *e = s2.head;
  Event *e2;

  head = tail = NULL;

  while (e != NULL)
  {
    e2 = e->Copy();
    Attach(e2);
    e = e->next;
  };
};

Sequence ::~Sequence() {  Delete_All(); };

Sequence* Sequence::Copy(void)
{
  Sequence *sp = new Sequence(*this);
  return sp;
};

/* -------------------------------------------------------------------- */

void Sequence::Attach(Event *e)
{
   if (head==NULL) tail = head = e;
   else
   {
      // Append to tail
      tail->next = e;
      e->prev = tail;
      e->next = NULL;
      tail = e;
   }; 
};

/* -------------------------------------------------------------------- */
  // Remove an Event from Head
Event* Sequence::Detach()
{
  Event* e = head;

  if (head)
  {
    head = head->next;
    if (head) head->prev = NULL;
    e->prev = e->next = NULL;
  };

  if (head==NULL) tail = NULL;

  return e;

};



/* -------------------------------------------------------------------- */

void Sequence::Delete_All(void)
{
  while (head) delete Detach();
};

/* -------------------------------------------------------------------- */
/* -------------------------------------------------------------------- */

ostream& operator << (ostream& ascii_out, Sequence& seq)
{
  for (Event *p = seq.head; p ; p=p->next ) *p >> ascii_out ;
  return ascii_out;
};


/* =================================================================== */
/*                             Track                                   */
/* =================================================================== */

Track :: Track() { current = NULL; };
Track :: Track( Sequence &seq)
{
  Sequence *sp = &seq;
  Sequence* sp2;

  sp2 = sp->Copy();

  head = ((Track *)sp2)->head;
  tail = ((Track *)sp2)->tail;

  current = NULL;

};

// Track :: Track(const Track &);

Track ::~Track() { };

/* -------------------------------------------------------------------- */

Track* Track::Copy(void)
{
  Track *tp = new Track(*this);
  return tp;
};

/* -------------------------------------------------------------------- */

char* Track::Name()
{
  Event *p = head;
  Text *tp;

  while (p != NULL)
  {
    if (p->Type() == TEXT_EVENT)
    {
      tp = (Text *)p;
      if (tp->type == SEQUENCE_NAME) return tp->str;
    };

    p = p->next;
  };

  return (char*)"";
};

/* -------------------------------------------------------------------- */

void Track::Insert(Event *e)
{
        Event* temp = current;

        Seek(e->Time.time,1);

        if (current)
        {
	      e->next = current;
              e->prev = current->prev;
              current->prev = e;
              if (e->prev) e->prev->next = e;
              else head = e;
              
        }
        else {
		Attach(e);
        }

        current = temp;
};

/* -------------------------------------------------------------------- */
  /**
	 Remove the given  Event 
	*/
void Track::Delete(Event *e)
{

  if (e==head)
  {
    head = head->next;
    if (head) head->prev = NULL;
  }
  else if (e==tail)
  {
	tail= tail->prev;
	if(tail)  tail->next = NULL;
  }
  else
  {
	Event *prevE=e->prev;
	Event *nextE=e->next;
	prevE->next=e->next;
	nextE->prev=e->prev;
  }

  if (head==NULL) tail = NULL;
  else if (tail==NULL) head = NULL;

	e->prev = e->next = NULL;
	delete e;
  return ;

};

/* -------------------------------------------------------------------- */

// Move Event Pointer to the time index

void Track::Seek(unsigned long seek_time, int start)
{
  switch (start)
  {
  case 0:
        current = head;
        while (current!=NULL)
        {
                if (current->Time.time >= seek_time) break;
                current = current->next;
        }
  break;
  case 1:
        current = tail;
        while (current!=NULL)
        {
                if (current->Time.time <= seek_time) break;
                current = current->prev;
        }
        if (current) current = current->next;
        else if (head) current = head;
  break;
  default:
  break;
  };
};

/* -------------------------------------------------------------------- */

  // Returns the current event and advances the event pointer
Event* Track::NextEvent()
{
        Event* p = current;
        if (current) current = current->next;
        return p;
};


unsigned long Track::GetEventCount()
{
  Event *ep;
  unsigned long Count = 0;
  Seek(0L);
  while ((ep = NextEvent())) Count++;
  return Count;
};


/* -------------------------------------------------------------------- */
/**
	Returns a string with note events in the given format
   */
int Track::PrintNotes(char *pformat,ostringstream &pntuples, int optMetadata)
{
	Event *ep;
	Note *nt;		
	TimeSignature *ts;	
	KeySignature *ks;	
	TempoChange *tch;
	Program *prog;
	//Text *te;

    
   	Seek(0L);
	
	while ((ep = NextEvent()))
	{  
		if(optMetadata)
		{
			//cout << ep->Type() << endl;
			
			if(ep->Type()==TIME_SIGNATURE)  
			{
					ts=(TimeSignature *)ep;
					ts->Print(pntuples);
			}
			
			else if(ep->Type()==KEY_SIGNATURE)  
			{
					ks=(KeySignature *)ep;
					ks->Print(pntuples);
			}	
			
			else if(ep->Type()==TEMPO_CHANGE)  
			{
			  			tch=(TempoChange *)ep;
			  			tch->Print(pntuples);
			}
			
			else if(ep->Type()==PROGRAM_CHANGE)
			{
				prog=(Program *)ep;
				prog->Print(pntuples);
			}
			
			/*
			else if(ep->Type()==TEXT_EVENT)
			{
				te = (Text*)ep;
				te->Print(pntuples);
			}
			*/
		} 
		
		if(ep->Type()==NOTE_ON)  // si es una nota
		{
			nt=(Note *)ep;
			nt->Print(pformat,pntuples);
		}
	}
    return 1;
}


void Track::printByChannel(char *pformat,int pchannel,ostringstream &pntuples)
{
	Event *ep;
	Note *nt;	

        Seek(0L);
	
      while ((ep = NextEvent()))
	{  
		if(ep->Type()==NOTE_ON)  // only note events
		{
			nt=(Note *)ep;
			if(nt->chan==pchannel)   //show only channels of the list
				nt->Print(pformat,pntuples);
		}
	}
}

/**
 * Prints metadata in the track. For use when printing notes by channel, to print
 * non-channel metadata.
 *
 */
void Track::PrintMetadata(ostringstream &pntuples)
{
	Event *ep;
	TimeSignature *ts;
	KeySignature *ks;
	TempoChange *tch;
	Program *prog;
	//Text *te;


   	Seek(0L);

	while ((ep = NextEvent()))
	{
			//cout << ep->Type() << endl;

			if(ep->Type()==TIME_SIGNATURE)
			{
					ts=(TimeSignature *)ep;
					ts->Print(pntuples);
			}

			else if(ep->Type()==KEY_SIGNATURE)
			{
					ks=(KeySignature *)ep;
					ks->Print(pntuples);
			}

			else if(ep->Type()==TEMPO_CHANGE)
			{
			  			tch=(TempoChange *)ep;
			  			tch->Print(pntuples);
			}

			else if(ep->Type()==PROGRAM_CHANGE)
			{
				prog=(Program *)ep;
				prog->Print(pntuples);
			}

			/*
			else if(ep->Type()==TEXT_EVENT)
			{
				te = (Text*)ep;
				te->Print(pntuples);
			}
			*/
	}
}

int Track::PrintTimeSig(ostringstream &pTimeSig)
{
	Event *ep;
	TimeSignature *ts;	
	int exists=0;
    
   	Seek(0L);
	
	while ((ep = NextEvent()))
	{  
		if(ep->Type()==TIME_SIGNATURE)  
		{
				ts=(TimeSignature *)ep;
				ts->Print(pTimeSig);
				exists=1;
		}
	}
    return exists;
}


int Track::PrintKeySig(ostringstream &pKeySig, int onlyfirst)
{
	Event *ep;
	KeySignature *ts;	
	int exists=0;
    
   	Seek(0L);
	
	while ((!onlyfirst || exists==0) && (ep = NextEvent()) )
	{
		if(ep->Type()==KEY_SIGNATURE)  
		{
				ts=(KeySignature *)ep;
			
//				pKeySig << "@KeySignature ";
//				ts->Print(pKeySig);
				
				ts->Print(pKeySig);
	

			exists=1;
		}
	}
    return exists;
}



 /**
  	modification of the notes with pedal events
   */
void Track::pedal()
{
	Event *ep;
	Parameter *par;
	//int initTick,endTick;
	int state=0; //state of the pedal  0->off   1->on
	
	vector <unsigned int> onPedal;
	vector <unsigned int> offPedal;
	
	Seek(0L);
	

	while ((ep = NextEvent()))
	{  
		if(ep->Type()==CONTROL_CHANGE)  
		{
			par=(Parameter *)ep;

			if(par->control==DAMPER_PEDAL || par->control==SOSTENUTO)  
			{

				if(state==0)	//off
				{
					if((par->value)>=64)
						{
						onPedal.push_back(par->Time.time);
						state=1;
						//cout << "pedal on en " << par->Time.time<< endl; 
					}
				}
				else
				{
					if((par->value)<64)
					{
						offPedal.push_back(par->Time.time);
						state=0;
						//cout << "pedal off en " << par->Time.time<< endl; 
					}
				}
			}
		}
	}
	
	Note *nt;
	unsigned int posVect=0;
	state=0;
	
	if(onPedal.size()>0	&& onPedal.size()==offPedal.size())
	{
		Seek(0L);
		
		while ((ep = NextEvent()))
		{  
			
			par=(Parameter *)ep;

			if(ep->Type()==NOTE_ON)  
			{
				nt=(Note *) ep;

				unsigned int endN=(nt->Time.time)+nt->dur;
				//cout << "onP1=" << onPedal.at(posVect)<< " " << endl; 
				//cout << "off1=" << offPedal.at(posVect) <<endl;
				while( (endN > (offPedal.at(posVect))) && posVect<offPedal.size()-1)
				{	
						posVect++;
						//cout << "onP2=" << onPedal.at(posVect)<< endl;
						//cout << " off2=" << offPedal.at(posVect) << endl;

				}
				//cout << "endN=" << endN << " onP=" << onPedal.at(posVect) << " offP=" << offPedal.at(posVect)<< endl ;
				if(endN > onPedal.at(posVect)  && endN < offPedal.at(posVect))
				{
					nt->dur=nt->dur+((offPedal.at(posVect)-endN));
				}
			}

			/*else if(par->control==DAMPER_PEDAL || par->control==SOSTENUTO)
			{
				if(state==0)
					state=1;
				else
				{
					state=0;
					posVect++;
					if(posVect>=onPedal.size())
						break;
					
				}
			}*/
		}
	}

	
}
  
  /**
	modification of the notes with tempo events
   */
  void Track::tempo(vector<unsigned long> changeTick,vector<unsigned long> tempoValue,int Division)
  {
  	Event *ep;
	Note *nt;
	unsigned long actTempo=500000L;
	unsigned long nextChange=0,prevChange=0;
	int end=0;
	double actSeconds=0;	//accumulated time in seconds
	
	if(tempoValue.size()>0)
	{			
		unsigned int posVect=0;
		if(changeTick.at(0)==0)
		{
			actTempo=tempoValue.at(0);
			if(changeTick.size()>1)
				nextChange=changeTick.at(1);
			else
			{
				end=1;  //arrives to the end of the vector
			}
		}
		else
		{
			actTempo=500000L;
			nextChange=changeTick.at(0);
		}
		Seek(0L);
		
		//cout << "next change=" << nextChange << " end=" << end<< endl;
		//int tam=tempoValue.size();
		while ((ep = NextEvent()))
		{
			if(ep->Type()==NOTE_ON)  
			{
				while(end!=1 && (ep->Time.time)>=nextChange)  
				{
					actSeconds=((double)((nextChange-prevChange)*actTempo)/(Division*1000000))+actSeconds;
					actTempo=tempoValue.at(posVect);
					prevChange=nextChange;
					posVect++;
					if(posVect>=changeTick.size())
						end=1;
					else
					nextChange=changeTick.at(posVect);
				}

				nt=(Note *)ep;
				//cout << "prev=" << prevChange << " tempo=" << actTempo << " time=" << nt->Time.time<<" dvi=" << Division<<endl;
				nt->Time.Division=Division;
				//double hola;
				double auxTempo=(double) actTempo/1000000;
				nt->onsetS=(double)(((nt->Time.time)-prevChange)*auxTempo)/(Division)+actSeconds;

				
				unsigned int posVect2=posVect;
				double durS=0;
				int durAc=0;  //duration calculated
				unsigned long actTempoAux=actTempo;
				
	

				//note duration in seconds 
				// While the note end is located past the tempo change tick...
				//FIXME: Doesn't compute durS correctly when tempo changes is in between note onset and note offset
				while(end!=1 && posVect2<changeTick.size() && ((nt->Time.time)+(nt->dur))>changeTick.at(posVect2))
				{
					// accumulate the difference in seconds between note onset and tempo change location
					// This IF is a patch for the fixme above
					// Don't compute durS or durAc if tempo change is located before note onset time (note still not sounding!)
					if (changeTick.at(posVect2) > nt->Time.time) {
						durS = (( (double)changeTick.at(posVect2) - nt->Time.time - durAc ) * actTempoAux) / (Division*1000000) + durS;
						durAc=durAc+((changeTick.at(posVect2)-(nt->Time.time)));
					}
					actTempoAux=tempoValue.at(posVect2);
					posVect2++;
				}
					durS=durS+( ((double)nt->dur - durAc) * actTempoAux )/(Division*1000000);
				nt->durS=durS;
				//cout << "nt dur=" << nt->dur << endl;
				if(durS < kMIN_DURATION)  //deletes notes with very short duration
				{
					Delete(ep);
				}
				
			}
		}
	}
	else	//not tempo changes
	{
		Seek(0L);
		while ((ep = NextEvent()))
		{  
			if(ep->Type()==NOTE_ON)  
			{
				nt=(Note *)ep;

				double auxTempo=(double) actTempo/1000000;
				nt->onsetS=(double)((nt->Time.time)*auxTempo)/(Division);
//				nt->onsetS=(double)((nt->Time.time)*actTempo)/(Division*1000000);
				nt->durS=(double)((nt->dur)*actTempo)/(Division*1000000);
				nt->Time.Division=Division;
			}
		}	
	}
  }


void Track::polyphonyRed(int poption)
{
	//Note *highNt,*lowNt;
	//int highPitch=0,lowPitch=129;
	Event *ep,*epaux;
	Note *nt;
	vector<Note *>	inter;
    
   	Seek(0L);
	
	while ((ep = NextEvent()))
	{  
		
		if(ep->Type()==NOTE_ON)  // only notes
		{
			nt=(Note *) ep;
			inter.push_back(nt);
			
			epaux=ep;
			while((epaux = NextEvent()))  
			{
				if(epaux->Type()==NOTE_ON)  // only notes
				{
					int maxTime=(nt->Time.time)+(nt->dur);
					int time=epaux->Time.time;	
					if(time < maxTime)				//events that begin before ep end
					{
						int ex=0;
						Note *ntaux=(Note*) epaux;
						vector<Note *>::iterator it;
						for (it = inter.begin(); it!=inter.end() && ex!=1; ++it) //order insert
						{
						    Note *nt2=(Note *) *it;
							if(poption==1 || poption==3)   //order top-down
							{
								if(nt2->pitch < ntaux->pitch)
								{
									it--;
									ex=1;
								}
							}
							else if(poption==2)
							{
								if(nt2->pitch > ntaux->pitch)
								{
									it--;
									ex=1;
								}
							}
							
						}
						inter.insert(it,ntaux);
					}
					else
						break;
				}		
			}

			if(inter.size()>1 && poption != 3)   //highest or lowest note
			{
				int Tinic,Tend;
				for (vector<Note *>::iterator it = inter.begin(); it!=(inter.end()); ++it) 
				{
					if(*it!=NULL)
					{
					nt=(Note *) *it;
					Tinic=nt->Time.time;
					Tend=Tinic + nt->dur;

					ostringstream temp;
					nt->Print("%o %e %p",temp);
					//cout << "max Tinic ="<< Tinic << " Tend=" << Tend << " " << temp.str() ;


					for (vector<Note *>::iterator it2 = it+1; it2!=inter.end(); ++it2) 
					{
						if(*it2!=NULL)
						{
						nt=(Note *) *it2;
						
						int TinicL,TendL; 
						TinicL=nt->Time.time;
						TendL=TinicL + nt->dur;

						//cout << "act TinicL ="<< TinicL << " TendL=" << TendL << " " << (int) nt->pitch  << " ";	

						if(TinicL < Tinic)  
						{
							if(TendL>Tinic)	//intersecs
							{				//cut the end  case 2,3
								nt->dur=(nt->dur)-(TendL-Tinic);
								ostringstream temp;
								nt->Print("%o %e %p",temp);
								//cout << "cut end " << temp.str();
							} //else cout << "case 1" << endl; //else case1
						}
						else if (TendL >  Tend) 
						{
							if(TinicL < Tend ) //intersecs
							{	
								if((Tend-TinicL) <= (nt->dur)*kCutPer) //cut beginning case 5. only  if cut < kCutPer 
								{
									nt->Time.time=Tend;
									nt->dur=(nt->dur)-(Tend-TinicL);
									ostringstream temp;
									nt->Print("%o %e %p",temp);
									//cout << "cut beginning " << temp.str();
									
								}
								else
								{
									ostringstream temp;
									nt->Print("%o %e %p",temp);
									//cout << "delete " << temp.str() << endl;
									if(nt==ep)  //current event
										ep=ep->prev;
									Delete(nt);
									*it2=NULL;
								}
							}   //else cout << "case 6" << endl;//else case 6
						}else   //all inside
						{	//delete the note  case 4
								ostringstream temp;
								nt->Print("%o %e %p",temp);
								//cout << "delete " << temp.str() << " minit=2" << endl;
								if(nt==ep) 	//current event
									ep=ep->prev;
								Delete(nt);
							*it2=NULL;
						}
						}
					}
					}
				}
							//////////////////////////////////////////////////////////////////
			}else if(inter.size()>2 && poption==3) //highest and lowest notes
			{
				unsigned int TinicM,TendM,Tinic,Tend;
				for (vector<Note *>::iterator maxit = inter.begin(); maxit!=(inter.end())-1; ++maxit) 
				{
					if(*maxit!=NULL)
					{
					nt=(Note *) *maxit;
					TinicM=nt->Time.time;
					TendM=TinicM + nt->dur;
					ostringstream temp;
					nt->Print("%o %e %p",temp);
					//cout << "max Tinic ="<< TinicM << " Tend=" << TendM << " " << temp.str() ;

					
					for (vector<Note *>::iterator minit = inter.end()-1; minit!=maxit+1; --minit) 
					{
						if(*minit!=NULL)
						{						
						nt=(Note *) *minit;
						if(nt->Time.time > TinicM)
							Tinic=nt->Time.time;
						else
							Tinic=TinicM;
						unsigned int endT=(nt->Time.time) + nt->dur;
						if( endT < TendM)
							Tend=endT;
						else
							Tend=TendM;
						ostringstream temp;
						nt->Print("%o %e %p",temp);
						//cout << "min Tinic ="<< Tinic << " Tend=" << Tend <<  " " << temp.str() ;
						
						if(Tinic<Tend)
						for (vector<Note *>::iterator actit = maxit+1; inter.size()>2 && actit!=minit; ++actit) 
						{
							if(*actit!=NULL)
							{
							Note *ntact=(Note *) *actit;
							
							unsigned int TinicL,TendL; 
							TinicL=ntact->Time.time;
							TendL=TinicL + ntact->dur;
							//cout << "act TinicL ="<< TinicL << " TendL=" << TendL << " " ;
							
							if(TinicL < Tinic)  
							{
								if(TendL>Tinic)	//intersecs
								{				//cut the end  case 2,3
									ntact->dur=(ntact->dur)-(TendL-Tinic);
									ostringstream temp;
									ntact->Print("%o %e %p",temp);
									//cout << "cut end " << temp.str();
								} //else cout << "case 1" << endl; //else case1
							}
							else if (TendL >  Tend) 
							{
								if(TinicL < Tend ) //intersecs
								{	
									if((Tend-TinicL) <= (ntact->dur)*kCutPer) //cut beginning case 5. only  if cut < kCutPer %							
									{
  										ostringstream temp;
										ntact->Print("%o %e %p",temp);
										//cout << "cut beginning " << temp.str();
										ntact->Time.time=Tend;
										ntact->dur=(ntact->dur)-(Tend-TinicL);
									}
									else
									{
										ostringstream temp;
										ntact->Print("%o %e %p",temp);
										//cout << "delete " << temp.str() << endl;
										if(ntact==ep)  //current event
											ep=ep->prev;
										Delete(ntact);
										*actit=NULL;
									} 
								}  //else cout << "case 6" << endl;//else case 6
							}else   //all inside
							{	//delete the note  case 4
								ostringstream temp;
								ntact->Print("%o %e %p",temp);
								//cout << "delete " << temp.str() << endl;
								if(ntact==ep)  //current event
								{
									//cout << "delete current" << endl;
									ep=ep->prev;
								}
								Delete(ntact);
								*actit=NULL;
							}
							}
						}
						}
					}
					}
					
				}
			} 
			
			inter.erase(inter.begin(), inter.end());

			current=ep->next;
			/*Note *borr=(Note *) ep;
			
			if(current!=NULL)
			{
				Note *borr=(Note *) current;
			}*/
			

		}//is note
	}
	
    return ;
}

   /**
   	Delete the notes out of the rank
   */
      
void Track::rank(double pBegin,double pEnd,int inSeconds)
{
	Event *ep;
	Note *nt;
	double NtBegin,NtEnd;

	Seek(0L);
	
	while ((ep = NextEvent()))
	{  
		if(ep->Type()==NOTE_ON)  // si es una nota
		{
			nt=(Note *)ep;
			if(inSeconds==0)
			{
				NtBegin=(double) nt->Time.time;
				NtEnd=(double) (nt->Time.time)+nt->dur;
			}
			else
			{
				NtBegin=nt->onsetS;
				NtEnd=(nt->onsetS) + (nt->durS);
			}
			
			if(!(NtBegin>=pBegin && NtEnd<=pEnd))
				Delete(ep);
		}
	}


}

/**
   	puts the number of the track into the note events
   */
  void Track::setNumber(unsigned int pnum)
   {
   	Event *ep;
	Note *nt;	
	Parameter *par;
    
   	Seek(0L);
	
	while ((ep = NextEvent()))
	{  
		if(ep->Type()==NOTE_ON)  // si es una nota
		{
			nt=(Note *)ep;
			nt->trk=pnum;
		}
		if(ep->Type()==CONTROL_CHANGE)  
		{
			par =(Parameter *)ep;
			par->trk=pnum;
		}
	}
   }


unsigned long Track::GetEventCount(int EVENT_TYPE)
{
  Event *ep;
  unsigned long Count = 0;
  Seek(0L);
  while ((ep = NextEvent())) { if (ep->Type()==EVENT_TYPE) Count++;  }
  return Count;
};



/* -------------------------------------------------------------------- */
/* -------------------------------------------------------------------- */

midi_ofstream& operator << (midi_ofstream& midi_out, Track& track)
{
        Track* nq = new Track;
        Event* e, *p;

        track.Seek(0L);

        midi_out.track_begin();

        while (( e = track.NextEvent()))
        {
          /* If the Event is a Note_on append the corresponding note_off to nq */
          if (e->Type() == NOTE_ON)
          {
                Note *e2 = (Note *)e;
                p = new Note(e2->chan, e2->pitch, 0);
                p->Time = e2->Time + e2->dur;
                nq->Insert(p);
          };

          /* Reset the nq and get the first event */
          nq->Seek(); p = nq->NextEvent();

          /* While the first event is earlier than *e send to output */
          while (p)
          {
                if ( p->Time > e->Time ) break;
                p = nq->Detach();
                *p >> midi_out;
                delete p;
                nq->Seek(); p = nq->NextEvent();
          }

          /* Write this event */
          *e >> midi_out; 
       };

       /* Write the remaining Events in the Noteoff Queue*/
       nq->Seek(); p = nq->NextEvent();
       while (p)
       {
                p = nq->Detach();
                *p >> midi_out; 
                delete p;
                nq->Seek(); p = nq->NextEvent();
       }

       delete nq;
       midi_out.track_end();
       return midi_out;
};


/* -------------------------------------------------------------------- */

ostream& operator << (ostream& ascii_out, Track& track)
{
  ascii_out << track.Name() << endl;
  for (Event *p = track.head; p ; p=p->next ) *p >> ascii_out;
  return ascii_out;
};

ostream& operator << (ostream& ascii_out, Track* trackp)
{
  ascii_out << *trackp; 
  return ascii_out;
};


/* -------------------------------------------------------------------- */


midi_ifstream& operator >> (midi_ifstream& midi_in, Track* & pTrk)
{
  pTrk = new Track;
  return midi_in >> (*pTrk);
};

/* -------------------------------------------------------------------- */

midi_ifstream& operator >> (midi_ifstream& midi_in, Track& track)
{
   MessageBuffer ms;
   InputQueue t;
   Event* e;

   midi_in.track_begin();

   while (!midi_in.eot())
   {
     midi_in >> ms;
     ms >> e;
     
     t.Insert(e);

     while ( t.OK() ) 
     {
       track.Attach(t.Detach());
     };
   }

   midi_in.track_end();

   // Flush pending Events
   while (1)
   {
     if (!t) break;
     track.Attach(t.Detach());
   };

   return midi_in;
}

/* =================================================================== */
/*                             InputQueue                              */
/* =================================================================== */

void InputQueue::Insert(Event *e)
{

    if (e==NULL) return;

    if (e->Type() != NOTE_OFF) Attach(e);
    else
    {
      Note *q = NULL;
      Note *e2 = (Note *)e;
      Event *p = head;

      while (p != NULL)
      {
        if (p->Type() == NOTE_ON)
        {
          q = (Note *)p;
          if ((q->chan == e2->chan) && (q->pitch == e2->pitch) && (q->dur == 0)) break;
        };
        p = p->next;
      };

      if (q)
      {
        q->dur = e2->Time.time - q->Time.time;
      };

    };

};

/* -------------------------------------------------------------------- */

int InputQueue::OK()
{
    Note *np = (Note *)head;

    if (!head) return 0;
    if (head->Type() != NOTE_ON) return 1;

    return (np->dur > 0) ;
};


/* =================================================================== */
/*                             Song                                    */
/* =================================================================== */

Song :: Song(int Tracksp)
{
    nTracks = 0;
    track = NULL;
    NewTracks(Tracksp);

    Format = (nTracks == 1) ? 0 : 1;

    Division = 192*4;
    DivisionFormat = MIDITIME_BEAT;

};


Song :: Song( Song &s2)
{
    nTracks = 0;
    track = NULL;
    NewTracks(s2.nTracks);

    Format = s2.Format;
    Division = s2.Division;
    DivisionFormat = s2.DivisionFormat;

    for (int i=0; i<nTracks; i++)
    {
      track[i] = s2[i]->Copy();
    };
};

Song ::~Song()
{
    for (int i=0; i<nTracks; i++) if (track[i]) delete track[i];
};

/* -------------------------------------------------------------------- */

Song* Song::Copy(void)
{
   Song* s = new Song(*this);
   return s;
};

Song& Song::operator = ( Song& s)
{
  //  Song* sp = s.Copy();

  NewTracks(s.nTracks);

  for (int i=0; i<nTracks; i++) track[i] = s[i]->Copy();

  Format = s.Format;
  Division = s.Division;

  return *this;
};

/* -------------------------------------------------------------------- */

void Song::NewTracks(int Tracksp)
{

  if (track) 
  for (int i=0; i<nTracks;i++) if (track[i])
  {
    delete track[i];
  };
  if ((Tracksp > nTracks || track==NULL) && Tracksp>0)
  {
    track = new Track* [Tracksp];
  }
  nTracks = Tracksp;
  for (int i=0; i<nTracks;i++) track[i] = new Track;
  return;
};


 


/* -------------------------------------------------------------------- */
  /**
	Generates a string with note events in the given format
   */

  int Song::printAllNotes(char *pformat,ostringstream &pntuples, int optMetadata)
  {
	Track *tr;
	int i;
	
	//for (int i=format(); i<ntracks(); i++)
	if(optMetadata)
		i=0;
	else
		i=format();
	for (; i<ntracks(); i++)
	{
		
	      tr = track[i];  
	      //if(i!=0)
	      	pntuples << "@track " << i  << " " << tr->Name() << endl;
	      tr->PrintNotes(pformat,pntuples, optMetadata);		  
    }
	return 1;
  }

/**
	Generates a string with note events (of selected format) in the given format
   */

int Song::printSelTracksNotes(char *pformat, int plist[], int psizeList,ostringstream &pntuples, int optMetadata)
{
	Track *tr;
	
	
	for(int i=0;i<psizeList;i++)
	{
		  int ntrack=plist[i];
          tr = track[ntrack]; 
	      //if(ntrack!=0)
	      	pntuples << "@track " << ntrack  << " " << tr->Name() << endl;
	      tr->PrintNotes(pformat,pntuples, optMetadata);		  
    	}
	return 1;
}

void Song::printTracksByChannel(char *pformat,int pchannel,ostringstream &pntuples)
{
	Track *tr;
	
	pntuples << "@channel "<< pchannel+1  <<  endl;
	for (int i=0; i<nTracks; i++)
	{
		tr = track[i];  
     		tr->printByChannel(pformat,pchannel,pntuples);
	}
}

  /**
  	modification of the notes with pedal events
   */
  void Song::pedalEvents()
  {
  	Track *tr;
	
	for (int i=0; i<nTracks; i++)
	{
		tr = track[i];  
     		tr->pedal();
	}
  }

   /**

   */
  void Song::tempoEvents()
  {
	Track *tr;
	Event *ep;
	TempoChange *tch;
	vector<unsigned long> changeTick;
	vector<unsigned long> tempoValue;

	tr = track[0];  
        tr->Seek(0L);
	
    while ((ep = tr->NextEvent()))
	{  
		if(ep->Type()==TEMPO_CHANGE)  
		{
			tch=(TempoChange *)ep;
			
			changeTick.push_back(ep->Time.time);

			tempoValue.push_back(tch -> tempo);
			//tch -> tempo = ptempo;
		}
	}  
  	for (int i=format(); i<nTracks; i++)
	{
		tr = track[i];  
		
     		tr->tempo(changeTick,tempoValue,Division);
	}
  }

  void Song::printTempoEvents(ostringstream &pTempoSig)
  {
  	Track *tr;
  	Event *ep;
  	TempoChange *tch;
  	vector<unsigned long> changeTick;
  	vector<unsigned long> tempoValue;

  	tr = track[0];  
          tr->Seek(0L);
  	
    while ((ep = tr->NextEvent()))
  	{  
  		if(ep->Type()==TEMPO_CHANGE)  
  		{
  			tch=(TempoChange *)ep;
  			
  			//changeTick.push_back(ep->Time.time);

  			//tempoValue.push_back(tch -> tempo);
  			//tch -> tempo = ptempo;

  			pTempoSig << "@Tempo ";
  			pTempoSig <<  ep->Time.time; 
  			pTempoSig << " ";
  			pTempoSig << ep->Length();
  			pTempoSig << " "; 
  			pTempoSig << 60000000.0/tch->tempo;
  			pTempoSig << endl;
  		}
  	}  
  }

/**
	quantize all the song events
		*/
void Song::Quantize(double prel)
{
	Track *tr;
	Event *ep;
	Note *nt;

	for (int i=0; i<nTracks; i++)
	{
		tr = track[i];  
     	tr->Seek(0L);
		while ((ep = tr->NextEvent()))
		{  
			if(ep->Type()==NOTE_ON)  // only note events
			{
				nt=(Note *) ep;
				nt->Quantize(prel);
			}
		}
		     	
	}
}



/**
	polyphony reduction
			poption: 1-> highest note
					 2-> lowest	note
					 3-> both
		*/
void Song::polyphonyRed(int poption)
{
	Track *tr;

	for(int i=0;i<nTracks;i++)
	{
		  tr=track[i];
		  tr->polyphonyRed(poption);
    }
}   

void Song::rank(double pBegin,double pEnd,int inSeconds)
{
	Track *tr;

	for(int i=0;i<nTracks;i++)
	{
		  tr=track[i];
		  tr->rank(pBegin,pEnd,inSeconds);  
	}
}   



/**
   	puts the number of the track to the note events
   */
  void Song::setTrkNumber()
   {
   	for (int i=0;i<nTracks;i++)
		track[i]->setNumber(i);
   }


void Song::setNtracks(int pnt)
{
  nTracks=pnt;
  if (track) 
  for (int i=pnt; i<nTracks;i++) if (track[i])
  {
    delete track[i];
  };	
	
}


  /**
   	joins the new notes in the fisrt track
   */
   
void Song::mergeTrack(Track *ptr)
{
	Event *ep;

	Format=0;
	
	ptr->Seek(0L);
	track[0]->Seek(0L);  
	   
	
	
	if(!(track[0]==ptr))  //if the track is empty -> direct copy
	{
		while ((ep = ptr->NextEvent()))
		{  
			if(ep->Type()==NOTE_ON)  // note	
			{
				track[0]->Insert(ep);
			}
		}
	}
	
}

/**
		adds the given track to the song
   */
   void Song::addTrack(int pTrkNumber,char *pTrkName)
	{	
		Track **oldTracks=NULL;
		//int oldNtracks=nTracks;
		//cout<<"addTracks " << nTracks<< endl;
		//track[nTracks]=new Track* [];
		//track[nTracks++]=ptr;
		//cout<<"addTracks2" << endl;

		if (track) 
		{
			oldTracks=track;			
		}
		if(pTrkNumber>=nTracks)
		{
		    track = new Track* [pTrkNumber+1];

		    for (int i=0; i<pTrkNumber+1;i++) 
			{
				if(i<nTracks)
					track[i] = oldTracks[i];		
				else
					track[i] = new Track();
			}
			nTracks=pTrkNumber+1;	
//			cout<< "Creada Pista Nueva" << endl;
		}
		//else cout << "ya existía ntracks="<<nTracks<< " pistanueva"<< pTrkNumber << endl;

		if(pTrkName != NULL)
		{
			string tmp(pTrkName);
 			Text *txt=new Text(SEQUENCE_NAME,tmp.length(),pTrkName);
			track[pTrkNumber]->Insert(txt);
		}
		  return;
	}
	

void Song::printMetadata(int tridx, ostringstream& stream) {
	if (tridx<nTracks)
		track[tridx]->PrintMetadata(stream);
}

  int Song::printTimeSignature(ostringstream &pTimeSig)
  {
	Track *tr;
	
	tr = track[0];  
        if((tr->PrintTimeSig(pTimeSig))==0)
			pTimeSig<<"@Time Signature 0 4 4"<<endl;
	
	return 1;
  }

int Song::printKeySignature(ostringstream &pKeySig, int onlyfirst)
  {
	Track *tr;
	tr = track[0];  
    tr->PrintKeySig(pKeySig, onlyfirst);

	return 1;
  }



/* -------------------------------------------------------------------- */
/**
  Returns a pointer to the i'th Track.
 */
Track*& Song::operator [] ( int i)
{
  if (i>=0 && i<nTracks) return track[i];
  else return track[0];
  //  else return NULL;
};

/* -------------------------------------------------------------------- */
/* -------------------------------------------------------------------- */

midi_ofstream& operator << (midi_ofstream& midi_out, Song& s)
{
  midi_out.division(s.division());
  midi_out.format(s.format());

  for (int i=0; i<s.nTracks ; i++) midi_out << *s.track[i];
  return midi_out;
};

/* -------------------------------------------------------------------- */

ostream& operator << (ostream& ascii_out, Song& s)
{
    static char *Form[] =
    {(char*)"0, one multi-channel track",
    	(char*)"1, several simultaneous tracks",
    	(char*)"2, several independent patterns"};
  
    ascii_out << endl;
    ascii_out << "Format         \t : " << Form[s.format()] << endl;
    ascii_out << "Division       \t : " << s.division() << endl;
    ascii_out << "# of Tracks\t : " << s.nTracks - (s.format() ? 1 : 0) << endl;
    ascii_out << endl << endl;

    MidiTime::Division = s.division();

    //    for (int i=0; i<s.nTracks; i++) if (s.track[i]) ascii_out << s.track[i] << endl;

 return ascii_out;
};

/* -------------------------------------------------------------------- */
/**
Reads a Song object from midi_ifstream
 */
midi_ifstream& operator >> (midi_ifstream& midi_in, Song& song)
{
  int Division = midi_in.division();
  song.NewTracks(midi_in.ntracks());
  song.Format   = midi_in.format();

  if (Division>0) {
    song.Division = Division;
    song.DivisionFormat = MIDITIME_BEAT;
  }
  else {
    song.Division = ((-upperbyte(Division))<<8) | lowerbyte(Division);
    song.DivisionFormat = MIDITIME_SMPTE;
  };


  for (int i=0; i<midi_in.ntracks(); i++)
  {
    midi_in >> song[i];
  };
  return midi_in;
};

/* -------------------------------------------------------------------- */
/**
Reads a Song object from midi_ifstream
 */
midi_ifstream& operator >> (midi_ifstream& midi_in, Song* &song_ptr)
{
  song_ptr = new Song(midi_in.ntracks());
  return midi_in >> (*song_ptr);
};











