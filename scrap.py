from lxml import html
import requests
import re
import math

errors = []
for i in range(1,10):
    try:
        page = requests.get('http://www.rabindra-rachanabali.nltr.org/print/' + str(i))
        tree = html.fromstring(page.content)

        htmlfile = page.content.decode('utf8')
        text = re.sub(r'<.*?>','',htmlfile)
        text = re.sub(r'[a-zA-Z]','',text)

        f= open("RobiThakur/" + str(i) + ".utf8","w")
        f.write(text)
        print("processed page number " + str(i))
    except requests.exceptions.ConnectionError:
        errors.append(str(i))
        print("Error at page number " + str(i))

log = open("errors.txt","w")
log.write(",".join(errors))
