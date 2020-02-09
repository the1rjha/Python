#!/usr/bin/env python
# coding: utf-8

# ## Ravi's Analysis of Apps in App Store and Google Play
# This analysis project will look at apps in Apple's App Store and Google's Google Play Store by pulling data from different type of apps (Free vs. Paid) and looking at the number of users. After having the data in a usable format, the plan will be to analyze the apps to determine which type of apps engage the most users, so an app development company can develop appropriate apps.

# In[2]:


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

# In[6]:


print(android[0])
print('\n')
print(android[10472])
print('\n')
print(android[10470])
print('\n')
del android[10472]
print("Number of remaining rows:", len(android)) #Should be 10,840 rows after deletion of row 10472


# ## Removing Duplicate Entries
# If we explore the Google Play data set long enough, we'll find that some apps have more than one entry. For instance, the application Instagram has four entries:

# In[7]:


for app in android:
    name = app[0]
    if name == 'Instagram':
        print(app)


# Going to evaluate the Android dataset to see how many duplicate apps appear. Will use a for loop for the datasets with an empty lists initialized before the for loop. The for loop will loop through the dataset and add each app name to the unique app list. The if statement will check to see if the app name the loop is iterating thorugh is already in the unique app list. If it is, the app name will be added to the duplicate app list. Otherwise, the app will be added to the unique name list. The loop will terminate once it has gone through the entire dataset.

# In[8]:


android_duplicate_apps = []
android_unique_apps = []

for app in android:
    name = app[0]
    if name in android_unique_apps:
        android_duplicate_apps.append(name)
    else:
        android_unique_apps.append(name)
        
print('Number of duplicate android apps:', len(android_duplicate_apps))
print('\n')
print('Examples of duplicate android apps:', android_duplicate_apps[:15])
print('\n')
print('Expected length:', len(android) - 1181)


# Since there are so many duplicate apps in Android, duplicates will be removed. The way this will be done will be to examine all the duplicate entries and look at the number of reviews. The app entry with the highest number of reviews will be utilized since that is the most recent data, and all other app entries will be removed.
# 
# 
# In a previous code cell, we found that there are 1,181 cases where an app occurs more than once, so the length of our dictionary (of unique apps) should be equal to the difference between the length of our data set and 1,181.

# In[10]:


reviews_max = {}

for app in android:
    name = app[0]
    n_reviews = float(app[3])
    if name in reviews_max and reviews_max[name] < n_reviews:
        reviews_max[name] = n_reviews
    elif name not in reviews_max:
        reviews_max[name] = n_reviews
        
print('Expected length:', len(android) - 1181)
print('Actual length:', len(reviews_max))


# Now, let's use the reviews_max dictionary to remove the duplicates. For the duplicate cases, we'll only keep the entries with the highest number of reviews. In the code cell below:
# 
#  - We start by initializing two empty lists, android_clean and already_added.
#  - We loop through the android data set, and for every iteration:
#      - We isolate the name of the app and the number of reviews.
#      - We add the current row (app) to the android_clean list, and the app name (name) to the already_cleaned list if:
#          - The number of reviews of the current app matches the number of reviews of that app as described in the reviews_max dictionary; and
#          - The name of the app is not already in the already_added list. We need to add this supplementary condition to account for those cases where the highest number of reviews of a duplicate app is the same for more than one entry (for example, the Box app has three entries, and the number of reviews is the same). If we just check for reviews_max[name] == n_reviews, we'll still end up with duplicate entries for some apps.

# In[12]:


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

# In[13]:


explore_data(android_clean, 0, 3, True)


# # # Removing Non-English Apps
# The apps we want to develop are for an English speaking audience. The data contains apps that have non-English characters. Therefore, we need to remove the Non-English apps from the store. First, a function will be written to look at an app's name to determine if it is all English text. English text are all in the range 0 to 127.

# In[24]:


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

# In[26]:


print(is_english_text('Docs To Go™ Free Office Suite'))
print(is_english_text('Instachat 😜'))

print(ord('™'))
print(ord('😜'))


# Below is a re-worked is_english_text function that will check to see if there are more than 3 non-English characters in a string. If there is more than 3, the string will fail.

# In[51]:


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

# In[56]:


ios_english = []
android_english = []

for app in ios:
    name = app[2]
    if is_english_text(name):
        ios_english.append(app)
        
for app in android_clean:
    name = app[0]
    if is_english_text(name):
        android_english.append(app)
        
explore_data(android_english, 0, 3, True)
print('\n')
explore_data(ios_english, 0, 3, True)
print('\n')
print('Number of rows in ios:', len(ios_english))
print('Number of rows in Android:', len(android_english))


# In[ ]:




