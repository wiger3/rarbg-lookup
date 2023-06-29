import sqlite3

db = "path/to/file"
cats = [
    "ebooks",
    "games_pc_iso",
    "games_pc_rip",
    "games_ps3",
    "games_ps4",
    "games_xbox360",
    "movies",
    "movies_bd_full",
    "movies_bd_remux",
    "movies_x264",
    "movies_x264_3d",
    "movies_x264_4k",
    "movies_x264_720",
    "movies_x265",
    "movies_x265_4k",
    "movies_x265_4k_hdr",
    "movies_xvid",
    "movies_xvid_720",
    "music_flac",
    "music_mp3",
    "software_pc_iso",
    "tv",
    "tv_sd",
    "tv_uhd"
]

def str_to_size(size_s: str):
    if size_s.isdecimal():
        return int(size_s)
    size_s = size_s.upper()
    if size_s.endswith('KB'):
        return int(float(size_s[:-2]) * 1024)
    if size_s.endswith('MB'):
        return int(float(size_s[:-2]) * 1048576)
    if size_s.endswith('GB'):
        return int(float(size_s[:-2]) * 1073741824)
    if size_s.endswith('B'):
        return int(size_s[:-1])
    print("Failed to convert size: " + size_s)
    return -1

con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
cur = con.cursor()

name = input("Search: ")
options = ""
limit = ""
xxx = 'cat!="xxx" AND '
args = name.split(' ')
if 'cat:' in name:
    _args = args.copy()
    for x in _args:
        if x.startswith('cat:'):
            cat = x.split(':')[1]
            args.remove(x)
            if not cat in cats:
                print("Unknown category: " + cat)
                continue
            if not 'cat' in options:
                options += ' AND (cat="' + cat + '"'
            else:
                options += ' OR cat="' + cat + '"'
    if options != '': options += ')'
if 'before:' in name:
    _args = args.copy()
    for x in _args:
        if x.startswith('before:'):
            date = x.split(':')[1]
            date = date.upper().replace('T', ' ')
            args.remove(x)
            options += ' AND dt<"' + date + '"'
if 'after:' in name:
    _args = args.copy()
    for x in _args:
        if x.startswith('after:'):
            date = x.split(':')[1]
            date = date.upper().replace('T', ' ')
            args.remove(x)
            options += ' AND dt>"' + date + '"'
if 'bigger:' in name:
    _args = args.copy()
    for x in _args:
        if x.startswith('bigger:'):
            size_s = x.split(':')[1]
            args.remove(x)
            size = str_to_size(size_s)
            if size == -1: continue
            options += ' AND size>' + str(size)
if 'smaller:' in name:
    _args = args.copy()
    for x in _args:
        if x.startswith('smaller:'):
            size_s = x.split(':')[1]
            args.remove(x)
            size = str_to_size(size_s)
            if size == -1: continue
            options += ' AND size<' + str(size)
if 'limit:' in name:
    _args = args.copy()
    for x in _args:
        if x.startswith('limit:'):
            limit = x.split(':')[1]
            args.remove(x)
            limit = ' LIMIT ' + str(limit)
if 'xxx:' in name:
    _args = args.copy()
    for x in _args:
        if x.startswith('xxx:'):
            porn = x.split(':')[1]
            args.remove(x)
            if porn.lower() in ['true', '1', 'yes', 'y', 't']:
                xxx = ''

name = '_'.join(args)

name = name.replace('\\', '\\\\')
name = name.replace('%', '\%')
name = f"%{name}%"
res = cur.execute(f'SELECT * FROM items WHERE {xxx}title LIKE ? ESCAPE "\\"{options} ORDER BY dt DESC{limit}', (name,))
print()
torrents = res.fetchall()
if len(torrents) != 0:
    pad_cat = 4
    pad_title = 5
    for x in torrents:
        if len(x[2]) > pad_title: # title
            pad_title = len(x[2])
        if len(x[4]) > pad_cat: # cat
            pad_cat = len(x[4])
    if pad_title > 128:
        pad_title = 128
    i_pad = len(str(len(torrents)))+1
    print(f"{'  '.ljust(i_pad)} {'Cat.'.ljust(pad_cat)} | {'title'.ljust(pad_title)} | {'added'.ljust(19)} | size")
    i = 0
    for t in torrents:
        size_s = ""
        cat: str = t[4]
        title: str = (t[2][:125] + '...') if len(t[2]) > 128 else t[2]
        added: str = t[3]
        size: int = 0 if t[5] == None else int(t[5])
        size_kb = size / 1024
        size_mb = size_kb / 1024
        size_gb = size_mb / 1024
        if size_gb >= 1:
            size_s = f"{size_gb:.2f}GB"
        elif size_mb >= 1:
            size_s = f"{size_mb:.2f}MB"
        elif size_kb >= 1:
            size_s = f"{size_mb:.2f}KB"
        else:
            size_s = f"{size}B"
        
        print(f"{f'{i}.'.ljust(i_pad)} {cat.ljust(pad_cat)} | {title.ljust(pad_title)} | {added} | {size_s.rjust(9)}")
        i+=1
    del i
    print()
    a = int(input("Select: "))
    print(f"\nmagnet:?xt=urn:btih:{torrents[a][1]}&dn={torrents[a][2]}")
else:
    print("No results found")