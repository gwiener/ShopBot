# Scripts
Bash snippets to download data from PhoneArena and extract features.
Snippets assumed to be ran from the data folder.

### Download PhoneArena index pages
    curl -s "http://www.phonearena.com/phones/page/[1-208]" -o "page_#1.html"

### Extract phones list:
    sed -n 's|.*href="/phones/\([^"]\+\)".*|\1|p' page_*.html

### Download PhoneArena phone pages using curl
    mkdir phones
    for phone in `cat phones.txt`; do
        if ! [ -f phones/${phone}.html ]; then
            curl -s "http://www.phonearena.com/phones/$phone" -o phones/${phone}.html;
        fi;
    done

### Download PhoneArena phone reviews using curl
    mkdir reviews
    for phone in `cat phones.txt`; do
        if ! [ -f reviews/${phone}.html ]; then
            curl -s "http://www.phonearena.com/phones/$phone/reviews" -o reviews/${phone}.html;
        fi;
    done

### Extract image-based features from a single phone page
    sed -n 's/.*s_\([^_]\+\)_rating_s\([123]\).*/\1: \2/p' phones/${phone}.html

yields 'battery' twice, first for stand-by time and second for talk time, use awk to compensate, if needed:

    sed -n 's/.*s_\([^_]\+\)_rating_s\([123]\).*/\1 \2/p' phones/${phone}.html | \
    awk '/battery/{c++;if(c==1){sub("battery","standby_time");}else{sub("battery","talk_time");}}1'

### Extract pros and cons bullets from single phone page
     sed -n '/<div class="proscons">/,/<\/div>/p' phones/${phone}.html | sed -n 's/.*<li>\([^<]*\)<.*/\1/p'

### Phones labels CSV header
    echo "phone, size, weight, resolution, display, camera, cpu, ram, standby_time, talk_time, data" > labels.csv

### Phone labels CSV content
**test convert this to JSON list of dictionaries**
     
     echo [ > labels.json
     for phone in `cat phones.txt`; do 
         echo -n "{'phone':\"$phone\","; 
         echo -n `sed -n 's/.*s_\([a-z_]\+\)_rating_s\([123]\).*/"\1":\2/p' phones/$phone.html | \
         awk '/battery/{c++;sub("battery", "battery"c);}1' | paste -sd "," -`; echo },; 
     done >> labels.json
     head -c -1 labels.json > foo # remove last comma
     mv foo labels.json
     echo ] >> labels.json
     

### Phones pros-cons text file, colon-separated, first value is the phone, the rest are sentences
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