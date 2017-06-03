# wordsbot
Twitter bot for posting random words as design inspiration. Uses a list of 5000 of the most popular english words. Picks a sample of words each day then uses the Google trends API to pick a word that is more likely to be popular.

1. Create config file:

  cp example_config.yml config.yml
  
2. Create images dir:

  mkdir images
  
3. Use original words csv:

  mv 5000words.csv.ori 5000words.csv


Words list sourced from here: http://www.wordfrequency.info/intro.asp
