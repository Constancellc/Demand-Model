import wikipedia

S = wikipedia.search('Ham and Cheese Sandwich')
page = wikipedia.WikipediaPage(S[0])

i=0
while i<20:
    page = wikipedia.WikipediaPage(page.links[int(random.random()*len(page.links))])
    print(page.title)
    i+=1
