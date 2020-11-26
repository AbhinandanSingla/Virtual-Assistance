"""
Credit : Abhinandan Singla

"""

# Description : This is a virtual assistant program that gets the date Current Time Responds backs with a random
# greeting and return information on a person
# Required Packages
# pip install pyaudio
# pip install SpeechRecognition
# pip install gTTS
# pip install Wikipedia
import json
import traceback
import bs4
import feedparser
import pyttsx3
import requests
import speech_recognition as sr
import datetime
import warnings
import calendar
import random
import wikipedia
import time

# ignore any waning message
warnings.filterwarnings('ignore')
# A converter that will convert fahrenheit to Celsius
convert_f_TO_C = lambda fahrenheit_temp: (fahrenheit_temp - 32) * 5 / 9


# Record Audio and return Audio as string
def recordAudio():
    # Record audio
    r = sr.Recognizer()  # Creating a recogizer object
    # open the microphone and start recording
    with sr.Microphone() as source:
        print("listening ")
        audio = r.listen(source)

        # use google speech recognition
        data = ""
        try:
            print('jake is recognizing please wait ')
            data = r.recognize_google(audio)
            print("\nYou said " + data)
        except sr.UnknownValueError:
            print('Google speech Recognition could not understand the audio , unknown error')

        except sr.RequestError as e:
            print('Request result from google Speech Recognition service error ' + str(e))
        return data


def get_headlines(news_country_code='ind'):
    try:
        if news_country_code is None:
            headlines_url = "https://news.google.com/news?ned=us&output=rss"
        else:
            headlines_url = "https://news.google.com/news?ned=%s&output=rss" % news_country_code
        feed = feedparser.parse(headlines_url)
        if feed['feed'] =={}:
            return "error no internet found"
        for post in feed.entries[0:5]:
            print(post['title'])
            print(post['link'])
            tim = post['published_parsed']
            hr, mins, sec = tim[3], tim[4], tim[5]
            hr, mins, sec = totalTime_taken(hr, mins, sec)
            print(time.strftime('%a, %d %b %Y', tim))
            print(time.strftime('%H:%M:%S', tim) + '\n')
            print('old time ' + str(hr) + ':' + str(mins))
        return 'here is the result i have found'
    except Exception as e:
        traceback.print_exc()
        return "Error : %s. Cannot get news." %e


def totalTime_taken(hr, mins, sec):
    current = time.strftime('%H %M %S')
    hr1 = int(current.split()[0])
    if hr1 == 00:
        hr1 = 12
    hr = hr - hr1
    mins = mins - int(current.split()[1])
    sec = sec - int(current.split()[2])
    return abs(hr), abs(mins), abs(sec)


# A Function to get the virtual assistant respond
def assistantResponse(text):
    engineio = pyttsx3.init()
    engineio.setProperty('rate', 120)
    engineio.setProperty('volume', 0.9)
    voices = engineio.getProperty('voices')
    engineio.setProperty('voice', voices[1].id)
    engineio.say(text)
    engineio.runAndWait()


# function for wake word or phase
def wakeWord(text):
    WAKE_WORDS = ['jake', 'Black Pearl']  # list of wake word

    text = text.lower()  # Converting the text in all lower case
    # print(text)
    # Check to see if the user command/text contain wake/phase
    for phase in text.split():
        if phase in WAKE_WORDS:
            return True
    # if the wake isn't found in the text from the loop so it will return false
    return False


# function for current date
def getDate():
    now = datetime.datetime.now()
    my_date = datetime.datetime.today()
    weekday = calendar.day_name[my_date.weekday()]  # eg Friday
    monthNum = now.month
    dayNum = now.day
    # list of month
    month_name = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                  'November',
                  'December']
    if dayNum == 1:
        return f'Today is {weekday}. {month_name[monthNum - 1]} the {dayNum}st'
    elif dayNum == 2:
        return f'Today is {weekday}. {month_name[monthNum - 1]} the {dayNum}nd'
    elif dayNum == 3:
        return f'Today is {weekday}. {month_name[monthNum - 1]} the {dayNum}rd'
    else:
        return f'Today is {weekday}. {month_name[monthNum - 1]} the {dayNum}th'


# to Return a random greeting Person
def greeting(text):
    # Greeting  inputs
    GREETING_INPUTS = ['hi', 'hello', 'ola', 'greeting', 'hey', 'wassup']
    # Greeting response
    GREETING_RESPONSE = ['howdy', 'good to see you ', 'hey', 'hi', 'yo']

    # if the user is a greeting then return a random greeting response
    for word in text.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSE)
    # if the is no greeting then we are returning empty string
    return ''


# A function to get a first and last name from text

def getPerson(text):
    wordList = text.split()  # Splitting the text into a list of words
    for i in range(0, len(wordList)):
        if i + 3 <= len(wordList) - 1 and wordList[i].lower() == 'who' and wordList[i + 1].lower() == 'is':
            return wordList[i + 2] + ' ' + wordList[i + 3]  # need improvement


def PersonINFO(text):
    person = getPerson(text)
    return wikipedia.summary(person, sentences=2)


def getLocation():
    ip = get_ip()
    location_token = "2e5b75c9b4ebc576f08d9e2fb041592f"
    req = requests.get(f"http://api.ipstack.com/{ip}?access_key={location_token}")
    parserReq = json.loads(req.text)
    # return {'latitude':parserReq['latitude'],'longitude':parserReq['longitude']}
    return parserReq['latitude'], parserReq['longitude']


def spliting_text(text):
    return text + '+'


def Search(text):
    text = text.split()
    print(text[1])
    for i in range(0, len(text)):
        if text[i].lower() == 'search':
            search = text[i + 1:]
            search = ''.join(map(spliting_text, search))
            search = search[: len(search) - 1]
            try:
                req = requests.get('https://www.bing.com/search?q=' + search)
                bs = bs4.BeautifulSoup(req.content, 'html5lib')
                div = bs.find('div', attrs={'id': 'b_content'})
                for link in div.findAll('li', attrs={'class': 'b_algo'}):
                    try:
                        print(link.a.text)
                        print(link.a['href'])
                        print(link.p.text + '\n\n')
                    except Exception as e:
                        pass
            except Exception as e:
                print(e)


def get_ip():
    try:
        ip_url = "http://jsonip.com/"
        req = requests.get(ip_url)
        ip_json = json.loads(req.text)
        return ip_json['ip']
    except Exception as e:
        traceback.print_exc()
        return "Error: %s. Cannot get ip." % e


def WeatherForecast():
    lat, long = getLocation()
    weather_key = "67bfd5376436887601019e6bab684a5d"
    weather_req = requests.get(f"https://api.darksky.net/forecast/{weather_key}/{lat},{long}")
    parser_weather = json.loads(weather_req.text)
    temperature = convert_f_TO_C(parser_weather['hourly']['data'][0]['temperature'])
    summary = parser_weather['hourly']['summary']
    return temperature, summary


def Talk(text):
    wordlist = text.split()
    response = ''
    r = ['I am fine', 'Awesome']
    for i in range(0, len(wordlist)):
        if 'how' == wordlist[i].lower() and 'are' == wordlist[i + 1].lower() and 'you' == wordlist[i + 2]:
            print(r[random.randint(0, 1)] + '. What about you. ')
            response += r[random.randint(0, 1)] + ' what about you. '
    return response


def getReplied(text):
    wordlist = text.split()
    response = ''
    for i in range(0, len(wordlist)):
        if 'i' == wordlist[i].lower() and 'am' == wordlist[i + 1].lower() and 'fine' == wordlist[i + 2]:
            print('cool. ')
            response += ' cool. '
    return response


print('Your virtual assistant Jake')
# text = 'hey jake news'
# print(text)
text = recordAudio()
response = ''
if wakeWord(text):
    print('jake is waked')
    if greeting(text):
        response += greeting(text)
    if 'date' in text.split():
        response += ' ' + getDate() + '.'
    if 'who' in text.split():
        response += ' ' + PersonINFO(text).replace('.', '\n')
        print(response)
    if 'weather' in text.split():
        temp, summ = WeatherForecast()
        print('Today weather is ' + summ + ' with ' + temp)
    if 'news' in text.split():
        response += get_headlines()
        print(get_headlines())
    elif 'headlines' in text.split():
        response += get_headlines()
        print(get_headlines())
    if 'oya' in text.split():
        response += 'fuck you dude'
        print(response)
assistantResponse(response)
# Search(text)
