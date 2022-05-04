from pydub import AudioSegment
from pydub.playback import play
import dearpygui.dearpygui as dpg
import simpleaudio as sa
from enum import Enum

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

class Song():
    def __init__(self, player):
        self.original_song = None,
        self.modded_song = None
        # Will be a self subscribtion most likely
        self.player = player

    def set_song(self, new_song_path):
        new_song = AudioSegment.from_file(new_song_path)
        self.original_song = new_song
        self.player.set_player_song(new_song)
        self.player.state = PlayerState.STOPPED

    def modify_song(self, modified_song):
        if(not self.modded_song):
            self.modded_song = modified_song
            self.player.set_player_song(modified_song)
        return

    def reset_song(self):
        self.modded_song = None
        self.player.set_player_song(self.original_song)

class Player():
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

       self.song_stoppable_format = sa.play_buffer(
            self.song.raw_data,
            num_channels=self.song.channels,
            bytes_per_sample=self.song.sample_width,
            sample_rate=self.song.frame_rate)
       self.state = PlayerState.PLAYING
       play(self.song_stoppable_format)

class SongModifier:
    def speed_up(self, song, speed_up_rate):
        song_with_changed_frame_rate = song._spawn(song.raw_data, overrides={
            "frame_rate": int(song.frame_rate * speed_up_rate)
        }).set_frame_rate(44100)
        return song_with_changed_frame_rate

class Nightcore(SongModifier):
    def __init__(self):
        self.speed_rate = 1.25

    def set_speed_rate(self, new_speed_rate):
        self.speed_rate = new_speed_rate

    def make_nightcore(self, song):
        nightcore = self.speed_up(song, self.speed_rate)
        return nightcore


if __name__ == '__main__':
    player = Player()
    song = Song(player)
    nightcore = Nightcore()


    dpg.create_context()
    dpg.create_viewport(title="Nightcoreify", width=500, height=500)
    dpg.setup_dearpygui()

    with dpg.window(tag="Primary Window"):
        with dpg.group(tag="pos"):
            dynamic_song_text = dpg.add_text(f"Current Song: None")
            dpg.add_slider_float(label="Night Core Rate", tag="NCR", default_value=1.25, max_value=2.0, min_value=1.0,
                                 width=100, callback=lambda: nightcore.set_speed_rate(dpg.get_value("NCR")))
            with dpg.group(horizontal=True):
                dpg.add_button(label="Play", callback=player.play_song)
                dpg.add_button(label="Stop", callback=player.stop_song)
            with dpg.group(horizontal=True):
                dpg.add_button(label="Nightcore Me", callback=lambda: song.modify_song(nightcore.make_nightcore(song.original_song)))
                dpg.add_button(label="Reset", callback=song.reset_song)
            dpg.add_button(label="Find File", callback=lambda: dpg.show_item("file_dialog_id"))

    with dpg.file_dialog(height=350, width=350, directory_selector=False, show=False, callback=set_file_path,
                         tag="file_dialog_id", user_data=[song, dynamic_song_text]):
        dpg.add_file_extension(".mp3")

    dpg.set_item_pos("pos", [150.0, 150.0])
    dpg.set_primary_window("Primary Window", True)

    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
