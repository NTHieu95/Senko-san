from PIL import Image,ImageDraw,ImageFont
import os

def breakingtext(string):
    stringlist = string.split(' ')
    outputstring = ""
    line = ""

    for word in stringlist:
        
        line = line + word + " " 
        # print(line)
        sumlen=len(line) + len(word)
        if sumlen >=12 or stringlist[-1] == word:
            line = line + "\n"
            outputstring = outputstring + line
            line = ""

    # print(stringlist)
    # print(outputstring)
    return outputstring

def slap(string):
    #setting varibles
    imgFile = "slap.jpg"
    output = "slapout.jpg"
    font = ImageFont.truetype("ArialUnicodeMS.ttf", 30)
    text = breakingtext(string) 
    textColor = 'white'
    shadowColor = 'black'
    outlineAmount = 3

    #open image
    img = Image.open(imgFile)
    draw = ImageDraw.Draw(img)

    #get the size of the image
    imgWidth,imgHeight = img.size

    #get text size
    txtWidth, txtHeight = draw.textsize(text, font=font)

    #get location to place text
    x = imgWidth - txtWidth - 310
    y = imgHeight - txtHeight - 135

    #create outline text
    for adj in range(outlineAmount):
        #move right
        draw.text((x-adj, y), text, font=font, fill=shadowColor)
        #move left
        draw.text((x+adj, y), text, font=font, fill=shadowColor)
        #move up
        draw.text((x, y+adj), text, font=font, fill=shadowColor)
        #move down
        draw.text((x, y-adj), text, font=font, fill=shadowColor)
        #diagnal left up
        draw.text((x-adj, y+adj), text, font=font, fill=shadowColor)
        #diagnal right up
        draw.text((x+adj, y+adj), text, font=font, fill=shadowColor)
        #diagnal left down
        draw.text((x-adj, y-adj), text, font=font, fill=shadowColor)
        #diagnal right down
        draw.text((x+adj, y-adj), text, font=font, fill=shadowColor)

    #create normal text on image
    draw.text((x,y), text, font=font, fill=textColor)

    img.save(output)
    # print('Finished')
    # os.startfile(output)
slap("nguyen trung kien")
