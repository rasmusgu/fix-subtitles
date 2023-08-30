# fix-subtitles
Python script using `subliminal` to download missing subtitles and `ffsubsync` to synchronise them to their respective video files' audio streams

It's mainly for my personal use and at the moment is heavily hardcoded to specific instances

### Assumptions
- the directory comprises of a single movie file or several videos for a single season of a single series
- all series video files are top level (not in directories) and marked with "S01E08" format -- those being the first numerical markings of the video/subtitle files
	- problem with numerical titles

### New additions
- Subliminal
	- automatic missing subtitle downloading
		- currently hardcoded for the English language
- subcleaner
	- removes ads from subtitles

### WIP:
- Interface
	- download all or a single subtitle
	- synchronise all or a single subtitle
- Support for various media formats and languages
	- currently only avi/mp4/mkv and "en" 
- Looking to support integrated subtitles

# Installation

## ffmpeg
### Windows
Install ffmpeg manually and add it to path (through environment variables) for ffsubsync to work.

### Linux
On Archlinux:

`sudo pacman -S ffmpeg`

## pipx
Install pipx

`python -m install --user pipx`

Install ffsubsync and subliminal with pipx

`pipx install ffsubsync && pipx install subliminal`

Clone the repository

`clone https://github.com/rasmusgu/fix-subtitles`

## Dependencies:
- ffmpeg
- ffsubsync
- subliminal
- colorama (optional for colored CLI output)
