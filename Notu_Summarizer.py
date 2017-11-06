# run it as python333 Notu_Summarizer.py; reads from file and summarizes conversation 
# need to install sumy 'pip3 install sumy'

from sumy.parsers.plaintext import PlaintextParser 
from sumy.nlp.tokenizers import Tokenizer 
from sumy.summarizers.lex_rank import LexRankSummarizer #We're choosing Lexrank, other algorithms are also built in

file = "plain_text.txt" #name of the plain-text file
parser = PlaintextParser.from_file(file, Tokenizer("english"))
summarizer = LexRankSummarizer()

summary = summarizer(parser.document, 5) #Summarize the document to 5 sentences

for sentence in summary:
    print (sentence)
