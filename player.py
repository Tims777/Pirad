import vlc

class RadioPlayer():

    stations = [
        {'name': 'SWR1', 'url': 'http://swr-swr1-bw.cast.addradio.de/swr/swr1/bw/aac/96/stream.aac'},
        {'name': 'SWR3', 'url': 'http://swr-swr3-live.cast.addradio.de/swr/swr3/live/aac/96/stream.aac'},
        {'name': 'Die neue Welle', 'url': 'http://dieneuewelle.cast.addradio.de/dieneuewelle/simulcast/high/stream.mp3'},
        {'name': 'Antenne 1', 'url': 'http://stream.antenne1.de/a1stg/livestream2.mp3'},
        {'name': 'Radio Ton', 'url': 'http://live.radioton.de/rt-live-bw'},
        {'name': 'bigFM', 'url': 'http://streams.bigfm.de/bigfm-deutschland-128-mp3'}
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

    def set_volume(self, value):
        return self.vlc_player.audio_set_volume(value)

    current_station_id = 0

    @property
    def current_station(self):
        return self.stations[self.current_station_id]

    @property
    def volume(self):
        return self.vlc_player.audio_get_volume()

    @property
    def current_audio_device(self):
        dev = self.vlc_player.audio_output_device_get()
        if dev == None: dev = ''
        return dev

    @property
    def currently_playing(self):
        media = self.vlc_player.get_media()
        metadata = media.get_meta(vlc.Meta.NowPlaying)
        if metadata and self.is_playing:
            return metadata
        else:
            return self.is_playing

    @property
    def is_playing(self):
        return self.vlc_player.is_playing()

    @property
    def available_audio_devices(self):
        output_devices = {}
        mods = self.vlc_player.audio_output_device_enum()
        if mods:
            mod = mods
            while mod:
                mod = mod.contents
                output_devices[mod.device.decode('utf-8')] = mod.description.decode('utf-8')
                mod = mod.next
        vlc.libvlc_audio_output_device_list_release(mods)
        return output_devices

    @property
    def available_stations(self):
        return {id: self.stations[id]['name'] for id in range(len(self.stations))}

    def switch_station(self, station_id):
        self.current_station_id = station_id
        self.reload_station()
        self.play()

    def switch_audio_device(self, device_id):
        self.vlc_player.audio_output_device_set(None, device_id)

    def next_station(self):
        self.current_station_id += 1
        self.current_station_id %= len(self.stations)
        self.reload_station()
        self.play()

    def reload_station(self):
        media = self.vlc_instance.media_new(self.current_station['url'])
        self.vlc_player.set_media(media)
