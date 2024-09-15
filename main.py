import discord
# client = discord.Client()
# reaction = discord.Reaction()
from keep_alive import keep_alive
import io, sys, urllib3, os, re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import zipfile
import imageio
from ffmpegpython import ffmpeg
import random
import glob
from mocking import mocking
from slap import slap
from pat import pat
from nameandemotefilter import nameAndEmoteFilter
from imagesoup import ImageSoup
# <:pikak:595999028240711691> <:okaynano:600017907296239617> <:lul:596361171049644032> <:cmonBruh:596003871319392287> <:BlackPepeHands:596024669685940234> <:engry:595473608973877254>
import tweepy
from pixivpy3 import *
import requests
import json
import convert

from dotenv import load_dotenv, dotenv_values 

load_dotenv() 

# Update collections for ffmpeg
import collections
collections.Iterable = collections.abc.Iterable

from googlesearch import search
# except ImportError:
#     print("No module named 'google' found")

pixiv_login = os.environ.get('PIXIV_EMAIL')
pixiv_password = os.environ.get('PIXIV_PW')
# print(pixiv_login, pixiv_password)
# print(pixiv_login,pixiv_password)
consumer_key = os.environ.get('COMSUMER_KEY')
consumer_secret = os.environ.get('COMSUMER_SECRET')
access_token_key = os.environ.get('ACCESS_TOKEN_KEY')
access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)
twitterapi = tweepy.API(auth)

marry = 0
divorce = 0
marryPartner = divorcePartner = marryProposer = divorceProposer = ''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = discord.Client(intents=intents)


def quack(string):
    string = list(string.lower())
    # print(string)
    for i in range(len(string)):
        if i % 2 == 0:
            string[i] = string[i].capitalize()
    return "".join(string)


def userFilterNick(string):
    list1 = string.split('<@!')
    print(list1)
    list2 = []
    for i in range(len(list1) - 1):
        list2.append(str(list1[i + 1]).split('>')[0])
    return list2


def userFilterOrig(string):
    list1 = string.split('<@')
    print(list1)
    list2 = []
    for i in range(len(list1) - 1):
        list2.append(str(list1[i + 1]).split('>')[0])
    return list2


def userIdFilter(string):
    if string.find('<@!') >= 0:
        return string.split('<@!')[1].split('>')[0]
    elif string.find('<@') >= 0:
        return string.split('<@')[1].split('>')[0]
    else:
        return ''


def jankenResult(senko, player):
    # if string == "bao":
    #     return -1
    # if string == "búa":
    #     return 0
    # if string == "kéo":
    #     return 1
    # else:
    #     return False
    if senko == player:
        return 0
    elif (senko == "bao" and player == "búa") \
    or (senko == "búa" and player == "kéo") \
    or (senko == "kéo" and player == "bao"):
        return -1  #player lose
    elif (senko == "bao" and player == "kéo") \
    or (senko == "búa" and player == "bao") \
    or (senko == "kéo" and player == "búa"):
        return 1  #player win


@client.event
async def on_ready():
    print("The bot is ready!")
    # await client.change_presence(game=discord.Game(name="Making a    bot"))
    # await client.get_channel(462170934196043799).send('Ta dậy rồi nanoja!')


@client.event
async def on_disconnect():
    print("The bot went to sleep!")
    # await client.change_presence(game=discord.Game(name="Making a    bot"))
    # await client.get_channel(462170934196043799).send('Ta đi ngủ trước đây nanoja!')


@client.event
async def on_member_join(member):
    await member.add_roles(member.guild.get_role(595122392850890752))
    for channel in member.guild.channels:
        if str(
            channel.name
        ) == "introduction":  # We check to make sure we are sending the message in the general channel

            await channel.send(
                'Xin chào ' + member.mention +
                ' đến với Ổ Dịch nanoja <:HinataYeah:597953425149394950>! Hãy **giới thiệu bản thân** và đọc '
                + client.get_channel(595127051418206218).mention +
                ' để hiểu rõ hơn về server này nhé nanoja <:HinataYeah:597953425149394950>!'
            )


@client.event
async def on_member_remove(member):
    for channel in member.guild.channels:
        if str(
            channel.name
        ) == "general-talk":  # We check to make sure we are sending the message in the general channel

            await channel.send('Tạm biệt *' + member.mention + '*(' +
                               str(member) + ')' +
                               '<:Aqua_cry:595633225637036043>')


@client.event
async def on_message(message):
    print(str(message.author.id) + ' ' + str(message.author))
    # print(nameAndEmoteFilter(message.content,client))
    print(message.channel.id, message.channel)
    # print(userFilter(str(message.content)))

    user = message.author
    read = open("list.txt", "r", encoding="utf-8")
    text = read.read()
    # print(text)
    if str(user.id) not in text:
        output = open("list.txt", "a+", encoding="utf-8")
        output.write(str(user.id) + ": " + user.name + '\n')
        output.close()
    read.close()
    print("text1")
    print(message, message.content)
    if message.author == client.user:
        return
    print("text2")
    read = open("blacklist.txt", "r", encoding="utf-8")
    text = read.read()
    read.close()
    # if one knows how to apology, delete the one's id from blacklist
    with open("blacklist.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
    if (message.content != None):
        if (message.content.lower() == "xin lỗi senko"
            and str(user.id) in text):
            os.remove("blacklist.txt")
            rewrite = open("blacklist.txt", "w+", encoding="utf-8")
            for line in lines:
                if str(user.id) not in line:
                    rewrite.write(line)
            rewrite.close()
            message.content = "OK..."
            await message.channel.send("OK...")
    print("text3")
    # Check if the one who just spoke in the blacklist or not, if yes: angry and mock him
    read = open("blacklist.txt", "r", encoding="utf-8")
    text = read.read()
    read.close()
    if str(user.id) in text:
        # self.reactToMessage(message_object.uid,MessageReaction.ANGRY)
        # message.content = quack(message.content)
        mocking(quack(nameAndEmoteFilter(message.content, client)))
        # await message.channel.send(quack(message.content))
        emoji = '<:pikak:595999028240711691>'
        await message.add_reaction(emoji)
        await message.channel.send(file=discord.File('output.jpg'))
        await message.channel.send(user.mention)
        await message.channel.send(user.mention)
        await message.channel.send(user.mention)
        # self.send(message_object, thread_id=thread_id, thread_type=thread_type)
    else:
        print("text4")
        # You mess with the wrong bot, motherfucker
        # if (message.content.lower().find("địt") >= 0 and message.content.lower().find("bot") >= 0) \
        # or (message.content.lower().find("đm") >= 0 and message.content.lower().find("bot") >= 0) \
        # or (message.content.lower().find("đ ") >= 0 and message.content.lower().find("bot") >= 0) \
        # or (message.content.lower().find("ngu") >= 0 and message.content.lower().find("bot") >= 0) \
        # or (message.content.lower().find("chó") >= 0 and message.content.lower().find("bot") >= 0) \
        # or (message.content.lower().find("lồn") >= 0 and message.content.lower().find("bot") >= 0) \
        # or (message.content.lower().find("phò") >= 0 and message.content.lower().find("bot") >= 0) \
        # or (message.content.lower().find("buồi") >= 0 and message.content.lower().find("bot") >= 0) \
        # or (message.content.lower().find("cax") >= 0 and message.content.lower().find("bot") >= 0) \
        # or (message.content.lower().find("dm") >= 0 and message.content.lower().find("bot") >= 0) \
        # or (message.content.lower().find("dkm") >= 0 and message.content.lower().find("bot") >= 0) \
        # or (message.content.lower().find("đkm") >= 0 and message.content.lower().find("bot") >= 0) \
        # or \
        
        if (message.content.lower().find("địt") >= 0 and message.content.lower().find("senko") >= 0) \
        or (message.content.lower().find("đm") >= 0 and message.content.lower().find("senko") >= 0) \
        or (message.content.lower().find("đ ") >= 0 and message.content.lower().find("senko") >= 0) \
        or (message.content.lower().find("ngu") >= 0 and message.content.lower().find("senko") >= 0) \
        or (message.content.lower().find("chó") >= 0 and message.content.lower().find("senko") >= 0) \
        or (message.content.lower().find("lồn") >= 0 and message.content.lower().find("senko") >= 0) \
        or (message.content.lower().find("phò") >= 0 and message.content.lower().find("senko") >= 0) \
        or (message.content.lower().find("buồi") >= 0 and message.content.lower().find("senko") >= 0) \
        or (message.content.lower().find("cax") >= 0 and message.content.lower().find("senko") >= 0) \
        or (message.content.lower().find("dm") >= 0 and message.content.lower().find("senko") >= 0) \
        or (message.content.lower().find("dkm") >= 0 and message.content.lower().find("senko") >= 0) \
        or (message.content.lower().find("đkm") >= 0 and message.content.lower().find("senko") >= 0):
            emoji = '<:REEEEE:656417641883500545>'
            await message.add_reaction(emoji)
            if message.author.dm_channel == None:
                await message.author.create_dm()
            await message.author.dm_channel.send('Xong đời mày rồi, con chó ạ!'
                                                 )
            blacklist = open("blacklist.txt", "a+", encoding="utf-8")
            blacklist.write(str(user.id) + '\n')
            blacklist.close()
        print("text5")
        if (message.content.lower().find(" sad") >= 0
            or message.content.lower().find("alexa") >= 0
            or message.content.lower().find("buồn") == 0):
            # message.content = "https://www.youtube.com/watch?v=kJQP7kiw5Fk"
            await message.channel.send(
                "https://www.youtube.com/watch?v=kJQP7kiw5Fk")
        if message.content != '' and message.content[-1] == '?':
            # message.content = "🤔"
            if random.randint(1, 4) == 2:
                await message.channel.send("<:senking:595632302495760439>")
        print("text6")
        print( message.content)
        if message.content.lower().find("chọn ") == 0:
            print("text6")
            choices = message.content[5:].split(',')
            if len(choices) > 1:
                message.content = random.choice(choices)
                await message.channel.send(message.content)
        elif message.content.lower(
        ).find("vả ") == 0 and message.content.lower().find(
            "quạt") < 0 and message.content.lower().find(
                "ranh") < 0 and message.content.lower().find(
                    "quat") < 0 and message.content.lower().find("rảnh") < 0:
            if message.content.lower().find("<@!") >= 0:
                slap(
                    client.get_user(int(userFilterNick(
                        message.content)[0])).name)
            elif message.content.lower().find("<@") >= 0:
                slap(
                    client.get_user(int(userFilterOrig(
                        message.content)[0])).name)
            else:
                slap(message.content[3:])
            await message.channel.send(file=discord.File('slapout.jpg'))
        elif message.content.lower().find("pat ") == 0:
            if message.content.lower().find("<@!") >= 0:
                pat(
                    client.get_user(int(userFilterNick(
                        message.content)[0])).name)
            elif message.content.lower().find("<@") >= 0:
                pat(
                    client.get_user(int(userFilterOrig(
                        message.content)[0])).name)
            else:
                pat(message.content[4:])
            await message.channel.send(file=discord.File('patout.jpg'))

        if message.content.lower().find(".gg ") == 0 and len(
            message.content) > 3:
            print(message.content.lower().find(".gg "), len(message.content))
            # try:
            #     from googlesearch import search
            # except ImportError:
            #     print("No module named 'google' found")

            # to search
            query = message.content[3:]
            message.content = "5 kết quả về " + message.content[3:] + ": \n"
            result = ""
            for j in search(query, num_results=5):
                result = result + j + "\n"
                print(j)
                print(result)

            message.content = message.content + result
            await message.channel.send(message.content)
        if message.content.lower() == 'nanoja':
            embed = discord.Embed(
                title='Tiểu sử',
                description=
                'Ta vốn là một chatbot trên facebook được Rảnh tạo ra vào một ngày đẹp trời tháng 5 năm 2019. Nhưng từ khi thanh niên Zucc nhúng tay vào thì ta được Rảnh cho chuyển sinh qua đây và hóa thành Senko vào 18/08/2019. \n今は童は仙狐じゃ！',
                colour=discord.Colour.orange())
            # embed.set_image(url='https://tenor.com/6NXd.gif')
            embed.set_thumbnail(
                url=
                'https://danbooru.donmai.us/data/__senko_sewayaki_kitsune_no_senko_san_drawn_by_araki495__c732565f9449561200981f705c540a78.png'
            )
            embed.set_author(
                name='Senko của Rảnh nanoja!',
                icon_url=
                'https://cdn.discordapp.com/emojis/595472994730770435.png')
            embed.add_field(
                name='Actions',
                value='vả, pat, chọn, .gg, .weather, .img, cưới, ly dị',
                inline=True)
            embed.add_field(
                name='Đừng buồn',
                value='Vì ta sẽ luôn ở bên để bật Despacito cho Người nghe',
                inline=True)
            embed.add_field(
                name='Đừng chửi ta',
                value=
                'Vì Người cũng không muốn bị chửi, phải không nào... Nếu đã lỡ mồm thì phải xin lỗi nghe chưa?',
                inline=True)
            embed.add_field(
                name='Hãy góp ý',
                value=
                'Vì ta không biết nhiều về thế giới hiện đại này lắm, nên là Người hãy chỉ cho ta biết là cần phải học thêm gì nhé. Ta sẽ cân nhắc nanoja.',
                inline=True)
            embed.set_footer(text='なのじゃ！')
            await message.channel.send(embed=embed)

        # Action Marry
        global marry
        global marryPartner
        global marryProposer

        if message.content.lower().find('cưới ') == 0 and len(
            message.content) > 5:
            if client.get_user(int(userIdFilter(message.content))) == None:
                await message.channel.send('Tag lại đối tượng của mình đi, ' +
                                           message.author.mention)
            elif userIdFilter(
                message.content
            ) == '589315866282164229' and message.author.id != 462170598399803394:
                await message.channel.send(
                    'Cảm ơn tấm lòng của Người, nhưng tấm thân này đã thuộc về Rảnh mất rồi... Hãy tìm ai đó tốt hơn ta đi nanoja.'
                )
            elif userIdFilter(
                message.content
            ) == '589315866282164229' and message.author.id == 462170598399803394:
                await message.channel.send(
                    'N-Người nói gì vậy? Chúng ta đã thuộc về nhau rồi cơ mà, '
                    + message.author.mention)
            else:
                marry = 1
                marryPartner = userIdFilter(message.content)
                marryProposer = str(message.author.id)

                read = open("couples.txt", "r", encoding="utf-8")
                text = read.read()
                read.close()
                # print(text)
                if marryPartner + ' ' + marryProposer in text or marryProposer + ' ' + marryPartner in text:
                    await message.channel.send(
                        'Ủa, hai người đã cưới nhau rồi mà? Đùa hoài nanoja!')
                else:
                    await message.channel.send(
                        message.author.mention +
                        ' đã cầu hôn ' + client.get_user(
                            int(userIdFilter(message.content))).mention +
                        '! Câu trả lời sẽ là gì đây? Ấn \'y\' để đồng ý hoặc ấn \'n\' để từ chối!'
                    )
        if message.content.lower(
        ) == 'y' and marry == 1 and marryPartner == str(message.author.id):
            marry = 0

            output = open("couples.txt", "a+", encoding="utf-8")
            output.write(marryProposer + " " + marryPartner + '\n')
            output.close()

            await message.channel.send(
                '🎉🎉🎉 Xin chúc mừng ' +
                client.get_user(int(marryProposer)).mention + ' và ' +
                message.author.mention +
                ' đã đến được bên nhau nanoja!🎊🎊🎊 Chúc hai người hạnh phúc nanoja!🎉🎉🎉'
            )
            marryPartner = ''
            marryProposer = ''
        if message.content.lower(
        ) == 'n' and marry == 1 and marryPartner == str(message.author.id):
            await message.channel.send(
                'Ôi tiếc quá, ' + client.get_user(int(marryProposer)).mention +
                ' đã bị ' + message.author.mention +
                ' từ chối! Hãy kiên nhẫn chờ đúng người, đúng thời điểm nhé nanoja!'
            )
            marry = 0
            marryPartner = ''
            marryProposer = ''

        #Action Divorce
        global divorce, divorcePartner, divorceProposer
        if message.content.lower().find('ly dị ') == 0 and len(
            message.content) > 6:
            read = open("couples.txt", "r", encoding="utf-8")
            text = read.read()
            read.close()
            # print(text)
            # if marryPartner+' '+marryProposer in text or marryProposer+' '+marryPartner in text:

            if client.get_user(int(userIdFilter(message.content))) == None:
                await message.channel.send('Tag lại đối tượng của mình đi, ' +
                                           message.author.mention)
            elif userIdFilter(message.content) + ' ' + str(
                message.author.id) not in text and str(
                    message.author.id) + ' ' + userIdFilter(
                        message.content) not in text:
                await message.channel.send(
                    'Ủa, hai người có cưới nhau đâu mà đòi ly dị nanoja?')
            else:
                divorce = 1
                divorcePartner = userIdFilter(message.content)
                divorceProposer = str(message.author.id)
                await message.channel.send(
                    'Ôi không, ' + message.author.mention +
                    ' muốn ly dị ' + client.get_user(
                        int(userIdFilter(message.content))).mention +
                    '! Liệu đối phương có muốn ly dị không? Ấn \'y\' để đồng ý hoặc ấn \'n\' để từ chối!'
                )

        if message.content.lower(
        ) == 'y' and divorce == 1 and divorcePartner == str(message.author.id):
            divorce = 0

            with open("couples.txt", "r") as f:
                lines = f.readlines()
            with open("couples.txt", "w") as f:
                for line in lines:
                    if line.find(divorcePartner + ' ' + divorceProposer
                                 ) < 0 and line.find(divorceProposer + ' ' +
                                                     divorcePartner) < 0:
                        f.write(line)

            await message.channel.send(
                client.get_user(int(divorceProposer)).mention + ' đã ly dị ' +
                message.author.mention +
                '! <:Aqua_cry:595633225637036043> <:Aqua_cry:595633225637036043> <:Aqua_cry:595633225637036043>'
            )
            divorcePartner = ''
            divorceProposer = ''
        if message.content.lower(
        ) == 'n' and divorce == 1 and divorcePartner == str(message.author.id):
            await message.channel.send(
                message.author.mention + ' vẫn còn muốn níu kéo ' +
                client.get_user(int(divorceProposer)).mention +
                ' ! Hai người nên đóng cửa bảo nhau nhé!')
            divorce = 0
            divorcePartner = ''
            divorceProposer = ''
        #Pixiv's url
        if message.content.lower().find('//www.pixiv.net/') >= 0:
            if message.content.lower().find(
                'member_illust.php?illust_id=') > 0:
                id = message.content.split('illust_id=')[1].split('&')[0]
            elif message.content.lower().find('/artworks/') >= 0:
                id = message.content.split('/artworks/')[1].split('?')[0]

            pixiv_api = AppPixivAPI()
            #-------- try to bypass cloudflare captcha
            pixiv_api = ByPassSniApi()  # Same as AppPixivAPI, but bypass the GFW
            pixiv_api.require_appapi_hosts(hostname="public-api.secure.pixiv.net")
            # api.set_additional_headers({'Accept-Language':'en-US'})
            pixiv_api.set_accept_language('en-us')
            #-----------------------------------------
            # pixiv_api.login(pixiv_login,pixiv_password)
            # pixiv_api.auth(
            #     refresh_token="_1JHDMEvgzwkY8UhlexskYYyNLITfgZCASwDhTTaeaE")

            pixiv_api.auth(
                refresh_token="_1JHDMEvgzwkY8UhlexskYYyNLITfgZCASwDhTTaeaE")

            # await message.channel.send('debuging...')
            # api = AppPixivAPI()
            # api.login("son.vuhuu18@gmail.com","Chicothe123")
            # await message.channel.send('debuging...')

            json_result = pixiv_api.illust_detail(id)
            ugoira_result = pixiv_api.ugoira_metadata(id)
            # await message.channel.send(id+"")

            illust = json_result.illust
            if (illust.type == "ugoira"):
                await message.channel.send("Đang đọc video nanoja...")
                if os.path.isfile('movie.gif'):
                    os.remove("movie.gif")
                #print(ugoira_result)
                # await message.channel.send(ugoira_result.ugoira_metadata)
                delay = int(ugoira_result.ugoira_metadata.frames[0].delay)
                ugoira_stream = requests.get(
                    ugoira_result.ugoira_metadata.zip_urls.medium,
                    headers={'Referer': 'https://app-api.pixiv.net/'},
                    stream=True)
                ugoira_file = io.BytesIO(ugoira_stream.content)
                with open("ugoira/file", "wb") as f:
                    f.write(ugoira_file.getbuffer())
                with zipfile.ZipFile("ugoira/file", 'r') as zip_ref:
                    zip_ref.extractall("ugoira/extracted/")

                # files = [f"ugoira/extracted/{file}" for file in os.listdir("ugoira/extracted/")]
                # files.sort()
                # print(files)
                # images = [imageio.v2.imread(file) for file in files]
                # imageio.mimsave('movie.gif', images, duration=delay/1000)

                (ffmpeg.input('ugoira/extracted/*.jpg',
                              pattern_type='glob',
                              framerate=1000 /
                              delay).output('movie.gif').run())

                
                files = glob.glob('ugoira/**/**')
                for f in files:
                    os.remove(f)

                await message.channel.send(file=discord.File("movie.gif"))
            else:
                #print(illust)
                if (illust.page_count == 1):
                    url = illust.meta_single_page['original_image_url']
                else:
                    await message.channel.send("Album gồm " +
                                               str(illust.page_count) +
                                               " ảnh nanoja!")
                    url = illust.meta_pages[0].image_urls['original']
                pixiv_image_rsp = requests.get(
                    url,
                    headers={'Referer': 'https://app-api.pixiv.net/'},
                    stream=True)
                pixiv_image_rsp_fp = io.BytesIO(pixiv_image_rsp.content)
                # Add file name to stream
                # print(illust)

                if pixiv_image_rsp_fp.getbuffer().nbytes >= 25*1024*1024:
                    await message.channel.send(
                        "Ảnh lớn hơn 25mb nên ta sẽ post ảnh resize nanoja!")
                    if (illust.page_count == 1):
                        url = illust.image_urls['large']
                    else:
                        url = illust.meta_pages[0].image_urls['large']

                    pixiv_image_rsp = requests.get(
                        url,
                        headers={'Referer': 'https://app-api.pixiv.net/'},
                        stream=True)
                    pixiv_image_rsp_fp = io.BytesIO(pixiv_image_rsp.content)
                    pixiv_image_rsp_fp.name = url.rsplit('/', 1)[-1]
                    await message.channel.send(
                        file=discord.File(pixiv_image_rsp_fp))
                else:
                    pixiv_image_rsp_fp.name = url.rsplit('/', 1)[-1]
                    # print(illust)
                    # await message.channel.send(illust.user)
                    await message.channel.send(
                        file=discord.File(pixiv_image_rsp_fp))
        # Twitter's url
        twitter_switch = 1
        if twitter_switch == 1 and (message.content.lower().find(
            '//twitter.com/') >= 0 or message.content.lower().find('//x.com/') >= 0):

            mess = message.content
            
            if mess.find('//twitter.com/') >= 0:
                mess = mess.replace('//twitter.com/', '//vxtwitter.com/')
            else:
                mess = mess.replace('//x.com/', '//fixvx.com/')
            # Old twitter api (rip)
            # status_id = message.content.split('status/')[1].split('?s')[0]
            # mess = ''
            # # await message.channel.send(status_id)
            # status = twitterapi.get_status(status_id, tweet_mode='extended')
            # # await message.channel.send(twitterapi.get_status(status_id))
            # if hasattr(status, 'extended_entities'):
            #     if 'media' in status.extended_entities:
            #         count = 0
            #         for pic in status.extended_entities['media']:
            #             if ('video' not in pic['type'] or 'animated_gif'
            #                 not in pic['type']) and count != 0:
            #                 mess = mess + pic['media_url'] + '\n'
            #             elif 'video' in pic['type'] or 'animated_gif' in pic[
            #                 'type']:
            #                 # mess = pic['video_info']['variants'][0]['url']
            #                 for i in pic['video_info']['variants']:
            #                     if i['url'].find('.mp4') >= 0:
            #                         mess = i['url']
            #                         break
            #             else:
            #                 count = count + 1
            # else:
            #     if 'media' in status.entities:
            #         count = 0
            #         for pic in status.entities['media']:
            #             if ('video' not in pic['type'] or 'animated_gif'
            #                 not in pic['type']) and count != 0:
            #                 mess = mess + pic['media_url'] + '\n'
            #             elif 'video' in pic['type'] or 'animated_gif' in pic[
            #                 'type']:
            #                 # mess = pic['video_info']['variants'][0]['url']
            #                 for i in pic['video_info']['variants']:
            #                     if i['url'].find('.mp4') >= 0:
            #                         mess = i['url']
            #                         break
            #             else:
            #                 count = count + 1
            await message.channel.send(mess)
        #Weather forecast
        if message.content.lower().find(".w ") == 0:
            w_api = "e0c439c2a3fb825f966d3abdc9a6c19d"
            city = message.content.split(".w ")[1]
            base_url = "http://api.openweathermap.org/data/2.5/weather?"
            complete_url = base_url + "appid=" + w_api + "&q=" + city
            response = requests.get(complete_url)
            info = response.json()
            # await message.channel.send(info)

            soup = ImageSoup()
            images = soup.search(city, n_images=1)
            print(images, images == [])
            if images == [] or images == None:
                city_img = ""
                city_img_url = ""

            else:
                city_img = images[0]
                city_img_url = city_img.URL

            arguments = {"keywords": "" + city, "limit": 1, "print_urls": True}
            if info["cod"] != "404":
                main = info["main"]
                weather = info["weather"]
                embed = discord.Embed(title="Today's weather in " + city + "",
                                      colour=discord.Colour.orange())
                temp = str(round(float(main["temp"]) - 273, 2))
                embed.add_field(name='Description',
                                value=str(weather[0]['description']),
                                inline=True)
                embed.add_field(name='Temprature',
                                value=temp + "°C",
                                inline=True)
                embed.add_field(name='Humidity',
                                value=str(main["humidity"]) + "%",
                                inline=True)
                embed.set_thumbnail(url=city_img_url)
                await message.channel.send(embed=embed)

            else:
                await message.channel.send(
                    "Không tìm thấy thành phố đó nanoja...")
        #Search for image
        if message.content.lower().find(".img ") == 0:
            searchimg = message.content.split(".img ")[1]
            soup = ImageSoup()
            images = soup.search(searchimg, n_images=5)
            mess = ""
            print(images)
            for i in images:
                mess = mess + i.URL + '\n'
            await message.channel.send(mess)
        # Jankenpon game
        janken = ["Bao", "Búa", "Kéo"]
        if message.content.lower().find(".ott ") == 0:
            if message.content.lower(
            ).split(" ")[1] == "bao" or message.content.lower().split(" ")[
                1] == "búa" or message.content.lower().split(" ")[1] == "kéo":
                player_janken = message.content.lower().split(" ")[1]
                senko_janken = random.choice(janken)
                # await message.channel.send(senko_janken)
                result = jankenResult(senko_janken.lower(), player_janken)

                read = open("jankenpon.txt", "r", encoding="utf-8")
                text = read.read()
                read.close()
                if str(message.author.id) not in text:
                    output = open("jankenpon.txt", "a+", encoding="utf-8")
                    output.write(str(message.author.id) + " 0 0 0 0\n")
                    output.close()

                with open("jankenpon.txt", "r") as f:
                    lines = f.readlines()

                    for line in lines:
                        if str(message.author.id) in line:
                            playerId = line.split(" ")[0]
                            win = int(line.split(" ")[1])
                            tie = int(line.split(" ")[2])
                            lose = int(line.split(" ")[3])
                            score = int(line.split(" ")[4])
                            lineOld = playerId + " " + str(win) + " " + str(
                                tie) + " " + str(lose) + " " + str(
                                    score) + "\n"
                            if result == -1:
                                lose = lose + 1
                                score = score - 10
                            if result == 0:
                                tie = tie + 1
                            if result == 1:
                                win = win + 1
                                score = score + 10
                            lineNew = playerId + " " + str(win) + " " + str(
                                tie) + " " + str(lose) + " " + str(
                                    score) + "\n"
                            # await message.channel.send(lines)
                lines[lines.index(lineOld)] = lineNew
                if score >= 1000:
                    await message.author.add_roles(
                        message.author.guild.get_role(658325379538354187))
                elif score >= 500:
                    await message.author.add_roles(
                        message.author.guild.get_role(658325189834178572))
                elif score >= 200:
                    await message.author.add_roles(
                        message.author.guild.get_role(658325047282499614))
                elif score >= 100:
                    await message.author.add_roles(
                        message.author.guild.get_role(658324756864565278))

                with open("jankenpon.txt", "w") as f:
                    f.writelines(lines)

                if result == 0:
                    await message.channel.send(senko_janken +
                                               " - Chúng ta hòa rồi!")
                elif result == -1:
                    await message.channel.send(senko_janken +
                                               " - Hoan hô, ta thắng rồi!")
                elif result == 1:
                    await message.channel.send(
                        senko_janken +
                        " - Hic, ta thua rồi <:Aqua_cry:595633225637036043>")
            else:
                await message.channel.send("Mời Người chọn bao, búa hoặc kéo.")
        if message.content.lower().find(".ottstatus") == 0:
            embed = discord.Embed(title="Thành tích oẳn tù tì của " +
                                  message.author.name,
                                  colour=discord.Colour.orange())
            with open("jankenpon.txt", "r") as f:
                lines = f.readlines()

                for line in lines:
                    if str(message.author.id) in line:
                        playerId = line.split(" ")[0]
                        win = line.split(" ")[1]
                        tie = line.split(" ")[2]
                        lose = line.split(" ")[3]
                        score = line.split(" ")[4]

            embed.add_field(name='Thắng', value=win + " ván", inline=True)
            embed.add_field(name='Hòa', value=tie + " ván", inline=True)
            embed.add_field(name='Thua', value=lose + " ván", inline=True)
            embed.add_field(name='Điểm', value=score, inline=True)
            embed.set_thumbnail(url=message.author.avatar_url)
            await message.channel.send(embed=embed)
        # Mazii
        if message.content.lower().find(".mazii ") == 0:
            word = message.content.lower().split(" ")[1]
            API_ENDPOINT = "https://mazii.net/api/search"

            data = {
                "dict": "javi",
                "type": "word",
                "query": word,
                "limit": "20",
                "page": "1"
            }

            # sending post request and saving response as response object
            r = requests.post(url=API_ENDPOINT, data=data)

            # extracting response text
            jsondata = json.loads(r.text)
            result = ""
            for i in jsondata["data"][0]["means"]:
                result = result + i["mean"] + "\n"

            await message.channel.send(result)
        # Fuck Tuong tac
        if message.content.lower().find("tương tác") == 0:
            await message.channel.send("Tương vào clmm ấy " +
                                       message.author.mention)


keep_alive()
token = os.environ.get("DISCORD_BOT_SECRET")
client.run(token)
