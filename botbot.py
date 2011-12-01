#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
<< cjtbot1 >>   v0.2

**********
2011-11-30


This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>. 
'''



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
        self.oppopoints_added = 0
        self.points_added = 0

        self.points_ratio = 0
        self.points_xratio = 0

        return None

    def set_n_rounds(self, n):
        self.n_rounds = n
        return None
    
    def set_cur_round(self, r):
        self.cur_round = r
        return None

    def process_offer(self, offer):
        """ Evaluate offer and send reply """
        
        if offer < 170:
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
        self.my_offers.append((self.last_offer, reply))
        return None

    def receive_points(self, points):
        #self.points.append(points)
        self.points_added  += points
        
        #assuming that I would never ever would touch offers of 0 bucks...
        if points>0:
            self.oppopoints_added += 1000.0-points

        if (self.oppopoints_added+self.points_added)>0:
            #self.points_ratio = self.points_added / (0.0+self.oppopoints_added+self.points_added)
            self.points_xratio=self.points_added/(0.0+self.oppopoints_added+self.points_added)
            self.points_ratio=(self.oppopoints_added-self.points_added)/(0.0+self.cur_round)
        else:
            #TODO: ok so???
            self.points_ratio=0

        return None
    
    def postprocess(self):
        """ RIP. """
        return None
    





class cjtbot1(Bot):
    """
    tries to find the minimum, yielding in avg the max payoff
    """ 
    
    def __init__(self):
        Bot.__init__(self)

        self.BOT_SENDS_RANDOM=False
        self.currentOffer=512
        self.lastGoodOffer=1024
        self.lastBadOffer=0
             
        return None



    def make_offer(self):
        """ find optimal value to send"""


        # 510 = 10 minus for me, +10 for him.
        # Bids < 490
        RATIO_LIMIT=100
        XRATIO_LIMIT=0.48
        BRAIN=20

        
        offer=self.currentOffer

        # backup
        if self.cur_round>50 and (self.points_ratio>RATIO_LIMIT or self.points_xratio<XRATIO_LIMIT):
            offer=500 # stop exploiting me


        #~ if self.BOT_ACCEPTS_RANDOM:
            #~ #ok, so 50% for anything I do...
            #~ offer = 0   #let them eat cake!


        # whohooo?!
        elif self.currentOffer>512:
            offer=512


        # bisection...
        elif not (self.cur_round%BRAIN):
            #~ check last BRAIN reactions
            replies=self.my_offers[-BRAIN:]
            
            val=len([x for x in replies if x[1]==REPLY_POSITIVE])/(0.0+BRAIN)
            #self.tested[self.currentOffer]= val

            
            # as time goes by... am I still at the optimum?
            if not self.cur_round%(BRAIN*20):
                # set values for starting with 512
                self.currentOffer=1024
                self.lastGoodOffer=2048
                self.lastBadOffer=0
                val=5   # force re-check


            # offers accepted
            if val>=0.2:

                # avoid too small steps
                if (self.lastGoodOffer-self.lastBadOffer)>10:
                    self.lastGoodOffer=self.currentOffer
                    self.currentOffer=round(self.currentOffer-((self.lastGoodOffer-self.lastBadOffer)/2.0))
                else:
                    pass
                    
            else:
                # avoid too small steps - and fall back to last known optimum
                if (self.lastGoodOffer-self.lastBadOffer)>10:
                    self.lastBadOffer=self.currentOffer  # remember, remember
                    self.currentOffer=round(self.currentOffer+((self.lastGoodOffer-self.lastBadOffer)/2.0))
                else:
                    self.currentOffer = self.lastGoodOffer
                
        offer=self.currentOffer
        # end bisection

        self.last_offer = offer
        return '%s' % self.last_offer   







    def process_offer(self, offer):
        """ Evaluate offer and send reply """

        BRAIN=25
        THRESHOLD_OF_PAIN=300
        XRATIO_GREEDY_LIMIT=0.53
        XRATIO_LIMIT=0.48


        reply = REPLY_NEGATIVE

        # that's always ok
        if offer >= 500:
            reply = REPLY_POSITIVE

        # on the bright side of life?
        elif offer >= THRESHOLD_OF_PAIN and self.points_xratio>XRATIO_GREEDY_LIMIT:
            reply = REPLY_POSITIVE # big fat bonus

        self.offers.append((offer, reply))
        return reply











def main(argv):
    # welcome to the show!
    the_bot = cjtbot1()
    
    
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

