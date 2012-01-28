from seevl import SeevlEntitySearch
for s in SeevlEntitySearch({'prefLabel' : 'the beatles'}).run():
    print "%s is an artist from:" %s.prefLabel
    for o in s.facts['origin']:
        print "- %s" %o['prefLabel']
