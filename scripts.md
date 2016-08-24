# Scripts
Bash snippets to download data from PhoneArena and extract features.
Snippets assumed to be ran from the data folder.

### Download PhoneArena index pages
```bash
curl -s "http://www.phonearena.com/phones/page/[1-208]" -o "page_#1.html"
```

### Extract phones list:
    sed -n 's|.*href="/phones/\([^"]\+\)".*|\1|p' page_*.html

### Download PhoneArena phone pages using curl
    mkdir phones
    for phone in `cat phones.txt`; do
        if ! [ -f phones/${phone}.html ]; then
            curl -s "http://www.phonearena.com/phones/$phone" -o phones/${phone}.html;
        fi;
    done

### Extract phones pros-cons lists to a colon-separated file, first value is the phone, the rest are sentences
     for phone in `cat phones.txt`; do
         echo -n $phone"|";
         echo `sed -n '/<div class="proscons">/,/<\/div>/p' phones/${phone}.html | \
         sed -n 's/.*<li>\([^<]*\)<.*/\1/p' | paste -sd "|" -`;
     done > proscons.csv

### Extract all unique pros and cons items
There are only about 37 of them

     cat pros_cons.csv | cut -d'|' -f2- | tr "|" "\n" | sed -e 's/^[ \t]*//;s/[ \t]*$//' | sort | uniq > tagged.csv

### Extract all descriptions from phone pages
    
    for phone in `cat phones.txt`; do
        echo -n $phone"|";
        echo `sed -n 's| *<meta name="description" content="\([^"]*\)"/>|\1|p' phones/$phone.html | \
        sed 's/[&#][^;]*;//g'`;
    done > desc.csv

### Download PhoneArena phone reviews using curl
For future reference. I did not have the time to analyze them during this project 

    mkdir reviews
    for phone in `cat phones.txt`; do
        if ! [ -f reviews/${phone}.html ]; then
            curl -s "http://www.phonearena.com/phones/$phone/reviews" -o reviews/${phone}.html;
        fi;
    done