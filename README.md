# ShopBot

## Prerequisits
The ShopBot requires Python 3.5 with the following packages installed:
- scikit-learn
- pandas
- klein
- nltk with the following resources:
  - Porter stemmer (no download required)
  - Punkt tokenizer models
  - The Brown corpus (only for extracting candidate phrases)

For running the service, execute the following commands, if needed:
    
    $ pip install pip.exe install scikit-learn pandas klein nltk
    $ python
    >>> nltk.download('punkt')

For following the steps for creating a corpus to tag, add

    >>> nltk.download('brown')
    
Alternatively, run `python install.py` for the full installation.
