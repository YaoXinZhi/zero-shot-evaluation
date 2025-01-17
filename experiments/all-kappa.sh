DOCS="1 2 3 4 5 6 7 8 9 10 11 12 13"
MODELS="gpt-4o-mini kimi"

echo -n -e 'Document'
for m in $MODELS
do
    echo -n -e '\t'$m
done
echo

for doc in $DOCS
do
    echo -n Texte$doc
    for m in $MODELS
    do
	echo -n -e '\t'
	if [ -f output/repetition/$m/scenario/Texte$doc/1.txt ]
	then
	    echo -n -e $(./kappa.py -m $m -i scenario -d Texte$doc)'\t'
	fi
    done
    echo
done
