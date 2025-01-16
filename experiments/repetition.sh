REPS="1 2 3 4 5"
INST="ner+rel scenario short"
DOCS="2 5 10"
#MODELS="mistral gpt-4o-mini"
MODELS="gpt-4o-mini"

BASE=experiments/repetition

for mod in $MODELS
do
    for inst in $INST
    do
	instfile="instruction_$inst.txt"
	for doc in $DOCS
	do
	    docname="Texte$doc"
	    docfile="example-docs/$docname.txt"
	    for rep in $REPS
	    do
		outfile=$BASE/$mod/$inst/$docname/$rep.txt
		./run.py -m $mod -i $instfile -d $docfile -o $outfile
	    done
	done
    done
done
