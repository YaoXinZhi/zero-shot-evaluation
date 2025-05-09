CORPORA="EPOP BB4 TAEC"
SETS="train dev"


SCRIPT=./bionlpst2json.py


for corpus in $CORPORA
do
    typemap=corpus/typemap/$corpus.json
    for st in $SETS
    do
	indir=corpus/bionlp-st/$corpus/$st/
	outdir=corpus/json/$corpus/$st/
	$SCRIPT $typemap $indir $indir $outdir
    done
done

