set -e

# Get the Git root
root="$(git rev-parse --show-toplevel)"
cd $root/slides

# Check that the file content indentical to what's in Git now
file=./control-questions.md
if [ $(git diff $file | wc -l) -ge 1 ] ; then
    echo "Error: control questions are not updated! See the diff:" ;
    git --no-pager diff $file ;
    exit 1 ;
else
    echo "Control questions are correct!"
fi
