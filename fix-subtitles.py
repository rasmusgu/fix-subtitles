import os
from colorama import Fore, Back, Style

# Terminology
# EAS = Episode And Season : In "S01E06" format, season = 01 and episode = 06

# Supported video formats. Hardcoded
video_formats = ['.avi', '.mkv', '.mp4']
# Preferred subtitle language
language = "en"
# Which subtitle the script should look for in your files
# for synchronisation purposes
subtitle_lang_formats = ['.en', '.eng']     # deprecated
# Hardcoded subtitle format
subtitle_format = ".srt"
# To be implemented later
subtitle_formats = ['.srt']

# Creates a list of the current directory files
listCurrentDirectory = os.listdir(path='.')
# Sort the list in lexicographical order
listCurrentDirectory.sort()

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

# Compares "S01E08" (EAS) of target file to a whole list
# and returns the first match           # Suggestion: return all matches
def getSub(targetEAS, list):
    for subtitle in list:
        if episodeAndSeason(subtitle) == targetEAS:
            #print("The matching subtitle was ", subtitle)
            return subtitle
    
# Downloads subtitles for (video)file using subliminal
def downloadSubtitles(videoFile):
    print("Downloading subtitles using subliminal")
    # Encases filename in quotation marks
    quotedVideoFile = '"' + videoFile + '"'
    # String of the command
    cmd = ("subliminal download -l " + language + " " + quotedVideoFile)
    print("Command: ", cmd)
    # Execution of command by shell/system
    os.system(cmd)
    
# Syncs the chosen video's subtitles to its audio reel using ffsubsync
def syncSubtitles(videoFile):
    #print("Synchronising subtitles for ", videoFile, " using ffsubsync")
    
    # Video title's "EAS"
    vidEAS = episodeAndSeason(videoFile)
    # Subtitle filename matching video's "EAS"
    subFile = getSub(vidEAS, subtitleList)
    checkMatch(videoFile, subFile)          # Useless since they've already been matched above
    
    # Synced subtitle format
    syncedsubFormat = ".retimed" + subtitle_format
    
    # Reformatting of the synchronised file to ".retimed.srt"
    syncedSubFile = subFile.replace(subtitle_format, syncedsubFormat)
    
    # Quoted variables due to blank spaces in filenames
    quotedVideoFile = '"' + videoFile + '"'
    quotedSubFile = '"' + subFile + '"'
    quotedSyncedSubfile = '"' + syncedSubFile + '"'

    # ffsubsync command with appropriate parameters
    command = "ffsubsync " + quotedVideoFile + " -i " + quotedSubFile + " -o " + quotedSyncSubFile
    # Print testing
    print("cmd: ", command)
    
    # Send command to be executed by "shell" or "system"
    os.system(command)
    
def synchronise_all():
    # Fancy coloring of colorama
    print(Fore.RED + "Synchronising all " + Style.RESET_ALL + "subtitles to their respective videos")
    # Synchronises all subtitles to their 
    # respective videos in current directory
    for episode in episodeList:
        syncSubtitles(episode)

############### END OF DEFINITIONS ###############

# List of episodes
episodeList = []

for file in listCurrentDirectory:
    if any(format in file for format in video_formats):
        # Print test
        #print(format)
        episodeList.append(file)
# Print test
#print("Episode list: ", episodeList)
seasonLength = len(episodeList)
print ("Amount of episodes: ", seasonLength)

# List of subtitles
subtitleList = []

for file in listCurrentDirectory:
    if ".srt" in file:
        subtitleList.append(file)
subtitleAmount = len(subtitleList)
print("Amount of subtitles: ", subtitleAmount)

# List of episodes without matches
noMatches = []

print("Checking for missing subtitles")
# Checks if a video file is missing a subtitle file
for episode in episodeList:
    # Print testing
    #print("New episode : ", episodeAndSeason(episode))
    
    # Resets the match variable to False
    match = False
    for subtitle in subtitleList:
        if episodeAndSeason(episode) == episodeAndSeason(subtitle):
            match = True
            # Print testing
            #print("It's a match for episode ", episodeAndSeason(episode), " and subtitle", episodeAndSeason(subtitle))
    if match == False:
        noMatches.append(episode)
        

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
    print("Downloading missing subtitles")
    for episode in noMatches:
        downloadSubtitles(episode)
    print("Done downloading missing subtitles!")        # Add error checking
    # Synchronises previously missing subtitles to their respective videos
    # Useless? Make synchronisation universal?
    print("Synchronising previously missing subtitles!")
    for video in noMatches:
        syncSubtitles(video)
    print("Done synchronising previously missing subtitles!")       # Add error checking
    
#synchronise_all()
