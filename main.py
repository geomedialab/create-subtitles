#requires oscar.mp4 video file in same folder
#transcript text file "oscar4.txt"
#might have to be in a folder name called oscar
#change certain character variables

import imageio
imageio.plugins.ffmpeg.download()
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import time
from time import strftime,localtime
from postprocess_and_fuse_subs import compileSubs
import pickle
import os

#adjust sleeping time as needed - ES
#adjust switches as needed
sleepingTime = 400

#___SWITCHES(defaults)___#

#ES: cut transcript into snippets based on the transcript's timestamps (must be set to True for other processes to run)
snipTranscript = True

#ES: upload video snippets
uploadVideos = True
#ES: if the video/caption upload process was terminated unexpectedly before and you want to continue where you left off (uploadVideos must still be set to True):
resumeUploads = False
#ES: upload snippet transcripts (.txt)
uploadTranscripts = True
#ES: download snippet subtitle files (.vtt)
downloadCaptions = True

#ES: delete uploaded video snippets from your Youtube account once subtitle processing is complete
deleteVideos = False
#ES: upload the full video and compiled transcript to your Youtube account once complete
uploadFull = False

#ES: combine vtt snippets that were downloaded from Youtube into a total subtitle file.
combineSubtitles = True
#ES: the following switches control how subtitles are altered when concatenating snippets (i.e. when combineSubtitles = True)
#ES A feature created by RG that has yet to be explored...
placeBasedTimestamping = False
#ES: resample subtitles to prevent cut-up phrases, lone-word subtitles, and improve the subtitle structure overall (can lead to short, choppy, fast subtitles that are hard to read)
resampleSubtitles = False
#ES: IF you enabled 'resampleSubtitles' (above), you have the option to make subtitle entries full sentences (not recommended, since some timestamp/subtitle units can end up being excessively large)
fullSentenceSubtitles = False
#ES: IF you enabled 'resampleSubtitles' (above), you have the option to remove subtitle entries which may be a single word (and put them in an adjacent subtitle (verify))
removeLoneWords = False

#____________#
#ES: USER INTERVIEW SECTION

def verify_y_n(a):
	while True:
		a = a.lower().strip()
		if a == 'y' or a == 'n':
			return a
		else:
			a = raw_input("Please answer 'y' or 'n': ")
			continue

def verify_y_n_none(a):
	while True:
		a = a.lower().strip()
		if a == 'y' or a == 'n' or a == '':
			return a
		else:
			a = raw_input("Please answer 'y' or 'n', or leave the answer blank by hitting 'Enter': ")
			continue

print "\n\n"
print "This application creates subtitles for a video for which you have an associated transcript. Make sure you have gone over README.md before proceeding."
time.sleep(1)
print "You may terminate the application at any point by pressing Ctrl+C (Cmd+C on Mac)."
time.sleep(1)
print "\n"

folderName = raw_input("Enter the name of the folder containing your transcript and video files\n(this folder must be located inside the 'files' folder): ")
try:
	verifyExistence = os.stat(folderName).st_size
except Exception as e:
	print e
	print "The folder named '" + folderName + "' does not exist in the current directory. Please see README.md for instructions."
	print "exiting application..."
	time.sleep(2)
	exit()
print "\n"

fileName = raw_input("Enter the file name of your transcript (excluding the \".txt\" extention): ")

try:
	verifyExistence = os.stat(folderName + '/' + fileName + '.txt').st_size
except Exception as e:
	print e
	print "The file named '" + fileName + ".txt' does not exist in the folder '" + folderName + "'. Please see README.md for instructions."
	print "exiting application..."
	time.sleep(2)
	exit()

print "\n"
originalVideo = raw_input("Enter the file name of your video (this time including the file's extention): ")

try:
	verifyExistence = os.stat(folderName + '/' + originalVideo).st_size
except Exception as e:
	print e
	print "The file named '" + originalVideo + "' does not exist in the folder '" + folderName + "'. Please see README.md for instructions."
	print "exiting application..."
	time.sleep(2)
	exit()
print "\n"

videoSize = os.stat(folderName + '/' + originalVideo).st_size/1000000

answer = raw_input("You will temporarily require " + str(videoSize) + " Mb available space on your hard drive to run this program. Continue? (y/n) ")
answer = verify_y_n(answer)

if answer == "n":
	print "Please make sure you have the available space on your hard drive, and then restart the program."
	print "exiting application..."
	time.sleep(2)
	exit()
print "\n"

while True:
	language = raw_input("Enter the language code of your video and transcript (e.g. en, fr, es, etc.):\n(You can refer to the second column in http://www.loc.gov/standards/iso639-2/php/code_list.php for the appropriate two-letter 'ISO 639-1' language code.)\n")
	if language != '':
		verifyLanguage = raw_input("\nYou have entered '" + language + "' as the language code for your transcript and video files. Youtube will use this code for processing your files. Continue? (y/n) ")
		if verifyLanguage.lower() == 'y':
			break
print "\n\n"

print "This tool:\n(1) snips your transcript (.txt) into text snippets based on its timestamps,\n(2) snips the associated video accordingly into video snippets,\n(3) uploads these video snippets to Youtube as private videos only visible to your account,\n(4) uploads the text snippets to Youtube as transcript files for these video snippets,\n(5) allows Youtube to sync the video and text snippets\n(6) downloads the text snippets as subtitle files (.vtt),\n(7) stitches these subtitle files together into a single subtitle file for your video.\n\nYou may switch these processes 'on' or 'off' depending on which steps you would like to run. If this is your first time running the tool, simply leave the following answers blank. For more advanced users or users who have already used this tool, please select which processes you would like to run: \n\n"
time.sleep(5)

answer = raw_input("\n1/6	Will you be uploading video snippets to Youtube for syncing? (y/n) ")
answer = verify_y_n_none(answer)
 
if answer == 'y':
	uploadVideos = True
elif answer == 'n':
	uploadVideos = False
elif answer == '':
	uploadVideos = True

answer = raw_input("\n2/6	Will you be resuming video uploads from a previously-initiated process? (y/n) ")
answer = verify_y_n_none(answer)

if answer == 'y':
	resumeUploads = True
elif answer == 'n':
	resumeUploads = False
elif answer == '':
	resumeUploads = False
	
answer = raw_input("\n3/6	Will you be uploading text snippets for syncing with your video snippets? (y/n) ")
answer = verify_y_n_none(answer)
			
if answer == 'y':
	uploadTranscripts = True
elif answer == 'n':
	uploadTranscripts = False
elif answer == '':
	uploadTranscripts = True

answer = raw_input("\n4/6	Will you be downloading the generated subtitle snippets from Youtube? (y/n) ")
answer = verify_y_n_none(answer)

if answer == 'y':
	downloadCaptions = True
elif answer == 'n':
	downloadCaptions = False
elif answer == '':
	downloadCaptions = True
	
answer = raw_input("\n5/6	Would you like your uploaded video snippets to be deleted from Youtube once subtitles have been successfully generated? (y/n) ")
answer = verify_y_n_none(answer)

if answer == 'y':
	deleteVideos = True
elif answer == 'n':
	deleteVideos = False
elif answer == '':
	deleteVideos = False

answer = raw_input("\n6/6	Will you be combining the downloaded subtitle snippets into a single subtitle file for your video? (y/n) ")
answer = verify_y_n_none(answer)

if answer == 'y':
	combineSubtitles = True
elif answer == 'n':
	combineSubtitles = False
elif answer == '':
	combineSubtitles = True

if combineSubtitles == True:
	answer = raw_input("\n6.1	Would you like to reorganize subtitles according to punctuation? (Experimental; can lead to short, choppy, fast subtitles that are hard to read) (y/n) ")
	answer = verify_y_n_none(answer)

	if answer == 'y':
		resampleSubtitles = True
	elif answer == 'n':
		resampleSubtitles = False
	elif answer == '':
		resampleSubtitles = False
	
	if resampleSubtitles == True:
		answer = raw_input("\n6.1.1	Would you like to reorganize subtitles to prioritize keeping full sentences intact? (Experimental; this feature is not recommended since subtitle units tend to become excessively long) (y/n) ")
		answer = verify_y_n_none(answer)

		if answer == 'y':
			fullSentenceSubtitles = True
		elif answer == 'n':
			fullSentenceSubtitles = False
		elif answer == '':
			fullSentenceSubtitles = False
			
		answer = raw_input("\n6.1.2	Would you like to reorganize subtitles to remove lone words? (Experimental) (y/n) ")
		answer = verify_y_n_none(answer)

		if answer == 'y':
			removeLoneWords = True
		elif answer == 'n':
			removeLoneWords = False
		elif answer == '':
			removeLoneWords = False
		
	answer = raw_input("\n6.2	Would you like to reorganize subtitles according to the presence of place names? (Experimental) (y/n) ")
	answer = verify_y_n_none(answer)

	if answer == 'y':
		placeBasedTimestamping = True
	elif answer == 'n':
		placeBasedTimestamping = False
	elif answer == '':
		placeBasedTimestamping = False

	print "\n6.3	If your transcript has speaker names (e.g. the interviewer or interviewee's names) that precede their discourse (e.g. \"Emmanuel: Hi, I'd like to ask you a few questions...\"), please input them. If this does not apply to your transcript, simply leave the following two answers blank by pressing the 'Enter' key."
	time.sleep(1)
	interviewer = raw_input("\n6.3.1	Please input your interviewer's name as it appears in the transcript: ")
	interviewee = raw_input("\n6.3.2	Please input your interviewee's name as it appears in the transcript: ")
	print "\n"

#____________#


# let rodolphe know if there is a problem with playlist id, might need to create a playlist in youtube online and copy url id to script
#playlistID = "PLSbFnWujSxCZxm7tYAGNeG9l5s19m4T65"

#language = 'fr'
#change these variables according to what story you want to process - ES

#interviewer = "C.V."
#interviewee = "V.S."
#where the video and txt files are stored
#folderName = 'venant'
#fileName refers to the name of the input .txt file (excluding .txt)
#fileName = 'venant'
#originalVideo refers to the name of the video file including its ext
#originalVideo = "venant.mp4"

#interviewer = "E.H."
#interviewee = "E.M."
#fileName = 'Frederic'
#originalVideo = "Frederic.mov"

#interviewer = "M.M."
#interviewee = "B.K."
#fileName = 'Berthe'
#originalVideo = "DD2FD4AE-FEE4-4DF3-9AF7-A4D6BF453B49.flv"

#interviewer = "S.G."
#interviewee = "O.G."
#folderName = 'oscar'
#fileName = 'oscar'
#originalVideo = "Oscar.mp4"




### START BOILERPLATE CODE

# Sample Python code for user authorization

import httplib2
import os
import sys
import httplib
import random

from apiclient.discovery import build
from apiclient.errors import HttpError
from apiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.

"""
to create a client secret file:
google apis dashboard --> create a new project
on the resulting dashboard, "enable apis and get credntials like keys"
search for youtube api
click "YouTube Data API v3" and ENABLE it
click "create credentials"
create and "OAUT client id"
"""

#CLIENT_SECRETS_FILE = "client_secret.json"
#api key is AIzaSyBtMCqWafhLmcFZWS3_lK0wer2edvi69Lg
#client id is in client_id.json
CLIENT_SECRETS_FILE = "client_id.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
YOUTUBE_READ_WRITE_SSL_SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = "WARNING: Please configure OAuth 2.0" 

# Authorize the request and store authorization credentials.
def get_authenticated_service(args):
	flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_READ_WRITE_SSL_SCOPE,
		message=MISSING_CLIENT_SECRETS_MESSAGE)

	storage = Storage("youtube-api-snippets-oauth2.json")
	credentials = storage.get()

	if credentials is None or credentials.invalid:
		credentials = run_flow(flow, storage, args)

	# Trusted testers can download this discovery document from the developers page
	# and it should be in the same directory with the code.
	return build(API_SERVICE_NAME, API_VERSION,
			http=credentials.authorize(httplib2.Http()))

# Explicitly tell the underlying HTTP transport library not to retry, since
# we are handling retry logic ourselves.
httplib2.RETRIES = 1

# Maximum number of times to retry before giving up.
MAX_RETRIES = 10

# Always retry when these exceptions are raised.
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, httplib.NotConnected,
	httplib.IncompleteRead, httplib.ImproperConnectionState,
	httplib.CannotSendRequest, httplib.CannotSendHeader,
	httplib.ResponseNotReady, httplib.BadStatusLine)

# Always retry when an apiclient.errors.HttpError with one of these status
# codes is raised.
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

# This method implements an exponential backoff strategy to resume a
# failed upload.
def resumable_upload(request, resource, method):
	response = None
	error = None
	retry = 0
	while response is None:
		try:
			print "Uploading file..."
			status, response = request.next_chunk()
			if response is not None:
				if method == 'insert' and 'id' in response:
					print "Video id '%s' was successfully uploaded." % response['id']
					videoid = response['id']
				elif method != 'insert' or 'id' not in response:
					print response
				else:
					exit("The upload failed with an unexpected response: %s" % response)
		except HttpError, e:
			if e.resp.status in RETRIABLE_STATUS_CODES:
				error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status,e.content)
			else:
				raise
		except RETRIABLE_EXCEPTIONS, e:
			error = "A retriable error occurred: %s" % e

		if error is not None:
			print error
			retry += 1
			if retry > MAX_RETRIES:
				exit("No longer attempting to retry.")

			max_sleep = 2 ** retry
			sleep_seconds = random.random() * max_sleep
			print "Sleeping %f seconds and then retrying..." % sleep_seconds
			time.sleep(sleep_seconds)
	return response['id']

args = argparser.parse_args()
service = get_authenticated_service(args)

def print_results(results):
	print(results)

# Build a resource based on a list of properties given as key-value pairs.
# Leave properties with empty values out of the inserted resource.
def build_resource(properties):
	resource = {}
	for p in properties:
		# Given a key like "snippet.title", split into "snippet" and "title", where
		# "snippet" will be an object and "title" will be a property in that object.
		prop_array = p.split('.')
		ref = resource
		for pa in range(0, len(prop_array)):
			is_array = False
			key = prop_array[pa]
			# Convert a name like "snippet.tags[]" to snippet.tags, but handle
			# the value as an array.
			if key[-2:] == '[]':
				key = key[0:len(key)-2:]
				is_array = True
			if pa == (len(prop_array) - 1):
				# Leave properties without values out of inserted resource.
				if properties[p]:
					if is_array:
						ref[key] = properties[p].split(',')
					else:
						ref[key] = properties[p]
			elif key not in ref:
				# For example, the property is "snippet.title", but the resource does
				# not yet have a "snippet" object. Create the snippet object here.
				# Setting "ref = ref[key]" means that in the next time through the
				# "for pa in range ..." loop, we will be setting a property in the
				# resource's "snippet" object.
				ref[key] = {}
				ref = ref[key]
			else:
				# For example, the property is "snippet.description", and the resource
				# already has a "snippet" object.
				ref = ref[key]
	return resource

# Remove keyword arguments that are not set
def remove_empty_kwargs(**kwargs):
	good_kwargs = {}
	if kwargs is not None:
		for key, value in kwargs.iteritems():
			if value:
				good_kwargs[key] = value
	return good_kwargs

### END BOILERPLATE CODE

# Sample python code for videos.insert

def videos_insert(properties, media_file, **kwargs):
	resource = build_resource(properties) # See full sample for function
	kwargs = remove_empty_kwargs(**kwargs) # See full sample for function
	request = service.videos().insert(
		body=resource,
		media_body=MediaFileUpload(media_file, chunksize=-1,
															 resumable=True),
		**kwargs
	)

	vid = resumable_upload(request, 'video', 'insert') # See full sample for function
	return vid

def hms_to_s(time):
	time = unicode(time, "UTF-8")
	time = time.split(" --> ")
	t_0 = time[0].split(":")
	t_1 = time[1].split(":")
	t0 = float(int(t_0[0])*3600) + int(float(t_0[1])*60) + int(float(t_0[2]))
	t1 = float(int(t_1[0])*3600) + int(float(t_1[1])*60) + int(float(t_1[2]))	
	return [t0,t1]

def s_to_hms(seconds):
	m, sec = divmod(seconds, 60)
	h, m = divmod(m, 60)	
	#print str(int(h)) + ":" + str(int(m)) + ":" + str(int(s))
	return str(int(h)) + ":" + str(int(m)) + ":" + str(int(sec)) 

#ES: open anita/Anita.txt as myfile
with open(folderName + "/" + fileName + ".txt", 'r') as myfile:
	text = myfile.read().replace('\n', '')
#print "ES: replace \\n with ''"

with open(folderName + "/" + fileName + ".txt") as f:
	text = f.readlines()
#print "ES: text is the following" + str(text)

#ES: strip whitespace
text = [x.strip() for x in text]

#split times (?)
splits = []
#list of cut-up texts
texts = [""]
t0 = 0
c = 0
#ES: several print commands were added for guidance. they can be removed. 

#ES: a list of the transcript's timestamps
t_list = []

#ES: PREPARE INPUT TEXT FOR PROCESSING
if snipTranscript == True:
	for t in text:
		#add a \n to the end of each line (why?)
		t += "\n"
		#ES: if the beginning of the line is not a digit and is not a next-line char
		#ES: removing punctuation from '[00:00:01.09]' since it is never qualified as a digit (False) and therefore the following condition is almost always met.
		if not t.replace('[','').replace(']','').replace(':','').replace('.','').replace('\n','').isdigit() and t != "\n":
			#ES: add t to position c of texts
			texts[c] += t#.encode('utf8')
			#print t.replace('[','').replace(']','').replace(':','').replace('.','').replace('\n','').isdigit()
			
			#ES: this will aggregate phrases (t) into one list item (a text) until a timestamp is reached
		#ES: if t is a timestamp
		#ES: removing punctuation from '[00:00:01.09]' since it is never qualified as a digit (False) and therefore the following condition is never met.
		if t != "" and t.replace('[','').replace(']','').replace(':','').replace('.','').replace('\n','').isdigit() and "[" in t:
			#increase pos on texts by 1
			c += 1
			
			#ES: printing deets
			#print t.replace('[','').replace(']','').replace(':','').replace('.','').replace('\n','').isdigit()
			#print "c: " + str(c)
			
			with open(folderName + "/" + fileName + "_" + str(c) + ".txt", 'w') as thefile:
			#thefile = open(folderName + "/" + fileName + "_" + str(c) + ".txt", 'w')
				try:
					#ES: write the previous position of c in texts (a chunk of text prior to timestamp) to thefile
					thefile.write("%s\n" % texts[c-1])
					#time.sleep(.1)
					texts.append("")
					texts[c] = ""
					#t = t.replace(" ", "")
					#t = t
					t = t.replace('[','').replace(']','').replace('\n','')
					t = unicode(t, "UTF-8")
					#split the timestamps at : (into 3)
					t = t.split(":")
					
					if len(t) == 2:
						splits.append([t0,int(t[0])*60 + int(t[1])])
						t0 = int(t[0])*60 + int(t[1])
					elif len(t) == 3:
						splits.append([t0,int(t[0])*3600 + int(t[1])*60 + float(t[2])])
						#print int(t[0])*3600 + int(t[1])*60 + int(t[2])
						t0 = int(t[0])*3600 + int(t[1])*60 + float(t[2])
						t_list.append(t0)
				except ValueError as e:
					print e
					print "\n One of your timestamps isn't formatted correctly. Consult README.md for guidelines on proper timestamp formatting."
				
	print "\nVerifying if timestamps are in ascending order..."
	
	sp1 = 0
	num = 0
	for sp in splits:
		if num > 0:
			if sp[1] <= sp1[1]:
				print "\nThere is a problem with one of your timestamps:"
				print "Timestamp number #",str(num+2)," (equivalent to ",str(sp[1])," seconds) should be a larger number than the timestamp that comes before it (",str(sp1[1])," seconds), but it is smaller."
				print "Please make sure your timestamps are in ascending order and that there are no mistakes (see README.md) and restart the program."
				exit()
		sp1 = sp
		num+=1
	
	print "\nThe document named '" + fileName + ".txt' was cut into " + str(len(splits)) + " text snippets based on it containing " + str(len(splits)) + " timestamps formatted like such '[HH:MM:SS.00]'."
else:
	print "Please set the variable 'snipTranscript' to True so that the code can properly run."
	exit()
#ES print texts[c]
#print "splits: " + str(splits)



#for i in splits:
#	print s_to_hms(i[0]),"->",s_to_hms(i[1])
	
#time.sleep(60)

#print splits,splits[len(splits)-1][1]
#splits.append([splits[len(splits)-1][1],7200])
#print splits

#print "Wait"
#time.sleep(30)
			
c = 0

#print splits
videoids = []

#videoids = [u'jDAZHgL-nG4', u'cMNTnd8pApk', u's5hLO6T_BhY', u'gOAoCh5Mecc', u'p0PX5s6k5DU', u'hSmPkLqOt0M', u'2Ik7_biRs9g', u'G64A_hpNWfI', u'ZzVVEcGekv0', u'ZxKJhN3JFfI', u'TsDnqWmpvrw', u'Kvem1XnPHF0', u'VwqhkmbiLh0', u'V1sv1MYLdC0']

#videoids = [u'cj62vgUfnik', u'5k9WCcWCLiU', u'MexTd0EGfRc', u'hWY_30yHOec', u'GrMtKARI9kQ', u'YDHnQAE7U0w', u'yc4IXkGHuXs', u'ZauR51lBjQo', u'kisoEOTjmVI', u'V9XdpjtUU4Q', u'eOdKfhePfTs', u'AAQ9YuybUxM', u'3BaTzSSL4_c', u'OriOoB5yF0s', u'91qOFKithgE', u'WQJQkGEwG-Q', u'n4eW0T6Oek0', u'2dRf-EbKYHA', u'RUgi4NfoPEw', u'n40bGD_9eZI', u'OWWAQTGKyMI', u'8a2De6Gzfek', u'VQJgxR3iAoA', u'UEzrAMq6fGc', u'PXCHMF-Z7X4', u'SU_Rbp9V_Zo', u'VLhSxDh9gI0', u'80rY1RlbVQw', u'1yumt5fRBF4', u'u5qAHXhhJoo', u'G3gO6DW-wrM', u'qAU_8DNEqP8', u'fbGaOVHXkvY', u'_Knl1rP8Z9w', u'O6f8ZWjSgiw', u'uXY-00DuLjY', u'WpreZ_gbEyw']
#with open(folderName + "/" + 'videoids.pkl', 'wb') as f:
#	pickle.dump(videoids, f)

if resumeUploads == True:
	print "\nResuming video uploads...\n"
	time.sleep(1)
	try:
		with open(folderName + "/" + 'videoids.pkl', 'rb') as f:videoids = pickle.load(f)
	except Exception as e:
		print e
		print "\nThe program is unable to resume uploads because there are no uploads to resume or your 'videoids.pkl' file has gone missing. The program will restart by uploading all videos. You may need to remove any previously-uploaded videos if the videos you are uploading are identical. If so, do this manually on youtube.com and then restart the program."
		uploadVideos = True
wait = False

def yes_or_no(question):
    while "the answer is invalid":
        reply = str(raw_input(question+' (y/n): ')).lower().strip()
        if reply[0] == 'y':
            return True
        if reply[0] == 'n':
            exit()

#ES: UPLOADS THE VIDEOS
if uploadVideos == True:
	#ES: the following is called when videos are being uploaded (uploadVideos = True) to warn the user as to how many videos will be uploaded.
	question = "\nThere were " + str(len(splits)) + " timestamps detected in " + fileName + ". " + str(len(splits)) + " video snippets will therefore be uploaded to YouTube for processing. YouTube allows a maximum of 100 video uploads per 24h using the current API credentials. Continue?"
	print "\nIf all input was correct, the program will begin snipping and uploading content to Youtube for processing. This may take between 20 minutes and several hours, depending on the size of your video file (" + str(videoSize) + " Mb)."
	yes_or_no(question)
	print "\n1. Slicing into " + str(len(splits)) + " parts & uploading videos..."
	time.sleep(1)
	if len(videoids) > 0:
		print "(However, it looks like ",len(videoids)," video snippets were already uploaded to Youtube. Now trying to resume uploading the remaining snippets...)"
		time.sleep(1)
	for s in splits:
		c += 1
		if c > len(videoids):
			ffmpeg_extract_subclip(folderName + "/" + originalVideo, s[0], s[1], targetname=folderName + "/" + fileName + "_" + str(c) +".mp4")

			media_file = folderName + '/' + fileName + "_" + str(c) + ".mp4"
			if not os.path.exists(media_file):
				exit('Please specify a valid file location.')
		
			vid = videos_insert(
					{'snippet.categoryId': '22',
					 'snippet.defaultLanguage': language,
 					 'snippet.defaultAudioLanguage': language,
					 'snippet.description': 'Description of uploaded video.',
					 'snippet.tags[]': '',
					 'snippet.title': media_file,
					 'status.embeddable': '',
					 'status.license': '',
					 'status.privacyStatus': 'unlisted',
					 'status.publicStatsViewable': ''},
					media_file,
					part='snippet,status')
			
			videoids.append(vid)
			print videoids
			#c += 1
			wait = True
			with open(folderName + "/" + 'videoids.pkl', 'wb') as f:
				pickle.dump(videoids, f)
else:
	if resumeUploads == True or deleteVideos == True or uploadTranscripts == True:
		with open(folderName + "/" + 'videoids.pkl', 'rb') as f:
			videoids = pickle.load(f)
		print "\nThe video IDs are composed of the following: " + str(videoids)

#print videoids
if resumeUploads == True or deleteVideos == True or uploadTranscripts == True:
	with open(folderName + "/" + 'videoids.pkl', 'wb') as f:
		pickle.dump(videoids, f)

if wait == True:
	print "\nWaiting for videos to be processed. It is",strftime("%H:%M:%S", localtime()),". Script will resume in " + str(sleepingTime/60) + " minutes..."
	time.sleep(sleepingTime)

#search_response = service.search().list(
#	q="Anita",
#	part="id",
#	type="video",
#	fields="items/id"
#).execute()
#
#videos = []
#
#for search_result in search_response.get("items", []):
#	videos.append("%s" % (search_result["id"]["videoId"]))
#
#print "Videos:\n", "\n".join(videos), "\n"

#ES: I don't think this function is ever called...
# Call the API's captions.insert method to upload a caption track in draft status.
def upload_caption(youtube, video_id, language, name, file):
	insert_result = youtube.captions().insert(
		part="snippet",
		body=dict(
			snippet=dict(
				videoId=video_id,
				language=language,
				name=name,
				isDraft=True
			)
		),
		media_body=file
	).execute()

	id = insert_result["id"]
	name = insert_result["snippet"]["name"]
	language = insert_result["snippet"]["language"]
	status = insert_result["snippet"]["status"]
	#print "Uploaded caption track '%s(%s) in '%s' language, '%s' status." % (name,
	#		id, language, status)


c = 1
captionsids = [] 
wait = False

if uploadTranscripts == True:
	
	#print splits,videoids
	#uploads transcripts
	print "\nUploading transcripts..."
	
	for s in splits:
		print c,s
		media_file = folderName + '/' + fileName + "_" + str(c) + ".flv"
		caption_file = folderName + '/' + fileName + "_" + str(c) + ".txt"
		#print s,media_file,caption_file,videoids[c-1]

		a = service.captions().insert(
				part="snippet",
				body=dict(
					snippet=dict(
						videoId=videoids[c-1],
						language=language,
						name=media_file,
						isDraft=True,
						sync=True
					)
				),
				media_body=caption_file
			).execute()
		captionsids.append(a['id'])
		c += 1
		#print a
		wait = True
	with open(folderName + "/" + 'captionsids.pkl', 'wb') as f:
		pickle.dump(captionsids, f)
	print "Waiting for transcripts to be processed into captions. It is",strftime("%H:%M:%S", localtime()),". Script will resume in " + str(2 * sleepingTime / 60) + " minutes..."
	time.sleep(2 * sleepingTime)
else:
	if downloadCaptions == True:
		with open(folderName + "/" + 'captionsids.pkl', 'rb') as f:
			captionsids = pickle.load(f)

#if wait == True:
if downloadCaptions == True:
	print "\nDownloading captions..."

	c = 1
	waitLonger = True
	for s in splits:
		print c,s,captionsids[c-1]
		sub_txt = ""
		while waitLonger == True:
			try:
				subtitle = service.captions().download(id=captionsids[c-1],tfmt='vtt').execute()
				waitLonger = False
			except:
				waitLonger = True
				print "Waiting for transcripts " + str(c) + " " + captionsids[c-1] + " to be processed into captions. It is",strftime("%H:%M:%S", localtime()),". Script will resume in " + str(2) + " minutes..."
				time.sleep(120)
		sub_txt += subtitle
		
		cc = ""
		if c < 10:
			cc = "0" + str(c)
		else:
			cc = str(c)
		
		#print subtitle
		print cc
		
		with open(folderName + "/" + fileName + "_" + str(cc) + ".vtt", 'w') as thefile:
			#thefile.write(sub_txt)
			thefile.write(subtitle)
		if cc == "31":
			print subtitle
		
		c += 1

	time.sleep(3)
		
#deletes videos from youtube -ES
if deleteVideos == True:
	print "\nDeleting videos...\n"

	c = 1
	for s in splits:
		print c,videoids[c-1]
		service.videos().delete(
			id=videoids[c-1]
			).execute()
		c += 1
	
	time.sleep(10)

if combineSubtitles == True:
	#compiles them all
	print "\nCombining subtitle snippets ..."
	#ES: this is a feature that needs exploration so as to make sure that place names are never split between 2 timestamps, at the least.
	#place-based time stamping can be set to True or False (make a variable for this)
	compiledSubs = compileSubs(folderName,fileName,[['_high-frequency-timestamps',0,placeBasedTimestamping]],t_list,interviewer,interviewee,False,language,resampleSubtitles,fullSentenceSubtitles,removeLoneWords)

	time.sleep(10)

#thefile = open(folderName + "/" + fileName + ".srt", 'w')
#thefile.write(compiledSubs)

if uploadFull == True:
	print "\nUploading full video..."

	vid = videos_insert(
			{'snippet.categoryId': '22',
			 'snippet.defaultLanguage': language,
			 'snippet.description': 'Description of uploaded video.',
			 'snippet.tags[]': '',
			 'snippet.title': fileName,
			 'status.embeddable': '',
			 'status.license': '',
			 'status.privacyStatus': 'unlisted',
			 'status.publicStatsViewable': ''},
			folderName + "/" + originalVideo,
			part='snippet,status')

	# place video in custom playlist
	def playlist_items_insert(properties, **kwargs):
		resource = build_resource(properties) # See full sample for function
		kwargs = remove_empty_kwargs(**kwargs) # See full sample for function
		results = service.playlistItems().insert(
			body=resource,
			**kwargs
		).execute()

		print_results(results)
#'snippet.playlistId': playlistID,
	playlist_items_insert(
			{'snippet.resourceId.kind': 'youtube#video',
			 'snippet.resourceId.videoId': vid,
			 'snippet.position': ''},
			part='snippet',
			onBehalfOfContentOwner='')

	print "Waiting for full video to be processed. It is",strftime("%H:%M:%S", localtime()),". Script will resume in " + str(sleepingTime/60) + " minutes..."
	time.sleep(sleepingTime)

	id = vid
			
	print "\nUploading compiled subtitles..."
	caption_file = folderName + '/' + fileName + ".srt"
	service.captions().insert(
					part="snippet",
					body=dict(
						snippet=dict(
							videoId=id,
							language=language,
							name=originalVideo,
							isDraft=True,
							sync=False
						)
					),
					media_body=caption_file
				).execute()
			
	print "\nFull video is soon available on your Youtube channel for you to check and adjust captions."
