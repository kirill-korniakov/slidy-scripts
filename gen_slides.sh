set -e

echo "Start rendering HTML slides from Markdown"

# Get the Git root
root="$(cd .. && git rev-parse --show-toplevel)"
cd $root/slides

python3 "./slidy-scripts/slides-py/test_slides.py"

# Create directory for rendered slides
rendered_slides_dir="$root/slides-rendered"
mkdir -p $rendered_slides_dir
echo "Created directory: $rendered_slides_dir"

# Rendering slides as HTML
echo -e "Processing folders:\n"
for dir in $(ls -d [0-9]*/);
do
    echo "dir = $dir"
    cd $dir

    f=$(find ./ -name '*.md')
    if [[ -z $f ]]
    then
        echo "ERROR: No *.md file"
        # exit 1
    else
        filename=$(basename "$f")
        filename="${filename%.*}"
        rendered="$rendered_slides_dir/$filename.html"
        if [ $f -nt $rendered ]; then
            echo "Processing $f"
            echo "Writing to $rendered"
            pandoc -t slidy -V slidy-url=../slidy-scripts/slidy2 --self-contained -o $rendered $f
        # else
        #     echo "Nothing new to generate..."
        fi
    fi

    echo
    cd ..
done
