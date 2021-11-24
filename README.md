# fix-subtitles
Uses sublimininal to download missing subtitles and ffsubsync to synchronise them to their respective video files' audio streams

It's mainly for my personal use and at the moment is heavily hardcoded to specific instances

### Assumptions
- the directory comprises of a single movie file or several videos for a single season of a single series
- all files are marked with "S01E08" format -- those being the first numerical markings of the video/subtitle files

### New additions
- Subliminal
	- automatic missing subtitle downloading
		- currently hardcoded for the English language

### WIP:
- Interface
	- download all or a single subtitle
	- synchronise all or a single subtitle
- Support for various media formats and languages
	- currently only avi/mp4/mkv and "en" 
- Looking to support integrated subtitles as well (?)

# Installation

Install pipx:

`python -m install --user pipx`

Install ffsubsync and subliminal through pipx:

`pipx install ffsubsync subliminal`

Clone the repository

`clone https://github.com/rasmusgu/fix-subtitles'
 
### Windows
You have to install ffmpeg manually and set it to your path through your environment variables for ffsubsync to work.

## Dependencies:
- ffsubsync
- ffmpeg
- subliminal
