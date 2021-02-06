from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
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

    current_station_id = 0

    @property
    def current_station_name(self):
        return self.stations[self.current_station_id][0]

    @property
    def current_station_url(self):
        return self.stations[self.current_station_id][1]

    def next_station(self):
        self.current_station_id += 1
        self.current_station_id %= len(self.stations)
        self.reload_station()
        self.play()

    def reload_station(self):
        media = self.vlc_instance.media_new(self.current_station_url)
        self.vlc_player.set_media(media)


player = RadioPlayer()


class RemoteControlHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/next':
            player.next_station()
            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()
        else:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<html>')
            self.wfile.write(b'<head><meta charset="UTF-8"><title>Pirad</title></head>')
            self.wfile.write(b'<body>')
            self.wfile.write(bytes(f'<p>Currently playing: {player.current_station_name}</p>', 'utf-8'))
            self.wfile.write(b'<p><a href="/next">Next Station</a></p>')
            self.wfile.write(b'</body>')
            self.wfile.write(b'</html>')


if __name__ == '__main__':
    address = ('', 80)
    server = ThreadingHTTPServer(address, RemoteControlHandler)

    try:
        player.play()
        server.serve_forever()
    except KeyboardInterrupt:
        player.stop()
        server.server_close()
