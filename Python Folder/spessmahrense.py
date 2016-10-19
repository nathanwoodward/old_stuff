from random import randrange

d6 = lambda : randrange(0,7)

roll = lambda n : d6() >= n

def round(nSM, nGN):
	
	spessMahrense = nSM
	greyKnights = nGN
	
	# grey knights attack first
	
	for attack in xrange(greyKnights*2+1):
		
		spessMahrense -= (roll(3) and roll(2) and roll(5))
	
	# spess mahrense attack last
	
	for attack in xrange(spessMahrense):
		
		greyKnights -= (roll(4) and roll(2) and roll(3))
	
	# less than 0 dudes is teh ghey
	
	if spessMahrense < 0 : spessMahrense = 0
	if greyKnights < 0 : greyKnights = 0
	
	return spessMahrense, greyKnights

def combat(nSM, nGM):
	
	sm = nSM
	gm = nGM
	
	while 1:
		
		sm, gm = round(sm, gm)
		
		if sm == 0:
			
			return 1
		
		elif gm == 0:
			
			return 0

def sim(n, nSM, nGM):
	
	smwins = 0
	gnwins = 0
	
	for x in xrange(n):
		
		win = combat(nSM,nGM)
		
		if win: gnwins += 1
		else: smwins += 1
	
	print "Number of Space Marine wins : " + str(smwins)
	print "Number of Grey Knight wins : " + str(gnwins)

def main():
	
	n = int(raw_input("How many times should the simulation be done? "))
	nSM = int(raw_input("Number of assualt termies? "))
	nGM = int(raw_input("Number of Grey Knights? "))
	
	sim(n, nSM, nGM)

if __name__ == '__main__':
	main()