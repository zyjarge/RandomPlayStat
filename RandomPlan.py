# -*- coding:utf-8 -*-
__author__ = 'Jarge'
import ConfigParser
import random

fRates = {}
config_parser = {}

def init_config_parser():
    config_parser = ConfigParser.ConfigParser()
    config_parser.read('params.ini')


def init_hour_rates(hRates):
    rates = hRates.split(',')
    for i in range(0, len(rates)):
        fRates[i] = float(rates[i]) / 100


def random_by_rate(rate):
    base = 10000
    rvalue = random.randint(1, base)
    return rvalue < base * rate


def main():
    print "Main"


if __name__ == '__main__':
    main()
