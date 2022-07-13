import pymongo
from math import floor, ceil
import itertools


def Livdistance(a, b):
    "Calculates the Levenshtein distance between a and b."
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n, m)) space
        a, b = b, a
        n, m = m, n

    current_row = range(n + 1)  # Keep current and previous row, not entire matrix
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if a[j - 1] != b[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]

# Function to calculate the
# Jaro Similarity of two s
def jaro_distance(s1, s2):
	
	# If the s are equal
	if (s1 == s2):
		return 1.0

	# Length of two s
	len1 = len(s1)
	len2 = len(s2)

	# Maximum distance upto which matching
	# is allowed
	max_dist = floor(max(len1, len2) / 2) - 1

	# Count of matches
	match = 0

	# Hash for matches
	hash_s1 = [0] * len(s1)
	hash_s2 = [0] * len(s2)

	# Traverse through the first
	for i in range(len1):

		# Check if there is any matches
		for j in range(max(0, i - max_dist),
					min(len2, i + max_dist + 1)):
			
			# If there is a match
			if (s1[i] == s2[j] and hash_s2[j] == 0):
				hash_s1[i] = 1
				hash_s2[j] = 1
				match += 1
				break

	# If there is no match
	if (match == 0):
		return 0.0

	# Number of transpositions
	t = 0
	point = 0

	# Count number of occurrences/////////////
	# where two characters match but
	# there is a third matched character
	# in between the indices
	for i in range(len1):
		if (hash_s1[i]):

			# Find the next matched character
			# in second
			while (hash_s2[point] == 0):
				point += 1

			if (s1[i] != s2[point]):
				t += 1
			point += 1
	t = t//2

	# Return the Jaro Similarity
	return (match/ len1 + match / len2 +
			(match - t) / match)/ 3.0


def DAS_sim(s1,s2):#s1>=s2
	if(len(s1)<len(s2)):
		s3=s1
		s1=s2
		s2=s3
	sim=0
	simr=0
	k=0
	w=1/len(s1)
	for i in range(len(s2)):
		if(s2[i]==s1[i]):
			k=1
		elif((len(s2)!=len(s1)) and (s2[i]==s1[i+1])):
			k=0.8
		elif((len(s2)!=len(s1)) and (i!=len(s2)-1)):
			k=0.8
		if(i==len(s2)-1):
			if(len(s2)!=len(s1)):
				if(s2[i]==s1[i+1]):
					k=0.8
			else:
				if(s2[i]==s1[i]):
					k=1
	sim+=w*k
	k=0

	s3 = s1[::-1]
	s4 = s2[::-1]

	for i in range(len(s4)):
		if(s4[i]==s3[i]):
			k=1
		elif((len(s4)!=len(s3)) and (s4[i]==s3[i+1])):
			k=0.8
		elif((len(s4)!=len(s3)) and (i!=len(s4)-1)):
			k=0.8
		if(i==len(s4)-1):
			if(len(s4)!=len(s3)):
				if(s4[i]==s3[i+1]):
					k=0.8
			else:
				if(s4[i]==s3[i]):
					k=1
		simr+=w*k
		k=0
	res=max(sim,simr)
	return resприговор#Мой алгоритм, работает плохо.


def FillDictObj(Objdict):#Заполнение Словаря объектов из файла.
	key = ""
	value = ""
	file = open("datatxt.txt",encoding="utf8")
	lines = file.readlines()
	i=1
	for line in lines:
		line=line.replace("\n", "")
		if(i%2==0):
			key = line
			Objdict[key] = value
		else:
			value = line
		i=i+1
	return Objdict

def FillDictNum(Somedict):#Заполнение Словаря числительных из файла.
	key=""
	value=""
	i=1
	file = open("DictionaryNumerals.txt", encoding="utf8")
	lines = file.readlines()
	for line in lines:
		line=line.replace("\n", "")
		if(i%2==0):
			key = line
			Somedict[key]=value
		else:
			value = line
		i=i+1
	return 	Somedict#Заполнение словаря Числительных

def all_the_same(lst):
	if len(lst)<1:
		return True
	return len(lst) == lst.count(lst[0])

def PreAnalysis(s1,s2):#Выпиливание лишнего текста, приводим к нормальной форме.
	s1=s1.replace('ё','е')
	s2=s2.replace('ё','е')
	s1=s1.replace('(',' ')# Important or not? Московское шоссе (п Прикольный)/ Московское шоссе 
	s1=s1.replace(')',' ')# ("-") Но только после редакц
	s2=s2.replace('(',' ')#
	s2=s2.replace(')',' ')#
	s1=s1.lower()
	s2=s2.lower()	

	lst1 = s1.split()#Разбиваем строки на массивы слов
	lst2 = s2.split()

	s1=' '.join(lst1)#удаление повторяющихся пробелов
	s2=' '.join(lst2)#

	keyObjs1 = ( set(lst1) & set(Objdict.keys()))#Ищем пересечение множества объектов в алфавите объектов и в наших словах and set(Objdict.values()) & set(lst1)
	keyObjs2 = ( set(lst2) & set(Objdict.keys()))#& set(Objdict.values()) Обдумываение нужды.
	keyNum1 = (set(lst1) & set(Numdict.keys()))#
	keyNum2 = (set(lst2) & set(Numdict.keys()))

	StrNums1=""
	StrNums2=""

	for i in keyNum1:
		StrNums1 = StrNums1 + i + " "
			
	for i in keyNum2:
		StrNums2 = StrNums2 + i + " "

	StrNums1=StrNums1.split()
	StrNums2=StrNums2.split()
			
	N1=0
	if (len(keyNum1)!= 0):#Перевод числа из листа слов в цифры по словарю
		for i in StrNums1:
			N1=N1+int(Numdict[i])
			s1=s1.replace(i,'')
			s1=s1.strip()
	if (N1!=0):
		s1=s1 + " " + str(N1)
	
	N2=0
	if (len(keyNum2)!= 0):
		for i in StrNums2:
			N2=N2+int(Numdict[i])
			s2=s2.replace(i,'')
			s2=s2.strip()
	if (N2!=0):
		s2=s2 + " " + str(N2)

	Preres="Unknown"
	if((N1!=N2) and ((any(map(str.isdigit,s1))) and (any(map(str.isdigit,s2)))) and (len(keyNum1)!=len(keyNum2))):#Если числительные не равны то разные улицы
		Preres=str(0)

	addition1=""#Часть 1 предложения отвечающая за тип объекта
	addition2=""
	for i in keyObjs1:
		addition1 = addition1 + " " + i
		
	for i in keyObjs2:
		addition2 = addition2 + " " + i

	AdditionList1 = addition1.split()
	AdditionList2 = addition2.split()
			
	lst1 = s1.split()#Разбиваем строки на массивы слов
	lst2 = s2.split()

	if((len(keyObjs1)==0) or (len(keyObjs2)==0)):
		#Если у одного из слов тип объекта неизвестен
		if ((len(keyObjs1) == 0) and (len(keyObjs2)==0)):#Если у обоих слов тип объекта неизвестен
			typeOfObj = "Неизвестно"
		elif(len(keyObjs1)==0):#Если у первого слова тип объекта неизвестен
			k=""
			lsttemp=s2.split()
			typeOfObj=""			
			for i in AdditionList2:
				k=k+Objdict[i]
				for j in lsttemp:
					if(j==i):
						lsttemp.remove(j)
				s2=' '.join(lsttemp)
				typeOfObj = "Неточный " + k
		elif(len(keyObjs2)==0):#Если у второго слова тип объекта неизвестен
			k=""
			lsttemp=s1.split()
			typeOfObj=""	
			for i in AdditionList1:
				k=k+Objdict[i]
				for j in lsttemp:
					if(j==i):
						lsttemp.remove(j)
				s1=' '.join(lsttemp)
				s1=s1.replace(i,'')#Удаляем из наших слов типы объектов
				typeOfObj = 'Неточный ' + k
	else:#Если у обоих слов тип объекта известен
		k=""
		lsttemp=s1.split()
		typeOfObj=""
		for i in AdditionList1:
			k=k+Objdict[i]
			for j in lsttemp:
				if(j==i):
					lsttemp.remove(j)
			s1=' '.join(lsttemp)
			s1=s1.strip()
		k=""
		lsttemp=s2.split()
		for i in AdditionList2:
			k=k+Objdict[i]
			for j in lsttemp:
				if(j==i):
					lsttemp.remove(j)
			s2=' '.join(lsttemp)
			s2=s2.strip()
			for i in AdditionList1:
				for k in AdditionList2:
					if(Objdict[i]==Objdict[k]):
						typeOfObj = typeOfObj + " " + Objdict[i]
	lst1=s1.split()
	lst2=s2.split()

	lst3=[]
	for i in lst1:#Увеличение границы верных значений
		if((i[-2:]=='ая') or (i[-2:]=='ой') or (i[-2:]=='ое') or (i[-2:]=='ый') or (i[-2:]=='ий') or (i[-2:]=='яя')):
			i=i[:-2]
			lst3.append(i)
		elif((i[-3:]=='ого')):
			i=i[:-3]
			lst3.append(i)
		elif(((i[-2:]=='ая') or (i[-2:]=='ой') or (i[-2:]=='ое') or (i[-2:]=='ый') or (i[-2:]=='ого')  or (i[-2:]=='ий') or (i[-2:]=='яя') ) == False):
			lst3.append(i)
	lst4=[]
	for i in lst2:#Увеличение границы верных значений
		if((i[-2:]=='ая') or (i[-2:]=='ой') or (i[-2:]=='ое') or (i[-2:]=='ый') or (i[-2:]=='ий') or (i[-2:]=='яя')):
			i=i[:-2]
			lst4.append(i)
		elif((i[-3:]=='ого')):
			i=i[:-3]
			lst4.append(i)
		elif(((i[-2:]=='ая') or (i[-2:]=='ой') or (i[-2:]=='ое') or (i[-2:]=='ый') or (i[-2:]=='ого') or (i[-2:]=='ий') or (i[-2:]=='яя') ) == False):
			lst4.append(i)

	
	return [lst3,lst4,typeOfObj,Preres]

#насколько похожи предложения. разбиваем на слова
Objdict = {}#Словарь для проверки на тип объекта(Улица, проспект и т.д.). Think something about try / catch and auto adding words in dictionary file. However.... 
Numdict = {}#Словарь для проверки числительных. Should i add search in values too (Objdict)?
#Закрыть файл после чтения.
FillDictObj(Objdict)
FillDictNum(Numdict)

#подключение к Mongodb
db_client = pymongo.MongoClient("mongodb://localhost:27017/")
current_db = db_client["local"]
collection0 = current_db["mar_houses"]
collection1 = current_db["2gis_houses"]
collection2 = current_db["fias_houses"]
collection3 = current_db["ingeo_houses"]
collection4 = current_db["osm_houses"]
collection5 = current_db["uiks_houses"]

s1 = ""#Наши строчки для сравнения
s2 = ""#

counterPlus=0
counterMinus=0
counterEmpty = 0
for channel in collection0.find():
	s1 = channel['Street']
	fiasId = channel['fiasID']
	if (fiasId == None):
		noneid = channel['_id']
		print(noneid,"Нету фиас id в mar_houses")
		counterEmpty+=1
	else:
		channel2 = collection2.find_one({'ID':fiasId})
		if (channel2 == None):
			print("В fias_houses нету такого ID:",fiasId )
			counterEmpty+=1
		else:
			print(s1)
			s2 = channel2['Street']
			print(s2)
			res=0;
			typtypeOfObjRes=""

			#lst = PreAnalysis('Улица Ульяновская','ул Ульяновская')

			if(s1!=s2):
				lst=PreAnalysis(s1,s2)
				lst1=lst[0]
				lst2=lst[1]
				typtypeOfObjRes=lst[2]
				Preres=lst[3]
				if((len(typtypeOfObjRes)==0) or (Preres==str(0))):#Если цифры не совпадают, то бан.
					res=0
				else:
					for i in itertools.permutations(lst1):
						s1 = " ".join(i)
						s1=s1.replace("-","")#Обработка тире
						for j in itertools.permutations(lst2):
							s2 = " ".join(j)
							s2=s2.replace("-","")#Обработка тире
							if(res<round(jaro_distance(s1, s2),6)):
								res=round(jaro_distance(s1, s2),6)
				if(res==0):
					counterMinus+=1
					print("hmm")
				else:
					counterPlus+=1
			else:
				res=1
			print("Jaro", res)
print("100%: ",counterPlus," 0%: ",counterMinus)
print("meme")