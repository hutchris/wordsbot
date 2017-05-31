try:
    import os
    import sys
    import pandas as pd
    from pytrends.request import TrendReq
    from PIL import Image, ImageDraw, ImageFont
    from datetime import datetime
    import tweepy
    import yaml
   
    baseDir = os.path.dirname(os.path.abspath(__file__))
     
    def addLog(logFile,message):
        if os.path.exists(logFile):
            append_write = "a"
        else:
            append_write = "w"
        with open(logFile,append_write) as logFileObj:
            dateStr = datetime.now().isoformat()
            logFileObj.write("{d} : {m}\n".format(d=dateStr,m=message))

    if os.path.exists("config.yml"):
        with open("config.yml","r") as yamlFile:
            params = yaml.load(yamlFile)    
        logFilePath = os.path.join(params['logFile'])
        addLog(logFilePath,"loaded params from config")
    else:
        print("no config.yml file detected, exiting")
        sys.exit()

    #csv params
    csvFileName = params['csvFile']
    csvFilePath = os.path.join(baseDir,csvFileName)

    #pytrends params
    googleUsername = params['google']['username']
    googlePassword = params['google']['password']

    #PIL params
    baseImg = params['baseImgFile']
    imgDir = os.path.join(baseDir,"images")
    fontFileName = params['fontFile']
    fontFile = os.path.join(baseDir,fontFileName)

    #twitter params
    hashtags = params['twitter']['hashtags']
    CK = params['twitter']['consumerKey']
    CS = params['twitter']['consumerSecret']
    AK = params['twitter']['accessKey']
    AS = params['twitter']['accessSecret']
    
    dataFrame = pd.DataFrame.from_csv(csvFilePath)
    words = dataFrame['Word'].sample(5)
    wordsList = words.tolist()

    addLog(logFilePath,"selected words: {w}".format(w=wordsList))

    pytrends = TrendReq(googleUsername,googlePassword)
    pytrends.build_payload(wordsList,timeframe='now 7-d')
    trendsDataFrame = pytrends.interest_over_time()

    addLog(logFilePath,"connected to google trends")

    maxes = trendsDataFrame.max().to_dict()
    maxest = 0
    for k,v in maxes.items():
        if v > maxest:
            word = k
            maxest = v

    addLog(logFilePath,"selected word: {w}".format(w=word))

    #remove word from csv
    dataFrameOut = dataFrame[dataFrame['Word']!=word]
    dataFrameOut.to_csv(csvFilePath)

    addLog(logFilePath,"saved csv sans word")

    #create image of word
    img = Image.open(baseImg)
    imgWidth,imgHeight = img.size
    draw = ImageDraw.Draw(img)
    myFont = ImageFont.truetype(fontFile,42)
    textWidth,textHeight = draw.textsize(word,font=myFont)
    x = (imgWidth/2)-(textWidth/2)
    y = (imgHeight/2)-(textHeight/2)
    draw.text((x,y),word,(100,100,100),font=myFont)
    imgFile = "{w}.jpg".format(w=word)
    imgPath = os.path.join(imgDir,imgFile)
    img.save(imgPath)

    addLog(logFilePath,"created image called: {f}".format(f=imgFile))

    #tweet word
    auth = tweepy.OAuthHandler(CK,CS)
    auth.set_access_token(AK,AS)
    api = tweepy.API(auth)
    tweetResp = api.update_with_media(imgFile,status="{w} {h}".format(w=word,h=hashtags))

    addLog(logFilePath,"tweet sent")

except Exception as err:
    addLog(logFilePath,"error occured: {e}".format(e=err))
