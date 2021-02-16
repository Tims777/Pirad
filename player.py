import vlc

class RadioPlayer():

    stations = [
        ('SWR1', 'https://swr-swr1-bw.cast.addradio.de/swr/swr1/bw/aac/96/stream.aac'),
        ('SWR3', 'https://swr-swr3-live.cast.addradio.de/swr/swr3/live/aac/96/stream.aac')
    ]

    def __init__(self):
        self.vlc_instance = vlc.Instance()
        self.vlc_player = self.vlc_instance.media_player_new()
        self.reload_station()

    def play(self):
        self.vlc_player.play()

    def pause(self):
        self.vlc_player.pause()

    def stop(self):
        self.vlc_player.stop()

    def is_playing(self):
        return self.vlc_player.is_playing()

    def set_volume(self, value):
        return self.vlc_player.audio_set_volume(value)

    current_station_id = 0

    @property
    def current_station_name(self):
        return self.stations[self.current_station_id][0]

    @property
    def current_station_url(self):
        return self.stations[self.current_station_id][1]

    @property
    def volume(self):
        return self.vlc_player.audio_get_volume()

    def next_station(self):
        self.current_station_id += 1
        self.current_station_id %= len(self.stations)
        self.reload_station()
        self.play()

    def reload_station(self):
        media = self.vlc_instance.media_new(self.current_station_url)
        self.vlc_player.set_media(media)
