from pydub import AudioSegment
from pydub.playback import play
import dearpygui.dearpygui as dpg
import simpleaudio as sa


class FileSystem:
    def file_finder_callback(self, sender, appdata):
        return appdata


class SongModifier:
    def speed_up(self, song, speed_up_rate):
        song_with_changed_frame_rate = song._spawn(song.raw_data, overrides={
            "frame_rate": int(song.frame_rate * speed_up_rate)
        }).set_frame_rate(44100)
        return song_with_changed_frame_rate


class Nightcoreify(SongModifier, FileSystem):
    def __init__(self, song, player):
        self.song = song
        self.speed_rate = 1.25
        self.nightcore = None
        self.player = player

    def set_speed_rate(self, speed_rate):
        self.speed_rate = speed_rate

    def make_nightcore(self):
        self.nightcore = self.speed_up(self.song, self.speed_rate)
        self.player.set_song(self.nightcore)


class Player():
    def __init__(self, song):
        self.play_obj = None
        self.song = song

    def set_song(self, new_song):
        self.song = new_song

    def play_song(self):
        self.play_obj = sa.play_buffer(
            self.song.raw_data,
            num_channels=self.song.channels,
            bytes_per_sample=self.song.sample_width,
            sample_rate=self.song.frame_rate
        )
        play(self.play_obj)

    def stop_song(self):
        self.play_obj.stop()


if __name__ == '__main__':
    song = AudioSegment.from_file("hkimn.mp3")
    songName = "heaven knows"
    music_player = Player(song)
    nightcoreify = Nightcoreify(song, music_player)

    dpg.create_context()
    dpg.create_viewport(title="Nightcoreify", width=500, height=500)
    dpg.setup_dearpygui()

    with dpg.file_dialog(directory_selector=False, show=False, callback=nightcoreify.file_finder_callback,
                         tag="file_dialog_id"):
        dpg.add_file_extension(".mp3")

    with dpg.window(tag="Primary Window"):
        with dpg.group(tag="pos"):
            dpg.add_text(f"Current Song: {songName}")
            dpg.add_slider_float(label="Night Core Rate", tag="NCR", default_value=1.25, max_value=2.0, min_value=1.0,
                                 width=100, callback=lambda: nightcoreify.set_speed_rate(dpg.get_value("NCR")))
            with dpg.group(horizontal=True):
                dpg.add_button(label="Play", callback=music_player.play_song)
                dpg.add_button(label="Stop", callback=music_player.stop_song)
            dpg.add_button(label="Nightcore Me", callback=nightcoreify.make_nightcore)
            dpg.add_button(label="Directory Selector", callback=lambda: dpg.show_item("file_dialog_id"))
    dpg.set_item_pos("pos", [150.0, 150.0])
    dpg.set_primary_window("Primary Window", True)

    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
