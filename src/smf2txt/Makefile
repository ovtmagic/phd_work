# you may need to change these for your system
CFLAGS	= #-static
MAKE	= make
CC	= g++ -Wall -O3
RM	= /bin/rm
LIB	= ./lib
OBJ	= $(LIB)/common.o $(LIB)/song.o $(LIB)/m_ifstrm.o $(LIB)/m_ofstrm.o $(LIB)/midieven.o 
DOC	= /home/snn/cemgil/bin/doc++
DOCIFY	= /home/snn/cemgil/bin/docify

all: smf2txt txt2smf

smf2txt: $(OBJ) smf2txt.cpp txt2smf
	$(CC) $(CFLAGS) -o $@ smf2txt.cpp $(OBJ)

txt2smf: $(OBJ) txt2smf.cpp 
	$(CC) $(CFLAGS) -o $@ txt2smf.cpp $(OBJ)
 

$(LIB)/common.o: $(LIB)/common.cpp $(LIB)/common.h
	$(CC) $(CFLAGS) -o $(LIB)/common.o  -c $*.cpp

$(LIB)/song.o: $(LIB)/song.cpp $(LIB)/song.h $(LIB)/m_ofstrm.h $(LIB)/m_ofstrm.h
	$(CC) $(CFLAGS) -o $(LIB)/song.o -c $*.cpp

$(LIB)/m_ifstrm.o: $(LIB)/m_ifstrm.cpp $(LIB)/m_ifstrm.h $(LIB)/common.h
	$(CC) $(CFLAGS)  -o $(LIB)/m_ifstrm.o  -c $*.cpp

$(LIB)/midieven.o: $(LIB)/midieven.cpp $(LIB)/midieven.h
	$(CC) $(CFLAGS)  -o $(LIB)/midieven.o  -c $*.cpp

$(LIB)/m_ofstrm.o: $(LIB)/m_ofstrm.cpp $(LIB)/m_ofstrm.h $(LIB)/common.h
	$(CC) $(CFLAGS) -o $(LIB)/m_ofstrm.o  -c $*.cpp

doc:
	$(DOCIFY) common.h common.h.doc
	$(DOCIFY) midieven.h midieven.h.doc
	$(DOCIFY) song.h song.h.doc        
	$(DOCIFY) m_ifstrm.h m_ifstrm.h.doc
	$(DOCIFY) m_ofstrm.h m_ofstrm.h.doc
	$(DOC) -d html `ls -1 *.h.doc`

clean:
	rm $(LIB)/*.o smf2txt txt2smf





