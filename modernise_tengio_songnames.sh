for file in *.m4a
do
    NAME=`birdbrain modernname $file`
    cp $file ./converted/$NAME
    echo $NAME
done
