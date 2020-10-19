# -*- coding:utf-8 -*-
# @author :adolf

def partition(L, left, right):
    pivot_key = L[left]

    while left < right:
        while left < right and L[right] >= pivot_key:
            right -= 1
        L[left] = L[right]