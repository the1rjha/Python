#!/usr/bin/env python
# coding: utf-8

# ## Ravi's Analysis of Apps in App Store and Google Play
# This analysis project will look at apps in Apple's App Store and Google's Google Play Store by pulling data from different type of apps (Free vs. Paid) and looking at the number of users. After having the data in a usable format, the plan will be to analyze the apps to determine which type of apps engage the most users, so an app development company can develop appropriate apps.

# In[1]:


from csv import reader
#Opening the Apple App Store data and converting it into a list
#Apple data from - https://www.kaggle.com/ramamet4/app-store-apple-data-set-10k-apps/home#AppleStore.csv
apple_opened_file = open('AppleStore.csv', encoding = 'utf8')
apple_read_file = reader(apple_opened_file)
ios = list(apple_read_file)
ios_header = ios[0]
ios = ios[1:]

#Opening the Google Play Store data and converting it into a list
#Google data from - https://www.kaggle.com/lava18/google-play-store-apps/home#googleplaystore.csv
google_opened_file = open("googleplaystore.csv", encoding = 'utf8')
google_read_file = reader(google_opened_file)
android = list(google_read_file)
android_header = android[0]
android = android[1:]

def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]    
    for row in dataset_slice:
        print(row)
        print('\n') # adds a new (empty) line after each row

    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))

#Printing out the first few rows to ensure files were read properly as well as total number of rows and columns for each data set
#ios
print(ios_header)
print('\n')
explore_data(ios, 0, 6, True)
print('\n')

#Android
print(android_header)
print('\n')
explore_data(android, 0, 6, True)
print('\n')


# ## Data Cleaning
# The Google Play data set has a dedicated discussion section, and we can see that one of the discussions outlines an error for row 10472. The row 10472 corresponds to the app Life Made WI-Fi Touchscreen Photo Frame, and we can see that the rating is 19. This is clearly off because the maximum rating for a Google Play app is 5. As a consequence, we'll delete this row.

# In[2]:


print(android[0])
print('\n')
print(android[10472])
print('\n')
print(android[10470])
print('\n')
del android[10472]
print("Number of remaining rows in Android:", len(android)) #Should be 10,840 rows after deletion of row 10472


# ## Removing Duplicate Entries
# If we explore the Google Play data set long enough, we'll find that some apps have more than one entry. For instance, the application Instagram has four entries:

# In[3]:


for app in android:
    name = app[0]
    if name == 'Instagram':
        print(app)


# Going to evaluate the Android dataset to see how many duplicate apps appear. Will use a for loop for the datasets with an empty lists initialized before the for loop. The for loop will loop through the dataset and add each app name to the unique app list. The if statement will check to see if the app name the loop is iterating thorugh is already in the unique app list. If it is, the app name will be added to the duplicate app list. Otherwise, the app will be added to the unique name list. The loop will terminate once it has gone through the entire dataset.

# In[4]:


android_duplicate_apps = []
android_unique_apps = []

for app in android:
    name = app[0]
    if name in android_unique_apps:
        android_duplicate_apps.append(name)
    else:
        android_unique_apps.append(name)
        
print('Number of duplicate Android apps:', len(android_duplicate_apps))
print('\n')
print('Examples of duplicate Android apps:', android_duplicate_apps[:15])
print('\n')
print('Expected length of Android apps:', len(android) - 1181)


# Since there are so many duplicate apps in Android, duplicates will be removed. The way this will be done will be to examine all the duplicate entries and look at the number of reviews. The app entry with the highest number of reviews will be utilized since that is the most recent data, and all other app entries will be removed.
# 
# 
# In a previous code cell, we found that there are 1,181 cases where an app occurs more than once, so the length of our dictionary (of unique apps) should be equal to the difference between the length of our data set and 1,181.

# In[5]:


reviews_max = {}

for app in android:
    name = app[0]
    n_reviews = float(app[3])
    if name in reviews_max and reviews_max[name] < n_reviews:
        reviews_max[name] = n_reviews
    elif name not in reviews_max:
        reviews_max[name] = n_reviews
        
print('Expected length for Android dataset:', len(android) - 1181)
print('Actual length of Android dataset:', len(reviews_max))


# Now, let's use the reviews_max dictionary to remove the duplicates. For the duplicate cases, we'll only keep the entries with the highest number of reviews. In the code cell below:
# 
#  - We start by initializing two empty lists, android_clean and already_added.
#  - We loop through the android data set, and for every iteration:
#      - We isolate the name of the app and the number of reviews.
#      - We add the current row (app) to the android_clean list, and the app name (name) to the already_cleaned list if:
#          - The number of reviews of the current app matches the number of reviews of that app as described in the reviews_max dictionary; and
#          - The name of the app is not already in the already_added list. We need to add this supplementary condition to account for those cases where the highest number of reviews of a duplicate app is the same for more than one entry (for example, the Box app has three entries, and the number of reviews is the same). If we just check for reviews_max[name] == n_reviews, we'll still end up with duplicate entries for some apps.

# In[6]:


#Removing duplicate rows
android_clean = []
already_added = []

for app in android:
    name = app[0]
    n_reviews = float(app[3])
    if (n_reviews == reviews_max[name]) and (name not in already_added):
        android_clean.append(app)
        already_added.append(name)
        
print(len(android_clean))


# Now let's quickly explore the new data set, and confirm that the number of rows is 9,659.

# In[7]:


explore_data(android_clean, 0, 3, True)


# ## Removing Non-English Apps
# The apps we want to develop are for an English speaking audience. The data contains apps that have non-English characters. Therefore, we need to remove the Non-English apps from the store. First, a function will be written to look at an app's name to determine if it is all English text. English text are all in the range 0 to 127.

# In[8]:


#Examples of non-English apps
print(ios[304][2])
print(ios[2071][2])

print(android_clean[4412][0])
print(android_clean[7940][0])

def is_english_text(astring):
    for character in astring:
        if ord(character) > 127:
            return False
    return True

#Test Cases        
print(is_english_text('Instagram'))
print(is_english_text('爱奇艺PPS -《欢乐颂2》电视剧热播'))
print(is_english_text('Docs To Go™ Free Office Suite'))
print(is_english_text('Instachat 😜'))


# Some English app names use emojis or other symbols (™, — (em dash), – (en dash), etc.) that fall outside of the ASCII range. Because of this, we'll remove useful apps if we use the function in its current form.

# In[9]:


print(is_english_text('Docs To Go™ Free Office Suite'))
print(is_english_text('Instachat 😜'))

print(ord('™'))
print(ord('😜'))


# Below is a re-worked is_english_text function that will check to see if there are more than 3 non-English characters in a string. If there is more than 3, the string will fail.

# In[10]:


def is_english_text(astring):
    non_ascii = 0
    for character in astring:
        if ord(character) > 127:
            non_ascii += 1
        
    if non_ascii > 3:
        return False
    else:
        return True

print(is_english_text('Docs To Go™ Free Office Suite'))
print(is_english_text('Instachat 😜'))


# The function is still not perfect, and very few non-English apps might get past our filter, but this seems good enough at this point in our analysis — we shouldn't spend too much time on optimization at this point.
# 
# Now the re-worked function will be used to filter out the non-English apps for both ios and Android.

# In[11]:


ios_english = []
android_english = []

for app in ios:
    name = app[1]
    if is_english_text(name):
        ios_english.append(app)
        
for app in android_clean:
    name = app[0]
    if is_english_text(name):
        android_english.append(app)

explore_data(ios_english, 0, 3, True)
print('\n')
explore_data(android_english, 0, 3, True)
print('\n')
print('Number of rows in ios:', len(ios_english))
print('Number of rows in Android:', len(android_english))


# ## Free Apps
# We want to develop free apps that make money through in-app ads. The data contains free and non-free apps. Therefore, we will go through the datasets and identify the free apps.

# In[32]:


#ios

free_ios_apps = []

for app in ios_english:
    name = app[1]
    price = app[4]
    if price == '0.0':
        free_ios_apps.append(app)

print("Number of free ios apps: ", len(free_ios_apps))

#Android

free_android_apps = []

for app in android_english:
    name = app[0]
    price = app[7]
    if price == '0':
        free_android_apps.append(app)

print("Number of free Android apps: ", len(free_android_apps))


# ## Most Common Apps by Genre
# We are looking to determine the kinds of apps that are likely to attract more users because our revenue is highly influenced by the number of people using our apps.
# 
# To minimize risks and overhead, our validation strategy for an app idea is comprised of three steps:
# 
#  - Build a minimal Android version of the app, and add it to Google Play.
#  - If the app has a good response from users, we then develop it further.
#  - If the app is profitable after six months, we also build an iOS version of the app and add it to the App Store.
# 
# Because our end goal is to add the app on both the App Store and Google Play, we need to find app profiles that are successful on both markets. For instance, a profile that might work well for both markets might be a productivity app that makes use of gamification.
# 
# Let's begin the analysis by getting a sense of the most common genres for each market. For this, we'll build a frequency table for the prime_genre column of the App Store data set, and the Genres and Category columns of the Google Play data set.
# 
# We'll build two functions to aid in determining most common genres. One will generate a frequency table that show percentages. The other function will display the percentages in a descending order.

# In[13]:


def freq_table(dataset, index):
    frq_table = {}
    total = 0 #Used for tracking total number of apps analyzed and later used for calculating percentage

    for row in dataset:
        total += 1
        category = row[index]
        if category in frq_table:
            frq_table[category] += 1
        else:
            frq_table[category] = 1
            
    table_percentages = {}
    for key in frq_table:
        percentage = (frq_table[key] / total) * 100
        table_percentages[key] = percentage
        
    return table_percentages

def display_table(dataset, index):
    table = freq_table(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)
        
    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])


# In[14]:


#prime_genre column for ios
display_table(free_ios_apps, 11)
print('\n')

#Genres and category for Android
display_table(free_android_apps, 9)
print('\n')
display_table(free_android_apps, 1)


# After analyzing the data, for ios, Games is the top genre of apps. For Android, the top genre is Tools and the top category is family. The difference between the Genres and the Category columns is not crystal clear, but one thing we can notice is that the Genres column is much more granular (it has more categories). We're only looking for the bigger picture at the moment, so we'll only work with the Category column moving forward.
# 
# Up to this point, we found that the App Store is dominated by apps designed for fun, while Google Play shows a more balanced landscape of both practical and for-fun apps. Now we'd like to get an idea about the kind of apps that have most users.
# 
# In the cell below, we will calculate the average number of installs for each app genre. For Google, we will refer to data in the Installs column. For ios, there isn't an equivalent column, so we will the use rating_count_tot column to get an idea of installs.

# In[39]:


#Calculating average number of ratings per genre for ios
ios_frequencies = freq_table(free_ios_apps, 11)

for genre in ios_frequencies:
    total = 0
    len_genre = 0
    
    for app in free_ios_apps:
        genre_app = app[11]
        if genre_app == genre:
            n_ratings = float(app[5])
            total += n_ratings
            len_genre += 1
    avg_n_ratings = total / len_genre
    print(genre, ':', avg_n_ratings)


# ## App Profile Recommendation for ios
# 
# Based on the results, the genre of apps with the highest average number of ratings are: 1) Navigation, 2) Reference, and 3) Social Networking. However, when you look at the apps in these genres, you see that the top 2-3 apps for each genre have a high number of ratings, which skews the results towards those categories of apps.
# 
# However, the Reference genre might have some potential. One thing we could do is take another popular book and turn it into an app where we could add different features besides the raw version of the book. This might include daily quotes from the book, an audio version of the book, quizzes about the book, etc. On top of that, we could also embed a dictionary within the app, so users don't need to exit our app to look up words in an external app.
# 
# This idea seems to fit well with the fact that the App Store is dominated by for-fun apps. This suggests the market might be a bit saturated with for-fun apps, which means a practical app might have more of a chance to stand out among the huge number of apps on the App Store.

# In[51]:


for app in free_ios_apps:
    if app[11] == 'Navigation':
        print(app[1], ':', app[5]) # print name and number of ratings

print('\n')
        
for app in free_ios_apps:
    if app[11] == 'Reference':
        print(app[1], ':', app[5]) # print name and number of ratings

print('\n')
        
for app in free_ios_apps:
    if app[11] == 'Social Networking':
        print(app[1], ':', app[5]) # print name and number of ratings


# In[44]:


#Calculating average number of installs per category for Android
android_frequencies = freq_table(free_android_apps, 1)

for category in android_frequencies:
    total = 0
    len_category = 0
    
    for app in free_android_apps:
        category_app = app[1]
        if category_app == category:
            n_installs = app[5]
            n_installs = n_installs.replace(',', '')
            n_installs = n_installs.replace('+', '')
            total += float(n_installs)
            len_category += 1
    avg_n_installs = total / len_category
    print(category, ':', avg_n_installs)


# ## App profile recommendation for Android
# 
# Based on the results, the category of apps with the highest average number of installs are: 1) Communication, 2) Video Players, and 3) Social. However, when you look at the apps in these genres, you see that the top 2-3 apps for each genre have a high number of average installs, which skews the results towards those categories of apps.
# 
# However, since we want to build the same app for Android as ios, we want to examine the Books and Reference category to see if there is opportunity. Based on the results for that category, we see there aren't as many popular apps like in Communication, Video Players, and Social. One thing we could do is take another popular book and turn it into an app where we could add different features besides the raw version of the book. This might include daily quotes from the book, an audio version of the book, quizzes about the book, etc. On top of that, we could also embed a dictionary within the app, so users don't need to exit our app to look up words in an external app.

# In[58]:


print("Communication:")
for app in free_android_apps:
    if app[1] == 'COMMUNICATION':
        print(app[0], ':', app[5]) # print name and number of installs

print('\n')

print("Video Players:")
for app in free_android_apps:
    if app[1] == 'VIDEO_PLAYERS':
        print(app[0], ':', app[5]) # print name and number of installs

print('\n')
 
print("Social:")    
for app in free_android_apps:
    if app[1] == 'SOCIAL':
        print(app[0], ':', app[5]) # print name and number of installs
        
print('\n')

print("Books and Reference:")
for app in free_android_apps:
    if app[1] == 'BOOKS_AND_REFERENCE':
        print(app[0], ':', app[5])


# In[ ]:




