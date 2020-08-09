import json
from sklearn.feature_extraction.text import TfidfVectorizer 
import re
import ftfy as ft
import time
import numpy as np
from scipy.sparse import csr_matrix
import sparse_dot_topn.sparse_dot_topn as ct
import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

t=open(r"C:\dev\personal\Web Scraping\projects\tesco\tesco_072720.json")
a=open(r"C:\dev\personal\Web Scraping\projects\asda\asda_072720.json")
s=open(r"C:\dev\personal\Web Scraping\projects\sainsburys\sainsburys_072720.json")
w=open(r"C:\dev\personal\Web Scraping\projects\waitrose\waitrose_072720.json")
m=open(r"C:\dev\personal\Web Scraping\projects\morrisons\morrisons_072720.json")

tesco_price=json.load(t)
# print(tesco_price)
ctr=1
tesco_prod_name=[]
for i in tesco_price:
    tesco_prod_name.insert(ctr,i['tesco_prod_name'])
    ctr+=1

#print(tesco_prod_name)
t.close()

asda_price=json.load(a)
# print(asda_price)
ctr=1
asda_prod_name=[]
for i in asda_price:
    asda_prod_name.insert(ctr,i['asda_prod_name'])
    ctr+=1

#print(asda_prod_name)
a.close()

morrisons_price=json.load(m)
# print(morrisons_price)
ctr=1
morrisons_prod_name=[]
for i in morrisons_price:
    morrisons_prod_name.insert(ctr,i['morrisons_prod_name'])
    ctr+=1

#print(morrisons_prod_name)
m.close()

waitrose_price=json.load(w)
# print(waitrose_price)
ctr=1
waitrose_prod_name=[]
for i in waitrose_price:
    waitrose_prod_name.insert(ctr,i['waitrose_prod_name'])
    ctr+=1

#print(waitrose_prod_name)
w.close()

sainsburys_price=json.load(s)
# print(sainsburys_price)
ctr=1
sainsburys_prod_name=[]
for i in sainsburys_price:
    sainsburys_prod_name.insert(ctr,i['sainsburys_prod_name'])
    ctr+=1

#print(sainsburys_prod_name)
s.close()

def uniq(list1):
    list_set=set(list1)
    unique_list=list(list_set)
    return unique_list

print("Shape of tesco pre deduping")
print(len(tesco_prod_name))
print("Shape of morrisons pre deduping")
print(len(morrisons_prod_name))

tesco_prod_name_uniq=uniq(tesco_prod_name)
asda_prod_name_uniq=uniq(asda_prod_name)
morrisons_prod_name_uniq=uniq(morrisons_prod_name)
sainsburys_prod_name_uniq=uniq(sainsburys_prod_name)
waitrose_prod_name_uniq=uniq(waitrose_prod_name)
print("Shape of tesco post deduping")
print(len(tesco_prod_name_uniq))
prim_vec_ount=len(tesco_prod_name_uniq)
print("Shape of morrisons post deduping")
print(len(morrisons_prod_name_uniq))
trg_vec_count=len(morrisons_prod_name_uniq)
test_vector=np.array(tesco_prod_name_uniq+morrisons_prod_name_uniq)
print("Shape of test_vector post deduping")
print(len(test_vector))

def ngrams(string, n=3):
    string = ft.fix_text(string) # fix text encoding issues
    string = string.encode("ascii", errors="ignore").decode() #remove non ascii chars
    string = string.lower() #make lower case
    chars_to_remove = [")","(",".","|","[","]","{","}","'"," "]
    rx = '[' + re.escape(''.join(chars_to_remove)) + ']'
    string = re.sub(rx, '', string) #remove the list of chars defined above
    string = string.replace('&', 'and')
    string = string.replace(',', ' ')
    string = string.replace('-', ' ')
    string = string.title() # normalise case - capital at start of each word
    string = re.sub(' +',' ',string).strip() # get rid of multiple spaces and replace with a single space
    # string = ' '+ string +' ' # pad names for ngrams...
    string = re.sub(r'[,-./]|\sBD',r'', string)
    ngrams = zip(*[string[i:] for i in range(n)])
    return [''.join(ngram) for ngram in ngrams]



vectorizer = TfidfVectorizer(min_df=1, analyzer=ngrams)
T = vectorizer.fit_transform(test_vector)
print("Shape of T")
print(T.shape)
# # A = vectorizer.fit_transform(asda_prod_name_uniq)

# # print("Printing T...")
# # print(T[0])
# # print(tesco_prod_name_uniq[0])
# # print(ngrams(asda_prod_name_uniq[0]))
# # print("Printing A")
# # print(A[0])
# # ngrams(asda_prod_name_uniq[0])

# """ Description
# ntop--> n top results
# A and B: 2 CSR matrix
# lower bound  """


def awesome_cossim_top(A, B, ntop, lower_bound=0):
    # force A and B as a CSR matrix.
    # If they have already been CSR, there is no overhead
    A = A.tocsr()
    B = B.tocsr()
    M, _ = A.shape
    _, N = B.shape
 
    idx_dtype = np.int32
 
    nnz_max = M*ntop
 
    indptr = np.zeros(M+1, dtype=idx_dtype)
    indices = np.zeros(nnz_max, dtype=idx_dtype)
    data = np.zeros(nnz_max, dtype=A.dtype)

    ct.sparse_dot_topn(
        M, N, np.asarray(A.indptr, dtype=idx_dtype),
        np.asarray(A.indices, dtype=idx_dtype),
        A.data,
        np.asarray(B.indptr, dtype=idx_dtype),
        np.asarray(B.indices, dtype=idx_dtype),
        B.data,
        ntop,
        lower_bound,
        indptr, indices, data)
    return csr_matrix((data,indices,indptr),shape=(M,N))

t1 = time.time()
matches = awesome_cossim_top(T, T.transpose(), 5, 0.5)
t = time.time()-t1
print("SELFTIMED:", t)
print("Shape of matches")
print(matches.shape)

def get_matches_df(sparse_matrix, name_vector, top=453):
    non_zeros = sparse_matrix.nonzero()
    
    sparserows = non_zeros[0]
    sparsecols = non_zeros[1]
    
    if top:
        nr_matches = top
    else:
        nr_matches = sparsecols.size
    
    left_side = np.empty([nr_matches], dtype=object) # returns a matrix of given shape
    right_side = np.empty([nr_matches], dtype=object) # returns a matrix of given shape
    similairity = np.zeros(nr_matches) # returns a matrix of given shape with zeros
    i=0
    for index in range(0, nr_matches):
        if (sparserows[index]!=sparsecols[index]):
            left_side[i] = name_vector[sparserows[index]]
            right_side[i] = name_vector[sparsecols[index]]
            similairity[i] = sparse_matrix.data[index]
            i=i+1

    
    return pd.DataFrame({'left_side': left_side,
                          'right_side': right_side,
                           'similairity': similairity})

matches_df = get_matches_df(matches, test_vector)
print(matches_df.shape)
matches_df=matches_df[matches_df['similairity'] < 1]

# print(matches_df.sample(100))

print(matches_df.sort_values(['similairity'], ascending=False).head(453))