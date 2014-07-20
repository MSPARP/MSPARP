# -*- coding: utf-8 -*-

import re
from random import randint

def scenify(redis, cookie, chat, line):
    bbcode_regex = re.compile("\[.+?\]")
    replacements = [
        ["color", "<BBCODE REMOVED xD>"],
        ["font", "<BBCODE REMOVED xD>"],
        ["y e s", "BURRITO!!!"],
        ["ye s", "PANCAKE MIXS"],
        ["y es", "i once tried dying my hair but it goes back to teh pinks because it no likeys the blue"],
        ["b i t c h", "grrrz"],
        ["a s s", "poo poo hole"],
        [":)", "xD"],
        [":(", "DX"],
        ["f u c k", "FIDDLY DIDDLY!"],
        ["lol", "LOLZ o◖(≧∀≦)◗o"],
        [":3", "x3"],
        ["you", "u"],
        ["omg", "ZOMGZ!!11"],
        ["yo", "im a gangzters"],
        ["nipple", "tinkle winkle"],
        [" hey", "hay"],
        ["fudge off", "my pits smell like applesauce with cream cheese!"],
        ["omfg", "oh my freaking gog!! xD"],
        ["oh my god", "oh my gob"],
        ["she", "her"],
        ["have", "has"],
        ["my", "mah"],
        ["im done", "RAWR MEANS I LOVE YOU IN DINOSAUR!"],
        ["im so done", "RAWR MEANS I LOVE YOU IN DINOSAUR!"],
        ["i'm done", "RAWR MEANS I LOVE YOU IN DINOSAUR!"],
        ["shit", "poopies~"],
        ["holy poopies~", "I'M SO RANDOM"],
        ["love", "LUrve"],
        ["ban", "[O___________0]< AWKWARD WHALE HERE to ask: r u highs XD"]
        ["me", "meh"],
        ["christ", "WHAT'S YOUR MYSPACE? XD maybe we can be bffs!!(warning i have a LOT of random music on mine."],
        ["fuck", "fudge"],
        ["hell", "heck"],
        ["damn", "darn"],
        ["ass", "booty"],
        ["haha", "mwahahaha!!!111"],
        ["what", "wat"],
        ["bye", "baiiii XD"],
        ["hello", "hallo! xD"],
        ["hate", "LOVE"],
        ["help", "halpz me"],
        ["jfc", "jegus fudging crust"],
        ["admins", "those cool guys"],
        ["sorry", "sawwy"],
        ["i'm sawwy", "I apologize to the MSPARP staff for being a little shit. Please don't ban me. [color=#eeeeee] haha your pain is funny[/color]"],
        ["im sawwy", "I apologize to the MSPARP staff for being a little shit. Please don't ban me. [color=#eeeeee] haha your pain is funny[/color]"],
        ["okay", "otay"],
        ["ok", "okayz"],
        ["brb", "AHLL BE BAC >:DDDD MWAHAHAHA"],
        ["later", "laterz!!1"],
        ["please", "plz"],
        [" oc ", "original character (mine dnt stealzies)"],
        ["special", "speshul"]
        ["stop", "staph"],
        ["its", "itz"],
        ["it's", "it'z"],
        ["wow", "wowzers"],
        ["seen", "sce[i][/i]ne"],
        ["crying", "THE FEELS! I'M CRYING IRL \◖(,◕ д ◕, )◗/"],
        ["scene", "not emo"],
        ["fudge u", "fak u ◖(◕◡◕)◗凸"],
        ["the feels", "oh glob i'm crying my mascara is running. it makes me look like a panda XD"],
        ["the", "teh"],
        ["yes", "yiff meh"],
        ["wait", "w8"],
        ["is", "iz"],
        ["bad", "badzies o-O"],
        ["bulge", "hentai tentacles!"],
        ["kill", "◖(◕◡◕)◗ huuuggggg ◖(◕◡◕)◗"],
        ["murder", "◖(◕◡◕)◗ luving huggles ◖(◕◡◕)◗"],
        ["die", "be my bff"],
        ["ddos", "im going to poo aggresively!"],
        ["nigger", "◖(◕◡◕)◗ i am ignorant p4nda ◖(◕◡◕)◗"],
        ["trans scum", "i am so sorry for everything i've said"],
        ["fag ", "CHEESE WHEELS XD"],
        ["staff", "the people i love"],
        ["faggot", "◖(◕◡◕)◗ <censored> ◖(◕◡◕)◗"],
        ["suicide", "◖(◕◡◕)◗ hug me now ◖(◕◡◕)◗"],
        ["nigga", "panda buddies <3"],
        ["proxy", "erigam is my otp"],
        ["proxies", "erigam is canon"],
        ["hack", "i love ice cream"],
        ["bitch", "karry"],
        ["bootyhole", "karry"],
        ["yesterday", "yiff mehterday"],
        ["sucks", "is the best"],
        ["gay", "rose"],
        ["jesus", "o_o mlp"],
        ["boob", "boobiehz XD"],
        ["dick", "anusfly"],
        ["vagina", "pee pee hole"],
        ["penis", "pee pee"],
        ["cunt", "meanie bobeanie"],
        ["bugger", "TACOS! XD"],
        ["cat", "nepeat"],
        ["jizz", "you said a bad word!"],
        ["cum", "i like potatoes"],
        ["cock", "dingler"],
        ["clit", "winky"],
        ["fuck this", "preps never understand QAQ"],
    ]

    r = lambda: randint(0, 255)
    color = '%02X%02X%02X' % (r(), r(), r())

    # Lower case quirk.
    line = line.lower()
    # Strip BBCode to prevent sneakyness.
    line = bbcode_regex.sub("", line)

    # Replacements.
    for replacement in replacements:
        line = line.replace(replacement[0].decode('utf-8', 'ignore'), replacement[1].decode('utf-8', 'ignore'))

    # Prefix
    line = "[font=Comic Sans MS] [color=#%s] k1nqp4ndA: ◖(◕ω◕)◗ < %s".decode('utf-8', 'ignore') % (color, line)

    # Redis stuffs.
    datakey = 'session.%s.chat.%s' % (cookie, chat)
    redis.hset(datakey, 'acronym', '')
    redis.hset(datakey, 'name', 'XxTEH PANDA KINGxX')
    redis.hset(datakey, 'quirk_prefix', '')

    return line[:1500]
