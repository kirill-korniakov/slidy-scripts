python3 ./slides/slidy-scripts/slides-py/extract-control-questions.py
file=./slides/control-questions.md
if [ $(git diff $file | wc -l) -ge 1 ] ; then
    echo "Error: control questions are not updated! See the diff:" ;
    git --no-pager diff $file ;
    exit 1 ;
fi
