- the following files should be included in this folder:

README.md
main.py
postprocess_and_fuse_subs.py
requirements.txt
client_id.json
run.bat

=== REQUIREMENTS ===
====================

You will require:
	- at least 100 Mb of space on you hard drive
	- an internet connection
	- a Google user account
	- Python 2.7 installed
		To install Python 2.7 on your computer...
		
		PC:
		Install Python 2.7.12:
		download: https://www.python.org/downloads/release/python-2712/
		When installing, make sure all boxes are checked in the install dialog.
		
		Mac:
		install Python 2.7.16:
		download: https://www.python.org/downloads/release/python-2716/
		Once installed, double-click the "Install Certificates.command" file in the installed python 2.7 app folder.


=== Installing the program ===
==============================

PC:
Double-click pc.bat (or run it in command line). The program will install the required files in a subfolder called 'files'. Run pc.bat again once installation has completed to start using the program.

Mac:
Under development


=== Setting up your media ===
=============================

- Create new folder inside the subfolder entitled 'files' and place your video and transcript files inside this folder.
- Your video can be of any file format
- Your transcript must be in .txt format (UTF-8 encoding is preferred).
	Your transcript will require a timestamp at every 10-minute interval for optimal processing by Youtube.
	The format of these timestamps must be the following: [HH:MM:SS.00] (microseconds are not required)
		Make sure to check your timestamps for formatting and number errors...

	
=== running the pipeline ===
============================

The program will ask you to specify the folder containing your media (video and transcript), the name of your transcript file, and the name of your video file. The program will then proceed to ask you some questions, allowing you to control specific parameters if need be. You may leave these questions blank if you want to proceed with the program's default parameters.

(Controlling which processes are to be run can be useful if the program terminated inadvertantly - due to a loss of internet connection, for example - and you need to start from where you left off. This can be especially useful when your video file is very large, meaning you can avoid having to upload the whole file again.)

Once completed, your final .vtt, .srt and .txt files will be available in your media folder within a subfolder called 'output'.

If there are any errors in your subtitle files due to very poor audio quality in your video, you may go to Youtube and edit the snippet subtitles directly from within Youtube's interface.

To view and/or edit your subtitles directly on Youtube:
---------------------------------------------

Youtube provides a useful subtitle editing platform that may come in handy if the audio quality in your video is very poor and leads to subtitle syncing errors. If this is happening, then you may want to edit your subtitles manually on Youtube.

To access your private Youtube videos:
- From your Youtube channel, click CUSTOMIZE CHANNEL > Videos (tab)
To access/edit/delete any and all Youtube videos:
- From your Youtube channel, click CREATOR STUDIO > Select videos to be deleted > Actions (dropdown) > Delete

Once having done this, you will need to run the program again, this time disabling any upload parameters (1-3), and enabling the 'download subtitle' and 'combine subtitle' parameters (4,6).


=== A note on Youtube credentials ===
=====================================

Since December 2018, all new projects using the "YouTube Data API v3" have a limit of 10 000 credits, whereas older projects have 1 000 000 credits. A single video upload takes up 1 600 credits. Therefore, you will be using the 'client_id.json' file provided, instead of creating your own. This means that your video snippet uploads will be using credits from an older project ("transcript-tether") that has more credits. Still, there seems to be an absolute cap on even old projects of 100 videos per day (despite this not adding up to 1 million credits...), so if you are running this script on the same day as other users of this package, you may encounter errors. You might also want to make sure that there are no more than 100 timestamps contained in the transcript you will be processing, since this will result in the creation of 100 videos...

IF you would like to run this script using your own Google credentials and overcome the limitations currently in place, see endnotes.

=========
ENDNOTES:
=========

The current product uses API credentials from its creator ('transcript-tether' project, by the Geomedia Lab). It needs to be run at least once every 90 days, otherwise it will be deactivated automatically by Google :(

IF you want to run this script using credentials from your own Google account (instructions from Winter 2019):

- go to https://console.cloud.google.com
- select a project > New project
- once a new project is created, make sure it's selected. On the left-pane, click 'APIs and Services' > Dashboard
- click + ENABLE APIS AND SERVICES, and search for and open the "YouTube Data API v3"
- click ENABLE
- Again under "APIs and Services" go to "Credentials" in the left pane
- Click "Create credentials" and then click "OAuth client ID"
- Click "Other"
- ignore the popup, in the restulting "Credentials" page, download the credentials you just created (download symbol on the right) and save it as 'client_id.json' in your virtual environment folder (i.e. 'files' folder).

- unless you have have an old Google project with the API in question already enabled, or unless your video is only sectionable into 6 snippets (i.e. it contains 7 timestamps), you will need to increase your quota limit.
	- to increase your limit, go to your project page (e.g. https://console.developers.google.com/apis/dashboard?project=PROJECTNAME)
	- On the Dashboard page, click on the "YouTube Data API v3" at the bottom of the page
	- click on the Quotas tab
	- Next to "Queries per day", click the edit icon
	- click "apply for a higher quota" and fill out the form (link also available here: https://docs.google.com/forms/d/e/1FAIpQLSd5HxReFtxATJLNfLwQiucfQwYL295Xemgc6nhFXo1vcitg3A/viewform)
- the request form takes about 10 minutes to fill out... the response time for Google is not certain, nor is a positive response guaranteed.