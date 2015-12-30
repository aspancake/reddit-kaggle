#~# Making CSVs with 50 most common words in each subreddit
#~# From this we can tell how similiar each subreddit is based on word commonality
import nltk
import re
import string
import pandas as pd
from collections import Counter

subred = ['femalefashionadvice', 'philadelphia', 'CrusaderKings', 'chicago', 'BigBrother', 'asoiaf', 'IAmA', 'MonsterHunter', 'miamidolphins', 'rawdenim', 'pcmasterrace', 'photoshopbattles', 'HomeImprovement', 'poker', 'GalaxyS6', 'fantasyfootball', 'syriancivilwar', 'asktrp', 'TheRedPill', 'Naruto', 'wicked_edge', 'MLS', 'GrandTheftAutoV', 'dogs', 'elderscrollsonline', 'newzealand', 'Unexpected', 'medicalschool', 'woodworking', 'microgrowery', 'smashbros', 'nexus6', 'DIY_eJuice', 'summonerschool', 'onewordeach', 'LosAngeles', 'supremeclothing', 'CasualPokemonTrades', 'personalfinance', 'redditgetsdrawn', 'toronto', 'twentyonepilots', 'gainit', 'realmadrid', 'SquaredCircle', 'minnesotavikings', 'baltimore', 'india', 'StarWarsBattlefront', 'OutOfTheLoop', 'breakingmom', 'Portland', 'boardgames', 'nsfw', 'JusticePorn', 'TampaBayLightning', 'RWBY', 'HeistTeams', 'MtF', 'Anarchism', 'Spiderman', 'Kappa', 'ftm', 'EDC', 'Pokemongiveaway', 'WritingPrompts', 'techsupportgore', 'patientgamers', 'Cooking', 'Frugal', 'AtlantaHawks', 'hcfactions', 'TumblrInAction', 'aww', 'amiugly', 'WaltDisneyWorld'] 

list_dfs = []
k=0
for ef in subred:
#~# Place the data into a data frame 
    df_2 = pd.read_csv('best_comments_connect.csv')

#~# Specifying which subreddit to look at
    df_2 = df_2.loc[df_2['subreddit'] == subred[k]]
    
    #~# Place all the comments into a list 
    dfList2 = df_2['body'].tolist()
    
    dfList2 = dfList2[0:400]
    
    output_2=''
    
    t = 0
    for y in dfList2:
        output_2 = output_2 + ' ' + str(dfList2[t])
        t = t+1
    
    dfList = [output_2]
    
    #~# Breaking apart into individual terms, remove punctuation
    punc = re.compile( '[%s]' % re.escape( string.punctuation ) )
    term_vec = [ ]
    
    #~# Get rid of all the floating observations 
    z = 0
    for d in dfList:
        if (type(dfList[z])) != str:
            dfList.remove(dfList[z])
        z = z + 1
    
    for d in dfList:
        d = d.lower()
        d = punc.sub( '', d )
        term_vec.append( nltk.word_tokenize( d ) )
    
    #~# Remove stop words from term vectors
    
    stop_words = nltk.corpus.stopwords.words('english')
    
    for i in range( 0, len( term_vec ) ):
        term_list = [ ]
    
        for term in term_vec[i]:
            if len(term) > 3:
                if term not in stop_words:
                    
                    term_list.append(term.decode('utf-8').replace(u'\u014c\u0106\u014d','-'))
        
            term_vec[i] = term_list
    
    
    #~# Porter stem remaining terms
    #~# Get rid of the strange characters
    
    porter = nltk.stem.porter.PorterStemmer()
    
    for i in range( 0, len( term_vec ) ):
        for j in range( 0, len( term_vec[ i ] ) ):
            term_vec[ i ][ j ] = porter.stem( term_vec[ i ][ j ] )
            if "\\" in repr(term_vec[i][j]):
                term_vec[i][j] = ''
                       
    
    #~# New Lists
    print_list=[]
    for i in term_vec:
        for j in range (0, len(term_vec[0])):
            word = str(term_vec[0][j])
            if len(word) > 4:
                print_list.append(word)
            
    #~# Count em up        
    output = Counter(print_list).most_common()
    
    def getKey(item):
        return item[1]
    
    best_list = sorted(output, key=getKey, reverse=True)
    best_list = best_list[0:50]
    
    #~# Create personalized data frame
    list_dfs.append(pd.DataFrame(best_list))       
    k = k + 1

#~# Empty list
cool = []
q = 0

#~# Now I need to compare all these data frames!
for eff in range (0,len(subred)):
    ok = list_dfs[eff]
    for zek in range (0,len(subred)):
        words = ok[0].tolist()
        ze = list_dfs[zek]
        words_z =ze[0].tolist()
        
        for h in range(0,len(words)):
            for z in range(0,len(words_z)):
                if words[h] == words_z[z]:
                    weight = weight + 1
        
        cool_w = [eff,zek,'Undirected',q,'',weight]
        cool.append(cool_w)
        print(q)
        q = q + 1
        weight = 0
        

frame = pd.DataFrame(cool)
frame.to_csv('Edges.csv')

