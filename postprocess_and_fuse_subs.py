# -*- coding: utf-8 -*-

import re
import glob
from geotext import GeoText
#ES: error tracking code for py 2 -------------
import logging
import time
import os
#----------------------------------------------

def compileSubs(folderName,fileName,files,t_list,interviewer,interviewee,pass2,language,resampleSubtitles,removeStamps,removeLoneWords):
	#files = [['_High_freq_timestamping',0,False]]
	for fil in files:
		
		#fil = ['name',60,False]
		#print fil

		min_timelapse_between_stamps = fil[1]
		place_based_timestamping = fil[2]

		if place_based_timestamping:
			min_timelapse_between_stamps = 10000000000000

		list_false_positives = ['David','Un','Mon']
		
		
		#ES: LIST OF SUBTITLE FILE SNIPPETS
		
		# Find all sub in the folder
		sub_files = glob.glob(folderName + '/*.vtt')
		#print sub_files
		
		#ES: list of NEW subtitles file elements
		new_sub = ["WEBVTT\nKind: captions\nLanguage: fr-CA"]
		c = 0
		
		t_list_pos = 0
		#ES: USEFUL FUNC PROBABLY
		def hms_to_s(time):
			time = unicode(time, "UTF-8")
			time = time.split(" --> ")
			#print time
			#print "--------"
			t_0 = time[0].split(":")
			t_1 = time[1].split(":")
					
			t0 = float(int(t_0[0])*3600) + int(float(t_0[1])*60) + int(float(t_0[2]))
			t1 = float(int(t_1[0])*3600) + int(float(t_1[1])*60) + int(float(t_1[2]))
			
			t0 = float(t_0[0])*3600 + float(t_0[1])*60 + float(t_0[2])
			t1 = float(t_1[0])*3600 + float(t_1[1])*60 + float(t_1[2])
			#return [int(t0),int(t1)]
			#print t0,t1
			return [t0,t1]

		def s_to_hms(seconds):
			#print seconds
			m, sec = divmod(seconds, 60)
			h, m = divmod(m, 60)	
			#print str(int(h)) + ":" + str(int(m)) + ":" + str(int(s))
			#return str(int(h)) + ":" + str(int(m)) + ":" + str(int(sec))
			return str(int(h)) + ":" + str(int(m)) + ":" + str(float("{0:.2f}".format(round(sec,2))))
		
		last = [0,0]
		offset = last
		new_line = True
		sentence = []
		ee = ""
		first_pass = True

		last_timestamp = 0

		cc = 0
		ccc = -1

		sub_times = []#ES: new final subtitles file list of timestamps
		sub_text = []#ES: new final subtitles file list of text elements
		
		#ES: custom list for the last timestamp of the prev vid (table_sentenses). this way we keep RG's resampling while maintaining original final timestamp of youtube-created timestamps.
		last_t22 = []
		#FUNCTION process-transform-aggregate-snippets
		z = 0
		#ES: FOR EACH SNIPPET IN LIST OF .VTT SNIPPETS
		for s in sub_files:
			#print ""
			#print s
			
			#ES: GO
			if (pass2 == False and s != folderName + "/" + fileName + ".vtt") or (pass2 == True and "pass" in s):
				print ""
				print s
				c += 1
				
				#FUNCTION extract-to-table_sentenses
				
				#ES: text READLINES IN .VTT FILES
				with open(s) as f:
					text = f.readlines()
					
				text = [x.strip() for x in text]
				
				table_sentenses = []
				row = []
				
				whereAreWe = s
				
				#ES: for line in snippet
				for t in text:
					count = 0
					#ES: clean snippet line
					while count < 3:
						try:
							t = t.replace('\n','')
							
							
							from chardet import detect
							encoding = lambda x: detect(x)['encoding']
							
							#print t,encoding(t)
							
							if '&nbsp;' in t:
								t = t.replace('&nbsp;','')
								#print t
							if '…' in t:
								t = t.replace('…','...')
								#print t
								
							#ES: if line is not Nothing
							if t != "":
								#print t,t != "" and t[0].isdigit() and ":" in t,t != "" and (not t[0].isdigit() and ":" not in t) and "WEBVTT" not in t and "Kind" not in t and "Language" not in t
								#ES: if first element in line is a digit and there is a colon in that line
								if t != "" and t[0].isdigit() and t[2] is ':':
									#print t
									if row != []:
										table_sentenses.append(row)
									row = []
									
									#ES: t needs to be turned into numbers in the current format and be part of a list in format of text3 so that it the said list can be put through the t in text3 loop (below, line 291)
									#ES: last_t is t transformed into seconds (numbers)
									
									last_t = hms_to_s(t)
									row.append(last_t)
								
								if t != "" and (t[0].isdigit() == False or t[2] is not ":") and "WEBVTT" not in t and "Kind" not in t and "Language" not in t:
									t = t.replace("&nbsp;","")
									t = t.replace("\xc2\xab...\xc2\xbb","[Pause]")
									t = t.replace("  "," ")
									
									t = t.replace(". ",".&&&")
									#t = t.replace(' "','"')
									#t = t.replace('" ','"')
									t = t.replace("‘’",'"')
									#t = t.replace("[Pause]","[Pause]&&&")
									t = t.replace("[Pause]","[...]")
									t = t.replace("? ","?&&&")
									#ES: adding conditional statements to preserve full functionality when user inputs no interviewer/ee variables.
									if interviewer != "":
										t = t.replace(interviewer,"&&&" + interviewer)
									if interviewee != "":
										t = t.replace(interviewee,"&&&" + interviewee)
									
									#ES: split t after periods or before person names (interviewee/interviewer).
									sentences = t.split("&&&")
									#print sentences
									for s in sentences:
										if interviewer != "":
											if s != '' and s != interviewer + ": ":
												row.append(s.strip().replace("  "," "))# + ".")
										else:
											if s != '':
												row.append(s.strip().replace("  "," "))
										
											#print row
									#print ""
						except Exception as ex:
							logging.exception('full stack trace:')
							print "--------"
							print "retrying to read t from ", whereAreWe, " - try #", count+1
							print "will retry 3 times. If unsuccesful, you will encounter an error. If so, run 'main.py' again with only 'combineSubtitles' set to True and it should work"
							count += 1
							time.sleep(8)
							continue
						break
				#END-FUNCTION extract-to-table_sentenses
				
				
				#ES: add a period to end of last line in snippet to make it look like ".."
				try:
					lastChar = row[len(row)-1][len(row[len(row)-1])-1]
				except IndexError:
					print "IndexError was handled for var 'row': ", row
					print "Using len(row)-2 instead..."
					lastChar = row[len(row)-2][len(row[len(row)-1])-1]
				if lastChar != "." or lastChar != "," or lastChar != "?" or lastChar != "!":
					row[len(row)-1] += "."
				
				#ES: identifies final timestamp and appends to list of snippet sentences.
				table_sentenses.append(row)
				
				last_t2 = [last_t[1],last_t[1]]
				
				#ES: last_t22 is a list of raw final timestamps that are used as offsets (i added this to fix the lagging concatenated timestamps)
				last_t22.append([last_t[1],last_t[1]])
				if len(last_t22) > 1:
					z += 1
					last_t22[z] = [a+b for a, b in zip(last_t22[z], last_t22[z-1])]
				table_sentenses.append([last_t2])
				
				
				
				"""
				print "printing table_sentenses"
				print "======================="
				print table_sentenses
				"""
				
				#FUNCTION table_sentenses-to-text2
				
				#ES: this is the code that is RESAMPLING and remixing the text...
				#ES: should this be ignored?
				if resampleSubtitles == True:
				
					resampled_text = []
					for ts in range(len(table_sentenses)):
						#print table_sentenses[ts]
						previousInterpolated = [0,0]
						
						#print table_sentenses[ts]
						if len(table_sentenses[ts]) > 0:
							listOfElements = []
							prev_ts_2 = 0
							for ts_2 in table_sentenses[ts]:
								if isinstance(ts_2, list) == False:
									listOfElements.append([prev_ts_2,len(ts_2) + prev_ts_2])
									prev_ts_2 += len(ts_2)
							c_ts2 = 0
							for ts_2 in table_sentenses[ts]:
								if isinstance(ts_2, list) == False:
									interpolated = len(ts_2)
									maximum = listOfElements[len(listOfElements)-1][1]
									#print ts_2,table_sentenses[ts][0]
									#print c_ts2,table_sentenses[ts][0],(float(listOfElements[c_ts2][0]) / float(maximum)) * (table_sentenses[ts][0][1] - table_sentenses[ts][0][0]) + table_sentenses[ts][0][0]
									#(10/100)*500+20
									interpolated = [(float(listOfElements[c_ts2][0]) / float(maximum)) * (table_sentenses[ts][0][1] - table_sentenses[ts][0][0]) + table_sentenses[ts][0][0],0]
									c_ts2 += 1
									
									resampled_text.append(interpolated)
									resampled_text.append(ts_2)
							
								#else:
									#resampled_text.append(ts_2)
									
							#print ""
						
	#					for tts in range(len(table_sentenses[ts])):
	#						if (str(table_sentenses[ts][tts][0]).isalpha() or table_sentenses[ts][tts][0] == '[' or table_sentenses[ts][tts][0] == 'à' or table_sentenses[ts][tts][0] == 'é') and (str(table_sentenses[ts][tts-1][0]).isalpha() or table_sentenses[ts][tts-1][0] == '[' or table_sentenses[ts][tts-1][0] == 'à' or table_sentenses[ts][tts-1][0] == 'é'):
	#							try:
	#								interpolated = [float(previous_time[0])+(((table_sentenses[ts+1][0][0]-float(previous_time[0]))/(len(table_sentenses[ts][1])+len(table_sentenses[ts][2])))*len(table_sentenses[ts][1])),0]
	#								previousInterpolated = interpolated #- moins
	#							except:
	#								interpolated = [(float(previous_time[0]) + float(previous_time[1])) / 2.0,0]
	#								#previousInterpolated = interpolated
	#							interpolated = [float("{0:.2f}".format(round(interpolated[0],2))),0]
	#							resampled_text.append(interpolated)
	#							resampled_text.append(table_sentenses[ts][tts])
	#						else:
	#							if isinstance(table_sentenses[ts][tts][0], int) or isinstance(table_sentenses[ts][tts][0], float):
	#								previous_time = table_sentenses[ts][tts]
	#								resampled_text.append(table_sentenses[ts][tts])
	#							else:
	#								resampled_text.append(table_sentenses[ts][tts])
						
					
					#for iiiii in resampled_text:
					#	print iiiii
					#print resampled_text[len(resampled_text)-1]
					
					text2 = [resampled_text[0]]			
					
					
					
					# Retirer les timestamps qui coupent les phrases
					
					#ES: the current conditional loop is necessary where the previous process is applied, and should therefore be removed along with it
					
					
					if removeStamps == True:
						for rt in range(len(resampled_text)-1):
							passAnyway = False
							if ((isinstance(resampled_text[rt][0], int) == False and isinstance(resampled_text[rt][0], float) == False) and resampled_text[rt][len(resampled_text[rt])-1] != "." and resampled_text[rt][len(resampled_text[rt])-1] != "!" and resampled_text[rt][len(resampled_text[rt])-1] != "?"):
								rien = 0
								if (isinstance(resampled_text[rt+1][0], int) == False and 	isinstance(resampled_text[rt+1][0], float) == False):
									#print "---------",resampled_text[rt+1]
									passAnyway = True
							else:
								#print resampled_text[rt+1]
								text2.append(resampled_text[rt+1])
							if passAnyway == True:
								#print resampled_text[rt+1]
								text2.append(resampled_text[rt+1])
					else:
						for rt in range(len(resampled_text)-1):
							text2.append(resampled_text[rt+1])
							#ES: forget text2, same as table_sentenses but resampled and reformatted slightly
							# [[41.99, 43.44], 'grande famille de six enfants; plus Papa et', 'Maman \xc3\xa7a fait huit.', 'Et on est tous ici au'], [[43.44, 48.4], 'Qu\xc3\xa9bec.', 'S.I.:: Et quel est votre \xc3\xa9tat matrimonial?'], [[48.4, 52.92], 'A.M.::Pas mari\xc3\xa9e.', 'S.I.:: Pas mari\xc3\xa9e, O.K.', 'Vous avez dit que'], 
							#to
							#[43.0775, 0], 'Et on est tous ici au', [43.44, 0], 'Qu\xc3\xa9bec.', [44.218039215686275, 0], 'S.I.:: Et quel est votre \xc3\xa9tat matrimonial?', [48.4, 0], 'A.M.::Pas mari\xc3\xa9e.', [49.77898305084746, 0], 'S.I.:: Pas mari\xc3\xa9e, O.K.', [51.617627118644066, 0], 'Vous avez dit que', 
							
					#END-FUNCTION table_sentenses-to-text2	
					"""
					print "printing text2"
					print "======================="
					print text2
					"""
	
				
					#ES: new interpolated 'smart' times (which need removing)
					
					#FUNCTION reformat-text2-as-vtt-list/text3
					
					text3 = ['WEBVTT','Kind: captions','Language: fr-CA','']
					for t2 in text2:
						#print t2
						if isinstance(t2[0], int):
							t2[0],t2[1] = float(t2[0]),float(t2[1])
						if isinstance(t2[0], float):
							for aa in text2:
								#print 2,aa
								if (isinstance(aa[0], float) or isinstance(aa[0], int)) and aa[0] > t2[0]:
									#print 2,aa
									break
							
							if not isinstance(aa[0],str):
								t2[1] = aa[0]
							else:
								t2[1] = t2[0] + 3.0
							#print 3,t2
							#t2 = [s_to_hms(t2[0]),s_to_hms(t2[1])]
							#print s_to_hms(t2[0])#.split(':')
							#print type(t2[1])
							
							#ES: function for turning time list into srt format timestamp
							t2 = str(s_to_hms(t2[0]).split(':')[0]) + ":" + str(s_to_hms(t2[0]).split(':')[1]) + ":" + str(s_to_hms(t2[0]).split(':')[2]) + " -->  " + str(s_to_hms(t2[1]).split(':')[0]) + ":" + str(s_to_hms(t2[1]).split(':')[1]) + ":" + str(s_to_hms(t2[1]).split(':')[2])
							#ES: t2 is now same format as t
							
						text3.append(t2)
					#END-FUNCTION reformat-text2-as-vtt-list/text3
					
					#del text3[-1]
					
					#ES: text3 is yet another iteration of the snippet version, this time with time formatted as TT ---> TT instead of [TT,TT] like text2
					#ES: might need to put table_sentenses through the spinner that transformed text2 into text3
					
					#ES: the following loop could have table_sentenses as input...
					#ES: this is the "cumulative" or "concatenation" loop (so there might be something wrong going on here)
					#ES: requires that what is being looped is a list in format of text3
					"""
					print "printing text3"
					print "======================="
					print text3
					"""
				#ES: code added as an option to avoid using the resampling method and simply use native Youtube sub style
				else:
					text3 = ['WEBVTT','Kind: captions','Language: fr-CA','']
					for t in table_sentenses:
						for el in t:
							if isinstance(el, list) == True:
								timestampES = str(s_to_hms(t[0][0]).split(':')[0]) + ":" + str(s_to_hms(t[0][0]).split(':')[1]) + ":" + str(s_to_hms(t[0][0]).split(':')[2]) + " -->  " + str(s_to_hms(t[0][1]).split(':')[0]) + ":" + str(s_to_hms(t[0][1]).split(':')[1]) + ":" + str(s_to_hms(t[0][1]).split(':')[2])
								text3.append(timestampES)
							else:
								text3.append(el)
				
				
				#ES: AT THIS POINT, TEXT3 IS SAME FORMAT AS PREV TEXT3 EXCEPT THAT TIMESTAMPS NATURALLY DON'T OCCUR AT EVERY 2ND ELEMENT
				
				#ES: once the snippet text is scanned and transposed into the list 'text3', each line in text3 is looped through for concatenation.
				#print "TEXT3: ",text3
				
				#FUNCTION concatenate_text3
				for t in text3:
					if "WEBVTT" not in t and "Kind" not in t and "Language" not in t:
						#ES: if timestamp
						#ES: change this conditional slightly if t is in table_sentenses instead of text3
						if t != "" and t[0].isdigit() and t[1] is ':':
							#print "1. t : ", t
							#ES: if timestamp is in between first and last timestamp in snippet
							"""
							print "t", t#timestamp being processed
							print "hms_to_s(t)",hms_to_s(t)[0]#the timestamp in seconds (for comparison)
							print "last", last#last represents the previous timestamp.
							print "offset", offset#offset inherited by last
							"""
							#ES: when last is at the beginning of a new snippet loop, it is naturally larger than the present timestamp (since it represents the last timestamp from the prev snippet), triggering the following code
							if hms_to_s(t)[0] < last[0]:
								#ES: in RG's code, offset is equal to last (last is the last timestamp of the prev snippet). However, since these last timestamps are erroneous and go beyond the actual video length due to the resampling of subtitles by RG, i am using the raw Youtube final (un-resampled) timestamps as offsets.
								offset = [t_list[t_list_pos],t_list[t_list_pos]]
								t_list_pos += 1
								#offset = [last_t22[z-1][0],last_t22[z-1][1]]
								#ES: OFFSET is the variable containing the cumulative timestamps
								#print 1,offset[1]
								#print ""
								
								#ES: when dealing with the first timestamp in a vtt file, make the opening time of this caption 0.0, otherwise concatenation can be problematic, resulting in subtitle lag (i.e. youtube doesn't always set the first caption to minute 0.0 in a video snippet)
								t_1 = t.split(" -->  ")
								t_1[0] = "0:0:0.0"
								t_2 = " -->  ".join(t_1)
								t = t_2
								timestamp = hms_to_s(t)
							else:
								timestamp = hms_to_s(t)
							"""
							print "timestamp", timestamp#ES: t to number array
							"""
							#ES: t will be directly in the form taken by timestamp if we use table_sentenses instead of text3
							
							#print 1,t,hms_to_s(t)
							new_timestamp = "\n" + s_to_hms(timestamp[0] + offset[1]) + " --> " + s_to_hms(timestamp[1] + offset[1])
							"""
							print "new timesamp", new_timestamp#ES: new_timestamp adds offset[1] (end-timestamp of last timestamp in prev snippet) to current t
							"""
							#new_sub.append(new_timestamp)
							last = hms_to_s(t)
							t = new_timestamp
							#print t
							t = hms_to_s(t)
							"""
							print "t new_timestamp", t#ES: new timestamp in s form.
							"""
							t = [float("{0:.2f}".format(round(t[0],2))),float("{0:.2f}".format(round(t[1],2)))]
							"""
							print "t rounded", t#ES: removes nanoseconds (worth keeping since these are only very small, rare numbers)
							"""
							t = s_to_hms(t[0]) + " --> " + s_to_hms(t[1])
							"""
							print "t final", t
							"""
							#print t,offset[1]
							
							latest_timestamp = s_to_hms(timestamp[1] + offset[1])#ES: the end-time of the current (new, unrounded) timestamp
							
							#ES: I don't see the point in processing t and latest_timestamp...
							#print len(sentence),sentence
							
							#ES: following code is not needed. it doesn't run if place_based_timestamping is False (which it always is)
							place = False
							#ES: following code is not needed
							if len(sentence) > 0:
								ee = ""
								for e in sentence:
									ee += e
									
								countries,cities = GeoText(ee).countries,GeoText(ee).cities
								nbr_places = 0
								for countr in countries:
									if countr not in list_false_positives:
										nbr_places += 1
								for citi in cities:
									if citi not in list_false_positives:
										nbr_places += 1
								#print cities
								if place_based_timestamping == False:
									nbr_places = 0
								
								#if len(GeoText(ee).countries) > 0 or len(GeoText(ee).cities) > 0:
								if nbr_places > 0 or " là-bas " in ee or " chez " in ee or " vers " in ee:
									place = True
									#print GeoText(ee).countries,GeoText(ee).cities,"là-bas" in ee , "chez" in ee , "vers" in ee
									#print ""
							#places.cities
							if fil[2] == False:
								place = False
							
							#ES: not sure what the following "passes" are about...
							
							if (hms_to_s(t)[0]-last_timestamp > min_timelapse_between_stamps or first_pass == True):
								delay_passed = True
								first_pass = False
							else:
								delay_passed = False
							
							#ES ADDED 24/03. removing delaypassed to see what this does.. 
							# it doesn't do any good
							#delay_passed = False
							
							if delay_passed == True or place == True:
								
								
								#ES new_sub.append(new_timestamp)
								sub_times.append(new_timestamp)
								last_timestamp = hms_to_s(t)[0]
								
								#print "new_timestamp: ", new_timestamp
								#print "new_sub.append(new_timestamp): ", new_sub
								#print "sub_times.append(new_timestamp): ", sub_times
								#print "last_timestamp: ", last_timestamp
								
								#ES: adds interviewer and interviewee codes
								if len(sentence) > 0:
									ee = ""
									for e in sentence:
										if interviewer != "":
											#print e
											if interviewer[:-1] in e and interviewer not in e:
												#print e
												e = e.replace(interviewer[:-1],interviewer)
												#print e
										if interviewee != "":
											if interviewee[:-1] in e and interviewee not in e:
												e.replace(interviewee[:-1],interviewee)
												#print e
										e.replace("  ", "")
										e.rstrip('\n')
										if ".:" in e and len(ee) > 0:
											ee += "\n"
										ee += e + " "
									#print ""
									#print "2. ee : ", ee
									if ee != '':
										new_sub.append(ee)
										sub_text.append(ee)
								
								new_sub.append(new_timestamp)
								sentence = []
								#print "3. new_sub: ", new_sub
								
						else:
							#sentence = []
							#print sentence#,t
							if len(t) > 0:
								sentence.append(t)
								#print "4. sentence: t: ", t
				
		#END_FUNCTION concatenate_text3
		"""

		"""
		#print new_sub
		
		
		#ES: set to false to prevent redistribution of lone words
		if removeLoneWords == True:
			ee = ""
			for e in sentence:
				#print e
				e.replace("  ", "")
				e.rstrip('\n')
				if ".:" in e and len(ee) > 0:
					ee += "\n"
				ee += e + " "
			
			new_sub.append(ee)
			sub_text.append(ee)
			new_sub2 = ["WEBVTT\nKind: captions\nLanguage: fr-CA"]
			c = 0
			
			#ES: 2nd PROCESS... cleans the resampled subs..
			for i in range(len(sub_times)):
				#print sub_text[i]
				for s in sub_text[i].split("\n"):
					# If there is a lone word on a line
					if len(s.split()) == 1:
						sub_text[i-1] = sub_text[i-1] + s
						sub_text[i] = sub_text[i].replace(s + "\n",'')

					# if there is a lone word, separated by a "." at the begining or end of a line
					#print sub_text[i]
					if sub_text[i][-2] != '?' and sub_text[i][-2] != '!' and sub_text[i][-2] != '.' and sub_text[i][-2] != ',' and sub_text[i][-2] != ';' and sub_text[i][-2] != ':':
						#print s
						for p in s.split("."):
							p = p.strip()
							if len(p) > 1 and len(p.split()) == 1 and p != ":O":# and p != '[Pause]':
								#print p,len(p),p.split(),len(p.split())
								c += 1
								if p.replace(" ","") in s.split()[0]:
									#print s,p,"devant"
									sub_text[i-1] = sub_text[i-1] + p.replace(" ","")  + "."
									sub_text[i] = sub_text[i].replace(p + ". ",'')
								elif p.replace(" ","") in s.split()[-1]:
									#print s,p,"derrière"
									sub_text[i+1] = p.replace(" ","") + " " + sub_text[i+1]
									sub_text[i] = sub_text[i].replace(p.replace(" ",""),'')
									
				
				new_sub2.append(sub_times[i])
				new_sub2.append(sub_text[i])
			
			#END-FUNCTION process-transform-aggregate-snippets
			
			#for i in new_sub2:
			#	print i

			new_sub2 = ["WEBVTT\nKind: captions\nLanguage: fr-CA"]
			for i in range(len(sub_times)):
				new_sub2.append(sub_times[i])
				if not sub_text[i].isspace():
					new_sub2.append(sub_text[i])

			#for i in new_sub2:
			#	print i	
			"""
			print "=========================="
			print "new_sub2"
			print new_sub2
			"""
			new_sub = new_sub2
		
		#print new_sub
		
		sub = ""
		sub_srt = ""
		sub_txt = ""
		sub_txt_debug = ""

		all_time_stamps =[]
		
		#print "printing new_sub or text3: ",new_sub
		
		for i in new_sub:
			#if "A.M" in i and "A.M.:" not in i:
			if i[1].isdigit() and i[2] is ':':
				#print i,hms_to_s(i)
				all_time_stamps.append(hms_to_s(i))
				#all_time_stamps.append([float(hms_to_s(i)[0]),float(hms_to_s(i)[1])])
				#ES WRITE EXCEPTION

		for i in range(len(all_time_stamps)):
			all_time_stamps[i][0] = s_to_hms(all_time_stamps[i][0])
			try:
				all_time_stamps[i][1] = s_to_hms(all_time_stamps[i+1][0])
			except:
				all_time_stamps[i][1] = s_to_hms(all_time_stamps[i][1])

		all_time_stamps[len(all_time_stamps)-1][1] = latest_timestamp

		all_time_stamps2 = []
		for i in all_time_stamps:
			if len(i[0].split(":")[0]) == 1:
				h1 = "0" + i[0].split(":")[0]
			else:
				h1 = i[0].split(":")[0]
			if len(i[0].split(":")[1]) == 1:
				m1 = "0" + i[0].split(":")[1]
			else:
				m1 = i[0].split(":")[1]
			if len(i[0].split(":")[2]) == 1:
				s1 = "0" + i[0].split(":")[2]
			else:
				s1 = i[0].split(":")[2]
			
			if len(i[1].split(":")[0]) == 1:
				h2 = "0" + i[1].split(":")[0]
			else:
				h2 = i[1].split(":")[0]
			if len(i[1].split(":")[1]) == 1:
				m2 = "0" + i[1].split(":")[1]
			else:
				m2 = i[1].split(":")[1]
			if len(i[1].split(":")[2]) == 1:
				s2 = "0" + i[1].split(":")[2]
			else:
				s2 = i[1].split(":")[2]
			
			#ES: add zeros to seconds
			if s2[1] == '.':
				s2 = '0' + s2
			if len(s2) == 4:
				s2 = s2 + '00'
			if len(s2) == 5:
				s2 = s2 + '0'
			
			if s1[1] == '.':
				s1 = '0' + s1
			if len(s1) == 4:
				s1 = s1 + '00'
			if len(s1) == 5:
				s1 = s1 + '0'
			
			"""
			if i[10] == ' ':
					i = i[:10] + '0' + i[10:]
				if i[9] == ' ':
					i = i[:9] + '00' + i[9:]
				if len(i) == 26:
					i = i + '0'
				if len(i) == 25:
					i = i + '00'
			"""
			all_time_stamps2.append([h1 + ":" + m1 + ":" + s1,h2 + ":" + m2 + ":" + s2])

		c = 0
		for i in new_sub:
			#ES: the below replacement was done for berthe's story, since there were many distracting " ... " in the transcript.
			i = i.replace('" ... "','[...]')
			i = i.replace('::',':')
			i = i.replace('‘’','"')
			i = i.replace('  ',' ')
			if i[1].isdigit() and i[2] is ':':
				i = "\n" + all_time_stamps2[c][0] + " --> " + all_time_stamps2[c][1]
				c += 1
			if i != "" or not i.isspace():
				sub += i + "\n"

		c = 0
		for i in new_sub:
			i = i.replace('‘’','"')
			i = i.replace('  ',' ')
			if i[1].isdigit() and i[2] is ':':
				i = "\n" + str(c+1) + "\n" + all_time_stamps2[c][0] + " --> " + all_time_stamps2[c][1]
				c += 1
			if (i != "" or not i.isspace()) and "WEBVTT" not in i:
				sub_srt += i + "\n"

		c = 0
		for i in new_sub:
			i = i.replace('‘’','"')
			i = i.replace('  ',' ')
			if i[1].isdigit() and i[2] is ':':
				#i = "\n" + all_time_stamps2[c][0]
				i = "[" + all_time_stamps2[c][0] + "]"
				c += 1
			if (i != "" or not i.isspace()) and "WEBVTT" not in i:
				if interviewer != "":
					i = i.replace(interviewer + ":", interviewer + "::")
				if interviewee != "":
					i = i.replace(interviewee + ":", interviewee + "::")
				i = i.replace("\n"," ")
				sub_txt += i + " "

		c = 0
		for i in new_sub:
			i = i.replace('‘’','"')
			i = i.replace('  ',' ')
			if i[1].isdigit() and i[2] is ':':
				i = "\n" + all_time_stamps2[c][0]
				#i = "[" + all_time_stamps2[c][0] + "]"
				c += 1
			if (i != "" or not i.isspace()) and "WEBVTT" not in i:
				if interviewer != "":
					i = i.replace(interviewer + ":", interviewer + "::")
				if interviewee != "":
					i = i.replace(interviewee + ":", interviewee + "::")
				sub_txt_debug += i + "\n"
		
		
		if fil[1] <= 10:
			print "\nprinting final subtitles to files...\n"
			try:
				os.mkdir(folderName + "/output")
			except Exception as e:
				print e
				print "Output folder already exists. \nOverwriting output folder and files..."
				time.sleep(1)
			
			thefile = open(folderName + "/output/" + fileName + "_" + language + ".vtt", 'w')
			thefile.write(sub)

			thefile = open(folderName + "/output/" + fileName + "_" + language + ".srt", 'w')
			thefile.write(sub_srt)

		thefile = open(folderName + "/output/" + fileName + fil[0] + "_" + language + ".txt", 'w')
		thefile.write(sub_txt)
		
		thefile = open(folderName + "/output/" + fileName + fil[0] + "_" + language + "_readable" + ".txt", 'w')
		thefile.write(sub_txt_debug)
		print "Compiled subtitle files are now available in '" + folderName + "/output' folder."
	return sub_srt
	"""
	except Exception as ex:
		print "an error occurred"
		print ex
		logging.exception('full stack trace:')
		pass
		"""
"""
interviewer = "S.G."
interviewee = "O.G."
folderName = 'Oscar'
fileName = 'Oscar_complete'
originalVideo = "Oscar.mp4"
compiledSubs = compileSubs(folderName,fileName,[['_High_freq_timestamping',0,False]],interviewer,interviewee,True)
"""