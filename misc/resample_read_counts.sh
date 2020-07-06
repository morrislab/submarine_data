#!/bin/bash
set -euo pipefail

BASEDIR=$HOME/work/submarine_data
INDIR=$BASEDIR/no_CNAs
OUTDIR=$SCRATCH/tmp/no_CNAs
PYTHON=python3

function main {
  for pickfn in $INDIR/sim_*/*.truth.pickle; do
    runid=$(basename $pickfn | cut -d. -f1)
    for depth in 30 100 300; do
      new_runid=$(echo $runid | sed 's/_run/_T'$depth'_run/')
      outd=$OUTDIR/$new_runid

      cmd="mkdir -p $outd"
      cmd+=" && $PYTHON $BASEDIR/misc/resample_read_counts.py"
      cmd+=" --depth $depth"
      cmd+=" $pickfn"
      cmd+=" $outd/$new_runid.truth.pickle"
      cmd+=" $outd/$new_runid.ssm"
      cmd+=" && cp -a $INDIR/$runid/$runid.params.json $outd/$new_runid.params.json"
      echo $cmd
    done
  done | parallel -j40 --halt 2 --eta
}

main
