#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def load_variables(inifilename):
	inputfile = open(inifilename)
	return_dict = {}
	for line in inputfile:
		line = line.strip()
		if line == '': continue
		data = line.split('=')
		variable = data[0]
		value = data[1]

		return_dict[variable] = value
	return return_dict

