def write_into_file_Status(status):

	myfile.write("\n\n--> Status ::")
	myfile.write("\nMessage ID : "+str(status.id))
	myfile.write("\nMessage : "+status.text)
	myfile.write("\nWritten By : "+status._json['user']['name'])
	myfile.write("\nWritter's Username : "+status._json['user']['screen_name'])
	myfile.write("\nWritter's ID : "+str(status._json['user']['id']))



def write_into_file_func(func):

	myfile.write("\n\n\n")
	myfile.write("##################-----"+func+"------------##################")
	myfile.write("\n\n\n")


from tweepy import (
	OAuthHandler,
	API,
	Cursor,

)

consumer_key = '461XyHMzRdFHY8ZxN8XArPkoG'
consumer_secret = 'CFMsYLcFOUCEvJ6f9wtAmGjSoivtU5Dqt2NHn8ZfdRKu3fhWh3'

access_token = '794909294168854528-Gx1rbjo7iCGIQ5tGslCPuyCbDEhmD9h'
access_secret = 'jvtsr4l755InF67FIdrcOGPO1rez2xLWQ0OYkpzsoJtAW'

callback_url = "http://google.com"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

#tweeter.api take arguments like auth_handler, host, search_host,..
api = API(auth)

myfile = open('twetdata.csv', 'a')

try:

###############------------Methods Using Cursor-------#####################


###############---------search(by Location)-------#####################
#Returns tweets by users located within a given radius of the given latitude/longitude.
#parameter value is specified by “latitide,longitude,radius”

	latitude = '21.755264'
	longitude = '72.146380'
	radius = '200km'

	write_into_file_func("search(by location)")

	for i in Cursor(api.search, geocode=latitude+","+longitude+","+radius).items(200):
		write_into_file_Status(i)

	

	print("Successfully implemented search by location")



except Exception as e:

	print("Error Occured. "+ str(e) +  " Try Again. ")
