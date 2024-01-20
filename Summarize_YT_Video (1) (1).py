#!/usr/bin/env python
# coding: utf-8

# # Python Code To Get The Summary of YouTube Video

# ***OPEN AI API KEY : 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***

# In[1]:


from youtube_transcript_api import YouTubeTranscriptApi #to get Subtitles
import re # Formatting the return value of Subtitles
import requests # To access OpenAI API
from pytube import YouTube # To extract title and Creator name
import json # to get request and response
import sys # To stop the program
import nltk # Natural Language Toolkit Lobrary for Splitting bigger paragraph
import time # To give delay in between 2 lines of codes as OpenAI does not support multiple queries at once.


# In[2]:


def Response_openAI(Paragraph):
    api_url = 'https://api.openai.com/v1/chat/completions'

    # Setting API key
    api_key = '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'

    # Set up the headers with API key
    headers = {
        'Authorization': 'Bearer ' + api_key,
        'Content-Type': 'application/json'
    }

    Number_of_words = "100"
    a = Paragraph + "\n" + "\n" + "\n" + "Summarize the above paragraph in " + Number_of_words + " " + "words"

    # Set up the payload with your input prompt
    payload = {
        'model': 'gpt-3.5-turbo',
        'messages': [{'role': 'system', 'content': 'You are summarizing youtube video'},
                     {'role': 'user', 'content': a }]
    }

    # Send the API request
    response = requests.post(api_url, headers=headers, json=payload)
    return response


# In[3]:


def Merge_openAI(a):
    api_url = 'https://api.openai.com/v1/chat/completions'

    # Set up your API key
    api_key = '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'

    # Set up the headers with your API key
    headers = {
        'Authorization': 'Bearer ' + api_key,
        'Content-Type': 'application/json'
    }

    # Set up the payload with your input prompt
    payload = {
        'model': 'gpt-3.5-turbo',
        'messages': [{'role': 'system', 'content': 'You are summarizing youtube video'},
                     {'role': 'user', 'content': a }]
    }

    # Send the API request
    response = requests.post(api_url, headers=headers, json=payload)
    return response


# In[4]:


def Subtitle_Generator(url):  
    #url = "https://www.youtube.com/watch?v=_sOis7EXJbk"
    #url = "https://www.youtube.com/watch?v=Qa4K7XsRO0g"
    #url = input("Enter the URL in the below format \n ")
    b = []
    def get_title(url):
        try:
            video = YouTube(url)
            title = video.title
            author = video.author
            views = video.views
            duration = video.length
            b.append(title)
            b.append(author)
            b.append(duration)
            return b
        except Exception as e:
            print(f"Error: {e}")
            return None
    title = get_title(url)
    time_minutes = b[2]//60
    if title:
        print("\n" + f"The title of the video is : {b[0]} \n The creator of this video is {b[1]} \n The Summary of this {time_minutes} minutes video is" + "\n" + "\n")
    # Input should be of the format: https://www.youtube.com/watch?v=[video_id]

    video_id = re.search(r"v=([^&]+)", url).group(1) # Extracting the Video Code

    srt = YouTubeTranscriptApi.get_transcript(video_id) # Getting the Subtitles in the format of List of Dictionaries

    Subtitle = []
    for text_dict in srt:
        Subtitle.append(text_dict['text']) #Getting the subtitle in list format

    Paragraph = ' '.join(Subtitle) # Subtitle in a Paragraph format
    return Paragraph


# In[5]:


def div_factor(sentence):
    #sentence = "This model's maximum context length is 4097 tokens. However, your messages resulted in 20000 tokens. Please reduce the length of the messages."

    # Extract numbers using regular expressions
    numbers = re.findall(r'\d+', sentence)

    limit = float(numbers[0])
    inp = float(numbers[1])
    x = inp/limit
    if 1.000 < x < 2.000:
        div_fact = 2
    elif 2.000 <= x < 3.000:
        div_fact = 3
    else:
        div_fact = 4
    
    return div_fact



# In[6]:


def split_2(paragraph):
    # Split the paragraph into words
    words = paragraph.split()
    a = len(words)//2
    # Determine the split point
    split_point = min(a, len(words))

    # Join the first half words into the first paragraph
    first_paragraph = ' '.join(words[:split_point])

    # Join the remaining words into the second paragraph
    second_paragraph = ' '.join(words[split_point:])
    
    response_1 = Response_openAI(first_paragraph)
    time.sleep(10)
    response_2 = Response_openAI(second_paragraph)
    time.sleep(5)
    if response_1.status_code == 200 and response_2.status_code == 200:
        data1 = response_1.json()
        reply1 = data1['choices'][0]['message']['content']
        data2 = response_2.json()
        reply2 = data2['choices'][0]['message']['content']
        a = "Merge these 2 Paragrapg and give the summary in 100 words after merging" + "\n" + "Paragraph 1 :" + reply1 +"\n" + "Paragraph 2 : " + reply2
        time.sleep(15)
        response = Merge_openAI(a)
        if response.status_code == 200:
            data = response.json()
            reply = data['choices'][0]['message']['content']
            return reply
        return ("Girish")


# In[7]:


def split_3(paragraph):
    # Split the paragraph into words
    words = paragraph.split()

    # Calculate the number of words per part
    words_per_part = len(words) // 3

    # Create three parts
    part1 = " ".join(words[:words_per_part])
    part2 = " ".join(words[words_per_part:2 * words_per_part])
    part3 = " ".join(words[2 * words_per_part:])

    response_1 = Response_openAI(part1)
    time.sleep(10)
    response_2 = Response_openAI(part2)
    time.sleep(10)
    response_3 = Response_openAI(part3)
    
    if response_1.status_code == 200 and response_2.status_code == 200 and response_3.status_code == 200:
        data1 = response_1.json()
        reply1 = data1['choices'][0]['message']['content']
        data2 = response_2.json()
        reply2 = data2['choices'][0]['message']['content']
        data3 = response_3.json()
        reply3 = data3['choices'][0]['message']['content']
        a = "Merge these 3 Paragrapg and give the summary in 100 words after merging" + "\n" + "Paragraph 1 : " + reply1 +"\n" + "Paragraph 2 : " + reply2 + "\n" + "Paragraph 3 : " + reply3
        time.sleep(10)
        response = Merge_openAI(a)
        #print(response.status_code)
        if response.status_code == 200:
            data = response.json()
            reply = data['choices'][0]['message']['content']
            return reply
        


# In[9]:


url = input("Enter the URL in the below format \n https://www.youtube.com/watch?v=[video_id] : ")
Paragraph = Subtitle_Generator(url)

response = Response_openAI(Paragraph)

# Process the API response
if response.status_code == 200:
    data = response.json()
    reply = data['choices'][0]['message']['content']
    print(reply)
else:
    #print(type(response.text))
    string_dict = response.text
    # Convert string to dictionary
    dictionary = json.loads(string_dict)
    message = dictionary["error"]["message"]

    div_fact = div_factor(message)
    
    if div_fact == 2:
        split_2_out = split_2(Paragraph)
        print(split_2_out)
    elif div_fact == 3:
        split_3_out = split_3(Paragraph)
        print(split_3_out)
    else:
        print("The video is lenghty or has more than 18,000 words")
        try:
            sys.exit()
        except SystemExit:
            pass
        
    
    
#https://www.youtube.com/watch?v=Qa4K7XsRO0g
#https://www.youtube.com/watch?v=Kfdj3AfDD74


# In[ ]:




