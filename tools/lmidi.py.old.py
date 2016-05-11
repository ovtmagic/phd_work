#!/usr/bin/python
import os
import re
import math
#import MySQLdb
import platform
from pprint import pprint
import timing
#import subprocess


# Default global variables

if platform.system() == 'Darwin':
    smf2txt_app="/Users/octavio/bin/smf2txt"
    txt2smf_app = "/Users/octavio/bin/txt2smf"
    #weka_app = "java -cp /Applications/weka-3-6-7.app/Contents/Resources/Java/weka.jar"
    weka_app = "java -cp /Applications/weka-3-6-11-oracle-jvm.app/Contents/Java/weka.jar"
elif platform.system() == 'CYGWIN_NT-6.1-WOW64':
    smf2txt_app="/cygdrive/d/bin/smf2txt"
    txt2smf_app = "/cygdrive/d/bin/bin/txt2smf"
    weka_app = "java -cp weka.jar"
else:
    smf2txt_app="/home/octavio/bin/smf2txt"
    txt2smf_app = "/home/octavio/bin/txt2smf"
    weka_app = "java -cp /usr/share/java/weka.jar"


#print ">>>>>",smf2txt_app,"   ",platform.system()

testTime = timing.Timing()


# se eliminan espacios y comillas de un texto
def parse(cad):
    #return cad.replace('\'','').replace('\"','').replace(' ','').lower()
    return cad.replace('\'','').replace(' ','').lower()
    

# Se eliminan las barras verticales que estan entre comillas
def parseVert(cad):
    newcad=""
    comillas=False
    for i in range(0,len(cad)):
        if( cad[i]=="'" ):
            comillas=not comillas
        if not(cad[i]=="|" and comillas):
            newcad=newcad+cad[i]
    return newcad


#===============================================================================
# FUNCIONES DE BASES DE DATOS Mysql
#===============================================================================
#def conecta_mysql(host_db,user_db,passwd_db,db):
#    con = MySQLdb.Connect(host=host_db, port=3306, user=user_db, passwd=passwd_db, db=db)
#    return con


# Insertamos un registro en la base de datos
def inserta_mysql(sql,con):
    cursor = con.cursor()
    cursor.execute(sql)
    con.commit()
    
# Ejecutamos un select y devolvemos todos los registros
def select_mysql(sql,con):
    cursor = con.cursor()
    cursor.execute(sql)
    result=cursor.fetchall()
    return result    

# Ejecutamos un select y devolvemos el primer registro
def select_sql_one(sql,con):
    cursor = con.cursor()
    cursor.execute(sql)
    result=cursor.fetchone()
    return result

#===============================================================================
# Se obtienen las probabilidades de cada pista de un fichero de test (test.arff)
# realizando el entrenamiento con un fichero train.arff
# train_filename: nombre del fichero train.arff o train.model (si se ha creado un modelo)
# test_filename: nombre del fichero test.arff
# debug=True : muestra por stdout las probabilidades obtenidas por Weka para cada pista
#===============================================================================
def get_probabilites(train_filename, test_filename, debug=False):
    prob={}
    if( re.search(".model$",train_filename) ):
        cmd = weka_app + " weka.classifiers.trees.RandomForest -l %s -T %s -p 0 -distribution" % (train_filename, test_filename)
    else:
        cmd = weka_app + " weka.classifiers.trees.RandomForest -K 6 -I 10 -t %s -T %s -p 0 -distribution" % (train_filename, test_filename)
    #print cmd
    testTime.start('D1')
    f=os.popen(cmd)
    cmd_result=f.read().split('\n')
    f.close()
    testTime.stop('D1')
    inst_found=False # busca la cadena "inst#     actual  predicted error distribution" en la salida del comando
    for i in cmd_result:
        if debug:
            print i
        if( inst_found ):
            testTime.start('D2')
            line=i.split()
            if len(line)>=4 :
                track_ord=int(line[0])
                if (line[3]=='+'):
                    p = float(line[4].split(',')[0].replace('*',''))
                else:
                    p=float(line[3].split(',')[0].replace('*',''))
                prob[track_ord]=p
            testTime.stop('D2')
        elif( i.split() and i.split()[0]=='inst#'):
           inst_found=True
    #pprint(prob)
    return prob

#===============================================================================
# get_probabilities devuelve la probabilidad obtenida en weka P(B|i) de que una pista sea
# bajo o no. Esta funcion devuelve las probabilidades P(i|B) de selecciion de
# una pista en un fichero MIDI. Se le pasan las probabilidades P(B|i) obtenidas
# en weka y un umbral para la pista -1 (pista 0 en los papers)
#===============================================================================
def get_prob_iB(prob_argv,tresh):
    # pista 0 (ficticia) con probabilidad igual al umbral. Copiamos el vector prob_argv para no modificar el original
    prob = prob_argv.copy()
    prob[-1] = tresh
    prob_iB = {}
    sum = 0.0
    # calcula la suma de todas las probabilidades P(B|i)
    for i in prob.keys():
        sum = sum + prob[i]
    # calcula la probabilidades P(i|B)
    for i in prob.keys():
        prob_iB[i] = prob[i]/sum
    return prob_iB


#===============================================================================
# Devuelve el numero (orden) de pista con la probabilidad mas alta
# prob: diccionario con la esstructura { 'trac_ord':probability }
#===============================================================================
def select_track_1(prob):
    track=prob.keys()[0]
    max_prob=prob[track]
    for i in prob.keys()[1:]:
        if prob[i]>max_prob:
            max_prob=prob[i]
            track=i
    return (track,max_prob)
    
def select_track_2(prob,tresh=0.25):
    # pista 0 (ficticia) con probabilidad igual al umbral
    prob[-1]=tresh
    sum=0.0  # sum P(B|j)
    #print ">>>>",prob
    for i in prob.keys():
        sum=sum+prob[i]
    #iB = argmax p(i|B)
    track = prob.keys()[0]  
    max_prob = prob[track]
    for i in prob.keys()[1:]:
        if prob[i] >max_prob:
            max_prob = prob[i]
            track = i
    return (track,max_prob)
    
def select_track3(prob,tresh=0.25):
    # pista 0 (ficticia) con probabilidad igual al umbral
    prob[-1]=tresh
    #iB = argmax p(B|i)
    track = prob.keys()[0]  
    max_prob = prob[track]
    for i in prob.keys()[1:]:
        if prob[i] >max_prob:
            max_prob = prob[i]
            track = i
    return (track,max_prob)

def select_track(prob,tresh=0.25):
    prob_iB = get_prob_iB(prob, tresh)
    # Se busca la pista que maximiza iB
    max_prob_iB = 0.0
    max_i = -1
    for i in prob_iB.keys():
        if prob_iB[i] >= max_prob_iB:
            max_prob_iB = prob_iB[i]
            max_i = i
    # devuele el numero de pista (valida) seleccionado en el fichero midi
    return (max_i, max_prob_iB)

def get_precision(TP, FP):
    tp_f = float(TP)
    fp_f = float(FP)
    return tp_f/(tp_f+fp_f)

def get_recall(TP, FN):
    tp_f = float(TP)
    fn_f = float(FN)
    return tp_f/(tp_f+fn_f)
    
def get_f_measure(precision, recall):
    return (2*recall*precision)/(recall+precision)

#===============================================================================
# Tipo de datos Pista
# notas + syline
# descriptores simbolicos
# cada pista tiene un numero (numero de la pista en el fichero midi) Y
# un "orden" (ord) o numero de pista valida, que es el numero de la pista en el 
# fichero arff (despues de eliminar las pistas no validas)
#===============================================================================
class TTrack:
    def __init__(self,name,number,resolution):
        self.name=name      # nombre de la pista
        self.number=number  # numero de pista en el fichero MIDI
        self.valid=False
        self.resolution=resolution
        self.ord=-1         # numero de orden de pista (numnero de pista valida)
        self.notes=[]       # notas 
        self.skyline=[]     # notas skyline
        # descriptores
        self.d={}           # descriptores simbolicos
        
        
    def add(self,data):
        self.notes.append(data)
        
    def add_skyline(self,data):
        self.skyline.append(data)
    
    # set the valid variable
    def set_valid(self):
        if( len(self.skyline) > 1 and self.notes[0]['channel']!=10):
            self.valid = True
        else:
            self.valid = False
    
    # Indicate if the midi track is valid. It has at least 2 notes
    def is_valid(self):
        return self.valid
          
    # Returns the note in position n
    def get_note(self, n):
        return self.notes[n]
    
    # Returns the skyline note in position n
    def get_note_skyline(self, n):
        return self.skyline[n]
    
    # Descriptores -------------------------------------------------------------
    
    # calula todos los descriptores, y se marca indica si la pista es valida
    def gen_descriptors(self):
        self.d["num_notes"]=self._get_num_notes()
        self.d["highest_pitch"]=self._get_highest_pitch()
        self.d["lowest_pitch"]=self._get_lowest_pitch()
        self.d["mean_pitch"]=self._get_mean_pitch()
        self.d["standard_dev_pitch"]=self._get_standard_dev_pitch()
        self.d["largest_pitch_int"]=self._get_largest_pitch_int()
        self.d["smallest_pitch_int"]=self._get_smallest_pitch_int()
        self.d["mean_pitch_int"]=self._get_mean_pitch_int()
        self.d["stdev_pitch_int"]=self._get_stdev_pitch_int()
        
        self.d["longest_note_dur"]=self._get_longest_note_dur()
        self.d["shortest_note_dur"]=self._get_shortest_note_dur()
        self.d["mean_note_dur"]=self._get_mean_note_dur()
        self.d["stdev_note_dur"]=self._get_stdev_note_dur()
        
        self.d["avg_poliphony"]=self._get_avg_poliphony()
        self.d["duration"]=self._get_duration()
        self.d["occupation"]=self._get_occupation()
        self.d["occupation_rate"]=self._get_occupation_rate()
        
    # devuelve el valor de un descriptor
    def getd(self,desc_name):
        return self.d[desc_name]
        
    # normaliza un descriptor en base a los valores maximo y minimo en el resto de pistas
    def normalize(self,descriptor,max_value,min_value):
        n_descriptor="%s_norm" % descriptor
        # si el valor maximo y minimo coinciden, el valor normalizado es 1
        if( max_value==min_value):
            self.d[n_descriptor]=1.0
        else:
            self.d[n_descriptor]=(self.d[descriptor]-min_value)/(max_value-min_value)
            

    # Get the number of notes
    def _get_num_notes(self):
        return float(len( self.notes ))
        
    # Get highest pitch
    def _get_highest_pitch(self):
        pitch=self.notes[0]["pitch"]
        for i in self.notes[1:]:
            pitch=max(pitch,i["pitch"])
        return float(pitch)

    # Get lowest pitch
    def _get_lowest_pitch(self):
        pitch=self.notes[0]["pitch"]
        for i in self.notes[1:]:
            pitch=min(pitch,i["pitch"])
        return float(pitch)

    # Get mean pitch
    def _get_mean_pitch(self):
        summ=0.0
        for j in self.notes:
            summ=summ + float(j["pitch"])
        return summ / len(self.notes)

    # Get standard deviation pitch
    def _get_standard_dev_pitch(self):
        mean=self._get_mean_pitch()
        summ=0.0
        for j in self.notes:
            summ=summ + (float(j["pitch"])-mean)**2
        return math.sqrt( summ/(len(self.notes)-1 ) )

    # get the largest pitch interval
    def _get_largest_pitch_int(self):
        #print "V>>>>>>",len(self.skyline[i]["content"])
        interval=self.skyline[1]["pitch"]-self.skyline[0]["pitch"]
        for j in range(1, len(self.skyline)):
            interval = max( interval , self.skyline[j]["pitch"]-self.skyline[j-1]["pitch"] )
        return float(interval)

    # get the smallest pitch interval
    def _get_smallest_pitch_int(self):
        interval=self.skyline[1]["pitch"]-self.skyline[0]["pitch"]
        for j in range(1, len(self.skyline)):
            interval = min( interval , self.skyline[j]["pitch"]-self.skyline[j-1]["pitch"]) 
        return float(interval)

    # get mean pitch interval
    def _get_mean_pitch_int(self):
        summ=0.0
        for j in range(1, len(self.skyline)):
            summ=summ+ (self.skyline[j]["pitch"]-self.skyline[j-1]["pitch"])
        return float( summ / (len(self.skyline)-1) )

    # Gets standard deviation for pitch intervals
    def _get_stdev_pitch_int(self):
        mean=self._get_mean_pitch_int()
        summ=0.0
        for j in range(1,len(self.skyline)):
            interval=float(self.skyline[j]["pitch"]-self.skyline[j-1]["pitch"])
            summ=summ + (interval-mean)**2
        return math.sqrt( summ / (len(self.skyline)-1) )

    # Gets the longest note duration
    def _get_longest_note_dur(self):
        duration=self.notes[0]["duration"]
        for j in self.notes:
            duration=max(duration, j["duration"])
        return float(duration)/self.resolution

    # Gets the shortest  note duration
    def _get_shortest_note_dur(self):
        duration=self.notes[0]["duration"]
        for j in self.notes:
            duration=min(duration, j["duration"])
        return float(duration)/self.resolution

    # Gets the mean for note durations
    def _get_mean_note_dur(self):
        summ=0.0
        for j in  self.notes:
            summ = summ + j["duration"]
        return float( summ / len(self.notes) )/self.resolution

    # Gets de standard deviation note duration
    def _get_stdev_note_dur(self,):
        mean = self._get_mean_note_dur()
        summ = 0.0
        for j in self.notes:
            summ = summ + ( float(j["duration"])/self.resolution-mean)**2
        return math.sqrt( summ / (len(self.notes)-1) )

    # Gets the avg poliphony
    def _get_avg_poliphony(self): 
        return float(len(self.notes))/float(len(self.skyline))


    # Gets the track duration
    def _get_duration(self):
        return float(self.skyline[len(self.skyline)-1]["onset"]-self.skyline[0]["onset"] + self.skyline[len(self.skyline)-1]["duration"])
        
        
    # Gets the track ocupation. This is the sound duration into a track
    def _get_occupation(self):
        summ=0.0
        for j in range(len(self.skyline)-1):
            note_duration=self.skyline[j]["duration"]
            duration_to_next_note=self.skyline[j+1]["onset"]-self.skyline[j]["onset"]
            summ=summ+min(note_duration,duration_to_next_note)
        # duracion de la ultima nota
        summ=summ+self.skyline[len(self.skyline)-1]["duration"]
        return float(summ)

    # Gets the occupation rate
    def _get_occupation_rate(self):
        duration=self._get_duration()
        occupation=self._get_occupation()
        return occupation/duration






################################################################################
# Applicacion smf2txt
################################################################################
#===============================================================================
# Tipo de datos: Midi
# Contiene el un fichero midi en el formato devuelt por el programa smf2txt
# 
#===============================================================================
class Midi:
    def __init__(self,filename=False,load_skyline=False):
        self.smf2txt = smf2txt_app + " -f \"%p %o %d %v %c\" "
        #self.smf2txt="/Users/octavio/bin/smf2txt -f \"%p %o %d %v %c\" "
        self.filename=filename
        #### --------------------------------------------------------------------
        #### Format esta obsoleto. hay que quitarlo
        #### ----------------------------------------------------------------------
        # format=midi: el fichero de entrada es midi; format=txt, el fichero de entrada se ha obtenido con smf2txt  
        self.format=format
        self.resolution=1   # beats / time
        self.debug=False
        # Notes for MIDI file. MIDI file is readed
        self.tracks={}
        # indica si se ha obtenido el skyline
        self.skyline_readed=False
        # Si se pasa un nombre de fichero como argumento se lee el fichero midi
        if (self.filename):
            self.load_midi(self.filename)
            if(load_skyline):
                self.load_skyline(self.filename)
        # indica si se han obtenido los descriptores
        self.descriptors_obtained=False
        # nombres de la clase para el fichero arff (pe: es pista de bajo, si o no)
        self.class_name=['yes','no']
        self.arff_head=""
        self.arff=""
        #lista de descriptores para construir el fichero arff
        self.descriptors=[
            'avg_poliphony',
            'avg_poliphony_norm',
            'duration_norm',
            'occupation_norm',
            'occupation_rate',
            'occupation_rate_norm',
            'num_notes_norm',
            'lowest_pitch',
            'lowest_pitch_norm',
            'highest_pitch',
            'highest_pitch_norm',
            'mean_pitch',
            'mean_pitch_norm',
            'standard_dev_pitch',
            'standard_dev_pitch_norm',
            'largest_pitch_int',
            'largest_pitch_int_norm',
            'smallest_pitch_int',
            'smallest_pitch_int_norm',
            'mean_pitch_int',
            'mean_pitch_int_norm',
            'stdev_pitch_int',
            'stdev_pitch_int_norm',
            'longest_note_dur',
            'longest_note_dur_norm',
            'shortest_note_dur',
            'shortest_note_dur_norm',
            'mean_note_dur',
            'mean_note_dur_norm',
            'stdev_note_dur',
            'stdev_note_dur_norm',
        ]
        #self.descriptors=['avg_poliphony','duration_norm','occupation_norm','occupation_rate','num_notes']
        #self.descriptors=['highest_pitch','lowest_pitch','num_notes']
        
        

    #=======================================================================
    # EXPERIMENTAL: ser borran las pistas para ganar memoria
    #=======================================================================
    def remove_notes(self):
        for t in self.tracks.keys():
            del self.tracks[t].notes
            del self.tracks[t].skyline
            #x=gc.collect()
        
    # Metodos para leer el fichero MIDI/smf2txt ------------------------------------
    # Gets the track label    
    def getTrackName(self,name):
        # removing "@track" tag
        new_name=name.replace("@track ","")
        # removing number of track
        i=0
        while (new_name[i]!=" "):
            i=i+1
        return new_name[i+1:]

    # Gets the track number
    def getTrackNumber(self,track):
        # removing "@track" tag
        new_track= int(track.replace("@track ","").split()[0])      
        #print ">>>>>>",new_track
        return new_track

    # devuelve el numero de pista del fichero MIDI a partir del numero de "pista valida"
    def get_numbyord(self,num_ord):
        if(num_ord==-1):
            return -1
        for i in self.tracks.keys():
            if self.tracks[i].ord==num_ord:
                return self.tracks[i].number
        return -1
    def gno(self,num_ord):
        return self.get_numbyord(num_ord)
    
    
    
    def load_file(self, file_name, file_format, is_skyline=False):
        #file_content={}
        # obtenemos la informacion simbolica del fichero MIDI utilizando smf2txt
        # se comprueba si se lee el fichero normal o se obtine el skyline
        if(is_skyline):
            if file_format == 'midi':
                f=os.popen(self.smf2txt+" -p 1 " + file_name)
            else:
                f=open(file_name+".sky")


        else:
            if file_format == 'midi':
                f=os.popen(self.smf2txt+" "+file_name)
            else:
                f=open(file_name)

        content=f.read()
        f.close()
        
        track_number=-1
        # search into all file lines
        for l in content.split("\n"):
            # checks if it is reading the line with the resolution
            if( re.search("@resolution",l)):
                self.resolution=float(l.split()[1])
            # checks if it is reading the a new track
            elif( re.search("@track",l)):
                track_number=self.getTrackNumber(l)
                #track_name = parse(self.getTrackName(l))
                track_name = self.getTrackName(l)
                # si se esta obteniendo el skyline no es necesario crear el obtjeto TTrack, ya esta creado
                if( not is_skyline):
                    self.tracks[track_number] = TTrack(track_name,track_number,self.resolution)
            # checks if the line starts with 3 integer number, otherwise: error
            elif re.search('^[0-9]+ [0-9]+ [0-9]+', l):
                # get pitch, onset and duration from l
                l2=l.split()
                if( len(l2) >= 3 and track_number>=0):
                    data={    "pitch":int(l2[0]),
                            "onset":int(l2[1]),
                            "duration":int(l2[2]),
                            "channel": int(l2[4]) 
                    }
                    if(is_skyline):
                        self.tracks[track_number].add_skyline(data)
                    else:
                        self.tracks[track_number].add(data)
        # each track is set to valid or no_valid
        if is_skyline:
            for t in self.tracks.keys():
                self.tracks[t].set_valid()        
             
    #def readSkyline(self):
    #    self.load_midi(True)
    #    self.skyline_readed=True
        
    def load_midi(self, file_name, ):
        self.load_file(file_name, 'midi')
        
    def load_skyline(self, file_name):
        self.load_file(file_name, 'midi', True)
        self.skyline_readed=True
        
    def load_txt(self, file_name):
        self.load_file(file_name,'txt')
    
    
    #----------------------------------------------------------------------------------------
    # calcula los descriptores para todas las pistas validas
    # se considera una pista valida si al menos tiene dos notas en el skyline
    #----------------------------------------------------------------------------------------
    def gen_descriptors(self):
        # Para calcular los descriptores es necesario obtener el skyline
        if( not self.skyline_readed):
            self.load_skyline(self.filename)
        # se calculan los descriptores para las pistas validas
        for i in self.tracks.keys():
            if(self.tracks[i].is_valid()):
                self.tracks[i].gen_descriptors()
        # Se calculan los valores maximo y minimo de cada descriptor en todas las pistas
        desc={}
        for i in self.tracks.keys():
            t=self.tracks[i]
            for d in t.d:
                #buscamos el valor maximo y minimo del descriptor
                if d in desc:
                    desc[d]['max']=max(desc[d]['max'],t.getd(d))
                    desc[d]['min']=min(desc[d]['min'],t.getd(d))
                else:
                    desc[d]={
                        'max':t.getd(d),
                        'min':t.getd(d)
                    }
        # Se obtiene el valor normalizado para todos los descriptores
        for i in self.tracks.keys():
            if( self.tracks[i].is_valid() ):
                for d in desc.keys():
                    self.tracks[i].normalize(d,desc[d]['max'],desc[d]['min'])
        # Se obtiene el numero de orden de cada pista. Solo pistas validas
        ord=1
        for i in self.tracks.keys():
            if( self.tracks[i].is_valid() ):
                self.tracks[i].ord=ord
                ord=ord+1
        #pprint( desc    )
        self.descriptors_obtained=True


    # ARFF ------------------------------------------------
    # se genera la cabecera arff
    def get_arff_header(self,relation_name="relation_name"):
        result="@relation %s\n\n" % relation_name
        for d in self.descriptors:
            result="%s@attribute %s numeric\n" % (result,d)
        result="%s@ATTRIBUTE class { %s %s }\n\n@data\n" % (result,self.class_name[0],self.class_name[1])
        return result
    
    # se devuelven todos los descriptores en formato arff
    # class_ok: lista con los numero de pista que pertenecen a la clase (pe: bass trakcs)
    def get_arff(self, class_ok):
        # si no se han calculado los descriptores se calculan
        if not self.descriptors_obtained:
            self.gen_descriptors()
        result=""
        for i in self.tracks.keys():
            t=self.tracks[i]
            if(t.is_valid()):
                line=""
                for d in self.descriptors:
                    if(line):
                        line="%s,%s" % (line,t.getd(d))
                    else:
                        line="%s" % t.getd(d)
                if t.number in class_ok:
                    line="%s,%s" % (line, self.class_name[0])
                else:
                    line="%s,%s" % (line, self.class_name[1])
                #print line, self.class_ok,t.number
                #result=result+line+"\t\t"+ str(t.number) +"\t"+t.name+" "+str(t.ord)+"\n"
                if self.debug :
                    result="%s%s \t%s\t%s\n" % (result,line,t.number,t.name)
                else:
                    result="%s%s\n" % (result,line)
        return result

    # from an arff file, a pe threshold , the {bass|melody|etc..} track is selected
    def get_selected_track(self, arff_file, midi_file, pe, probabilities={}):
        #testTime.start('C1')
        arff_test = self.get_arff_header("test") + self.get_arff([])
        #testTime.stop('C1')
        #testTime.start('C2')
        
        #testTime.stop('C2')
        #testTime.start('C3')
        if not probabilities:
            f = open("./tmp/" + midi_file + ".arff", "w")
            f.write(arff_test)
            f.close() # se calcula la probabilidad y cual es la pista de bajo
            probabilities = get_probabilites(arff_file, "./tmp/" + midi_file + ".arff", False)
        #testTime.stop('C3')
        #testTime.start('C4')
        track_t, p = select_track(probabilities, pe)
        #testTime.stop('C4') 
        #print short_midi_file,track_t
        #testTime.start('C5')
        track = self.get_numbyord(track_t)
        #testTime.stop('C5')
        return track
    
    # devuelve el tipo de error (tipo 1, 2 o 3, o acierto) en la seleccion de un tipo
    # de pista determinado 
    # type={bass|melody|...}
    # arff_file: fichero arff the entrenamiento
    # pe: umbral
    # csv: fichro csv con las pistas de bajo etiquetadas (indica cual es la pista de bajo)
    def get_selected_error(self, type, arff_file, pe, csv, probabilities={}):
        # midi file name without path
        midi_file=self.filename.split("/")[-1]
        # the type={bass|melody} tack is selected
        #testTime.start('B1')
        track = self.get_selected_track(arff_file, midi_file, pe, probabilities)
        #testTime.stop('B1')
        #testTime.start('B2')
        # error in selection is obtained
        error = csv.error(midi_file, track, type)
        #testTime.stop('B2')
        return error
    
    # devuelve la matriz de confusion (TP, FP, FN, TN)
    # type={bass|melody|...}
    # arff_file: fichero arff the entrenamiento
    # pe: umbral
    # csv: fichro csv con las pistas de bajo etiquetadas (indica cual es la pista de bajo)
    def get_confusion_matrix(self, type, arff_file, pe, csv, probabilities={}):
        # midi file name without path
        midi_file=self.filename.split("/")[-1]
        # the type={bass|melody} track is selected
        track = self.get_selected_track(arff_file, midi_file, pe, probabilities)
        # error in selection is obtained
        return  csv.get_confusion_matrix(midi_file, track, type)
        
    
    
    #===========================================================================
    # Bigrams
    #===========================================================================
    
    
    def bigram_pitch_interval(self,tk_num):
        bigram_counter = {}
        track = self.tracks[tk_num]
        for i in range(2, len(track.skyline)):
            note_0 = track.get_note_skyline(i)['pitch']       # note at n
            note_1 = track.get_note_skyline(i-1)['pitch']   # note at n-1
            note_2 = track.get_note_skyline(i-2)['pitch']   # note at n-2
            interval_2_1 = note_1 - note_2
            interval_1_0 = note_0 - note_1
            if ( not interval_1_0 in bigram_counter.keys() ):
                bigram_counter[interval_1_0] = {}
            if ( not interval_2_1 in bigram_counter[interval_1_0].keys() ):
                bigram_counter[interval_1_0][interval_2_1] = 1
            else:
                bigram_counter[interval_1_0][interval_2_1] += 1
                
        # P(a|b) = bigram[a][b], where a=interval(-2,-1) and b=interval(-1,0)
        bigram={}
        for a in bigram_counter.keys():
            bigram[a]={}
            total_a=0.0
            # total_a is 
            for b in bigram_counter[a].keys():
                total_a += bigram_counter[a][b]
            # P(a|b)= count of b / total_a
            for b in bigram_counter[a].keys():
                prob = float(bigram_counter[a][b]) / total_a
                bigram[a][b] = prob
        return bigram
    
    
    def bigram_pitch(self,tk_num):
        bigram_counter = {}
        track = self.tracks[tk_num]
        for i in range(2, len(track.skyline)):
            note_0 = track.get_note_skyline(i)['pitch']       # note at n
            note_1 = track.get_note_skyline(i-1)['pitch']   # note at n-1
            if ( not note_0 in bigram_counter.keys() ):
                bigram_counter[note_0] = {}
            if ( not note_1 in bigram_counter[note_0].keys() ):
                bigram_counter[note_0][note_1] = 1
            else:
                bigram_counter[note_0][note_1] += 1
                
        # P(a|b) = bigram[a][b], where a=interval(-2,-1) and b=interval(-1,0)
        bigram={}
        for a in bigram_counter.keys():
            bigram[a]={}
            total_a=0.0
            # total_a is 
            for b in bigram_counter[a].keys():
                total_a += bigram_counter[a][b]
            # P(a|b)= count of b / total_a
            for b in bigram_counter[a].keys():
                prob = float(bigram_counter[a][b]) / total_a
                bigram[a][b] = prob
        return bigram
    
    def bigram_pitchtime(self,tk_num):
        res=self.resolution/4   # resolution: /4=semicorchea
        bigram_counter = {}
        track = self.tracks[tk_num]
        for i in range(2, len(track.skyline)-1):
            note_0 = track.get_note_skyline(i)['pitch']       # note at n
            note_1 = track.get_note_skyline(i-1)['pitch']   # note at n-1
            time_0 = int(round(float(track.get_note_skyline(i+1)['onset'] - track.get_note_skyline(i)['onset'])/res)*res) # duration note n
            time_1 = int(round(float(track.get_note_skyline(i)['onset'] - track.get_note_skyline(i-1)['onset'])/res)*res) # duration note n-1
            if ( not (note_0,time_0) in bigram_counter.keys() ):
                bigram_counter[(note_0,time_0)] = {}
            if ( not note_1 in bigram_counter[(note_0,time_0)].keys() ):
                bigram_counter[(note_0,time_0)][(note_1,time_1)] = 1
            else:
                bigram_counter[(note_0,time_0)][(note_1,time_1)] += 1
                
        # P(a|b) = bigram[a][b], where a=interval(-2,-1) and b=interval(-1,0)
        bigram={}
        for a in bigram_counter.keys():
            bigram[a]={}
            total_a=0.0
            # total_a is 
            for b in bigram_counter[a].keys():
                total_a += bigram_counter[a][b]
            # P(a|b)= count of b / total_a
            for b in bigram_counter[a].keys():
                prob = float(bigram_counter[a][b]) / total_a
                bigram[a][b] = prob
        return bigram
            
################################################################################
#
# Clase para gestionar los ficheros CSV con los diferentes tipos de pista
#
#
################################################################################
class TCsv:
    def __init__(self,file_csv):
        self.dic = self._read_csv(file_csv)
        self.tags = ['melody','bass','piano_rh','piano_lh','mixdown']
        
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



#===================================================================================
#
# Clase para generar ficheros ARFF
#
#
#===================================================================================

    
class TArff:
    def __init__(self,filename,class_ok):        
        self.class_ok = class_ok
        self.midifile = Midi(filename)
        self.midifile.load_skyline(filename)
        self.midifile.gen_descriptors()
        #
        self.name = "name"
        self.class_name =["ok","no"]
        
    # se genera la cabecera arff
    def get_header(self):
        result="@relation %s\n\n" % self.name
        for d in self.descriptors:
            result="%s@attribute %s numeric\n" % (result,d)
        result="%s@ATTRIBUTE class { %s %s }\n\n@data\n" % (result,self.class_name[0],self.class_name[1])
        return result
        

    # se devuelven todos los descriptores en formato arff
    def get(self):
        result=""
        for i in self.midifile.tracks.keys():
            t=self.midifile.tracks[i]
            if(t.is_valid()):
                line=""
                for d in self.descriptors:
                    if(line):
                        line="%s,%s" % (line,t.getd(d))
                    else:
                        line="%s" % t.getd(d)
                if t.number in self.class_ok:
                    line="%s,%s" % (line, self.class_name[0])
                else:
                    line="%s,%s" % (line, self.class_name[1])
                #print line, self.class_ok,t.number
                #result=result+line+"\t\t"+ str(t.number) +"\t"+t.name+" "+str(t.ord)+"\n"
                result=result+line+"\n"
        return result
    
    
    
    
#===============================================================================
# Aplicacion txt2smf
#===============================================================================
class Ttxt2smf:
    # Constructor:
    # Ttxt2sms( m ) -> m es un objeto Tsmf2txt
    # Ttxt2sms( filename, resolution )
    def __init__(self, arg1, resolution=1):
        self.tracks = {}
        self.txt2sms = txt2smf_app
        # se comprueba si argv1 es el nombre
        if type(arg1) is str:
            self.filename = arg1
            self.resolution = resolution
        # argv1 es un objeto Tsmf2txt. Se importan las pistas de argv1
        else:
            self.filename = arg1.filename
            self.resolution = arg1.resolution
            for track_id in arg1.tracks.keys():
                track = arg1.tracks[track_id]
                self.add_track(track)
       
    # Indica el directorio donde se va a crear el fichero MIDI 
    def set_name(self, filename):
        self.filename = filename
        
    # Anade una pista que se pasa como argumento. si no se pasa ninguna
    # pista se crea una vacia. Devuelve el numero de pista creada 
    def add_track(self, track=False):
        #print type(track)
        num_track = len(self.tracks) + 1
        # se copia la pista 
        if track:
            self.tracks[num_track] = track
        # si no se pasa ninguna pista, se crea una vacia
        else:
            self.tracks[num_track] = TTrack('', num_track, self.resolution)
        return num_track
    
    # Crea un fichero de texto (en formato smf2txt) con las pistas que se 
    # pasan como arugmento. track_list es un array de enteros
    def get_txt(self, track_list, skyline=False):
        print self.resolution
        result = '# path %s\n' % (self.filename)
        result = result + '@resolution %s\n' % self.resolution
        result = result + '@format "%p %o %d %v"\n'
        # se obtienen las pistas indicadas en track_list. Si track_list no contiene
        # ninguna pista, se obtienen todas las pistas
        for i in track_list or self.tracks.keys():
            result = result + "@track %s %s\n" % (i, self.tracks[i].name) 
            if(skyline):
                for line in self.tracks[i].skyline:
                    result = result + "%s %s %s 127\n" % (line['pitch'], line['onset'], line['duration'])
            else:
                for line in self.tracks[i].notes:
                    result = result + "%s %s %s 127\n" % (line['pitch'], line['onset'], line['duration'])
        # se devuelve el resultado sin el ultimo \n
        return result[:-1]
    
    # Crea el fichero midi
    def create_midi(self, track_list, skyline=False):
        filename = self.filename
        print filename
        cmd = "%s -i %s -o %s" % (self.txt2sms, filename + ".txt", filename)
        print cmd
        # se crea el fichero de texto con txt2smf
        f = open(filename + ".txt", "w")
        f.write(self.get_txt(track_list, skyline))
        f.close()
        # se crea el fichero MIDI
        f = os.popen(cmd)
        f.read()
        f.close()
