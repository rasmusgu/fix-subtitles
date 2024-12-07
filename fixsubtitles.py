import os
import subprocess
import re
# print output formatting
from colorama import Fore, Style  # , Back
# Used to process ffprobe output
from subprocess import Popen, PIPE
# Used to store ffprobe output
import json

# Terminology #
# EAS = Episode And Season : In "S01E06" format, season = 01 and episode = 06
### Todo ###
# - Add flags/arguments for calling the program
# - Add recursion to directory traversal
# - Add database functionality, files, dates, logs (changes, etc..)

### OPTIONS ###
SYNC_ALL = False            # Synchronise all subtitles
DEBUG = False               # Debug flag, for downloads etc
CLEAN_ALL = False           # Clean all subtitles of adverts etc.
EXTRACT_ALL = False         # Extract all embedded subtitles
# Supported video formats. Hardcoded
video_formats = ['.avi', '.mkv', '.mp4', '.webm']
# Preferred subtitle language
pref_sub_language = "en"
# Supported subtitle lang formats       #deprecated
subtitle_lang_formats = ['.en', '.eng']  # deprecated
# Hardcoded subtitle format
subrip_format = ".srt"
# Supported subtitle formats. To be implemented later
subtitle_formats = ['.srt', '.ass']
subcleaner = f"{os.environ['HOME']}/git/subcleaner/subcleaner.py"

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

"""
# Checks video file for embedded subtitles
def check_embedded_subtitles(video_file):
    print(f"check_embed_subtitles({video_file}")
    #cmd = "ffprobe -i ", video_file, " "
    cmd = "ffprobe -show_streams -select_streams s " + "'" + video_file + "'"
    print("Command: ", cmd)
    subprocess.run(cmd, shell=True, capture_output=True)
    #print("Embedded info: ", embedded_info)
    #log_append(embed_info)
    #return True, subtitle_name

# Fourth iteration of the same function--currently in use ;)
def has_embedded_subtitles3(video_file):
    try:
        # ffprobe command to get stream information
        # sanitise filepath
        if DEBUG == True:
            print(f"Checking {video_file} embeds with: {cmd}")
        cmd = "/usr/bin/ffprobe -v error -show_streams " + "'" + video_file + "'"
        output = subprocess.run(cmd, shell=True, capture_output=True)
        if DEBUG == True:
            print("    Output: ", output)
        # 'b"subtitle" for "byte-size" rather than str
        if (b"subtitle" in output.stdout):
            if DEBUG == True:
                print(f"Embedded subtitle found in stdout for {video_file}")
            #print(f"subtitle found in stdout: ", output.stdout)
            #return True
            # doesn't get called due to above indented `return True`....
            return re.search(r'subtitle', output, re.I) is not None
    except Exception as e:
        # Handle the case where ffprobe returns an error (e.g., file not found)
        print(f"Error running ffprobe on {video_file}: ", e)
        return False

def has_embedded_subtitles2(video_file):
    cmd = "/usr/bin/ffprobe -v error -show_streams -select_streams s " + "'" + video_file + "'"
    with Popen(cmd, stdout=PIPE, universal_newlines=True) as process:
        for line in process.stdout:
            if ("subtitle" in line):
                print(f"subtitle found in stdout: ", line)
                return True

def has_embedded_subtitles(video_file):
    try:
        # Run ffprobe command to get stream information
        ffprobe_cmd = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'stream=index,codec_name',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            video_file
        ]
        output = subprocess.check_output(ffprobe_cmd, stderr=subprocess.STDOUT, universal_newlines=True)
        # Check if the output contains a 'stream' with codec_name 'subtitles'
        return re.search(r'subtitles', output, re.I) is not None
    except:
        # Handle the case where ffprobe returns an error (e.g., file not found)
        print(f"Error running ffprobe on {video_file}: ", exception)
        return False
"""
""" # Example usage
video_file_path = 'path_to_your_video_file.mp4'
if has_embedded_subtitles(video_file_path):
    print(f"{video_file_path} has embedded subtitles.")
else:
    print(f"{video_file_path} does not have embedded subtitles.") """

# Checks if video file and subtitle file have
# same episode/season S01E07 style
def check_match(video_file, subtitle_file):
    if episode_and_season(video_file) == episode_and_season(subtitle_file):
        if DEBUG == True:
            # Fancy coloring from colorama
            print(Fore.GREEN + "Match found " + Style.RESET_ALL + "between ", video_file, " and ", subtitle_file)
        return True
    else:
        if DEBUG == True:
            print("The files, ", video_file, " and ", subtitle_file, " were not a match")
        return False

# Compares "S01E08" (EAS) of target file to a whole list
# and returns the first match           # Suggestion: return all matches
def get_sub(target_EAS, sub_list):
    for subtitle in sub_list:
        if episode_and_season(subtitle) == target_EAS:
            print(f"The matching subtitle was: {subtitle}")
            if subtitle == None:
                print(f"subtitle == {subtitle} for some reason.\nList of subtitles: {subtitle_list}")
            return subtitle
        else:
            print(f"No matching subtitles for {subtitle} and {target_EAS}")

# Downloads subtitles for (video)file using subliminal
def download_subtitles(video_file, sub_language=pref_sub_language):
    # Encases filename in quotation marks
    quoted_video_file = '"' + video_file + '"'
    # String of the command
    cmd = ("subliminal download -l " + sub_language + " " + quoted_video_file)
    print(f"Downloading subtitles: {cmd}")
    # Execution of command by shell/system
    os.system(cmd)
    downloaded_subtitles.append(video_file)

def log_append(data, log_file='log.txt'):
    #test_string = "\ntest"
    nextline_data = "\n" + data
    try:
        with open(log_file, 'a') as f:
            #todo: add time here
            f.write(nextline_data)
            print("Activity logged to", os.path.abspath(log_file))
    except:
        print("Something went wrong with logging")

"""
def extract_subtitles_old(input_video, output_subtitle_file=None):
    base_name = os.path.splitext(input_video)[0]  # Extract the file name without extension

    # Run ffprobe to get subtitle streams in JSON format
    cmd_ffprobe = [
        "ffprobe", "-v", "error",
        "-select_streams", "s",  # Select subtitle streams
        "-show_entries", "stream=index,codec_name,language",
        "-of", "json", input_video
    ]
    
    try:
        result = subprocess.run(cmd_ffprobe, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        streams = json.loads(result.stdout).get("streams", [])
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error running ffprobe: {e.stderr}")
    except json.JSONDecodeError:
        raise RuntimeError("Failed to parse ffprobe output.")
    
    # Extract subtitle stream information
    subtitle_streams = []
    for stream in streams:
        subtitle_streams.append({
            "index": stream["index"],
            "codec": stream.get("codec_name", "unknown"),
            "language": stream.get("language", "unknown")
        })

    extracted_files = []

    for i, stream in enumerate(subtitle_streams):
        output_subtitle_file = f"{base_name}{subrip_format}"
        print(f"output_subtitle_file: {output_subtitle_file}")
        try:
            # Run ffmpeg command to extract subtitles to a separate file
            ffmpeg_cmd = [
                    "ffmpeg", "-i", input_video, "-map", stream, output_subtitle_file, "-y", "-loglevel", "error"
            ]
            subprocess.run(ffmpeg_cmd, check=True)
            print(f"Subtitles extracted to {output_subtitle_file}")
            extracted_files.append(output_subtitle_file)
        except subprocess.CalledProcessError as e:
            print(f"Error extracting subtitles: {e}")
"""

def get_subtitle_streams_ffprobe(video_file):
    """
    Identifies all embedded subtitle streams in a video file using ffprobe.
    
    Parameters:
        video_file (str): Path to the input video file.
        
    Returns:
        list: A list of dictionaries containing stream index, codec, and language for each subtitle stream.
    """
    if not os.path.exists(video_file):
        raise FileNotFoundError(f"Video file '{video_file}' does not exist.")
    
    # Run ffprobe to get subtitle streams in JSON format
    cmd_ffprobe = [
        "ffprobe", "-v", "error",
        "-select_streams", "s",  # Select subtitle streams
        "-show_entries", "stream=index,codec_name,language",
        "-of", "json", video_file
    ]
    
    try:
        result = subprocess.run(cmd_ffprobe, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        streams = json.loads(result.stdout).get("streams", [])
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error running ffprobe: {e.stderr}")
    except json.JSONDecodeError:
        raise RuntimeError("Failed to parse ffprobe output.")
    
    # Extract subtitle stream information
    subtitle_streams = []
    for stream in streams:
        subtitle_streams.append({
            "index": stream["index"],
            "codec": stream.get("codec_name", "unknown"),
            "language": stream.get("language", "unknown")
        })
    if DEBUG:
        print(f"{video_file} embedded sub streams: {subtitle_streams}")
    return subtitle_streams

def extract_subtitles(video_file, output_dir, subtitle_streams):
    """
    Extracts all identified subtitle streams from a video file using ffmpeg.
    
    Parameters:
        video_file (str): Path to the input video file.
        output_dir (str): Directory where extracted subtitle files will be saved.
        subtitle_streams (list): List of subtitle stream dictionaries obtained from get_subtitle_streams_ffprobe.
        
    Returns:
        list: A list of paths to the extracted subtitle files.
    """
    print(f"output_dir: {output_dir}")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"\n 1 \n")

    extracted_files = []
    for sub in subtitle_streams:
        # Todo: fix language always being unknown
        language = sub["language"] if sub["language"] != "unknown" else f"stream_{sub['index']}"
        output_file = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(video_file))[0]}_{language}.srt")
        # My manual thing
        #output_file = f"{os.path.splitext(os.path.basename(video_file))[0]}_{language}.srt"
        
        # ffmpeg command to extract subtitle
        cmd_extract = [
            "ffmpeg", "-i", video_file,
            "-map", f"0:{sub['index']}",  # Map the subtitle stream
            output_file, "-y", "-loglevel", "error"
        ]
        
        try:
            subprocess.run(cmd_extract, check=True)
            extracted_files.append(output_file)
            print(f"Extracted subtitle to: {output_file}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to extract subtitle stream {sub['index']}: {e.stderr}")
    
    print(f"\n    extraction ran SUCCESFULLY!\n")
    return extracted_files

# Syncs the chosen video's subtitles to its audio reel using ffsubsync
def sync_subtitle(video_file):
    if DEBUG == True:
        print("Synchronising subtitles for ", video_file, " using ffsubsync")

    # Video title's "EAS"
    vid_EAS = episode_and_season(video_file)
    # Subtitle filename matching video's "EAS"
    subtitle_file = get_sub(vid_EAS, subtitle_list)
    if subtitle_file != None:
        # Synced subtitle format
        synced_subtitle_format = ".retimed" + subrip_format
    
        # Reformatting of the synchronised file to ".retimed.srt"
        if DEBUG == True:
            print(f"subtitle_file: {subtitle_file}")
            print(f"Subtitle list: {subtitle_list}")
        # Gives: AttributeError: 'NoneType' object has no attribute 'replace'
        # Deprecated in favour of os.path.splitext
        #synced_subtitle_file = subtitle_file.replace(subrip_format, synced_subtitle_format)
        # os.path.splitext(file) splits file name into tuple ["basename", "extension"]
        base_file = os.path.splitext(subtitle_file)[0] # Extract filename without format suffix/extension
        synced_subtitle_file = f"{base_file}.retimed{subrip_format}"

        # Quoted variables due to blank spaces in filenames
        quoted_video_file = '"' + video_file + '"'
        quoted_subtitle_file = '"' + subtitle_file + '"'
        quoted_synced_subtitle_file = '"' + synced_subtitle_file + '"'

        # ffsubsync command with appropriate parameters
        command = "ffsubsync " + quoted_video_file + " -i " + quoted_subtitle_file + " -o " + quoted_synced_subtitle_file
        if DEBUG == True:
            print("cmd: ", command)

        # Send command to be executed by "shell" or "system"
        os.system(command)
    else:
        print(f"    No external subtitle to sync for {video_file}. Returns: {subtitle_file}")

def synchronise_all():
    # Fancy coloring of colorama
    # Todo: fix.... Broken....
    print("")
    print(Fore.RED + "Synchronising all "
          + Style.RESET_ALL + "subtitles to their respective videos")
    # Synchronises all subtitles to their 
    # respective videos in current directory
    for video in video_list:
        sync_subtitle(video)

def clean_subtitles(subtitle_file):
    # Using https://github.com/KBlixt/subcleaner to clean subtitles of advertisements etc.
    command = f"python {subcleaner} '{subtitle_file}'"
    print(f"Command: {command}")
    #os.system(command)
    # Use subprocess rather than os.system?
    res = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    log_append(res.stdout)
    print(f"COMMAND:\n{' '.join(res.args)}")
    print(f"STDERR: {repr(res.stderr)}")
    print(f'STDOUT: {res.stdout}')
    print(f'RETURN CODE: {res.returncode}')

def clean_all_subtitles():
    for file in subtitle_list:
        clean_subtitles(file)

        base_file, extension = os.path.splitext(file)[0], os.path.splitext(file)[1] # Extract filename without format suffix/extension
        print(f"base_file: {base_file}, extension: {extension}")
        if extension == ".srt":
            clean_subtitles(file)
            if DEBUG == True:
                print("Subtitle extension .srt found in: ", file)
        elif DEBUG == True:
            print(f"file: not subtitle, apparently...")
    print(f"Done cleaning all subtitle files in {current_directory}")

############### END OF DEFINITIONS ###############

if __name__ == "__main__":
    # Stupid manual line-by-line file appending "logging method"
    #log_append("Test")

    # Array initialisation
    video_list = []
    subtitle_list = []
    embed_sub_list = []
    misc_list = []
    downloaded_subtitles = []

    for file in current_directory_list:
        if any(format in file for format in video_formats):
            # Print debug
            # print(format)
            video_list.append(file)
            #if has_embedded_subtitles3(file):
            #if check_embedded_subtitles(file):
                # Print debugging already in has_embedded_subtitles3()
                #print(f"{file} has embedded subtitles!")
                # Get subtitle streams as json -> python directory
            subtitle_streams = get_subtitle_streams_ffprobe(file)
            if subtitle_streams:
                embed_sub_list.append(file)
                if EXTRACT_ALL:
                    extract_subtitles(file, current_directory, subtitle_streams)
            else:
                if DEBUG == True:
                    print(f"{file} does not have embedded subtitles\n    get_subtitle_streams_ffprobe(file) returns:", subtitle_streams)
        elif any(format in file for format in subtitle_formats):
            # print debug
            #print(f"External subtitle: {file}")
            subtitle_list.append(file)
        else:
            if DEBUG:
                print("Unidentified file! Added to misc_list")
            misc_list.append(file)
        
    # Print debug
    # print("Episode list: ", video_list)
    video_sum = len(video_list)
    print("Amount of videos: ", video_sum)

    embed_sub_sum = len(embed_sub_list)
    print("Amount of videos with embedded subtitles: ", embed_sub_sum)

    subtitle_sum = len(subtitle_list)
    print("Amount of external subtitles: ", subtitle_sum)

    # List of episodes without matches
    no_subtitles = []

    if video_sum > 0:
        print("Checking for missing subtitles...")
        # Checks if a video file is missing a subtitle file
        for video in video_list:
            # Resets the match variable to False
            match = False
            for subtitle in subtitle_list:
                if episode_and_season(video) == episode_and_season(subtitle):
                    match = True
                    if DEBUG == True:
                        print("It's a match for video ", video, " and subtitle ", subtitle)
                        # is supposed to print episode and season -- doesn't?
                        """print("It's a match for video ", episode_and_season(video),
                            " and subtitle", episode_and_season(subtitle)) """
            if video not in embed_sub_list and not match:
                no_subtitles.append(video)
        print("Done checking for missing subtitles!")

        # Only runs if 1 or more subtitles were missing                  
        if len(no_subtitles) > 0:
            # Corrects next code block's spelling to singular or plural 
            # based on amount referred to (elements of no_subtitles list)
            was_or_were = "were "
            ep_or_eps = " videos"
            if len(no_subtitles) == 1:
                was_or_were = "was "
                ep_or_eps = " video"
            # Print video(s) without subtitles
            print("There ", was_or_were, len(no_subtitles),
            ep_or_eps, " without subtitle(s), as follows: ",
            no_subtitles)
            # Download subtitles for episodes missing .srt file
            for video in no_subtitles:
                if DEBUG == True:
                    print(f"Debug: No subtitle download for you, {video}")
                else:
                    download_subtitles(video)
            print("Done downloading missing subtitles!")  # Todo: Add error checking
            # Synchronises previously missing subtitles to their respective videos
            print("Synchronising previously missing subtitles!")
            for video in no_subtitles:
                sync_subtitle(video)
            print("Done synchronising previously missing subtitles!")  # Todo: Add error checking
        else:
            print(f"No episodes missing subtitles :]")
        
        # Clean subtitles from ads etc.
        if CLEAN_ALL == True:
            clean_all_subtitles()
        else:
            for subtitles in downloaded_subtitles:
                clean_subtitles(subtitles)

        if SYNC_ALL:
            #todo: fix synchronizing breaking after the first process
            synchronise_all()
