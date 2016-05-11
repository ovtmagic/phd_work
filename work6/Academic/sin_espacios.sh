# Cambiar espacios por subrayados a los nombres de fichero del directorio
# indicado y recursivamente por el arbol.
# (si alguien sabe hacerlo de forma mas sencilla, que cambie este script)
# Para ejecutar el script ./sin_espacios.sh <carpeta_a_analizar>
#gsub(" |_,_|,|_\-_|	-|_&_|+|=" , "_");
#!/bin/bash
rename_recursive()
{
   for file in $1/*; do
      if [ -d "$file" ]; then
         rename_recursive "$file"
      else
        #echo -n $file | mv -i "$file" $(awk '{gsub(" ","_"); print}')
        new_file=`echo -n $file | echo $(awk '{
		gsub(" |_,_|,|_\-_|	-|=" , "_");
                gsub("\\\._\\\.|_\\\." , "." );
                gsub("\\\(|\\\)|\"|!|&|\\\[|\\\]|\\\?|{|}|\`" , "");
                gsub("___|__" , "_");
                gsub("coraz=n","corazon");
                gsub("_\\\.",".");
                gsub("/_","/");
                print}' | sed s/\'//g)`
        #new_file=`echo $new_file||sed s/^_//g`
		#gsub(" |_,_|,|_\-_|	-|_&_|\+|=" , "_");
        #echo $new_file
        if [ "$file" != "$new_file" ]
        then
            while [ -e "$new_file" ]
            do
                echo
                echo "El fichero \"$new_file\" existe"
                echo "Introduce un nuevo nombre (con el path completo):"
                read new_file
                
            done
            #echo "* Renombrando " $file " a " $new_file
            mv "$file" "$new_file"
        fi
      fi
   done
}

for dir in $@; do
   dirpath="$PWD/$dir"
   if [ -d "$dirpath" ]; then
      echo "Dir: $dirpath"
      rename_recursive "$dirpath"
   fi
done
