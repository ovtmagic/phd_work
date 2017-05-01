#include <iostream>
#include "./lib/m_ofstrm.h"
#include "./lib/m_ifstrm.h"
#include "./lib/song.h"
#include <getopt.h>
#include <sstream>
#include <string>
#include <cmath>
#include <string.h>



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




int main(int argc, char** argv)
{


  int opt;
  string outputFile="default.mid";
  string inputFile="";
  int Dstart=-1,Dchan=-1,Dpitch=-1,Dvol=-1,Ddur=-1,Dtempo=-1;
  int option_index=0;

    static struct option long_options[]=
    {
    /*  {"track_list", required_argument , 0, 't'},
      {"no_track_list", required_argument , 0, 'x'},
      {"channel_list", required_argument , 0, 'c'},
      {"tuples_format", required_argument , 0, 'f'},
      {"show_by_channels", no_argument, 0, 'C'},*/

      {"output-file", no_argument, 0, 'f'},
      {"input-file", required_argument , 0, 'i'},
      {"def-onset", no_argument, 0, 'o'},
      {"def-channel", required_argument , 0, 'c'},
      {"def-pitch", required_argument , 0, 'p'},
      {"def-volume", required_argument , 0, 'v'},
      {"def-duration", required_argument , 0, 'd'},
      {"help", no_argument, 0, 'h'},
      {           0, 0, 0,   0}
    };



    while ((opt = getopt_long(argc, argv, "f:i:o:c:p:v:d:h", long_options, &option_index)) != -1)
	{
	switch (opt) {
	 case 'f':    //output file
		outputFile.replace(0,outputFile.size(),optarg);
	    break;
	 case 'i':
	   inputFile = optarg;
	   outputFile = inputFile.substr(0, inputFile.length()-4) + ".mid";
	   break;
	 case 'o':  //default onset
	     Dstart = atoi(optarg);
         break;
	 case 'c':     // default channel
	    Dchan = atoi(optarg);
	    break;
	 case 'p':     // default pitch
	    Dpitch = atoi(optarg);
	    break;

	 case 'v':     // default volume
	    Dvol = atoi(optarg);
	    break;
	 case 'd':     // default duration
	    Ddur= atoi(optarg);
	    break;

	case 'h':	//help
	    fprintf(stdout,
			"TXT2SMF: text notes to standard midi file.\n\
Developed by:\n\
Pattern Recognition and Artificial Intelligence Group,\n\
http://grfia.dlsi.ua.es\n\
Departamento de Lenguajes y Sistemas Inform�ticos,\n\
http://www.dlsi.ua.es\n\
University of Alicante.\n\
http://www.ua.es\n\
Usage: txt2smf  [-f output-file] [-i input-file]\n\
    [-o default-onset] [-c default-channel]\n\
    [-p default-pitch] [-v default-velocity]\n\
    [-d default-duration] [-h]\n\
Options:\n\
-f		: output file\n\
-o		: default onset\n\
-c		: default channel\n\
-p 		: default pitch\n\
-v 		: default velocity\n\
-d 		: default duration\n\
-h 		: list available command line options (this page)\n"
			);
	    exit(0);
	    break;

	 default:
	    fprintf(stderr,
				"Usage: txt2smf  [-f output-file] [-o default-onset]\n\
		[-c default-channel] [-p default-pitch] \n\
		[-v default-velocity] [-d default-duration] [-h]\n\
Try `smf2txt --help' for more information.\n"	);
	    exit(1);
	}
    }

/*
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
  */

//Default values
if(Dstart==-1)
	Dstart=0;
if(Dpitch==-1)
	Dpitch=60;
if(Dvol==-1)
	Dvol=127;
if(Dchan==-1)
	Dchan=0;
if(Dtempo==-1)
	Dtempo=120;


  int cotn=0;

char buffer[200];

Song Ssal;


Ssal.setFormat(1);
string *form=NULL;

int firstNote=0;
int trkNumber=0;
int chnNumber=0;
char *trkName;
KeySignature *ks=NULL;
TimeSignature *ts=NULL;
TempoChange *tc=NULL;
Program *prog=NULL;

ifstream input;
istream *is;

if (inputFile.length()>0) {
  input.open(inputFile.c_str(), ios::in);
  if (!input.is_open()) {
    cerr << "Error opening file " << inputFile << endl;
    exit(-1);
  }
  is = &input;
}
else {
  is = &cin;
}
while ( is->getline(buffer, sizeof(buffer)) ) //for each file line
{
	string linea(buffer);
	if(buffer[0]=='@')  //control command
	{
			if(linea.find("format",0)==1)
			{
				form=new string(&buffer[8]);
			}
			else
			{
				if(linea.find("track",0)==1)
				{
					firstNote=1;
					size_t fin=linea.find(" ",7);
					if (fin != string::npos) {
						trkNumber=atoi((linea.substr(7,fin-7)).c_str());
						trkName=&buffer[fin+1];
					} else  { // no track name, eol
						trkNumber=atoi(linea.substr(7,linea.length()-7).c_str());
						trkName= &buffer[strlen(buffer)]; // '\0', so empty string
					}
					Ssal.addTrack(trkNumber,trkName);
				}
				else
				{
						if(linea.find("resolution",0)==1)
						{
							char *res=&buffer[11];
							int iRes=atoi(res);
							Ssal.setDivision(iRes);

							if(Ddur==-1)
								Ddur=iRes;
						}
						else
						{
							if(linea.find("channel",0)==1)
							{
								firstNote=1;
								int fin=linea.find("\n",2);
								chnNumber=atoi((linea.substr(9,fin-9)).c_str());
								trkName=&buffer[fin+1];
								trkNumber=chnNumber;
								Ssal.addTrack(chnNumber,trkName);
							}
							else
							{
								if(linea.find("Meter",0)==1)
								{
									char *saux;
									char delims[] = " ";
									char *result = NULL;
									char *meter;
									int iToken=0, nn=0, denom=0, dd=0;
									unsigned int iTick=0;


									saux = strdup(linea.c_str());

									result = strtok( saux, delims );
									iToken++;
									while( result != NULL ) {
										//printf( "result is \"%s\"\n", result );
										result = strtok( NULL, delims );

										switch(iToken)
										{
										case 0:
											break;
										case 1:
											iTick = atoi(result);
											break;
										case 2:
											break;
										case 3:

											meter = strdup(result);
											char *result2 = NULL;
											char delims2[] = "/";

											result2 = strtok( meter, delims2 );
											nn = atoi(result2);
											//cerr << nn << "*************************************" << endl;

											result2 = strtok( NULL, delims2 );
											denom = atoi(result2);
											//cerr << denom << "****" << endl;
											break;
										}
										iToken++;
									}

									// cc parameter for TimeSignature ctor:
									// 96/dd : a metronome click for every beat pulse
									// 96 is one pulse per bar in a 4/4
									// 48 is one pulse every 2 beats in a 4/4
									// 24 is one pulse every beat in a 4/4
									// etc...
									int de = denom;
									dd=0; // dd is the negative power of two that corresponds to 'denom' value
									while (de > 1) {
										de >>= 1; // divide by two;
										dd++;
									}
									ts= new TimeSignature(nn, dd, 96/denom, 8);
									ts->Time.time=iTick;
									Ssal[0]->Insert(ts); //inserts the timesignature event
								}
								else
								{
									if(linea.find("KeySignature",0)==1)
									{
										char *saux;
										char delims[] = " ";
										char *result = NULL;
		
										char *skey=NULL;
										int iToken=0, sf=0, mi=0;
										unsigned int iTick=0;
										
										saux = strdup(linea.c_str());

										result = strtok( saux, delims );
										iToken++;
										while( result != NULL ) {
											//printf( "result is \"%s\"\n", result );
											result = strtok( NULL, delims );

											switch(iToken)
											{
											case 0:
												break;
											case 1:
												iTick = atoi(result);
												break;
											case 2:
												break;
											case 3:
												skey = strdup(result);
												break;
											}
											iToken++;
										}

										int j;
										for(j=0;j<30;j++)
										{
											if( strcmp(KeySignature::Key[j],skey)==0 )
												break;
										}
										if(j>7)
											sf = j-7;
										else
											sf = j-7+256;

										if(skey[1] == 'M')
										{
											mi=0;
										}
										else
										{
											mi=1;
											sf = sf-15;
										}


										ks=new KeySignature(sf,mi);
										ks->Time.time = iTick;
										Ssal[0]->Insert(ks); //inserts the keysignature event
									}
									else
									{
										if(linea.find("Tempo",0)==1)
										{
											char *saux;
											char delims[] = " ";
											char *result = NULL;
											int iToken=0;

											unsigned int iTempo=0, iTick=0;
											
											saux = strdup(linea.c_str());

											result = strtok( saux, delims );
											iToken++;
											while( result != NULL ) {
												//printf( "result is \"%s\"\n", result );
												result = strtok( NULL, delims );

												switch(iToken)
												{
												case 0:
													break;
												case 1:
													iTick = atoi(result);
													break;
												case 2:
													break;
												case 3:
													iTempo = atoi(result);
													break;
												}
												iToken++;
											}

											tc = new TempoChange(iTempo);
											tc->Time.time = iTick;
											cout << endl;
											Ssal[0]->Insert(tc); //inserts the tempochange event
											
											//se cambia el tempo por defecto
											Dtempo = (int)iTempo;
										}
										else
										{
											if(linea.find("Program",0)==1)
											{
												char *saux;
												char delims[] = " ";
												char *result = NULL;
												int iToken=0;
												int iProgram=0;
												unsigned int iTick = 0, ichan = 0;
											
												//cout << "program" << endl;
												
												saux = strdup(linea.c_str());

												result = strtok( saux, delims );
												iToken++;
												while( result != NULL ) {
													
													result = strtok( NULL, delims );
													//cout << iToken << " " << result << endl;

													switch(iToken)
													{
													case 0:
														break;
													case 1:
														iTick = atoi(result);
														break;
													case 2:
														ichan = atoi(result);
														break;
													case 3:
														iProgram = atoi(result);
														break;
													}
													iToken++;
												}
												
												//cout << trkNumber << " " << iTick << " " << ichan << " " << iProgram << endl;
												
												
												prog = new Program(ichan-1, iProgram-1);
												prog->Time.time = iTick;
												
												Ssal[trkNumber]->Insert(prog); //inserts the programchange event
												//prog=NULL;
											}
											else
											{
													cout<<"controlBFALTA!!! " << linea << endl;
											}
										}
									}
								}
							}
						}
					}
			}
	}
	else	 //note data
	{
		if(buffer[0]!='#')
		{
			if(buffer[0]>='0' && buffer[0]<='9')
			{
				if(firstNote==0)
				{
					Ssal.addTrack(1,(char*)"default");
					trkNumber=1;
					firstNote=1;
				}
				Note *nt;
				nt=new Note(*form,linea,Dstart,Dchan,Dpitch,Dvol,Ddur,trkNumber,Ssal.division(), Dtempo);   //creates de Note event

				//if the track don't exists
				if(nt->getTrk()>=Ssal.ntracks())
				{
					char *aux=(char*)"";
					Ssal.addTrack(nt->getTrk(),aux);
				}
				Ssal[nt->getTrk()]->Insert(nt);
			}
			else
			{
				showError("bad line format",1);
			}

		}

	}
	cotn++;

}
/*
if(ks!=NULL)
	Ssal[0]->Insert(ks); //inserts the keysignature event
if(ts!=NULL)
	Ssal[0]->Insert(ts); //inserts the timesignature event
if(tc!=NULL)
	Ssal[0]->Insert(tc); //inserts the tempochange event
*/

midi_ofstream midi_out((char *)outputFile.c_str());

midi_out << Ssal;


}








