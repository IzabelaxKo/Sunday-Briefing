import smtplib
import requests as r
import datetime as dt

today = dt.datetime.now()
week_ago = today - dt.timedelta(days=7)

news_api = "your_api_key_goes_here"

# getting the data from the api
data_get = r.get("https://api.sheety.co/[your_api]/sundayBriefing/sheet1").json()['sheet1']

# checking if today is Sunday
isTime = True if today.weekday() == 6 else False

if isTime: 
    for user in data_get:
        # clearing news counter
        news_counter = 0

        # clearing the text file with news
        clear_file = open("/SundayBriefing/news.txt", "w")
        clear_file.write("---------------------------------\n") 
        clear_file.close()

        # users topics
        topics = user['topics'].replace("; ", " OR ")

        # getting the news from api
        news = r.get(f"https://newsapi.org/v2/everything?q={topics}&from={today.strftime('%Y-%m-%d')}&to={week_ago.strftime('%Y-%m-%d')}"
                    f"&language=en&sortBy=popularity&pageSize=20", headers={"x-api-key": news_api}).json()['articles']
        
        for new in news:

            # checking if the news is 'removed'
            if new['title'] != "[Removed]":
                # appending the news to the text file
                with open("./SundayBriefing/news.txt", "a") as f:
                    f.write(f"New No. {news_counter+1}: \n")
                    f.write(str(new["title"] )+ "\n")
                    f.write("Link: " + str(new["url"]) + "\n")
                    f.write("---------------------------------\n") 
                news_counter += 1

            # counting the number of news - sends only 10 emails
            if news_counter == 10:
                break

        # sending emails
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as mail:
            mail.login("[your_gmail_goes_here]", "[your_password_goes_here]")
            with open("./SundayBriefing/news.txt", "r") as file:
                text = str(file.read())
                mail.sendmail(from_addr="[your_email]", to_addrs=user["email"], msg=f"Subject: Sunday Briefing!\n\n{text}")
                print(f"Email sent to {user['email']}")
