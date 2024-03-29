#!/usr/bin/env python

# Metpy Monday
# 60 - Scripting Part 1
# https://www.youtube.com/watch?v=PzKzlelmEkE

import time

print('Beginning of my Python script')
for i in range(10, 0, -1):
	print(f'Launch in {i}')
	time.sleep(1)
print('Blast-off!')
