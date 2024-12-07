import unittest
import os

from fixsubtitles import log_append, has_embedded_subtitles, extract_subtitles

video_without_embed_sub = '/home/ras/Videos/SERIES/Ergo Proxy (2006)/Season 1/Ergo Proxy - S01E01 - Awakening 720p h264.mkv'
video_with_embed_subs = '/home/ras/Videos/SERIES/The Glory (2022)/Season 1/The Glory - S01E01 - Episode 1 720p h264.mkv'

class TestLogAppend(unittest.TestCase):
    def test_log_append(self):
        with open('test_file.txt', 'w') as file:
            file.write('Line 1\nLine 2')

        log_append('Appended Line', 'test_file.txt')

        with open('test_file.txt', 'r') as file:
            lines = file.readlines()
            self.assertIn('Appended Line\n', lines)

class TestHasEmbeddedSubtitles(unittest.TestCase):
    
    def test_with_subtitles(self):
        # Ensure the video with subtitles returns True
        self.assertTrue(has_embedded_subtitles(video_with_embed_subs))

    def test_without_subtitles(self):
        # Ensure the video without subtitles returns False
        self.assertFalse(has_embedded_subtitles(video_without_embed_sub))

class TestExtractSubtitles(unittest.TestCase):
    def test_extraction(self):
        input_video = video_with_embed_subs
        output_subtitle_file = 'extracted_subtitles.srt'
        extract_subtitles(input_video, output_subtitle_file)

        self.assertTrue(os.path.exists(output_subtitle_file))
        self.assertTrue(os.path.getsize(output_subtitle_file) > 0)

if __name__ == '__main__':
    unittest.main()1