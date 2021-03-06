################################################################################
#
# Clase para gestionar los ficheros CSV con los diferentes tipos de pista
#
#
################################################################################
class TCsv:
    def __init__(self,file_csv):
        self.numtracks={}
        self.dic = self._read_csv(file_csv)
        self.tags = ['melody','bass','piano_rh','piano_lh','mixdown','accomp']
        
    # convierte la lista de numeros de pista en un array de enteros
    def _list_to_int(self,list_txt):
        list_int=[]
        for i in list_txt.replace('"','').split(' '):
            if(i):
                list_int.append(int(i))
        return list_int
        
    # lee el fichero csv con los tipos de pista de cada fichero MIDI
    def _read_csv(self,file_csv):
        dic={}
        f=open(file_csv)
        lines=f.read().split("\n")
        for l in lines[1:]:
            if l:
                #print ">>>%s<<<" %l
                name=l.split(',')[0].replace('"','')
                #print ">>>>>",name
                self.numtracks[name]=int(l.split(',')[1])
                if len(l.split(',')) > 7:
                    dic[name]={
                        'melody': self._list_to_int( l.split(',')[2] ),
                        'bass': self._list_to_int( l.split(',')[3] ),
                        'piano_rh':self._list_to_int( l.split(',')[4] ),
                        'piano_lh':self._list_to_int( l.split(',')[5] ),
                        'mixdown':self._list_to_int( l.split(',')[6] ),
                        'accomp':self._list_to_int( l.split(',')[7] ),
                    }
                else:
                    dic[name]={
                        'melody': self._list_to_int( l.split(',')[2] ),
                        'bass': self._list_to_int( l.split(',')[3] ),
                        'piano_rh':self._list_to_int( l.split(',')[4] ),
                        'piano_lh':self._list_to_int( l.split(',')[5] ),
                        'mixdown':self._list_to_int( l.split(',')[6] ),
                    }
        return dic

    # Devuelve las pistas de un fichero MIDI que pertenecen a un tipo 
    # determinado. p.e: name=pepito.mid, track_type="melody"
    def get(self,name,track_type):
        if name in self.dic.keys():
            return self.dic[name][track_type]
        else:
            return -1
    
    # Devuelve las etiquetas de una pista determinada de un fichero
    # solo devuelve la primera etiqueta que encuentre
    def get_tag_by_track(self, name, track):
        for track_type in self.tags:
            if track in self.dic[name][track_type]:
                return track_type
        return ""    
    
    # Devuelve el numero de pistas de un fichero midi
    def get_num_tracks(self, name):
        return self.numtracks[name]
        
           
    # Devuelve los nombre de los ficheros midi
    def get_files(self):
    	return self.dic.keys()

    # indica el tipo de error (tipo1=1, tipo2=2 o tipo3)=3
    # si no hay error devuelve 0
    def error(self,filename,track_selected,filetype):
        # no hay error
        if (track_selected in self.dic[filename][filetype]) or (track_selected==-1 and not self.dic[filename][filetype]):
            return 0
        # error tipo 1
        elif track_selected!= -1 and self.dic[filename][filetype] and track_selected not in self.dic[filename][filetype]:
            return 1
        # error tipo 2
        elif  not self.dic[filename][filetype] and track_selected!=-1:
            return 2
        # error tipo 3
        elif self.dic[filename][filetype] and track_selected==-1:
            return 3
        # otro error ????
        else:
            return -1
            
    # Devuelve la matriz de confusion (TP, FP, FN, TN)
    def get_confusion_matrix(self,filename,track_selected,filetype):
        #  TP
        if (track_selected != -1 and track_selected in self.dic[filename][filetype]):
            return (1,0,0,0)
        # FP
        elif track_selected != -1 and track_selected not in self.dic[filename][filetype]:
            return (0,1,0,0)
        # FN
        elif  track_selected == -1 and self.dic[filename][filetype]:
            return (0,0,1,0)
        # error tipo 3
        elif track_selected == -1 and not self.dic[filename][filetype]:
            return (0,0,0,1)
        # otro error ????
        else:
            print "KK",track_selected,self.dic[filename][filetype]
            return -1

