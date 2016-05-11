#!/usr/bin/python


class X:

	def __init__(self, a, b):
		self.a = a
		self.b = b
		
		a = a + 1
		b[1]=1000
		print a
		print b
		
		
		
		
i = 20
j = {1:10, 2:20, 3:30 }

print "- antes"
print i,j


print "- durante"
x = X(i,j)


print "- despues"
print i,j