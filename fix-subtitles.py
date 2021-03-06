import os
from colorama import Fore, Back, Style

# Terminology
# EAS = Episode And Season : In "S01E06" format, season = 01 and episode = 06
# Instructions
# Read README.md

# Change below to True to synchronise all subtitles, new or old
sync_all = True

# Supported video formats. Hardcoded
video_formats = ['.avi', '.mkv', '.mp4']
# Preferred subtitle language
language = "en"
# Supported subtitle lang formats       #deprecated
subtitle_lang_formats = ['.en', '.eng']  # deprecated
# Hardcoded subtitle format
subtitle_format = ".srt"
# Supported subtitle formats. To be implemented later
subtitle_formats = ['.srt']  # wip

# Creates a list of the current directory files
current_directory_list = os.listdir(path='.')
# Sort the list in lexicographical order
current_directory_list.sort()

print("Current directory files:", current_directory_list)


# Checks a filename for its episode and season, if applicable       # Currently only episode
# Assumes the first numbers in a series' filename to be S01E05 format!!
def episode_and_season(file_name):
    # Checks for digits/numbers in the file name
    numbers = [int(i) for i in file_name if i.isdigit()]
    # Turns digits into single coherent number
    # In this case, due to S01E06 format, takes the 3rd and 4th digit
    str_epandseason = str(numbers[2]) + str(numbers[3])
    # Creates an integer out of the string
    epandseason = int(str_epandseason)
    return epandseason


# Checks if video file and subtitle file have
# same episode/season S01E07 style
def check_match(video_file, subtitle_file):
    if episode_and_season(video_file) == episode_and_season(subtitle_file):
        # Print testing
        # Fancy coloring from colorama
        print(Fore.GREEN + "Match found " + Style.RESET_ALL + "between ", video_file, " and ", subtitle_file)
        return True
    else:
        # Print testing
        print("The files, ", video_file, " and ", subtitle_file, " were not a match")
        return False


# Compares "S01E08" (EAS) of target file to a whole list
# and returns the first match           # Suggestion: return all matches
def get_sub(target_EAS, list):
    for subtitle in list:
        if episode_and_season(subtitle) == target_EAS:
            # print("The matching subtitle was ", subtitle)
            return subtitle


# Downloads subtitles for (video)file using subliminal
def download_subtitles(video_file):
    print("Downloading subtitles using subliminal")
    # Encases filename in quotation marks
    quoted_video_file = '"' + video_file + '"'
    # String of the command
    cmd = ("subliminal download -l " + language + " " + quoted_video_file)
    print("Command: ", cmd)
    # Execution of command by shell/system
    os.system(cmd)


# Syncs the chosen video's subtitles to its audio reel using ffsubsync
def sync_subtitles(video_file):
    # print("Synchronising subtitles for ", video_file, " using ffsubsync")

    # Video title's "EAS"
    vid_EAS = episode_and_season(video_file)
    # Subtitle filename matching video's "EAS"
    subtitle_file = get_sub(vid_EAS, subtitle_list)
    check_match(video_file, subtitle_file)  # Useless since they've already been matched above

    # Synced subtitle format
    synced_subtitle_format = ".retimed" + subtitle_format

    # Reformatting of the synchronised file to ".retimed.srt"
    synced_subtitle_file = subtitle_file.replace(subtitle_format, synced_subtitle_format)

    # Quoted variables due to blank spaces in filenames
    quoted_video_file = '"' + video_file + '"'
    quoted_subtitle_file = '"' + subtitle_file + '"'
    quoted_synced_subtitle_file = '"' + synced_subtitle_file + '"'

    # ffsubsync command with appropriate parameters
    command = "ffsubsync " + quoted_video_file + " -i " + quoted_subtitle_file + " -o " + quoted_synced_subtitle_file
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
        sync_subtitles(episode)


############### END OF DEFINITIONS ###############

# List of episodes
episodeList = []

for file in current_directory_list:
    if any(format in file for format in video_formats):
        # Print test
        # print(format)
        episodeList.append(file)
# Print test
# print("Episode list: ", episodeList)
seasonLength = len(episodeList)
print("Amount of episodes: ", seasonLength)

# List of subtitles
subtitle_list = []

for file in current_directory_list:
    if ".srt" in file:
        subtitle_list.append(file)
subtitleAmount = len(subtitle_list)
print("Amount of subtitles: ", subtitleAmount)

# List of episodes without matches
no_subtitles = []

print("Checking for missing subtitles")
# Checks if a video file is missing a subtitle file
for episode in episodeList:
    # Print testing
    # print("New episode : ", episode_and_season(episode))

    # Resets the match variable to False
    match = False
    for subtitle in subtitle_list:
        if episode_and_season(episode) == episode_and_season(subtitle):
            match = True
            # Print testing
            print("It's a match for episode ", episode_and_season(episode),
                  " and subtitle", episode_and_season(subtitle))
    if not match:
        no_subtitles.append(episode)

# Corrects next code block's spelling to singular or plural 
# based on amount referred to (elements of no_subtitles list)
was_or_were = "were "
ep_or_eps = " episodes"
if len(no_subtitles) == 1:
    was_or_were = "was "
    ep_or_eps = " episode"

# Print episode(s) without subtitles
print("There ", was_or_were, len(no_subtitles),
      ep_or_eps, " without external* subtitle(s), as follows: ",
      no_subtitles)

# Only runs if 1 or more subtitles were missing                  
if len(no_subtitles) > 0:
    # Download subtitles for episodes missing .srt file
    print("Downloading missing subtitles")
    for episode in no_subtitles:
        download_subtitles(episode)
    print("Done downloading missing subtitles!")  # Add error checking
    # Synchronises previously missing subtitles to their respective videos
    # Useless? Make synchronisation universal?
    print("Synchronising previously missing subtitles!")
    for video in no_subtitles:
        sync_subtitles(video)
    print("Done synchronising previously missing subtitles!")  # Add error checking

if sync_all:
    synchronise_all()
