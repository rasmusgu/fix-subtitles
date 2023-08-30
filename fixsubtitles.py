import os
# print output formatting
from colorama import Fore, Style  # , Back

# Terminology #
# EAS = Episode And Season : In "S01E06" format, season = 01 and episode = 06

# OPTIONS #

# Synchronise all subtitles, new and old
SYNC_ALL = False
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


# List of current directory files
current_directory_list = os.listdir(path='.')
# Directory files listed in lexicographical order
current_directory_list.sort()

# Current directory/system path
current_directory = os.getcwd()

# Print current directory and its files
print("Current directory: ", current_directory)
#print("Current directory files:", current_directory_list)


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
def sync_subtitle(video_file):
    # print("Synchronising subtitles for ", video_file, " using ffsubsync")

    # Video title's "EAS"
    vid_EAS = episode_and_season(video_file)
    # Subtitle filename matching video's "EAS"
    subtitle_file = get_sub(vid_EAS, subtitle_list)
    #check_match(video_file, subtitle_file)  # Useless since they've already been matched above

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

def log_test():
    test_string = "\ntest"
    log_filename = 'log.txt'
    try:
        with open(log_filename, 'a') as log_file:
            log_file.write(test_string)
            print("Activity logged to", os.path.abspath(log_filename))
    except:
        print("Something went wrong with logging")

def synchronise_all():
    # Fancy coloring of colorama
    print(Fore.RED + "Synchronising all "
          + Style.RESET_ALL + "subtitles to their respective videos")
    # Synchronises all subtitles to their 
    # respective videos in current directory
    for video in video_list:
        sync_subtitle(video)


def clean_subtitles(subtitle_file):
    # Using https://github.com/KBlixt/subcleaner to clean subtitles of advertisements etc.

    command = "python /home/ras/git/subcleaner/subcleaner.py " + subtitle_file
    os.system(command)

############### END OF DEFINITIONS ###############


log_test()

# List initialisation
video_list = []
subtitle_list = []

for file in current_directory_list:
    if any(format in file for format in video_formats):
        # Print test
        # print(format)
        video_list.append(file)
    elif ".srt" in file:
        subtitle_list.append(file)
# Print test
# print("Episode list: ", video_list)
video_sum = len(video_list)
print("Amount of episodes: ", video_sum)

subtitle_sum = len(subtitle_list)
print("Amount of external subtitles: ", subtitle_sum)

# List of episodes without matches
no_subtitles = []

if video_sum > 0:
    print("Checking for missing subtitles")
    # Checks if a video file is missing a subtitle file
    for video in video_list:
        # Resets the match variable to False
        match = False
        for subtitle in subtitle_list:
            if episode_and_season(video) == episode_and_season(subtitle):
                match = True
                # Print testing
                print("It's a match for video ", episode_and_season(video),
                    " and subtitle", episode_and_season(subtitle))
        if not match:
            no_subtitles.append(video)

    # Corrects next code block's spelling to singular or plural 
    # based on amount referred to (elements of no_subtitles list)
    was_or_were = "were "
    ep_or_eps = " videos"
    if len(no_subtitles) == 1:
        was_or_were = "was "
        ep_or_eps = " video"

    # Only runs if 1 or more subtitles were missing                  
    if len(no_subtitles) > 0:
        # Print video(s) without subtitles
        print("There ", was_or_were, len(no_subtitles),
        ep_or_eps, " without external* subtitle(s), as follows: ",
        no_subtitles)
        # Download subtitles for episodes missing .srt file
        for video in no_subtitles:
            download_subtitles(video)
        print("Done downloading missing subtitles!")  # Add error checking
        # Synchronises previously missing subtitles to their respective videos
        # Useless? Make synchronisation universal?
        print("Synchronising previously missing subtitles!")
        for video in no_subtitles:
            sync_subtitle(video)
        print("Done synchronising previously missing subtitles!")  # Add error checking

if SYNC_ALL:
    synchronise_all()
