from pathlib import Path
import nltk
import re
path = Path.cwd().joinpath('RobiThakur')
'''pths = [pth for pth in path.iterdir() if pth.suffix == '.utf8']
for i in pths:
f=open(i,"r")
print(i)
s = f.read()
s = re.sub('[>;&,/\.+\-%&!#]','',s)
f.close()
#f = open(i,"w")
#f.write(s)
#f.close()'''
'''word_tokenize = nltk.RegexpTokenizer("[\u0980-\u09FF']+")

reader = nltk.corpus.reader(str(path),r'.*\.utf8',cat_pattern=r'',word_tokenizer=word_tokenize)
print(reader.sents(categories='pos'))'''

def do_tokenize(content):
    tokenizer=nltk.RegexpTokenizer("[\u0980-\u09FF']+")
    return tokenizer.tokenize(content)
 
def do_it(si):
    words = []
    for word in do_tokenize(si):
        words.append(word)
    return words

if __name__=='__main__':
    path = Path.cwd().joinpath('RobiThakur')
    pths = [pth for pth in path.iterdir() if pth.suffix == '.utf8']
    lexicons = []
    for i in pths:
        f=open(i,"r")
        print(i)
        s = f.read()
        lexicons = lexicons + do_it(s)
        outfile = open('lexicons.txt',"w")
    
    outfile.write("\n".join(sorted(lexicons)))

