import urllib2
import optparse
import sqlite3

SERVICES = [{"name": "twitter"}]

# TERMS [twitter]
TERMS = [["%23fuzzy"],
         ["%23wazzy"]]

DEBUG = True

def fetch_twitter(term):
    conn = sqlite3.connect('twitter_state.db')
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS stats")
    c.execute("CREATE TABLE stats (service text, date text, term text, count integer)")
    conn.commit()

    req = urllib2.Request(url='http://search.twitter.com/search.json?q=%s' % term)    
    print urllib2.urlopen(req).read()

def main(options):
    conn = sqlite3.connect('stats.db')

    if options.init:
        c = conn.cursor()
        c.execute("DROP TABLE IF EXISTS stats")
        c.execute("CREATE TABLE stats (service text, date text, term text, count integer)")
        conn.commit()

    for term in TERMS:
        if DEBUG:
            print "Term %s" % term[0]
            (state, count) = fetch_twitter(term[0])
        else:
            pass

    conn.close()

if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("--init", dest="init", default=False, action="store_true", help="Initialize the database")
    (options, args) = parser.parse_args()
    main(options)
