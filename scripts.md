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
    sed -n 's/.*s_\([^_]\+\)_rating_s\([123]\).*/\1 \2/p' phones/${phone}.html

yields 'battery' twice, first for stand-by time and second for talk time, use awk to compensate, if needed:

    sed -n 's/.*s_\([^_]\+\)_rating_s\([123]\).*/\1 \2/p' phones/${phone}.html | \
    awk '/battery/{c++;if(c==1){sub("battery","standby_time");}else{sub("battery","talk_time");}}1'

### Extract pros and cons bullets from single phone page
     sed -n '/<div class="proscons">/,/<\/div>/p' phones/${phone}.html | sed -n 's/.*<li>\([^<]*\)<.*/\1/p'

### Phones labels CSV header
    echo "phone, size, weight, resolution, display, camera, cpu, ram, standby_time, talk_time, data" > labels.csv

### Phone labels CSV content
     for phone in `cat phones.txt`; do
         echo -n $phone,;
         echo `sed -n 's/.*s_\([^_]\+\)_rating_s\([123]\).*/\2/p' phones/${phone}.html | paste -sd "," -`;
     done >> labels.csv

### Phones pros-cons text file, colon-separated, first value is the phone, the rest are sentences
     for phone in `cat phones.txt`; do
         echo -n $phone"|";
         echo `sed -n '/<div class="proscons">/,/<\/div>/p' phones/${phone}.html | \
         sed -n 's/.*<li>\([^<]*\)<.*/\1/p' | paste -sd "|" -`;
     done > proscons.csv
