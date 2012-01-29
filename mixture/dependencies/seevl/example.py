from seevl.seevl import SeevlEntitySearch, SeevlEntity

## Plain-text search
for s in SeevlEntitySearch({'prefLabel' : 'the beatles'}).run():
    print "%s is an artist from:" %s.prefLabel
    for o in s.facts['origin']:
        print "- %s" %o['prefLabel']

print "===="

## Semantic search (punk-rock from Australia)
for s in SeevlEntitySearch({
        'genre' : 'BntvuZAy',
        'origin' : 'SgnADcN9'
    }).run():
    print "Punk-rock from Australia"
    print "- %s" %s

print "==="

## Related artists
e = SeevlEntity('http://data.seevl.net/entity/exBzc2Wk#id')
print "Here are some bands related to The Clash"
for r in e.related:
    print "- %s" %r

print "==="

## Explanations
e = SeevlEntity('http://data.seevl.net/entity/exBzc2Wk#id')
o = SeevlEntity('http://data.seevl.net/entity/xWYNBFS2#id')
print "Here are some relations between The Clash and Public Image Limited"
for r in e.relations(o):
    for k, v in r.items():
        if isinstance(v, (list, tuple)):
            print "Same %s" %k
            for i in v:
                print "- %s" %i