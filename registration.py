import requests as r

print("Welcome to the Sunday Briefing!")
print("This program will send you a briefings every Sunday.")
print("Please enter your name:")
name = input()
print("Please enter your email address:")
email = input()
print("Please enter your topics:")
topics = input()

isOk = True
data_get = r.get("https://api.sheety.co/[your_api]/sundayBriefing/sheet1").json()['sheet1']

for user in data_get:
    if user['email'] == email:
        print("You are already registered!")
        

if isOk:
    r.post("https://api.sheety.co/[your_api]/sundayBriefing/sheet1", json={"sheet1": {"email": email, "userName": name, "topics": topics}})
    print("You have been registered!")
