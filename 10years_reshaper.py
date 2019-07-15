import json
import requests


with open('10yearchallenge.json', 'r') as myfile:
    data=myfile.read()

things = json.loads(data)
import pandas as pd
df = pd.DataFrame(columns=['pic_url','ig_link','username','video','hash_tags',
                           'image_height','image_width','image_caption','no_people','image_desc'])

import time

start_time = time.time()
counter = 0
tagerr = 0
for data in things:
    try:
      image_height = data['dimensions']['height']
      image_width = data['dimensions']['width']
      pic_url = data['display_url']
      ig_link = "https://www.instagram.com/p/" + data['shortcode']
      if data['is_video'] == True:
          video = 'yes'
      else:
          video = 'no'
      hash_tags = data['tags']
      image_caption = data['edge_media_to_caption']['edges'][0]['node']['text']
      try:
          username = requests.get('https://api.instagram.com/oembed/?url='+ig_link)
          if username.status_code == requests.codes.ok:
              username = username.json()
              image_caption = username['title']
              username = username['author_name']
          else:
              pass
      except Exception as e:
          errors = errors + 1
          print(e, 'error number: ',errors)
      data = {'pic_url':pic_url,'ig_link':ig_link,'username':username,'video':video,
              'hash_tags':hash_tags,'image_height':image_height,'image_width':image_width,
              'image_caption':image_caption}
      df = df.append(data,ignore_index=True)
      counter = counter + 1
      if counter%1000==0:
        print("Finished: ",str(counter) ," of ", str(len(things)))   
        print("--- %s seconds ---" % (time.time() - start_time)) 
    except Exception as e:
      tagerr+=1
      if tagerr%20==0:
        print(e,tagerr)

len(things)

df.head()

df.to_csv('modified.csv',index=False)
