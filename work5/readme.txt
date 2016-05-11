* Obtiene un histograma con la posici—n normalizada de la pista del bajo

* Ejecuci—n:

run.py <csv file> <bass|melody>





* lmidi.py: Se ha cambiado la librer’a. Ahora la clase se llama "Midi" en lugar
de TSmf2txt. Los metodos para cargar un fichero midi son:
	Midi.load_midi(file_name)
	Midi.load_skyline(file_name)
	
Para generar descriptores:
x = Midi()
x.load_midi(file_name)
x.load_sky_line(file_name)
x.gen_descriptors.