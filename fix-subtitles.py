import os
import ffsubsync
from colorama import Fore, Back, Style

# Terminology
# EAS = Episode And Season : In "S01E06" format, season = 01 and episode = 06

# Creates a list of the current directory files
listCurrentDirectory = os.listdir(path='.')

# Checks a filename for its episode and season, if applicable       # Currently only episode
# Assumes the first numbers in a series' filename to be S01E05 format!!
def episodeAndSeason(fileName):
    # Checks for digits/numbers in the file name
    numbers = [int (i) for i in fileName if i.isdigit()]
    # Turns digits into single coherent number
    # In this case, due to S01E06 format, takes the 3rd and 4th digit
    str_epandseason = str(numbers[2]) + str(numbers[3])
    # Creates an integer out of the string
    epandseason = int(str_epandseason)
    return epandseason
    
# Checks if videofile and subtitle file have 
# same episode/season S01E07 style
def checkMatch(videoFile, subtitleFile):
    if episodeAndSeason(videoFile) == episodeAndSeason(subtitleFile):
        # Print testing
        # Fancy coloring of colorama
        print(Fore.GREEN + "Match found " + Style.RESET_ALL + "between ", videoFile, " and ", subtitleFile)
        return True
    else:
        # Print testing
        print("The files, ", videoFile, " and ", subtitleFile, " were not a match")
        return False

# Compares "S01E08" of target file to a whole list
# and returns the first match           # Suggestion: return all matches
def getSub(targetEAS, list):
    for i in list:
        if episodeAndSeason(i) == targetEAS:
            #print("The matching subtitle was ", i)
            return i
    
# Downloads subtitles for (video)file using subliminal
def downloadSubtitles(videoFile):
    print("Downloading subtitles using subliminal")
    quotedVideoFile = '"' + videoFile + '"'
    # Hard coded (for now) language format
    language_format = "en"
    # String of the command
    cmd = ("subliminal download -l " + language_format + " " + quotedVideoFile)
    print("Command: ", cmd)
    # Execution of command by shell/system
    os.system(cmd)
    
# Syncs the chosen video's subtitles to its audio reel using ffsubsync
def syncSubtitles(videoFile):
    #print("Synchronising subtitles for ", videoFile, " using ffsubsync")
    # Guesses the subtitle file based on video file     # Change to taking the "matching" sub file name from the matching sequence of this code
    videoFile = videoFile
    #episodeIndex = episodeList.index(videoFile)        # unused - useless?
    
    # Variable for language format of subtitle
    subLangFormat = ""
    # Video title's "EAS"
    vidEAS = episodeAndSeason(videoFile)
    # Subtitle filename matching video's "EAS"
    subFile = getSub(vidEAS, subtitleList)
    checkMatch(videoFile, subFile)          # Useless since they've already been matched above
    
    # Checks whether the subtitle is formatted .en or .eng
    if ".eng" in subFile:
        subLangFormat = ".eng.srt"
        syncedsubLangFormat = ".eng.retimed.srt"
    elif ".en" in subFile:
        subLangFormat = ".en.srt"
        syncedsubLangFormat = ".en.retimed.srt"
    
    # Reformatting of the synchronised file to ".retimed.srt"
    syncedSubFile = subFile.replace(subLangFormat, syncedsubLangFormat)         # Fix to include .en.srt
    
    # Calls ffsubsync using the appropriate parameters
    quotedList = [videoFile, subFile, syncedSubFile]
    x = 0
    for i in quotedList:
        quotedList[x] = '"' + quotedList[x] + '"'
        x += 1
    # Creates a list out of the command             # Pointless? It's made into a string later anyway
    commandList = "ffsubsync", quotedList[0], "-i", quotedList[1], "-o", quotedList[2]
    
    # Initialising variable
    command = ""
    # Creates  a string with spaces between list 
    # entries in order to be used as a command
    for i in commandList:
        command=command+i+" "
    # Print testing
    print("cmd: ", command)
    
    # Send command to be executed by "shell" or "system"
    os.system(command)
    
def synchronise_all():
    # Fancy coloring of colorama
    print(Fore.RED + "Synchronising " + Style.RESET_ALL + "all subtitles to their respective videos")
    # Synchronises all subtitles to their 
    # respective videos in current directory        # Make into a callable function?
    for i in episodeList:
        syncSubtitles(i)

############### END OF DEFINITIONS ###############

# List of episodes
episodeList = []
for i in listCurrentDirectory:
    if '.avi' in i:
        episodeList.append(i)
#print("Episode list: ", episodeList)   # Testing code
seasonLength = len(episodeList)
print ("Amount of episodes: ", seasonLength)

# List of subtitles
subtitleList = []
for i in listCurrentDirectory:
    if ".srt" in i:
        subtitleList.append(i)
subtitleAmount = len(subtitleList)
print("Amount of subtitles: ", subtitleAmount)

# Checks if there are the same amount of episode and subtitle files
#if len(subtitleList) != len(episodeList):
#    subepmatch = False
#else:
#    subepmatch = True
# Print testing
#print("Episode and subtitle count match: ", subepmatch)

# List of episodes without matches
noMatches = []
print("Checking for missing subtitles")
# Checks if a video file is missing a subtitle file
for i in episodeList:
    # Print testing
    #print("New episode : ", episodeAndSeason(i))
    # Resets the match variable from the previous episode
    match = False
    # Makes sure the while only runs once. Useless?
    x = 0
    while match == False and x < 1:
        for y in subtitleList:
            if episodeAndSeason(i) == episodeAndSeason(y):
                match = True
                # Print testing
                #print("It's a match for episode ", episodeAndSeason(i), " and ", episodeAndSeason(y))
        if match == False:
            noMatches.append(i)
        x += 1
        

# Corrects next code block's spelling to singular or plural 
# based on amount referred to (elements of noMatches list)
wasorwere = "were "
eporeps = " episodes"
if len(noMatches) == 1:
    wasorwere = "was "
    eporeps = " episode"
    
# Print episodes without subtitles
print("There ", wasorwere, len(noMatches), 
eporeps, " without subtitle(s), as follows: ", 
noMatches)
                       
if len(noMatches) > 0:
    # Download subtitles for episodes missing .srt file
    #print("Downloading missing subtitles")
    for i in noMatches:
        downloadSubtitles(i)
    print("Done downloading missing subtitles!")        # Add error checking
    # Synchronises previously missing subtitles to their respective videos
    # Useless? Make synchronisation universal?
    print("Synchronising previously missing subtitles!")
    for i in noMatches:
        syncSubtitles(i)
    print("Done synchronising previously missing subtitles!")       # Add error checking
    
#synchronise_all()