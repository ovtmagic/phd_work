if [ $# -ne 1 ]; then
	echo "Missing folder"
	exit 1
fi

CP=""
FOLDERS="lib"

for folder in $FOLDERS; do
	for jarfile in ${folder}/*.jar; do
		CP=${CP}:$jarfile
	done
done

#echo $CP
java  -Xmx3000m -Xms1024m  -cp $CP es.ua.dlsi.im.corpus.repetitions.FolderSongRepetitionsFinder $1
