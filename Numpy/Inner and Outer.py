'''
Task
You are given two arrays:
A and B
.
Your task is to compute their inner and outer product.
Input Format
The first line contains the space separated elements of array A
The second line contains the space separated elements of array A
.
Output Format
First, print the inner product.
Second, print the outer product.
'''
import numpy as np

A = np.array(input().strip().split(), int)
B = np.array(input().strip().split(), int)
print(np.inner(A, B), np.outer(A, B), sep = "\n")
