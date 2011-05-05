from optparse import OptionParser
from getpass import getpass
from drink_the_hose import drink, Counter, Timedfilewriter

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-u", "--username", dest="username", help= "Twitter username", default=None)
    parser.add_option("-p", "--password", dest="password", help= "Twitter password", default=None)

    (options, args) = parser.parse_args()
    if options.username is None:
        options.username = raw_input()
    if options.password is None:
        options.password = getpass()
        
    drink(username=options.username, password=options.password, stringlist=args, consumers=[Timedfilewriter(), Counter()])
