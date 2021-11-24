# fix-subtitles
Uses ffsubsync to synchronise subtitles to their respective video files


## What it does
Synchronises all subtitles in the directory to their respective videos.

## Assumptions
- the directory has a single season for a single series.
- all files are marked with "S01E08" format

## WIP:
- subliminal
	- Missing subtitle downloading
- Interface
	- download all or a single subtitle and 
	- synchronise all a single subtitle
- Support for various media and subtitle formats
	- Currently only .avi and .srt
		- only en.srt and eng.srt as language formats
	- Looking to support integrated subtitles as well (?)

## Dependencies:
- ffsubsync
- ffmpeg
- subliminal (not yet)
