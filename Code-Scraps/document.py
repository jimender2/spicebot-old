#!/usr/bin/env python
# coding=utf-8
import os


def save():
    #write buffer to the file
    f.flush()
    os.fsync(f.fileno())



##############
##############
######ONE#####
##############
##############


def one():
    fileToRead = raw_input("What is the file name?")
    read = open(fileToRead, "r")
    line = read.readline()


##############
##############
#####MAIN#####
##############
##############
version = raw_input("What version do you want to run? (all or one?)")

if version == "one":
    one()
elif version == "all":
    all()
