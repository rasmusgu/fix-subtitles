# fix-subtitles
Uses sublimininal to download missing subtitles and ffsubsync to synchronise them to their respective video files' audio streams

It's mainly for my personal use and at the moment is heavily hardcoded to specific instances

## Assumptions
- the directory comprises of a single movie file or several videos for a single season of a single series
- all files are marked with "S01E08" format -- those being the first numerical markings of the video/subtitle files

## New additions
- Subliminal
	- automatic missing subtitle downloading
		- currently hardcoded for the English language

## WIP:
- Interface
	- download all or a single subtitle
	- synchronise all or a single subtitle
- Support for various media and subtitle formats
	- Currently only .avi and .srt
		- only en.srt and eng.srt as language formats as well
	- Looking to support integrated subtitles as well (?)

## Dependencies:
- ffsubsync
- ffmpeg
- subliminal
