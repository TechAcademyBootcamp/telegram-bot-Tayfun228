import requests as r
from bs4 import BeautifulSoup
import telegram
import random



class telegramBot():
    index=None
    search=False
    oyret=False
    oyret2=False
    stored=""
    def main(self):
        self.token = '1120109536:AAEFexLLxffdLNTeOSBGM89WsZm0Ytabvk4'
        bot = telegram.Bot(self.token)
        while True:
            telegramBot.echo(bot)

    def echo(bot):
        indexx=telegramBot.index

        for update in bot.get_updates(offset=indexx,timeout=100):
                telegramBot.index=update.update_id+1
                if telegramBot.search:
                    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
                    headers = {"user-agent" : USER_AGENT}
                    text=r.get(f"https://www.google.com/search?q={update.message.text}",headers=headers).text
                    soup=BeautifulSoup(text,"html.parser")
                    news=soup.findAll("div",{"class":"g"})
                    try:
                        for i in news:
                            # print(i)
                            href=i.find("a")["href"]
                            print(href)
                            name=i.find("h3",{"class":"LC20lb DKV0Md"}).text
                            print(name)
                            update.message.reply_text(f"{name}\n{href}")
                    except:
                        pass
                        
                    telegramBot.search=False
                    # print("YOU DID IT")
                elif "weather" in update.message.text:
                    page=r.get("https://api.openweathermap.org/data/2.5/weather?q=Baku&appid=fc5c619a3e41cdde434f955f7502ed48").json()
                    temp=int(page["main"]["temp"])-273
                    update.message.reply_text(f"BAKU  {temp} C")
                elif "google" in update.message.text:
                    telegramBot.search=True
                    # print("YES")

                # /////////////////////////////////////////////////////////////////////////////////////////   X E B E R L E R
                elif telegramBot.levenshtein(update.message.text,"xeberler")<=2:
                    print(update.message.text)
                    text=r.get("https://oxu.az").text
                    soup=BeautifulSoup(text,"html.parser")
                    news=soup.findAll("a",{"class":"news-i-inner"})
                    for i in news:
                        name=i.find("div",{"class":"title"}).text
                        returned=f'{name}    LINK - https://oxu.az{i["href"]}'
                        update.message.reply_text(returned)
                # /////////////////////////////////////////////////////////////////////////////////////////   V A L Y U T A
                elif telegramBot.levenshtein(update.message.text,"valyuta")<=2:
                    text=r.get("https://api.exchangeratesapi.io/latest").json()
                    datas=text["rates"]
                    for i in datas:
                        update.message.reply_text(f'{i} : {datas[i]}')

                # /////////////////////////////////////////////////////////////////////////////////////////   O Y R E T
                elif telegramBot.oyret2:
                    newM=update.message.text
                    with open("text.txt","r+") as t:
                        t.seek(0)
                        txt=t.read()
                        t.write(f"\n{telegramBot.stored}:{newM}::")
                        t.seek(0)

                    telegramBot.oyret2=False
                elif telegramBot.oyret:
                    if "he" in update.message.text:
                        telegramBot.oyret2=True

                    telegramBot.oyret=False
                    
                else:
                    answer=telegramBot.q_answer(update.message.text)
                    update.message.reply_text(answer)
                    telegramBot.stored=update.message.text
                

    def q_answer(asked):
        print("ISLEDI")
        ask=asked.split(" ")
        for f in ask:
            rating=1000
            ans=""
            # print(f)
            with open("text.txt","r") as t:
                t.seek(0)
                lines=t.readlines()
                for i in lines:
                    splitted=i.split(":")
                    # print(splitted[0].split(","))
                    ask2=splitted[0].split(",")
                    answers=splitted[1].split(",")
                    answers2=splitted[2].split(",")
                    # print(answers2)
                    for i in ask2:
                        if telegramBot.levenshtein(f,i)<=rating:

                            rating=telegramBot.levenshtein(f,i)
                            answer=random.choice(answers)
                            ans=random.choice(answers2)
                if rating<=2:
                    if ans=="":
                        return answer
                    else:
                        return(answer+", "+ans)
                else:
                    telegramBot.oyret=True
                    return("Öyrətmək istəyirsən? he ya yox")    


    
    def news():
        text=r.get("https://oxu.az").text
        soup=BeautifulSoup(text,"html.parser")
        news=soup.findAll("a",{"class":"news-i-inner"})
        for i in news:
            name=i.find("div",{"class":"title"}).text

            # print(f'{name}    LINK - https://oxu.az{i["href"]}')
            returned=f'{name}    LINK - https://oxu.az{i["href"]}'
            # update.message.reply_text(returned)
            # return returned


    def valyuta():
        text=r.get("https://api.exchangeratesapi.io/latest").json()
        datas=text["rates"]
        for i in datas:
            print(f'{i} : {datas[i]}')

    def levenshtein(s1, s2):
        if len(s1) < len(s2):
            return telegramBot.levenshtein(s2, s1)

        # len(s1) >= len(s2)
        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
                deletions = current_row[j] + 1       # than s2
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]

     

if __name__=="__main__":
    a=telegramBot()
    a.main()
    # telegramBot.main()
    