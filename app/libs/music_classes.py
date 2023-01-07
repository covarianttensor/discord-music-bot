class MusicTrack:
    def __init__(self,
        source="N/A",source_thumb_url="",source_icon_url="",webpage_url="",
        title="N/A",stream_url="",duration="N/A",added_by="N/A"):
        self.source = source # YouTube/Spotify/ etc..
        self.source_thumb_url = source_thumb_url
        self.source_icon_url = source_icon_url
        self.webpage_url = webpage_url
        self.title = title
        self.stream_url = stream_url
        self.duration = duration
        self.added_by = added_by

    def pp_from_seconds(self, seconds:int) -> str:
        seconds = seconds % (24 * 3600)
        hours = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        ppstr = ''
        hstr= ''
        mstr = ''
        sstr = ''
        if hours > 0:
            if hours == 1:
                hstr = 'One hour'
            else:
                hstr = f'{hours} hours'
        if minutes > 0:
            if minutes == 1:
                mstr = 'One minute'
            else:
                mstr = f'{minutes} minutes'
        if seconds > 0:
            if seconds == 1:
                sstr = 'One second'
            else:
                sstr = f'{seconds} seconds'
        if hstr != '' and mstr != '' and sstr != '':
            ppstr += hstr
        elif hstr != '' and mstr == '' and sstr != '':
            ppstr += hstr + ' and '
        elif hstr != '' and mstr != '' and sstr == '':
            ppstr += hstr + ' and '
        elif hstr != '' and mstr == '' and sstr == '':
            ppstr += hstr + ' and '
        if mstr != '' and sstr != '':
            ppstr += mstr + ' and '
        elif mstr != '' and sstr == '':
            ppstr += mstr
        if sstr != '':
            ppstr += sstr
        return ppstr

    def set_defaults(self):
        self.source = "N/A"
        self.source_thumb_url = ""
        self.source_icon_url = ""
        self.webpage_url = ""
        self.title = "N/A"
        self.stream_url = ""
        self.duration = "N/A"
        self.added_by = "N/A"

    def set_youtube_source(self,adder,youtube_info):
        def find_audio_url(info:dict) -> str:
            if 'formats' in info:
                fmts = info['formats']
                exts = ['m4a','mp3','ogg']
                for item in fmts:
                    if 'ext' in item:
                        for ext in exts:
                            if ext == item['ext'] and 'url' in item:
                                return item['url']
            return ""

        self.source = "YouTube"
        self.source_thumb_url = youtube_info["thumbnail"]
        self.source_icon_url = "https://covarianttensor.github.io/Uploads/youtube.png"
        self.webpage_url = youtube_info["webpage_url"]
        self.title = youtube_info["title"]
        self.stream_url = find_audio_url(youtube_info)
        self.duration = self.pp_from_seconds(int(youtube_info["duration"]))
        self.added_by = f"{adder}"