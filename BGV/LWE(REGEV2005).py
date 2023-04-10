import numpy as np
import random
import math
import sys

def primesInRange(x, y):
    prime_list = []
    for n in range(x, y):
        isPrime = True
        for num in range(2, n):
            if n % num == 0:
                isPrime = False

        if isPrime:
            prime_list.append(n)

    return prime_list

def encode(plaintext):
    bin_arr = bytearray(plaintext, 'utf-8')
    res = []
    bin_str=''
    for bit in bin_arr:
        binary_rep = format(bit,'08b')
        #print(binary_rep)
        res.append(binary_rep)
    bin_str = bin_str.join(res)
    length = len(bin_str)

    return bin_str, length


def LWE_KeyGen(splambda, prime_list):
    global A
    global q
    #if splambda >=2:
    #    prime_list = primesInRange(splambda**2, 2*splambda**2)
    #else:
    #    prime_list = primesInRange(5, 10)
    #q = random.choice(prime_list)  #随机生成素数q
    #print("Prime Number = ", q)
    q = 297
    n = 320
    #n = random.randint(1, q)       #随机生成维度N
    m = 320
    #m = random.randint(50,150)#随机生成维度M
    A = np.random.randint(0,q,(m,n)) #生成公钥A
    s = np.random.randint(0,q,(n,1)) #生成私钥s
    b = np.dot(A,s)%q
    return A, b, s, q

def encrypt(plaintext, splambda, A, b, s):
    bin_str, length = encode(plaintext)
    m = len(A)
    samples = random.randint(1,15)
    #samples = 5
    bound = 2
    #bound = random.randint(1,math.floor(q/(8*samples)))
    print("B = ", bound)
    e = np.random.randint(-bound,bound,(m,1))
    #print(e)
    cipertext_u = []
    cipertext_v = []
    for i in range(0,length):
        u = [0]*len(A[0])
        v = 0
        #print(i,"=======",bin_str[i],"=====\n", )
        samples_Index = random.sample(range(0,m),samples)
        for j in samples_Index:
            u += A[j]
            v += b[j] + e[j]
            #print("Bj = ", b[j], "Errors = ", e[j], "cipertext: ", bin_str[i], "Vi = ", v_i,"============\n")

        #print(v)
        #print(u,v)
        #u = [u_i % q for u_i in u]

        #print("True V = ", true_v, "VE = ", v %q , "VEQ = ",  (v + int(bin_str[i])*math.floor(q/2))%q)
        #print(bin_str[i])
        v = (v + int(bin_str[i])*math.floor(q/2))%q
        #print("Real v = ", int(true_v%q))
        #print("encrypt v = ", v)
        #if v-true_v < math.ceil(q/2):
        #    print("Plaintext = ", 0)
        #else:
        #    print("Plaintext = ", 1)
        cipertext_u.append(u)
        cipertext_v.append(v)
    #print(len(cipertext))
    return cipertext_u,cipertext_v


def decrypt(u,v,s,a):
    plainbinary = []
    #print(len(v))
    for i in range(0,len(u)):
        temp = (np.dot(u[i],s)-v[i])%q
        #print(np.dot(u[i],s))

        if temp <= math.floor(q/2):
            bit = 0
        else:
            bit = 1
        #print("prime = ", q, "bit = ", temp)
        plainbinary.append(bit)
    plainbinary = ''.join(str(e)for e in plainbinary)
    #print(plainbinary)
    return plainbinary

def CheckTrue(plaintext):
    splambda = 10
    prime_list = primesInRange(splambda**2, 2*(splambda**2))
    A, b, s, q = LWE_KeyGen(splambda,prime_list)
    u, v = encrypt(plaintext, 10, A,b,s)
    a, length = encode(plaintext)
    plainbinary = decrypt(u,v,s,a)
    print(a)
    print(plainbinary)
    res1 = (a ==plainbinary)
    return res1

def main():
    count = 0
    times = 10000
    for i in range(0,times):
        testlength = random.randint(3,10)
        teststr = ''
        #teststr = '2k23niujiao'
        teststr = teststr.join(random.sample(['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a'], testlength))
        print("======Test Number ", i, "======")
        print("Test String:   ", teststr)
        res = CheckTrue(teststr)
        print("Result: ", res)
        if res:
            count +=1
    acc = count/times * 100
    print("=====================Accuracy===================")
    print(count/100,"%")

if __name__ == '__main__':
    sys.exit(main())