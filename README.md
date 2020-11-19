About
=====

This research tool is intended to help turn verbatim transcripts for video recordings into subtitle files. It can also be used for concatenating standalone subtitle files you may already have.

Youtube provides a *Creator Studio* for turning transcripts into subtitles, yet results tend to be unsatisfactory for longer videos. This tool uses Youtube API and some python code to solve this problem by taking a video file and an appropriately timestamped verbatim transcript file, snipping them into pieces, uploading them to Youtube for syncing, downloading the generated subtitle files and stitching them together into a final subtitle file.

The tool was developed in the context of ***Atlascine 4.0***, an online story mapping research tool developed by the Geomedia Lab at Concordia University in collaboration with the Geomatics and Cartographic Research Centre (GCRC) at Carleton University. More information on this CANARIE-funded project can be found by visiting http://geomedialab.org/

To begin
========

Start by downloading this repository to your local machine...

Requirements
===================

You will require:
- A PC or Mac computer (PC preferred)
- at least 100 Mb of space on you hard drive
- an internet connection
- A Youtube Channel (created using a Google user account)
- Python 2.7 installed
	- To install Python 2.7 on your computer...
		- PC:	Python 2.7.12: https://www.python.org/downloads/release/python-2712/ (When installing, make sure all boxes are checked in the install dialog.)
		- Mac:	Python 2.7.16: https://www.python.org/downloads/release/python-2716/ (Once installed, double-click the *Install Certificates.command* file in the installed python 2.7 app folder.)
	- You should make sure that the command `python` is indeed python 2.7. To verify this, open command line (PC) or terminal (Mac) and enter `python --version`. This should show you the version of python that is running. If not, then make sure you have properly installed python 2.7.
		- if you have a different python 2.7 command (ex.: `py -2`, `python2`, etc.), then you could alternatively *replace all* instances of *python* in the file **pc.bat** with your appropraite python 2.7 command...

Installing the tool
===================

- PC: Double-click **pc.bat** (or run it in command line). The program will install the required files in a subfolder it will generate called **/files**.
- Mac: There is currently no bash file to run this tool in the terminal. If you are familiar with the terminal, you may install the virtual environment and activate it manually by emulating the commands found in **pc.bat** within the terminal. Contact the Geomedia Lab if you need assistance.

Setting up your video and transcript files
==========================================

Once you have succesfully installed the program:
- Create a new folder inside the subfolder entitled **/files** and place your video and transcript files inside this folder (your video can be of any file format).
- Your transcript must be in *.txt* format (UTF-8 encoding is preferred).
- Your transcript will require accurate timestamps (roughly 10-minute intervals between timestamps are recommended for optimal processing by Youtube). Be sure to also add a final timestamp that demarcates the end of your video.
	- The format of these timestamps must be the following: `[HH:MM:SS.00]` (microseconds are not required). Timestamps must also be separated from surrounding text by a blank line. Example:

```
E.B.: C'est un choc. Mais en même temps je voyais la reconstruction physique. Physiquement c'est vraiment un beau pays le Rwanda. C'est là où je me suis souvenu...j'ai commencé en disant que les Canadiens ou les Européens disaient que le Rwanda était un beau pays, je ne voyais pas en quoi ce pays était beau. Là après avoir vu d'autres pays en Afrique, après avoir voyagé, c'est vrai que c'est un beau pays.

[02:26:07.00]

J.B.G.: Pour revenir sur la reconstruction physique je ne sais pas s'il y avait aussi une reconstruction psychologique?
```

- Finally, you must add a timestamp that demarcates the end of your video.

Running the tool
================

- PC: Double-click **pc.bat** (or run it in command line).
- The program will ask you to specify the *folder containing your media files*, the *name of your transcript file*, and the *name of your video file*. The program will then proceed to ask you some questions, allowing you to control specific parameters if need be. You may leave these questions blank if you want to proceed with the program's default parameters.
	- (Controlling which processes are to be run can be useful if the program terminated inadvertantly - due to a loss of internet connection, for example - and you need to start from where you left off. This can be especially useful when your video file is very large, meaning you can avoid having to upload the whole file again.)
- Once parameters are set, if this is your first time using the tool, your browser will open automatically for you to authenticate the tool to access your Youtube (Google) account. You will be prompted to sign into your Google account and click to authenicate (you may need to click *Advanced* first if the page tells you the app isn't verified by Google...). A page will appear stating *The authentication flow has completed*. You may then exit your browser.
- Once the tool has finished running, your final *.vtt*, *.srt* and *.txt* files will be available in your media folder within a subfolder called **/output**. You can then use the *.srt* or *.vtt* files as subtitles for your video in any media player.
	- If there are any major syncing errors in your subtitle files due to very poor audio quality in your video, you may go to Youtube and manually make adjustments the snippet subtitles directly from within Youtube*s interface.

	

Working with Youtube directly:
-------------------------------------------------------

Youtube provides a useful subtitle editing platform that may come in handy if the audio quality in your video is very poor and leads to subtitle syncing errors. If this is happening, then you may want to edit your subtitles manually on Youtube. Alternatively, if your media file is shorter than 10 minutes long, then you may also choose to forego using this tool entirely and try uploading and synchronizing your transcript using Youtube's interface.

- To edit a subtitle file directly from Youtube's interface:
	- When logged into your Youtube channel, click **Your Videos** on the left (this is where you will find any videos you may have uploaded or wish to upload with the tool). If you wish, you may upload videos and transcript files directly from within this page.
	- To edit any previously uploaded transcripts:
		- Hover over a video and click **Details**
		- In the next page, click **Subtitles** on the left
		- Then, click **EDIT** for the transcript file you wish to edit.

If you are doing this to correct subtitles from videos that you have already snipped and uploaded using this command line tool, you will need to run the command line tool again: this time disabling any upload parameters and enabling only the *download subtitle* and *combine subtitle* parameters (5,7).

A note on Youtube credentials
-----------------------------

Since December 2018, all new projects using the *YouTube Data API v3* have a limit of 10 000 credits, whereas older projects have 1 000 000 credits. A single video upload takes up 1 600 credits. Therefore, you will be using the **client_id.json** file provided, instead of creating your own. This means that your video snippet uploads will be using credits from an older project (*transcript-tether*) that has more credits. Still, there seems to be an absolute cap on even old projects of ~400 videos per day, so if you are running this script on the same day as other users of this package, you may encounter errors. You might also want to make sure that there are no more than 400 timestamps contained in the transcript you will be processing, since this will result in the creation of 400 videos...

The current product uses API credentials from its creator (*transcript-tether* project, by the Geomedia Lab). The credentials need to be used at least once every 90 days, otherwise they will be deactivated automatically by Google :(

IF you would like to run this script using credentials from your own Google account (instructions from Winter 2019):

- go to https://console.cloud.google.com
- select a project > New project
- once a new project is created, make sure it*s selected. On the left-pane, click *APIs and Services* > Dashboard
- click + ENABLE APIS AND SERVICES, and search for and open the *YouTube Data API v3*
- click ENABLE
- Again under *APIs and Services* go to *Credentials* in the left pane
- Click *Create credentials* and then click *OAuth client ID*
- Click *Other*
- ignore the popup, in the restulting *Credentials* page, download the credentials you just created (download symbol on the right) and save it as **client_id.json** in your virtual environment folder (i.e. **/files** folder).

- unless you have have an old Google project with the API in question already enabled, or unless your video is only sectionable into 6 snippets (i.e. it contains 7 timestamps), you will need to increase your quota limit.
	- to increase your limit, go to your project page (e.g. https://console.developers.google.com/apis/dashboard?project=PROJECTNAME)
	- On the Dashboard page, click on the *YouTube Data API v3* at the bottom of the page
	- click on the Quotas tab
	- Next to *Queries per day*, click the edit icon
	- click *apply for a higher quota* and fill out the form (link also available here: https://docs.google.com/forms/d/e/1FAIpQLSd5HxReFtxATJLNfLwQiucfQwYL295Xemgc6nhFXo1vcitg3A/viewform)
- the request form takes about 10 minutes to fill out... the response time for Google is not certain, nor is a positive response guaranteed.

Credits
=======

This tool was created by Rodolphe Gonzalès (https://github.com/ateliercartographique) and elaborated by Emory Shaw (https://github.com/maphouse) of the Geomedia Lab at Concordia University in the context of the Living Archives project: a collaboration with the Centre for Oral History and Digital Storytelling (COHDS), Computational Linguistics at Concordia (CLaC), and the Geomatics and Cartographic Research Centre (GCRC) at Carleton University (https://github.com/GCRC). More information can be found at http://geomedialab.org/
