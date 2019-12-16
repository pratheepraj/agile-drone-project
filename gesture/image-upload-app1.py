from twython import Twython
from auth import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)

twitter = Twython(
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)

#message = "ha ha this is my first tweet using api. Hi I am Saiful"
#twitter.update_status(status=message)
#print("Tweeted: %s" % message)


message = "Yay!!! this is my 3rd tweet using api. Hi firends, I am Saiful!"
image = open('saiful-100-100.jpg', 'rb')

response = twitter.upload_media(media=image)
media_id = [response['media_id']]

twitter.update_status(status=message, media_ids=media_id)

