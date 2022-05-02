from pydub import AudioSegment
from pydub.playback import play
from PyQt6.QtWidgets import QApplication, QWidget
import sys


def speed_up(song, speed_up_rate):
    song_with_changed_frame_rate = song._spawn(song.raw_data, overrides={
        "frame_rate": int(song.frame_rate * speed_up_rate)
    }).set_frame_rate(44100)
    return song_with_changed_frame_rate


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QWidget()
    window.show()
    song_to_up = AudioSegment.from_file("hkimn.mp3")
    nightcore = speed_up(song_to_up, 1.33)
    play(nightcore)
    app.exec()

