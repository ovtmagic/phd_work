#include <iostream> 
#include "./lib/m_ofstrm.h" 
#include "./lib/m_ifstrm.h" 
#include "./lib/song.h"
#include <getopt.h>
#include <sstream>


using namespace std;

int verbose=0;


void showError(string pmsg,int pexit)
{
	
	if(pexit)
	{
		cerr << "ERROR: " << pmsg << "." <<endl;
		exit(1);	
	}
	else
	{
		if(verbose)
		   cerr << "WARNING: " << pmsg << "." <<endl;
	}

}



//function to obtain a list of numbers from a string with comas
int parseList(char *pstring,int plist[],int pnumTracks)
{
	int cont=0,contNum=0,listNum=0;
	char num[4];
	
	while(pstring[cont]!='\0')
	{
		if (pstring[cont]>='0' && pstring[cont]<='9') // only numbers
		{
			num[contNum]=pstring[cont];
			contNum++;
			if(contNum>=4)
			{
				contNum=0;
				showError("A number from the list exceeds the maximum number of tracks",1);
			}
		}
		else if(pstring[cont]==',')		// end of the number
		{
			if(contNum==0)
			{
				showError("Two consecutive commas in the list",0);
				contNum=0;	
				cont++;
				continue;	//continue number search
			}
			num[contNum]='\0';
			contNum=0;

			if (atoi(num)>=pnumTracks)
			{
				showError("A number from the list exceeds the maximum number of tracks of the file",0);
				cont++;
				continue;

			}
			plist[listNum]=atoi(num);
			listNum++;
		}else
		{
			showError("not allowed characters in the list",0);
			contNum=0;
			while(pstring[cont]!=',' && pstring[cont]!='\0')cont++;
			if(pstring[cont]==',')
				cont++;
			continue;
		}	
		cont++;
		if(listNum>=255)
		{
			showError("too many tracks to show",0);
			contNum=0;
			break;
		}
	}
	//last number from the list
	if(contNum>0)
	{
		num[contNum]='\0';
		if (atoi(num)>=pnumTracks)
		{
			showError("A number from the list exceeds the maximum number of tracks of the file",0);
		}
		else
		{
			plist[listNum]=atoi(num);
			listNum++;
		}
	}
	plist[listNum]=-1; //list end
	
	return listNum;
}

//function to obtain a list of numbers from a string with comas
int parseChannelsList(char *pstring,int plist[], int poptChannels,Track ptr)
{
	int cont=0,contNum=0,listNum=0;
	char num[4];
	
	for(int i=0;i<16;i++)
		plist[i]=-1;   

	//search the number of channels of the midi file
	Event *ep;
	Note *nt;	

    ptr.Seek(0L);
	
    	while ((ep = ptr.NextEvent()))
	{  
		if(ep->Type()==NOTE_ON)  // note event
		{
			nt=(Note *)ep;
			plist[nt->chan]=-2;  //used channel 
		}
	}
	
	if(poptChannels==1)  //show all channels
	{
		for(int i=0;i<16;i++)
		{
			if(plist[i]==-2)	
				plist[i]=1;
		}
		return 16;
	}
	else
	{

		while(pstring[cont]!='\0')
		{
			if (pstring[cont]>='0' && pstring[cont]<='9') // is number
			{
				num[contNum]=pstring[cont];
				contNum++;
				if(contNum>=4)
				{
					contNum=0;
					showError("in channel list, midi supports a maximum of 16 channels",0);
					while(pstring[cont]>='0' && pstring[cont]<='9') cont++;   
					cont++;  //comma 
				}
			}
			else if(pstring[cont]==',')
			{
				if(contNum==0)
				{
					showError("in channel list, two consecutive commas in the list",0);
					contNum=0;	
					cont++;
					continue;	//continue number search
				}
				num[contNum]='\0';
				contNum=0;

				if (atoi(num)>16)
				{
					showError("in channel list, midi supports a maximum of 16 channels",0);
					cont++;
					continue;
	
				}
				int canal=atoi(num)-1;
				if(plist[canal]==-2)
					plist[canal]=1;
				listNum++;
			}else
			{
				showError("in channel list, not allowed characters in the channel list",0);
				contNum=0;
				while(pstring[cont]!=',' && pstring[cont]!='\0')cont++;
				if(pstring[cont]==',')
					cont++;
				continue;
			}	
			cont++;
			if(listNum>16)
			{
				showError("in channel list, too many channels to show",0);
				contNum=0;
				break;
			}
		}
		//last element
		num[contNum]='\0';
		if (atoi(num)>16)
		{
			showError("in channel list, midi supports a maximum of 16 channels",0);
		}
		else
		{
			int canal=atoi(num)-1;
			if(plist[canal]==-2)
				plist[canal]=1;
			listNum++;
		}

		return listNum;
	}
}


//range of seconds or ticks to show 
int parseRank(char *prank,double &pBegin, double &pEnd)
{	string rank(prank);
	size_t pos=rank.find(":",0);
	//char buffer[50];
	char *two;
	int inSeconds=0;
	
	int twoP=0;
	int point=0;
	for(unsigned int i=0; i<rank.size();i++)
	{
		if(! ((rank[i]>='0' && rank[i]<='9') || (rank[i]==':' && twoP==0 )|| (rank[i]=='.' && point==0)))
		{
			
			showError("in rank, incorrect character \"begin:end\"",0);
			return -1;
		}
		else
		{
			if(rank[i]==':')
			{
				twoP++;
				point=0;
			}
			if(rank[i]=='.')
			{
				point++;
				inSeconds=1;
			}
			
		}
	}
	
	if( pos != string::npos )
	{
		pBegin=strtod( rank.c_str(),&two );
	
		pEnd=strtod(two+1, &two);
		if(pEnd==0) 
			pEnd=999999999;
	}
	else 
	{
		showError("in rank, incorrect format \"begin:end\"",0);
		return -1;
	}
	
	if(pBegin>=pEnd)
	{	
		showError("in rank, end time should be greater than begin",0);
		return -1;
	}
	return inSeconds;
}


int main(int argc, char** argv) 
{ 

  Song s,sAux;
  Track*  tr,totalTr;
  int list[256],listC[16],listAux[256];
  
  char defFormat[]="%p %o %d %v";   //default format
  char *format=NULL,*parList=NULL,*fileName=NULL,*rank=NULL;
  int qTarget=-1; //target quantization
  int res;	//resolution
  double rel;  //relation between the original resolution of the document and the new one

  int posAct;
  
  int opt;
  int optList=0; //option for select what tracks must be shown
  int optFmt=1;  //output format  0-> group tracks
			    //    1-> separated tracks
  
  int optChannels=1;   // channels option   1-> show all channels 
					//  0-> only list channels
  int opcPolRed=0;    //option for polyphomy reduction
  int opcRank=0;	
  //int opcTimeSig=0;  //option for show time signature	

  ostringstream ntuples;	//string with output file content

    int option_index=0;
    
    int optMetadata = 0;	// no metadata information is showed by defect

    static struct option long_options[]=
    {
      {"track_list", required_argument , 0, 't'},
      {"no_track_list", required_argument , 0, 'x'},
      {"channel_list", required_argument , 0, 'c'},
      {"tuples_format", required_argument , 0, 'f'},
      {"show_by_channels", no_argument, 0, 'C'},
      {"group", no_argument, 0, 'g'}, 
      {"quantization", required_argument , 0, 'q'},
      {"rank", required_argument , 0, 'r'},      
      {"polyphony_reduction", required_argument , 0, 'r'},
      {"metadata", no_argument, 0, 'm'},
      {"help", no_argument, 0, 'h'},
      {"verbose", no_argument, 0, 'v'},
      {           0, 0, 0,   0}
    };


    format=defFormat;
    
    while ((opt = getopt_long(argc, argv, "p:t:x:n:gf:c:Cq:r:svhm", long_options, &option_index)) != -1) {
	switch (opt) {
	 case 'm':
		 optMetadata = 1;
		 break;
	 
	 case 't':   //track_list
	    parList=optarg;
	    optList=1;
	    break;

	 case 'x':    //no_track_list
	    parList=optarg;
	    optList=2;
	    break;
         
	 case 'c':    //channel_list
	    parList=optarg;
	    optList=3;
	    optChannels=0;
	    break;
	 case 'C':    //show_by_channels
	    optList=3;
	    optChannels=1;
	    break;

	 case 'g':  //group
	     optFmt = 0;
         break;

	 case 'f':     //tuples_format
	    format = optarg;
	    break;
	case 'p':	//polyphony_reduction
	    opcPolRed =atoi(optarg);
		if(opcPolRed<1 || opcPolRed>3)
			showError("the value for polyphony reduction must be [1-3]",1);
	    break;

	 case 'r':
	    opcRank = 1;
	    rank=optarg;
	    break;
	    /*
	 case 's':
	    opcTimeSig = 1;
	    break;
	    */
	case 'q':	//quantization
	    qTarget=atoi(optarg);
	    break;
	case 'v':	//verbose
	    verbose=1;
	    break;
	case 'h':	//help
	    fprintf(stdout, 
			"SMF2TXT: standard midi file to text notes.\n\
Developed by:\n\
Pattern Recognition and Artificial Intelligence Group,\n\
http://grfia.dlsi.ua.es\n\
Departamento de Lenguajes y Sistemas Inform�ticos,\n\
http://www.dlsi.ua.es\n\
University of Alicante.\n\
http://www.ua.es\n\
Usage: smf2txt  [-t list] [-x list] [-c list] [-C]\n\
		[-f \"format\"] [-g] [-q quantization] [-s]\n\
		[-p reduction] [-r begin:end] [-v] [-h] [-m] files\n\
Options:\n\
-t list		: show only tracks in the list\n\
-x list		: don't show tracks in the list\n\
-c list		: show only channels in the list\n\
-f format	: text format\n\
			  %%p pitch (0-127)\n\
			  #p pitch (Hz)\n\
			  %%o onset (ticks)\n\
			  %%d duration (ticks)\n\
			  #o onset (seconds)\n\
			  #d duration (seconds)\n\
			  %%v velocity\n\
			  %%c channel\n\
			  %%t track\n\
-q quantization : target quantization (ticks)\n\
-p reduction	: polyphony reduction\n\
				  1 highest note\n\
				  2 lowest note\n\
				  3 highest & lowest notes\n\
-r begin:end	: output rank\n\
-C		: order by channel\n\
-g		: group events\n\
-v 		: verbose\n\
-h 		: list available command line options (this page)\n\
-m		: show metadata\n"
	    		
			);
	    exit(0);
	    break;

	 default:
	    fprintf(stderr, 
				"Usage: smf2txt  [-t list] [-x list] [-c list] [-C] \n\
		[-f \"format\"] [-g] [-q quantization] [-s]\n\
		[-p reduction] [-r begin:end] [-v] [-h] [-m] files\n\
Try `smf2txt --help' for more information.\n"	);
	    exit(1);
	}
    }



if (argc<2 || optind==argc)
{
	fprintf(stderr, 
				"Usage: smf2txt  [-t list] [-x list] [-c list] [-C]\n\
		[-f \"format\"] [-g] [-q quantization] [-s] \n\
		[-p reduction] [-r begin:end] [-v] [-h] [-m] files\n\
Try `smf2txt --help' for more information.\n"	
				);
	return 1;
}



for (;optind<argc;optind++)
{

  fileName=argv[optind];


  //reads midi file
  midi_ifstream midi_in(fileName);



  if (!midi_in) {
      ostringstream buf;
	  buf << "File \"" << fileName << "\" not found";
	  showError(buf.str(),1);
    }


  midi_in >> s;
  

  
  
 
  
  
s.setTrkNumber();

s.pedalEvents();    //recalculates the note duration if the damper pedal is on





	
ntuples <<"# path " << fileName << endl;   // file information

//target resolution
res=s.division();
if(qTarget==-1)  //the same of the original midi
{
	ntuples <<"@resolution " << res  << endl;
}
else //change
{
	//we verified if  qTarget is multiple or splitter
	ntuples <<"@resolution " << qTarget  << endl;
	if( (res % qTarget)==0 || (qTarget % res)==0)
	{
		rel=(double) qTarget/res;
		s.Quantize(rel);
		s.setDivision(qTarget);
	}	
	else
	{
		ostringstream buf;
		buf << "the new quantization value must be multiple or splitter of the original one (" << res << ")";
		showError(buf.str(),1);
	}
}

if(opcPolRed>0 && optFmt==1)
{
	s.polyphonyRed(opcPolRed);
}



s.tempoEvents();   //calculates the notes onsets and duration in seconds, deletes short notes


double beg,end;
if(opcRank==1)
{
	int inSeconds=parseRank(rank,beg,end);
	if(inSeconds!=-1)
		s.rank(beg,end,inSeconds);
}

ntuples <<"@format \"" << format <<"\""<<endl;
  
//shows time signature events
/*
if(opcTimeSig)
	s.printTimeSignature(ntuples);
*/
/*
//show key signature events
if(metadata == 1)
{
//	s.printKeySignature(ntuples, 0);
//	s.printTempoEvents(ntuples);
//	s.printTimeSignature(ntuples);
}
else
{	
	s.printKeySignature(ntuples, 1);
}
*/


int sizeList;

sAux=s;

switch(optList)
{	
	case 1:  //track list
		sizeList=parseList(parList,list,s.ntracks());
		if(optFmt==1)  
		{
			s.printSelTracksNotes(format,list,sizeList,ntuples,optMetadata);
		}
		else  
		{
			for(int i=0;i<sizeList;i++)
			{
				int track=list[i];
        			tr = sAux[track];  
				sAux.mergeTrack(tr);  
			}
			sAux.setNtracks(1);
		}
		break;
	case 2:  //not into list tracks
	        parseList(parList,list,s.ntracks());
		posAct=0;
		for(int i=s.format();i<s.ntracks();i++)     //creates  a list with the desired tracks
		{
			int show=1;
			for(int j=0;j<256 &&  show==1;j++)
			{
				if(list[j]==i)
					show=0;
				if(list[j]==-1)
					break;
			}
			if(show==1)
				listAux[posAct++]=i;
		}
		listAux[posAct]=-1;
		
		if(optFmt==1)  
	    	{
			s.printSelTracksNotes(format,listAux,posAct,ntuples, optMetadata);
		}	
		else  
	    	{
			for(int i=0;i<posAct;i++)
			{
				int track=listAux[i];
        			tr = sAux[track];  
				sAux.mergeTrack(tr);  
			}
			sAux.setNtracks(1);
		}
		break;
	case 3:	//all tracks, selected channels
           
		for (int i=1; i<sAux.ntracks(); i++)
		{
			tr = sAux[i];  
			sAux.mergeTrack(tr);  
		}
		sAux.setNtracks(1);
		
		sizeList=parseChannelsList(parList,listC,optChannels,*sAux[0]);
		if (optMetadata) {
			// Print Metadata from track 0
			sAux.printMetadata(0,ntuples);
		}
		for(int channel=0;channel<16;channel++)
		{
			if(listC[channel]==1)
			{
				sAux.printTracksByChannel(format,channel,ntuples);
  			}  
		}
	    break;
	default:	//show all tracks
		if(optFmt==1)  //no group
		{
			s.printAllNotes(format,ntuples, optMetadata);
		}
		else	//group note events
		{
			for (int i=1; i<sAux.ntracks(); i++)
			{
				tr = sAux[i];  
				sAux.mergeTrack(tr);  
			}
			sAux.setNtracks(1);
		}
}

if(optFmt==0)   //group events
{
	if(opcPolRed>0)
	{
		sAux.polyphonyRed(opcPolRed);  
	}
	sAux.tempoEvents();
	if(optList!=3)
	{
		sAux.printAllNotes(format,ntuples, optMetadata);
        }
}

}//for end (files)
cout << ntuples.str();





 
} 








