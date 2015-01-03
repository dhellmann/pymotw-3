#!/bin/bash
#
# Run cog to process reST files.

BEGIN_SPEC='{{{cog'
END_SPEC='}}}'
END_OUTPUT='{{{end}}}'

files="$*"
if [ -z "$files" ]
then
    files=$(find source -name '*.rst')
fi

for f in $files
do
    cog.py \
        --begin-spec="$BEGIN_SPEC" \
        --end-spec="$END_SPEC" \
        --end-output="$END_OUTPUT" \
        -r \
        $f
done
