# rarbg-lookup
A Python script to look up torrents in the rarbg-db.sqlite file

Terrible code

## Usage
First, open the file and replace "path/to/file" to the path of your downloaded rarbg-db.sqlite (google it)

Then you can just run the script in a console window `python rarbg.py`

### Search modifiers
- `cat:<category>` - Filters by category. Available categories are: `ebooks, games_pc_iso, games_pc_rip, games_ps3, games_ps4, games_xbox360, movies, movies_bd_full, movies_bd_remux, movies_x264, movies_x264_3d, movies_x264_4k, movies_x264_720, movies_x265, movies_x265_4k, movies_x265_4k_hdr, movies_xvid, movies_xvid_720, music_flac, music_mp3, software_pc_iso, tv, tv_sd, tv_uhd`
- `before:<date>` `after:<date>`- Filters by date in the format of `YYYY-MM-DDThh:mm:ss`
- `bigger:<size>` `smaller:<size>` - Filters by size. Can be specified in bytes, KB, MB, GB.
- `limit:<number>` - Limits the search results to the provided number
- `xxx:<true/false>` - Enables porn in the search results since it is disabled by default.
