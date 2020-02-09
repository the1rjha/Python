#!/usr/bin/env python
# coding: utf-8

# # Which Hacker News Post Gets the Most Engagement?
# 
# The purpose of this project is to look at posts made on Hacker News (HN) over a twelve month period (data is as of Sept. 2016) to understand what kind of content gets the most engagement from users. Specifically, this analysis will look at comments on posts that either begin with, "Ask HN" or "Show HN" to see which of the two gets more engagement as well as look and see if posts created at certain times get more engagement.

# In[1]:


#Opening Hacker News .csv file and turning it into a list of lists
from csv import reader

opened_file = open('hacker_news.csv')
read_file = reader(opened_file)
hn = list(read_file)
hn_5 = hn[:5]
print(hn_5)


# In[2]:


#removing headers and display first five rows to verify header is removed
header = hn[0]
print(header)
print('\n')
hn = hn[1:]
print(hn[:5])


# In[3]:


#Separating posts into unique lists
ask_posts = []
show_posts = []
other_posts = []

for row in hn:
    title = row[1]
    if title.lower().startswith('ask hn'):
        ask_posts.append(row)
    elif title.lower().startswith('show hn'):
        show_posts.append(row)
    else:
        other_posts.append(row)
        
print(len(ask_posts))
print(len(show_posts))
print(len(other_posts))
print('\n')
print(ask_posts[:5])
print('\n')
print(show_posts[:5])
print('\n')
print(other_posts[:5])


# In[4]:


#Determine if ask posts or show posts receive more comments on average
total_ask_comments = 0

for comments in ask_posts:
    num_comments = comments[4]
    total_ask_comments += int(num_comments)
    
avg_ask_comments = total_ask_comments / len(ask_posts)
print(avg_ask_comments)

total_show_comments = 0

for comments in show_posts:
    num_comments = comments[4]
    total_show_comments += int(num_comments)
    
avg_show_comments = total_show_comments / len(show_posts)
print(avg_show_comments)


# Per the calculations in the above cell, Ask HN posts get 14 comments/post vs. 10 comments/post for Show HN posts. Based on this finding, it appears that HN users tend to have the same questions of those that are asked on the site and tend to engage more with the site.

# In[5]:


# Determining if Ask HN posts created at a certain time of day get more comments that posts made at other times of day
import datetime as dt
result_list = []

for row in ask_posts:
    result_list.append([row[6], int(row[4])])

#Printing first few results to verify that post created date and number of comments were appended to the list
print(result_list[:4])
print('\n')

#Extract hour from the date and create a dictionary to show comment counts for each corresponding hour added to the dictionary
counts_by_hour = {}
comments_by_hour = {}
date_format = "%m/%d/%Y %H:%M"

for row in result_list:
    time = row[0]
    comments = row[1]
    date_object = dt.datetime.strptime(time, date_format)
    hour = dt.datetime.strftime(date_object, '%H')
    
    if hour not in counts_by_hour:
        counts_by_hour[hour] = 1
        comments_by_hour[hour] = comments
    else:
        counts_by_hour[hour] += 1
        comments_by_hour[hour] += comments
        
print(counts_by_hour)
print('\n')
print(comments_by_hour)


# In[6]:


# Calculating average number of comments per posts created during each hour of the day

avg_by_hour = []

for hour in comments_by_hour:
    avg_by_hour.append([hour, comments_by_hour[hour] / counts_by_hour[hour]])

print(avg_by_hour)


# In[7]:


# Cleaning up the avg_by_hours lists of lists to make data easier to understand
swap_avg_by_hours = []

for row in avg_by_hour:
    swap_avg_by_hours.append([row[1], row[0]])
    
print(swap_avg_by_hours)

sorted_swap = sorted(swap_avg_by_hours, reverse = True)


# In[8]:


# Sort the values and print the the 5 hours with the highest average comments.

print("Top 5 Hours for 'Ask HN' Comments")
for avg, hr in sorted_swap[:5]:
    print(
        "{}: {:.2f} average comments per post".format(
            dt.datetime.strptime(hr, "%H").strftime("%H:%M"),avg
        )
    )


# # Conclusion
# 
# The hour that receives the most comments per post on average is 15:00 (3:00 p.m. EST per the source data), with an average of 38.59 comments per post. There's about a 60% increase in the number of comments between the hours with the highest and second highest average number of comments.
# 
# In this project, we analyzed ask posts and show posts to determine which type of post and time receive the most comments on average. Based on our analysis, to maximize the amount of comments a post receives, we'd recommend the post be categorized as ask post and created between 15:00 and 16:00 (3:00 pm est - 4:00 pm est).
# 
# However, it should be noted that the data set we analyzed excluded posts without any comments. Given that, it's more accurate to say that of the posts that received comments, ask posts received more comments on average and ask posts created between 15:00 and 16:00 (3:00 pm est - 4:00 pm est) received the most comments on average.
