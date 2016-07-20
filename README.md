# mojify
Represent an image with a emoji in the spirit of old school ASCII art

## usage
First generate color comprehension data for your font. I like [twemoji](https://github.com/twitter/twemoji)
```
$ python3 emoji_processor.py ~/path/to/emoji/pngs -a average
Processed 851 emoji, Output in proc.csv
```
Currently there is no user interface and the script must be edited directly to specify the input image
