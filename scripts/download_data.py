import re
import urllib.request


# parameter
downloads_base_url = 'https://echanges.dila.gouv.fr/OPENDATA/CAPP/'
output_folder = 'data/raw/'

# download urls page
req = urllib.request.Request(url='https://echanges.dila.gouv.fr/OPENDATA/CAPP/')
with urllib.request.urlopen(req) as f:
    download_page = f.read().decode('utf-8')

# find file names
urls = re.findall('href="(.*?\.tar\.gz)"', download_page)

# download them
for url in urls:
    urllib.request.urlretrieve(downloads_base_url + url, output_folder + url)
