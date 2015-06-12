# pydict.py
#
# the class that handles the dictionary in PyProse
# including all language-massage duties (conjugating verbs, etc.)

import random
from pyprosecommon import *
from dictionary import DICTIONARY

flagchars = '!\#@'		# mark special comps in sentence template


# dictionary encoding note: self.Di[partname][someinx][0] is the word,
# self.Di[partname][someinx][1] is syllables, [2] is stress;
# the flags at the end of each entry are encoded as:
# self.Di[part][inx][FLAGS][ISSING], . . . [FLAGS][ISPLUR],
# . . . [FLAGS][ISREG] -- see pyprosecommon.py

class PDict:

    def __init__(self, mom):
        self.mom = mom
        self.Di = {}
        for part, entries in DICTIONARY.items():
            self.Di[part] = []
            for entry in entries:
                self.Di[part].append(entry.split())

    # central distribution point for language-massage machinery --
    # returns a string which is the finished sentence
    # alters sData, but it's mutable (object of type Sentence), no need
    # to return it (and will anything else use it anyway?)
    # TODO: note missing underbar-to-invisible-compound translation
    def BuildSentence(self, template, sData):
        s = ''			# where our sentence accumulates
        for i in template:	# from grammar.BuildTemplate
            addword = ''
            if i[0] == '!':
                addword = i[1:]		# word-literal
            elif i[0] == '#':
                self.doFlags(i[1:], sData)
            elif i[0] == '@':
                addword = self.doPunct(i[1:], sData)
            elif i == 'Determiner':
                addword = self.doDeterminer(sData)
            elif i == 'IndefArt':	# sometimes the grammar specifies
                addword = self.doIndefArt(sData)
            elif i == 'Copula':
                addword = self.doCopula(sData)
            elif i == 'ToHave':
                addword = self.doToHave(sData)
            elif i == 'SubjPron':
                addword = self.doSubjPron(sData)
            elif i == 'Possessive':
                addword = self.doPossessive(sData)
            elif i in ('TransVerb', 'IntrVerb', 'AuxInf'):
                addword = self.doFiniteVerb(i, sData)
            elif i[-4:] == 'Part':
                addword = self.doParticiple(i, sData)
            elif i not in ('Noun', 'Substance', 'Adjective', 'AuxVerb'):
                addword = random.choice(self.Di[i])[0]
            else:
                if sData.person == UNSET:
                    sData.person = THIRD	# cheat
                while True:	# loop until word can be made to conform
                    w = random.choice(self.Di[i])
                    if sData.pIsUnset():
                        if w[FLAGS][ISSING] in 'tT':
                            sData.pSetSing()
                        else:
                            sData.pSetPlur()
                    if self.agree(w, sData):
                        addword = w[0]
                        break			# success, by luck
                    # what gets here disagrees with current plurality
                    if i not in ('Noun', 'Substance'):
                        continue # retry
                    if w[FLAGS][ISREG] in 'fF': # irregular noun
                        continue	# retry new word
                    addword = self.doPlural(w[0])
                    break
            if sData.indefArtPending and addword and addword != 'a':
                if addword[0] in VOWELS:
                    s += 'n'
                sData.indefArtPending = False
            # conditions for adding blank before "words"
            if s and (i[0] not in '#@') and (s[-1] != '('):
                s += ' '
            if addword == None:
                addword = "<program error!>"
            s += addword
            # looping back for next component
        s1 = ' '.join(s.split('_'))        # should be ''.join instead???
        return s1[0].upper() + s1[1:] + ' '
    # end of BuildSentence (major distribution point)

    def agree(self, wordentry, sData):
        return (wordentry[FLAGS][ISSING] in 'tT' and sData.pIsSing()
             or wordentry[FLAGS][ISPLUR] in 'tT' and sData.pIsPlur())

    def doIndefArt(self, sData):
        sData.indefArtPending = True
        sData.pSetSing()
        return "a"

    def doPossessive(self, sData):
        # noun if plural and 2/3 of other; count nouns better possesives
        if sData.pIsPlur() or random.randint(0,2):
            w = random.choice(self.Di['Noun'])
            if w[FLAGS][ISPLUR] in 'tT' or sData.pIsSing():
                return w[0] + "'s"
            else:
                while w[FLAGS][ISREG] not in 'tT':
                    w = random.choice(self.Di['Noun'])
                return self.doPlural(w[0]) + "'"
        else:
            return random.choice(self.Di['Substance'])[0] + "'s"

    # presumes word wd has been tested and is regular
    def doPlural(self, wd):
        if wd[-1] == 'y':
            if wd[-2] not in VOWELS: nw = wd[:-1] + 'ies'
            else: nw = wd + 's'
            return nw
        elif wd[-1] in 'xs': return wd + 'es'
        elif wd[-1] == 'h':
            if wd[-2] in 'cs': return wd + 'es'
            else: return wd + 's'
        else: return wd + 's'

    def doFlags(self, s, sData):
        # see pyprosecommon.py for definitions
        if s == 'PushPlur': sData.plurStack.append(UNSET)		# stack grows from end!
        elif s == 'PopPlur': sData.plurStack.pop(CURRENT)
        # I've seen some problems with ForcePlur (and presumably ForceSing) being ignored.
        # I suspect that these flags should work whether plurality is set or not. Experiment:
        #elif s == 'ForceSing' and sData.pIsUnset(): sData.pSetSing()
        #elif s == 'ForcePlur' and sData.pIsUnset(): sData.pSetPlur()
        elif s == 'ForceSing': sData.pSetSing()
        elif s == 'ForcePlur': sData.pSetPlur()
        elif s == 'ForcePast': sData.tense = PAST
        elif s == 'ForceThird': sData.person = THIRD
        else: pass		# ? unknown sentence flag

    def doPunct(self, char, sData):
        if char in (',', ';'):
            sData.pUnset()	# plurality and person end (arbitrarily!)
            sData.person = UNSET	# at phrase/clause bounds
        if char == '-': return ' --'
        elif char == '(': return ' ' + char
        else: return char
        # omitting the random parens-to-dash conversion

    def doDeterminer(self, sData):
        i = random.randint(0, 100)
        if i <= 50: return 'the'	    # no effect on plurality
        if sData.pIsUnset():
            if i <= 75:
                sData.indefArtPending = True
                sData.pSetSing()
                return 'a'
            else:
                w = random.choice(self.Di['Determiner'])
                if w[FLAGS][ISSING] in 'tT': sData.pSetSing()
                else: sData.pSetPlur()
                return w[0]
        else:
            if i <= 70 and sData.pIsSing():
                sData.indefArtPending = True
                return 'a'
            else:
                while 1:		# pick randomly until one matches
                    w = random.choice(self.Di['Determiner'])
                    if self.agree(w, sData):
                        break
            return w[0]

    def doCopula(self, sData):
        if not sData.person:
            sData.person = random.choice((FIRST, SECOND, THIRD))
        if sData.pIsUnset():
            if random.randint(0,1): sData.pSetSing()
            else: sData.pSetPlur()
        if sData.tense == PRESENT:
            if sData.pIsSing():
                if sData.person == FIRST: ret = 'am'
                elif sData.person == SECOND: ret = 'are'
                else: ret = 'is'
            else: ret = 'are'
        else:
            if sData.pIsSing() and sData.person in (FIRST, THIRD):
                ret = 'was'
            else: ret = 'were'
        return ret

    def doToHave(self, sData):
        if not sData.person:
            sData.person = random.choice((FIRST, SECOND, THIRD))
        if sData.pIsUnset():
            if random.randint(0,1): sData.pSetSing()
            else: sData.pSetPlur()
        if sData.tense == PRESENT:
            if sData.pIsSing() and sData.person == THIRD:	ret = 'has'
            else: ret = 'have'
        else: ret = 'had'
        return ret

    def doSubjPron(self, sData):
        if not sData.person:
            sData.person = random.choice((FIRST, SECOND, THIRD))
        if sData.pIsUnset():
            if random.randint(0,1): sData.pSetSing()
            else: sData.pSetPlur()
        if sData.person == FIRST:
            if sData.pIsSing(): return 'I'
            else: return 'we'
        elif sData.person == SECOND: return 'you'
        else:			# the messier third person
            if sData.pIsPlur():
                if not random.randint(0,2): # 1/3 of the time
                    return 'they'
                else:
                    try:
                        while 1:
                            w = random.choice(self.Di['SubjPron'])
                            if w[FLAGS][ISPLUR] in 'tT': break
                        return w[0]
                    except IndexError:	# probably bad dict entry?
                        print `w` + ' went wrong as plur subjpron'
                        return w[0]
            else:	# singular
                if random.randint(0,1): # 1/2 time, use "he/she"
                    if random.randint(0,1): return 'she'
                    else: return 'he'
                else:
                    try:
                        while 1:
                            w = random.choice(self.Di['SubjPron'])
                            if w[FLAGS][ISSING] in 'tT': break
                        return w[0]
                    except IndexError:	# probably bad dict entry!
                        print `w` + ' went wrong as sing subjpron'
                        return w[0] # use it anyway
    # end of doSubjPron

    # the ONLY use of SYLS and STRESS in dictionary
    def doubleLastLetter(self, wd):
        if len(wd[0]) < 3: return False
        ult = wd[0][-1]
        penult = wd[0][-2]
        apult = wd[0][-3]
        if ult in VOWELS or ult in 'yxw': return False
        # adding this in response to "lookking"; but IS it general?
        if ult == 'k': return False
        if penult not in VOWELS or apult in VOWELS: return False
        if wd[SYLS] != wd[STRESS]: return False
        return True

    def getIrregVerb(self, wd, part):
        irregs = self.Di['IrregPart']
        for e in range(0, len(irregs), 4):
            if irregs[e][0] == wd:
                return irregs[e + part][0]

    def doFiniteVerb(self, part, sData):
        if part == 'TransVerb':
            dentry = random.choice(self.Di['TransInf'])
        elif part == 'IntrVerb':
            dentry = random.choice(self.Di['IntransInf'])
        else: dentry = random.choice(self.Di['AuxInf'])
        compound = dentry[0].split('_')      # phrasal verb
        w = compound[0]		# the main-verb part of a phrasal
        if len(compound) > 1: postpos = compound[1]
        else: postpos = ''	# test at end for "if phrasal"
        # build a plurality-matching re(urn)word string
        if dentry[FLAGS][ISREG] in 'fF' and sData.tense == PAST:
            retword = self.getIrregVerb(w, PASTTENSE)
        elif (dentry[FLAGS][ISREG] in 'fF' and sData.person == THIRD and sData.pIsSing()):
            retword = self.getIrregVerb(w, THIRDPRESENT)
        else:		# conjugate a regular verb
            if (sData.tense == PRESENT and sData.person == THIRD and	sData.pIsSing()):
                if w[-1] == 'y' and w[-2] not in VOWELS:
                    retword = w[:-1] + 'ie'
                else:
                    if w[-1] == 'x': retword = w + 'e'
                    elif w[-1] in 'sh' and w[-2] in 'sc':
                        retword = w + 'e'
                    else: retword = w
                retword += 's'
            else:
                if sData.tense == PAST:
                    if w[-1] == 'y' and w[-2] not in VOWELS:
                        retword = w[:-1] + 'i'
                    else: retword = w
                    if self.doubleLastLetter(dentry):
                        retword += w[-1]
                    if retword[-1] == 'e': retword += 'd'
                    else: retword += 'ed'
                else:
                    retword = w
        if postpos: return retword + ' ' + postpos
        else: return retword
    # end of doFiniteVerb

    def doParticiple(self, part, sData):
        if part in ('TrPresPart', 'TrPastPart'):
            dentry = random.choice(self.Di['TransInf'])
        else: dentry = random.choice(self.Di['IntransInf'])
        compound = dentry[0].split('_')     # phrasal verb
        w = compound[0]
        if len(compound) > 1: postpos = compound[1]
        else: postpos = ''
        retword = w 	# first assumption, revised in following block
        if part in ('TrPresPart', 'InPresPart'):
            if w[-1] == 'e':
                if w[-2] == 'u' or w[-2] not in VOWELS:
                    retword = w[:-1]		# "value", "smile"
                elif w[-2] == 'i':  		# "die" -> "dy-"
                    retword = w[:-2] + 'y'
            elif self.doubleLastLetter(dentry):
                retword = w + w[-1]
            retword += 'ing'
        else:		# past participles
            if dentry[FLAGS][ISREG] in 'tT':		# form regular pp
                if w[-1] == 'y' and w[-2] not in VOWELS:
                    retword = w[:-1] + 'i'		# "remedy" ->"remedied"
                if self.doubleLastLetter(dentry):
                    retword += w[-1]
                if retword[-1] == 'e': retword += 'd'
                else: retword += 'ed'
            else:
                retword = self.getIrregVerb(w, PASTPARTICIPLE)
        if postpos: return retword + ' ' + postpos
        else: return retword
