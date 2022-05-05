from pydub import AudioSegment
from pydub.playback import play
import simpleaudio as sa
import pathlib
from enum import Enum
import dearpygui.dearpygui as dpg

class PlayerState(Enum):
    PLAYING = 0,
    STOPPED = 1


def set_file_path(self, sender, appdata):
    song_object = appdata[0]
    dynamic_song_text = appdata[1]
    path = sender['file_path_name']
    song_name = sender['file_name']
    song_object.set_song(path)
    dpg.set_value(dynamic_song_text, f"Current Song: {song_name}")
    song_object.set_song_name(song_name)

class Song():
    def __init__(self, player):
        self.original_song = None,
        self.modded_song = None,
        self.song_name = None,
        # Will be a self subscribtion most likely
        self.player = player

    def set_song_name(self, new_song_name):
        self.song_name = new_song_name

    def set_song(self, new_song_path):
        new_song = AudioSegment.from_file(new_song_path)
        self.original_song = new_song
        self.player.set_player_song(new_song)
        self.player.state = PlayerState.STOPPED

    def modify_song(self, modified_song):
        if(self.modded_song is not None):
            print(self.modded_song)
            self.modded_song = modified_song
            self.player.set_player_song(modified_song)
        else:
            print("Song has already been Nightcored")

    def reset_song(self):
        self.modded_song = None
        self.player.set_player_song(self.original_song)

    def export_song(self):
        file_path = str(pathlib.Path.home()) + "/Desktop/nightcore_" + self.song_name
        self.modded_song.export(file_path, format="mp3")

class FormatSong:
    def format_song_to_stop(self, song):
        return sa.play_buffer(
            self.song.raw_data,
            num_channels=self.song.channels,
            bytes_per_sample=self.song.sample_width,
            sample_rate=self.song.frame_rate)

class Player(FormatSong):
    def __init__(self):
        self.song = None
        self.song_stoppable_format = None
        self.state = PlayerState.STOPPED

    def stop_song(self):
        if(self.state == PlayerState.STOPPED):
            return
        self.state = PlayerState.STOPPED
        self.song_stoppable_format.stop()

    def set_player_song(self, song):
        if (self.song_stoppable_format != None):
            self.song_stoppable_format.stop()
        self.song = song

    def play_song(self, song):
       if(self.state == PlayerState.PLAYING):
           return
       self.song_stoppable_format = self.format_song_to_stop(self.song)
       self.state = PlayerState.PLAYING
       play(self.song_stoppable_format)


class Nightcore():
    def __init__(self):
        self.speed_up_rate = 1.00

    def speed_up(self, song):
        song_with_changed_frame_rate = song._spawn(song.raw_data, overrides={
            "frame_rate": int(song.frame_rate * self.speed_up_rate)
        }).set_frame_rate(44100)
        return song_with_changed_frame_rate

    def set_speed_rate(self, new_speed_rate):
        self.speed_up_rate = new_speed_rate

    def make_nightcore(self, song):
        nightcore = self.speed_up(song)
        return nightcore

def main():
    player = Player()
    song = Song(player)
    nightcore = Nightcore()

    dpg.create_context()
    dpg.create_viewport(title="Nightcoreify", width=500, height=500)
    dpg.setup_dearpygui()

    with dpg.window(tag="Primary Window"):
        with dpg.group(tag="pos"):
            dynamic_song_text = dpg.add_text(f"Current Song: None")
            dpg.add_slider_float(label="Night Core Rate", tag="NCR", default_value=1.00, max_value=2.0, min_value=.05,
                                 width=100, callback=lambda: nightcore.set_speed_rate(dpg.get_value("NCR")))
            with dpg.group(horizontal=True):
                dpg.add_button(label="Play", callback=player.play_song)
                dpg.add_button(label="Stop", callback=player.stop_song)
            with dpg.group(horizontal=True):
                dpg.add_button(label="Nightcore",
                               callback=lambda: song.modify_song(nightcore.make_nightcore(song.original_song)))
                dpg.add_button(label="Reset", callback=song.reset_song)
            with dpg.group(horizontal=True):
                dpg.add_button(label="Find File", callback=lambda: dpg.show_item("file_dialog_id"))
                dpg.add_button(label="Export File", callback=song.export_song)
    with dpg.file_dialog(height=350, width=350, directory_selector=False, show=False, callback=set_file_path,
                         tag="file_dialog_id", user_data=[song, dynamic_song_text]):
        dpg.add_file_extension(".mp3")

    dpg.set_item_pos("pos", [150.0, 150.0])
    dpg.set_primary_window("Primary Window", True)

    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == '__main__':
    main()
