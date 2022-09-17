# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 20:48:53 2019

@author: user
"""
#==============================================================
#                    Importation of library
#==============================================================
import itertools as ite
import math as mt
import numpy as np
import pickle as pk
import copy as cp

class Information_set_Decoding:
    def __init__(self, n=0, n1=0, n2=0, w1=0,w2=0):
        self.k, self.n=n//2, n
        self.H=np.zeros((self.k, n-self.k), dtype='int')
        self.word=[]
        self.t=w1+w2
        self.n1, self.n2, self.w1, self.w2=n1, n2, w1, w2
        self.syndrome=[]
    def Syndrome(self):
        sfile='Syndrome'+str(self.n)+'.txt'
        s=open(sfile, 'r')
        self.syndrome=list(map(int, list(s.readline())))
        s.close()
#============================================================
# We try to save the generator matrix of the dual code and
# the syndrome in a binary file.
# This allows us to improve our algorithm because we use
# directly the binary saved matrix and syndrome
#============================================================
    def Matrice(self):
        mfile='Matrix'+str(self.n)+'.txt'
        m=open(mfile, 'r')
        M=np.zeros((self.k, self.n-self.k), dtype='int')
        for i in range(self.k):
            x=list(m.readline())
            l=list(map(int,x[0:self.n-self.k]))
            M[i]=cp.copy(l)
        self.H=np.concatenate((np.eye(self.n-self.k, dtype='int'), np.transpose(M)), axis=1)
    def __binary_file__(self):    
        mfile= 'Matrix'+str(self.n)   
        m=open(mfile, 'wb')
        mm=pk.Pickler(m)
        mm.dump(self.H)
        m.close()
        sfile='Syndrome'+str(self.n)
        s=open(sfile, 'wb')
        ss=pk.Pickler(s)
        ss.dump(self.syndrome)
        s.close()
    def ISD_F_and_S_algo1(self):
#===========================================================
# We load the binary Matrix of the dual code and the
# syndrome from the binary file
#===========================================================
        sfile='Syndrome'+str(self.n)
        mfile= 'Matrix'+str(self.n) 
        m=open(mfile, 'rb')
        mm=pk.Unpickler(m)
        self.H=mm.load()
        m.close()
        s=open(sfile, 'rb')
        ss=pk.Unpickler(s)
        self.syndrome=np.array(ss.load())
        s.close()
        test=''
#===========================================================
# We compute some supplementary parameters of F_and_S ISD
# 
#===========================================================
        H1=cp.copy(self.H[:,:self.n1])
        H2=cp.copy(self.H[:,self.n1:])
        S1=dict([])
        print("Okay nous y sommes")
        
        for j in ite.combinations(range(self.n1), self.w1):
            e1=np.array([0 for i in range(self.n1)])
            e11=[0 for i in range(self.n1)]
            for i in range(self.w1):
                e1 ^=H1[:, j[i]]
                e11[i]=1
            tmp=''.join(map(str, list(e1)))
            if tmp in S1:
                S1[tmp].append(e11)
            else:
                S1[tmp]=[]
                S1[tmp].append(e11)
        e22=[0 for i in range(self.n1)]
        print(S1)  
        print("Okay nous y sommes")
        for j in ite.combinations(range(self.n2), self.w2):
            e2=  cp.copy(self.syndrome)
            for i in range(self.w2):
                e2 ^=H2[:, j[i]]
            tmp=''.join(map(str, list(e2)))
            print(tmp)
            if tmp in S1:
                test='ok'
                for i in range(self.w2):
                    e22[j[i]]=1
                break
        if test=='ok':
            print("okay")
            b=S1[tmp][0]
            b.extend(e22)
            self.word=cp.copy(b)
            return 1
        else:
            return 0
    """def ISD_F_and_S_algo2(self):
        m1=open('W1_50', 'rb')
        mm1=pk.Unpickler(m1)
        S1=mm1.load()
        m1.close()
        s1=open('Syndrome100', 'rb')
        ss1=pk.Unpickler(s1)
        Synd=ss1.load()
        s1.close()
        w2=mt.ceil(self.weight/2)
        for j in ite.combinations(range(self.lenth), w2):
            for i in j:
                e[i]=1
            x=Synd^np.dot(e, H)
            y=''
            for i in range(self.dual_dim):
                y+=str(x[i])
            z=int(y, 2)
            if z in S1.keys():
                re=np.array(S1[z])^np.array(e)
                break
        return re"""
a=Information_set_Decoding(460, 230, 230, 12, 12)
a.Syndrome()
a.Matrice()
a.__binary_file__()
a.ISD_F_and_S_algo1()
print(a.word)
print(a.syndrome)
print(a.H)



