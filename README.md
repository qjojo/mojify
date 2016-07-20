# mojify
Represent an image with a emoji in the spirit of old school ASCII art

## usage
First generate color comprehension data for your font. I like [twemoji](https://github.com/twitter/twemoji)
```
$ python3 emoji_processor.py ~/path/to/emoji/pngs -a average
Processed 851 emoji, Output in proc.csv
```
then its easy as
```
$ python3 main.py my_image.png
Output in out.txt
```
This was mostly a way for me to learn some data processing and unicode stuff but if you like it that's great!
![dratini](https://github.com/showtimesynergy/mojify/blob/master/example.PNG "dratini!")

