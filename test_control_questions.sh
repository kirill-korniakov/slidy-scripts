set -e

# Get the Git root
root="$(git rev-parse --show-toplevel)"
cd $root/slides

# Extract control questions
python3 ./slidy-scripts/slides-py/extract-control-questions.py

# Compare with what's in Git now
file=./control-questions.md
if [ $(git diff $file | wc -l) -ge 1 ] ; then
    echo "Error: control questions are not updated! See the diff:" ;
    git --no-pager diff $file ;
    exit 1 ;
else
    echo "Control questions are correct"
fi
