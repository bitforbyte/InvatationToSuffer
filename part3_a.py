import sys, re

def net_buster(filename, seek_loc):
    round_done = False
    round_offer_done = False
    round_ack_done = False
    with open(f, 'r') as f:
        f.seek(seek_loc)
