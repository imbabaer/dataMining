lst = [1,2,3,4,5,6,7,8,9]
lst2 = [x**2 for x in lst]
print lst
print lst2

#fobj_in = open("D:\Dropbox\Dropbox\HdM\6.Semester\Data Mining und Mustererkennung\yellow_snow.txt","r")
#fobj_out = open("D:\Dropbox\Dropbox\HdM\6.Semester\Data Mining und Mustererkennung\yellow_snow2.txt","w")

#fileHandle = open ( 'D:\Dropbox\Dropbox\HdM\6.Semester\Data Mining und Mustererkennung\yellow_snow.txt', 'r' )
fobj_in = open("yellow_snow.txt")
fobj_out = open("yellow_snow2.txt","w")
i = 1
for line in fobj_in:
    print line.rstrip()
    fobj_out.write(str(i) + ": " + line)
    i = i + 1
fobj_in.close()
fobj_out.close()
'''
fin = open("yellow_snow.txt","r")
dateiinhalt = fin.read()
print "Typ:  ",type(dateiinhalt)
print "Inhalt:\n", dateiinhalt
fin.close()'''

import numpy as np
a1 = np.zeros( (3,4) )
print a1

a = np.array([1,2,3,4])
print a

x = np.array(range(24))
print x

a1 =a1.reshape((2,6))
print a1

a1.transpose()
print a1

b = np.arange(12).reshape(4,3)
print b

c = np.arange(12).reshape(4,3)
print c
print b*c
print "/////////////////////"
a = np.arange(15).reshape(3, 5)
print a
print a.shape
print a.ndim
print a.dtype.name
print a.itemsize

A =  np.matrix('1.0 2.0; 3.0 4.0')
print A

B =  np.matrix('5.0 7.0')
B= B.T
print B

print A*B
print np.dot(A,B)

a = np.arange(12).reshape(3,4)
print a
print a[2,3]

#print a[:1]

print a[:,0]

a = np.arange(10)
print a
a = np.sqrt(a)
print a

print np.matrix('1 2 3 4')