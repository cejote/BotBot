#!/usr/bin/python
# -*- coding: UTF-8 -*-



#~ gegebene Strategien: 
#~ simple - Angebot: 250; Annahme: ab 250
#~ more - Angebot: 499; Annahme: ab 501
#~ random - Angebot: zufaellig; Annahme: zufaellig
#~ semirandom - Angebot: zufaellig zwischen 0 und 500; Annahme: ab 500 sicher, zufaellig darunter


import sys
import os
import random
from math import sqrt

DEFAULT_OFFER = 500
REPLY_POSITIVE = 'JA'
REPLY_NEGATIVE = 'NEIN'

class Bot:
    def __init__(self):
        self.n_rounds = 0
        self.cur_round = 0
        self.offers = []
        self.my_offers = []
        self.points = [] #brauchen wir wohl nicht
        self.oppopoints_added = 0
        self.points_added = 0

        self.points_ratio = 0

        self.logfile = open('bot_logfile.txt', 'w+a')
        self.logfile.write("\n ====== %s ====== \n\n" % self.__class__.__name__)

        return None

    def set_n_rounds(self, n):
        self.n_rounds = n
        return None
    
    def set_cur_round(self, r):
        self.cur_round = r
        self.logfile.write("\n=========: RUNDE %s :=========\n" % self.cur_round)    
        return None

    def process_offer(self, offer):
        """ Evaluate offer and send reply """
        #reply = REPLY_POSITIVE
        
        if offer < 300:
            reply = REPLY_NEGATIVE
        else:
            reply = REPLY_POSITIVE
            
        self.offers.append((offer, reply))
        return reply

    def make_offer(self):
        """ Make an offer (that cannot be refused) """
        self.last_offer = DEFAULT_OFFER
        return '%s' % self.last_offer

    def process_reply(self, reply):
        """ Evaluate reply to latest offer """
        self.logfile.write("%s %s\n" % (self.last_offer, reply))
        self.my_offers.append((self.last_offer, reply))
        return None

    def receive_points(self, points):
        self.points.append(points)
        self.points_added  += points
        
        #assuming that I would never ever would touch offers of 0 bucks...
        if points>0:
            self.oppopoints_added += 1000-points

        self.points_ratio = self.points_added / (0.0+self.oppopoints_added+self.points_added)

        self.logfile.write(": punkteverhältniss %s\t(%s : %s)\n" % (self.points_ratio,self.points_added,self.oppopoints_added))
        return None
    
    def postprocess(self):
        """ !!! """

        self.logfile.write(": letzter stand: %s = %s\t%s \n" % (sum(self.points), self.points_added, self.oppopoints_added))


        self.logfile.close()
        return None
    




class cjtbot0(Bot):
    """
    uses static optimum and never defects
    """ 
    def make_offer(self):
        """ find optimal value """
        offer = 300
        self.last_offer = offer
        return '%s' % self.last_offer  






class cjtbot1(Bot):
    """
    tries to find the minimum, yielding in avg the max payoff
    """ 
    
    def __init__(self):
        Bot.__init__(self)

        self.std = 300
        self.var = 100
        
        self.BOT_ACCEPTS_RANDOM=False    
        self.BOT_SENDS_RANDOM=False
       
        self.deny=False
        self.spreading = 50
        return None



    def make_offer(self):
        """ find optimal value to send"""

        MAX_BRAIN=100
        MIN_BRAIN=25
        SWITCH_BEHAV=100
        DEFAULT_OFFER=300



        if self.BOT_ACCEPTS_RANDOM:
            #ok, so 50% for anything I do...
            offer = 0   #let them eat cake!
        
        if self.deny:
            #recalcitrant...
            offer = 500
        
        
        elif self.n_rounds<=SWITCH_BEHAV:
            #too short game for goods statistics
            offer = DEFAULT_OFFER
        
        #start with some interesting offers that are unlikely to be part of the random sampling
        elif self.cur_round<2:
            #send 2 times an offer such that he would win 10bucks per round
            offer=510
            self.logfile.write("510\n")            
        elif self.cur_round<4:
            #send 2 times an offer such that he would win 1 per round
            offer=501
            self.logfile.write("501\n")
        elif self.cur_round<6:
            #send 2 times a neutral offer
            offer=500
            self.logfile.write("500\n")
        
        #now send some test balloons without attracting attention until we reach the era of SWITCH_BEHAV
        elif self.cur_round<SWITCH_BEHAV:
            #TODO: using gaussians?
            #TODO: sampling via bisection method!
            offer = random.randint(0, 19)*25 #in 25 schritten von 0 bis 475
                
        #and finally, send what we learned
        else:


           
            #precalc based on dynamic history aka "brain"
            #~ brain=[x for x in self.my_offers if x[1] == "JA"]

            #~ length=max(min(len(brain), int(self.var), MAX_BRAIN), MIN_BRAIN) #if var=0 or too large, limit length to [MIN_BRAIN,MAX_BRAIN] entries
            
            
            #~ brain=brain[-length:]
            #~ length=len(self.my_offers)
            
            #~ brain22=self.my_offers[-length:]
                    
            #~ for (a,b) in brain22:
                #~ self.logfile.write('%s %s\n' % (a, b))
            

            #get mean and stdev
            #~ (self.std, self.var)=statistics([x[0] for x in brain])
            #~ self.logfile.write("=== brain: %s # µ=%s o=%s ===\n" % (len(brain), self.std, self.var))

            #~ data = self.my_offers[-length:]
            #~ hist=[x for x in data if lim<=x[0]<lim+step]
#~ 
            #~ for (a,b) in hist:
                #~ self.logfile.write('>> %s    %s %s\n' % (lim, a, b))  
                        
            
            
            
            
            
            
            # TODO: wenn mein score zu schlecht wird, dann weniger bieten
            #   wenn ich das kann
            #   sonst weniger großzuügig annehmen
            #   oder beides gleichzeitig?
            #   oder blockiert der die ganze Zeit, egal was ich mache?

            
           
            spreading=50
            (offer,mean,stdv, bar) = maxexpect(self.offers, 1, 900, spreading, self.logfile)
            self.BOT_ACCEPTS_RANDOM =  self.BOT_ACCEPTS_RANDOM and bar #avoid falling back in a unlikely case of bad luck
            
            #self.logfile.write(": stats %s\t%s\n" % (mean,stdv))
            
        self.logfile.write(": ANGEBOT %s\n" % offer)

            
        self.last_offer = offer




        return '%s' % self.last_offer        







    def process_offer(self, offer):
        """ Evaluate offer and send reply """

        self.logfile.write("-- got offer: %s --\n" % offer)    


        #that's always fine
        if offer >= 500:
            self.logfile.write("CASE 1: >500\n")
            reply = REPLY_POSITIVE

        #is it me paying all the time?
        #elif self.points_ratio<0.45 :
        elif self.oppopoints_added-self.points_added>1000:
            self.logfile.write("CASE 2: exploiting me - %s\n" % self.points_ratio)
            reply = REPLY_NEGATIVE
        else:
            

#            (offer,mean,stdv, bsr) = maxexpect(self.my_offers, 1, 600, self.spreading, self.logfile)
#            self.BOT_SENDS_RANDOM =  self.BOT_ACCEPTS_RANDOM and bsr #avoid falling back in a unlikely case of bad luck
#            self.logfile.write(" %s %s       %s--\n" % (mean,stdv, bsr))

            #TODO: to be implemented...


            reply = REPLY_POSITIVE
       
            #1 sendet der nur zufallswerte?
            #2 oder sendet der immer den gleichen wert?
            #3 ist es mehr als ich durchschnittlich einstecke?
            #5 wenn ich ein paar mal ablehne - wird dann die varianz größer? - lohnt sich eine interaktion?

        self.logfile.write("%s %s\n" % (offer, reply))        

            
        self.offers.append((offer, reply))
        return reply













def maxexpect(data, lrange, urange, step, logfile):
    maxscore=0.0
    maxval=0.0
    
    BOT_IS_RANDOM=False

    s2 = 0.0
    s = 0.0
    N=0
    t=0


    histvalues={}

    for lim in xrange(lrange, urange, step):
        hist=[x for x in data if lim<=x[0]<lim+step]

        expect=0.0
        total=0.0+sum([x[0] for x in hist])
        if total>0:
            expect=0.0+sum([x[0] for x in hist if x[1]=="JA"])/total

        e=(1000-lim)*expect

        logfile.write(": hist %s\t%s\t%s\n" % (lim, expect, e))

        if lim==lrange:
            if abs(0.5-expect) < 0.1:
                logfile.write("RANDOM!!!! *******\n")
                BOT_IS_RANDOM=True
                return (maxval, 0, 0, True)


        #do not cosider hell...
        if lim>500 and maxscore>0:
            break


        histvalues[lim]=expect

        
        s2 += expect*expect
        s += expect
        N+=1
    
        if e>=maxscore:
            maxscore=e
            maxval=lim

    (a,b)=statistics(histvalues)



########################
    mean = s/N
    sdev = sqrt((s2-(s*s)/N) /N)
    
    logfile.write(" %s  %s    %s %s*****\n" % (a,mean, b, sdev))
##########################

    
    return (maxval, mean, sdev, BOT_IS_RANDOM)




def statistics(vallist):
    if len(vallist)==0:
        return (0,0)
    s2 = 0.0
    s = 0.0
    N=0.0+len(vallist)
    
    for e in vallist:
        s += e
        s2 += e * e
    
    mean = s/N
    sdev = sqrt((s2-(s*s)/N) /N)
    return (mean, sdev)


def upperquartil(vallist):

    if len(vallist)==0:
        return 0
    
    tmplist=[x[0] for x in vallist]
    total=sum(tmplist)
    if total==0:
        return 0
        
    sortedvallist=sorted(tmplist)[::-1]
    
    s = 0
    for e in sortedvallist:
        s += e
        if s> 0.75*total:
            return e

    return 0



def main(argv):
    if "sadistiker" in argv:
        the_bot = cjtbot1()
    if "statiker" in argv:
        the_bot = cjtbot0()
    
    
    while True:
        next = sys.stdin.readline()
        if not next:
            break
        data = next.strip()
        
        data = data.split()
        if len(data) == 2:
            value = int(data[1])
            if data[0] == 'RUNDEN':
                the_bot.set_n_rounds(value)
            elif data[0] == 'RUNDE':
                the_bot.set_cur_round(value)
            elif data[0] == 'ANGEBOT':
                reply = the_bot.process_offer(value)
                """ Reaction: Send JA or NEIN """
                sys.stdout.write('%s\n' % reply)
                sys.stdout.flush()
            elif data[0] == 'PUNKTE':
                the_bot.receive_points(value)
        elif len(data) == 1:
            if data[0] == 'START':
                """ Reaction: Send offer \in [0,1000] """
                offer = the_bot.make_offer()
                sys.stdout.write('%s\n' % offer)
                sys.stdout.flush()
                pass
            elif data[0] == 'ENDE':
                """ Reaction: Postprocessing and shut down """
                the_bot.postprocess()
                break
            elif data[0] == 'JA' or data[0] == 'NEIN':
                """ Reaction: Process reply (optionally) """
                """ Can only occur after replying to a START cmd """
                the_bot.process_reply(data[0])
                pass
            else:
                pass
        else:
            pass
                

    return None


if __name__ == '__main__': main(sys.argv[1:])

