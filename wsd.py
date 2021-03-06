from pywsd.lesk import adapted_lesk
from nltk.corpus import wordnet as wn
import pickle
import time
import sys

def main(file_name):
	start = time.time()
	#string = '/home/adriana/Dropbox/mine/Tese/preprocessing/data_output/'
	#string = '/home/aferrugento/Desktop/'
	string = ''
	h = open(string + file_name + '_proc.txt')
	sentences = h.read()
	h.close()
	extra_synsets = {}
	sentences = sentences.split("\n")
	for i in range(len(sentences)):
		sentences[i] = sentences[i].split(" ")
		for j in range(len(sentences[i])):
			if sentences[i][j] == '':
				continue
			sentences[i][j] = sentences[i][j].split("_")[0]

	for i in range(len(sentences)):
		aux = ''
		for j in range(len(sentences[i])):
			aux += sentences[i][j] + ' '
		sentences[i] = aux
	word_count = pickle.load(open('word_count_new.p'))
	synset_count = pickle.load(open('synset_count.p'))
	word_count_corpus = calculate_word_frequency(sentences)

	sum_word_corpus = 0
	for key in word_count_corpus.keys():
		sum_word_corpus += word_count_corpus.get(key)
	sum_word = 0
	for key in word_count.keys():
		sum_word += word_count.get(key)
	sum_synset = 0
	for key in synset_count.keys():
		sum_synset += synset_count.get(key)

	word_list = []
	for key in word_count.keys():
		word_list.append(word_count.get(key))
	synset_list = []
	for key in synset_count.keys():
		synset_list.append(synset_count.get(key))
	word_list.sort()
	synset_list.sort()

	#print len(word_list), len(synset_list)
	#print len(word_list)/2., len(synset_list)/2., (len(word_list)/2.) -1, (len(synset_list)/2.) -1
	#print word_list[len(word_list)/2], word_list[(len(word_list)/2)-1]
	#print synset_list[len(synset_list)/2], synset_list[(len(synset_list)/2)-1]
	word_median = round(2./sum_word, 5)
	synset_median = round(2./sum_synset, 5)
	#print word_median, synset_median
	#print sum_word, sum_synset
	#return

	
	#f = open(string + 'preprocess_semLDA_EPIA/NEWS2_snowballstopword_wordnetlemma_pos_freq.txt')
	f = open(string + file_name +'_freq.txt')
	m = f.read()
	f.close()
	m = m.split("\n")

	for i in range(len(m)):
		m[i] = m[i].split(" ")

	count = 0
	imag = -1
	#f = open(string + 'preprocess_semLDA_EPIA/znew_eta_NEWS2.txt')
	f = open(string + file_name + '_eta.txt')
	g = f.read()
	f.close()

	g = g.split("\n")
	for i in range(len(g)):
		g[i] = g[i].split(" ")


	dic_g = create_dicio(g)

	g = open(string + file_name +'_wsd.txt','w')
	
	#dictio = pickle.load(open(string + 'preprocess_semLDA_EPIA/NEWS2_snowballstopword_wordnetlemma_pos_vocab.p'))
	dictio = pickle.load(open(string + file_name +'_vocab.p'))
	nn = open(string + file_name +'_synsetVoc.txt','w')
	synsets = {}
	to_write = []
	p = open(string + 'NEWS2_wsd.log','w')
	for i in range(len(m)):
		nana = str(m[i][0]) + ' '
		print 'Doc ' + str(i)
		p.write('---------- DOC ' +str(i) + ' ----------\n')
		#words_probs = bayes_theorem(sentences[i], dictio, word_count, sum_word, word_median)
		#return
		#g.write(str(m[i][0]) + ' ')
		for k in range(1, len(m[i])):
			#print sentences[i]
			
			if m[i][k] == '':
				continue
			#print dictio.get(int(m[i][k].split(":")[0])) + str(m[i][k].split(":")[0])
			#print wn.synsets(dictio.get(int(m[i][k].split(":")[0])).split("_")[0], penn_to_wn(dictio.get(int(m[i][k].split(":")[0])).split("_")[1]))
			#caso nao existam synsets para aquela palavra
			if len(wn.synsets(dictio.get(int(m[i][k].split(":")[0])).split("_")[0], penn_to_wn(dictio.get(int(m[i][k].split(":")[0])).split("_")[1]))) == 0:
				nana += m[i][k]+":1[" +str(count)+":"+str(1)+"] "
				synsets[imag] = count
				extra_synsets[imag] = dictio.get(int(m[i][k].split(":")[0]))
				#g.write(m[i][k]+":1[" +str(imag)+":"+str(1)+"] ")
				imag -= 1
				count += 1
				continue
			sent = sentences[i]
			ambiguous = dictio.get(int(m[i][k].split(":")[0])).split("_")[0]
			post = dictio.get(int(m[i][k].split(":")[0])).split("_")[1]
			try:
				answer = adapted_lesk(sent, ambiguous, pos= penn_to_wn(post), nbest=True)
			except Exception, e:
				#caso o lesk se arme em estupido

				s = wn.synsets(dictio.get(int(m[i][k].split(":")[0])).split("_")[0], penn_to_wn(dictio.get(int(m[i][k].split(":")[0])).split("_")[1]))
				if len(s) != 0:
					count2 = 0
					#ver quantos synsets existem no semcor
					#for n in range(len(s)):
					#	if dic_g.has_key(str(s[n].offset)):
					#		words = dic_g.get(str(s[n].offset))
					#		for j in range(len(words)):
					#			if words[j].split(":")[0] == m[i][k].split(":")[0]:
					#				count2 += 1
					# se nao existir nenhum criar synset imaginario
					#if count2 == 0:
					#	nana += m[i][k]+":1[" +str(count)+":"+str(1)+"] "
					#	synsets[imag] = count
					#	extra_synsets[imag] = dictio.get(int(m[i][k].split(":")[0]))
						#g.write(m[i][k]+":1[" +str(imag)+":"+str(1)+"] ")
					#	count += 1
					#	imag -= 1
					#	continue
					#caso existam ir buscar as suas probabilidades ao semcor
					nana += m[i][k] +':'+ str(len(s)) + '['
					c = 1
					prob = 1.0/len(s)
					for n in range(len(s)):
						#print answer[n][1].offset
						#print 'Coco ' + str(s[n].offset)
						#if dic_g.has_key(str(s[n].offset)):
						#words = dic_g.get(str(s[n].offset))
						#for j in range(len(words)):
						#	if words[j].split(":")[0] == m[i][k].split(":")[0]:
						#		aux = 0
						a = (s[n].offset())
								#print s[n].offset()
						if synsets.has_key(a):
							aux = synsets.get(a)
						else:
							synsets[a] = count
							aux = count
							count += 1
						if n == len(s) - 1:
							nana += str(aux) + ':' + str(prob) + '] '
						else:
							nana += str(aux) + ':' + str(prob) + ' '
				else:
					nana += m[i][k]+":1[" +str(count)+":"+str(1)+"] "
					synsets[imag] = count
					extra_synsets[imag] = dictio.get(int(m[i][k].split(":")[0]))
					#g.write(m[i][k]+":1[" +str(imag)+":"+str(1)+"] ")
					count += 1
					imag -= 1
				continue
			
			
			#g.write(m[i][k] +':'+ str(len(answer)) + '[')
			total = 0

			for j in range(len(answer)):
				total += answer[j][0]
			#caso lesk nao devolva nenhuma resposta criar synset imaginario
			if len(answer) == 0:
				nana += m[i][k]+":1[" +str(count)+":"+str(1)+"] "
				synsets[imag] = count
				extra_synsets[imag] = dictio.get(int(m[i][k].split(":")[0]))
				#g.write(m[i][k]+":1[" +str(imag)+":"+str(1)+"] ")
				count += 1
				imag -= 1
				continue

			#print ambiguous
			#print total
			#print answer
			#caso nenhum dos synsets tenha overlap ir ver ao semcor as suas probabilidades
			if total == 0:
				#print 'ZERO'
				count2 = 0
				#for n in range(len(answer)):
				#	if dic_g.has_key(str(answer[n][1].offset)):
				#		words = dic_g.get(str(answer[n][1].offset))
				#		for j in range(len(words)):
				#			if words[j].split(":")[0] == m[i][k].split(":")[0]:
				#				count2 += 1
				#if count2 == 0:
				#	nana += m[i][k]+":1[" +str(count)+":"+str(1)+"] "
				#	synsets[imag] = count
				#	extra_synsets[imag] = dictio.get(int(m[i][k].split(":")[0]))
					#g.write(m[i][k]+":1[" +str(imag)+":"+str(1)+"] ")
				#	count += 1
				#	imag -= 1
				#	continue
				s = wn.synsets(dictio.get(int(m[i][k].split(":")[0])).split("_")[0], penn_to_wn(dictio.get(int(m[i][k].split(":")[0])).split("_")[1]))
				nana += m[i][k] +':'+ str(len(s)) + '['
				c = 1
				prob = 1.0/len(s)
				for n in range(len(s)):
					#print answer[n][1].offset
					#print 'Coco ' + str(s[n].offset)
					#if dic_g.has_key(str(s[n].offset)):
					#words = dic_g.get(str(s[n].offset))
					#for j in range(len(words)):
					#	if words[j].split(":")[0] == m[i][k].split(":")[0]:
					#		aux = 0
					a = (s[n].offset())
							#print s[n].offset()
					if synsets.has_key(a):
						aux = synsets.get(a)
					else:
						synsets[a] = count
						aux = count
						count += 1
					if n == len(s) - 1:
						nana += str(aux) + ':' + str(prob) + '] '
					else:
						nana += str(aux) + ':' + str(prob) + ' '

				#print nana
				continue
			#contar quantos synsets e que nao estao a zero
			count2 = 0
			for j in range(len(answer)):
				if answer[j][0] == 0:
					continue
				else:
					count2 += 1
			c = 1
			nana += m[i][k] +':'+ str(count2) + '['
			for j in range(len(answer)):
				#words_synsets = words_probs.get(int(m[i][k].split(':')[0]))
				#s.write(answer[j][1].offset+"\n")
				if answer[j][0] == 0:
					continue
				aux = 0
				a = (answer[j][1].offset())
				#print 'Coco '+ str(answer[j][1].offset())
				if synsets.has_key(a):
					aux = synsets.get(a)
				else:
					synsets[a] = count
					aux = count
					count += 1
				prob_s = 0.0
				prob_w = 0.0
				prob_s_w = float(answer[j][0])/total
				
				#if synset_count.has_key(str(answer[j][1].offset)):
				#	prob_s = synset_count.get(str(answer[j][1].offset))/float(sum_synset)
				#else:
				#	prob_s = 0.1
				prob_s_s = 1.0/count2

				#if word_count.has_key(dictio.get(int(m[i][k].split(":")[0]))):
				#	prob_w = word_count.get(dictio.get(int(m[i][k].split(":")[0])))/float(sum_word)
				#else:
				#	prob_w = 0.1

				if word_count_corpus.has_key(dictio.get(int(m[i][k].split(":")[0])).split("_")[0]):
					prob_w = word_count_corpus.get(dictio.get(int(m[i][k].split(":")[0])).split("_")[0])/float(sum_word_corpus)
				else:
					prob_w = 0.1
				prob_w_s = (prob_w * prob_s_w) / prob_s_s 

				if j == len(answer) - 1 or count2 == c:
					if prob_w_s > 1.0:
						#print 'Word: 'dictio.get(int(m[i][k].split(":")[0])) + ' Synset: ' + str(answer[j][1])
						p.write('Word: '+ dictio.get(int(m[i][k].split(":")[0])) + ' Synset: ' + str(answer[j][1]))
						#print 'Synsets disambiguated: ' + str(answer)
						p.write('---- Synsets disambiguated: ' + str(answer))
						#print synset_count.get(str(answer[j][1].offset)), word_count.get(dictio.get(int(m[i][k].split(":")[0]))), sum_synset, sum_word
						#print 'P(s)=' +prob_s +', P(w)='+prob_w  +', P(s|w)='+ prob_s_w  +', P(w|s)='+ prob_w_s
						p.write('---- P(s)=' +str(prob_s) +', P(w)='+ str(prob_w)  +', P(s|w)='+ str(prob_s_w)  +', P(w|s)='+ str(prob_w_s))
						p.write("\n")
						nana += str(aux) + ':' + str(1) + '] '
					#nana += str(aux) + ':' + str(words_synsets.get(answer[j][1].offset)) + '] '
					else:
						nana += str(aux) + ':' + str(prob_w_s) + '] '
					#g.write(str(aux) + ':' + str(float(answer[j][0]/total)) + '] ')
				else:
					c += 1 
					if prob_w_s > 1.0:
						#print 'Word: 'dictio.get(int(m[i][k].split(":")[0])) + ' Synset: ' + str(answer[j][1])
						p.write('Word: '+ dictio.get(int(m[i][k].split(":")[0])) + ' Synset: ' + str(answer[j][1]))
						#print 'Synsets disambiguated: ' + str(answer)
						p.write('---- Synsets disambiguated: ' + str(answer))
						#print synset_count.get(str(answer[j][1].offset)), word_count.get(dictio.get(int(m[i][k].split(":")[0]))), sum_synset, sum_word
						#print 'P(s)=' +prob_s +', P(w)='+prob_w  +', P(s|w)='+ prob_s_w  +', P(w|s)='+ prob_w_s
						p.write('---- P(s)=' +str(prob_s) +', P(w)='+ str(prob_w)  +', P(s|w)='+ str(prob_s_w)  +', P(w|s)='+ str(prob_w_s))
						p.write("\n")
						nana += str(aux) + ':' + str(1) + '] '
					#nana += str(aux) + ':' + str(words_synsets.get(answer[j][1].offset)) +' '
					else:
						nana += str(aux) + ':' + str(prob_w_s) +' '
					#g.write(str(aux) + ':' + str(float(answer[j][0]/total)) +' ')
		nana += '\n'
		#print nana
		#return
		to_write.append(nana)
		#g.write("\n")

	ne = revert_dicio(synsets)
	for i in range(len(ne)):
		#print ne.get(i), type(ne.get(i))
		nn.write(str(ne.get(i))+'\n')

	g.write(str(len(ne))+"\n")
	for i in range(len(to_write)):
		g.write(to_write[i])
	nn.close()
	p.close()
	g.close()
	end = time.time()
	pickle.dump(extra_synsets, open(string + file_name +"_imag.p","w"))
	print end - start

def calculate_word_frequency(corpus):
	word_count_dict = {}
	for i in range(len(corpus)):
		for j in range(len(corpus[i])):
			if word_count_dict.has_key(corpus[i][j]):
				aux = word_count_dict.get(corpus[i][j])
				word_count_dict[corpus[i][j]] = aux + 1
			else:
				word_count_dict[corpus[i][j]] = 1
	return word_count_dict

#bayes_theorem(sentences[i], dictio, synset_count, word_count, sum_synset, sum_word, synset_median, word_median)
def bayes_theorem(context, vocab, word_count, sum_word, word_median):
	words_probs = {}
	print len(vocab)
	count = 0
	for word in vocab:
		if count%1000 == 0:
			print 'word ' + str(count)
		count += 1
		sent = context

		ambiguous = vocab.get(word).split("_")[0]
		post = vocab.get(word).split("_")[1]
		#print ambiguous, post
		try:
			answer = adapted_lesk(sent, ambiguous, pos= penn_to_wn(post), nbest=True)
		except Exception, e:
			continue
		total = 0
		for j in range(len(answer)):
			total += answer[j][0]		
		
		if total == 0:
			continue

		for j in range(len(answer)):
			if answer[j][0] == 0:
				continue
			prob_w = 0.0
			prob_s_w = float(answer[j][0])/total
			
			if word_count.has_key(vocab.get(word)):
				prob_w = word_count.get(vocab.get(word))/float(sum_word)
			else:
				prob_w = word_median

			prob_w_s = prob_s_w * prob_w

			if words_probs.has_key(word):
				aux = words_probs.get(word)
				aux[int(answer[j][1].offset)] = prob_w_s
				words_probs[word] = aux
			else:
				aux = {}
				aux[int(answer[j][1].offset)] = prob_w_s
				words_probs[word] = aux
	#print words_probs


	synsets_probs = {}

	for word in words_probs:
		for synset in words_probs.get(word):
			if synsets_probs.has_key(synset):
				aux = synsets_probs.get(synset)
				aux[word] = words_probs.get(word).get(synset)
				synsets_probs[synset] = aux

			else:
				aux = {}
				aux[word] = words_probs.get(word).get(synset)
				synsets_probs[synset] = aux

	for synset in synsets_probs:
		sum_words = 0.0
		for word in synsets_probs.get(synset):
			sum_words += synsets_probs.get(synset).get(word)
		for word in synsets_probs.get(synset):
			aux = synsets_probs.get(synset).get(word)
			synsets_probs.get(synset)[word] = float(aux)/sum_words

	new_word_probs = {}
	for word in synsets_probs:
		for synset in synsets_probs.get(word):
			if new_word_probs.has_key(synset):
				aux = new_word_probs.get(synset)
				aux[word] = synsets_probs.get(word).get(synset)
				new_word_probs[synset] = aux
			else:
				aux = {}
				aux[word] = synsets_probs.get(word).get(synset)
				new_word_probs[synset] = aux

	return new_word_probs



def create_dicio(eta):
	dictio = {}

	for i in range(len(eta)-1):
		for j in range(2, len(eta[i])):
			if dictio.has_key(eta[i][0]):
				aux = dictio.get(eta[i][0])
				aux.append(eta[i][j])
				dictio[eta[i][0]] = aux
			else:
				aux = []
				aux.append(eta[i][j])
				dictio[eta[i][0]] = aux
	return dictio


def revert_dicio(words_ids):
	new_dictio = {}
	for key in words_ids:
		new_dictio[words_ids[key]] = key

	return new_dictio


def is_noun(tag):
    return tag in ['NN', 'NNS', 'NNP', 'NNPS']


def is_verb(tag):
    return tag in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']


def is_adverb(tag):
    return tag in ['RB', 'RBR', 'RBS']


def is_adjective(tag):
    return tag in ['JJ', 'JJR', 'JJS']


def penn_to_wn(tag):
    if is_adjective(tag):
        return wn.ADJ
    elif is_noun(tag):
        return wn.NOUN
    elif is_adverb(tag):
        return wn.ADV
    elif is_verb(tag):
        return wn.VERB
    return None
if __name__ == "__main__":
	main(sys.argv[1])
