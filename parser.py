import requests  # pip install requests
from time import time
import os

FILENAME = "video-{}.ts"  # {} - index !important!

url = input("URL to download .m3u8 file: ")
resp = requests.get(url)
if resp.status_code == 200:
    links = []
    for i, size in enumerate(resp.text.split("RESOLUTION=")[1:]):
        size, link = map(lambda s: s.strip(), size.split('\n')[:2])
        links.append((size, link))
        print(f"{i+1}) to download {size}")
    download_id = input("ID to download: ")
    while not download_id.isdigit() or 0 > int(download_id) - 1 or int(download_id) > len(links):
        download_id = input("ID to download: ")
    download_id = int(download_id)
    data_to_parse = requests.get(links[download_id-1][1])
    if data_to_parse.status_code:
        links = list(map(lambda text: text.split('\n')[1], data_to_parse.text.split("EXTINF")[1:]))
        print(f"Count segments - {len(links)}")
        path = input("Folder to save: ")
        while not os.path.isdir(path):
            path = input("Folder to save: ")
        if not (path.endswith("/") or path.endswith("\\")):
            path += "/"
        from_download = input("From which to download (1 - default): ")
        while not from_download.isdigit() or 0 > int(from_download) - 1 or int(from_download) > len(links):
            from_download = input("From which to download (1 - default): ")
        from_download = int(from_download)
        to_download = input("Until what download (0 - all): ")
        while not to_download.isdigit() or int(to_download) != 0 and from_download > int(to_download) - 1 or int(to_download) > len(links):
            to_download = input("Until what download (0 - all): ")
        to_download = int(to_download)
        links = links[from_download-1:(to_download-1 if to_download != 0 else len(links))]
        print(f"Downloading from: {from_download}, to: {to_download if to_download != 0 else len(links)}, count: {len(links)}")
        rotate = ['—', '—', '—', '\\', '\\', '|', '|', '/', '/']
        count = len(links), len(rotate)
        for i, link in enumerate(links):
            print(f'\r{round((i+1)/count[0] * 100, 2)}% \t{rotate[int(time()*4) % count[1]]} \tfile №{i+1}', end="")
            data = requests.get(link)
            if data.status_code == 200:
                try:
                    with open(path+FILENAME.format(i), 'wb') as w:
                        w.write(data.content)
                except Exception:
                    print(f"Error on write segment {i}")
            else:
                print(f"Error on download segment ERROR: {data.status_code}")
    else:
        print(f"Error on download links ERROR: {data_to_parse.status_code}")
else:
    print(f"Error on download .m3u8 file ERROR: {resp.status_code}")
