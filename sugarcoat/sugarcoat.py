#! /c/Python27/python
# -*- coding: utf-8 -*-
"""Sugarcoat

Usage:
  sugarcoat.py compile [<template>...]

Options:
  -h --help     Show this screen.
  -v --version  Show version.
"""

from bs4 import BeautifulSoup
from docopt import docopt


class Sugarcoat(object):
    def __init__(self, templates):
        self.templates = self.get_templates(templates)
        self.results = self.compile(self.templates)

    def get_templates(self, templates):
        html = []
        for template in templates:
            with open(template, 'r') as f:
                html.append(f.read())
        html = map(BeautifulSoup, html)
        return html

    def compile(self, soups):
        def make_child(child, soup):
            """
            Makes children tags based on parent tags.
            """
            parent_name = child['from']
            del child['from']
            parent_tag = soup.find_all('div',
                attrs={'name': parent_name})[0]
            child.name = parent_tag.name

            # Prepending parent tag contents
            # text = True, gets content of tag
            parent_content = parent_tag.find_all(True)[0]
            child_content = parent_tag.find_all(True)[0]
            child.clear()
            child.append(parent_content)
            child.append(child_content)

            # Replicating class, id, attrs
            tag_datas = ['id', 'class']
            for data in tag_datas:
                try:
                    child[data] = parent_tag.__dict__[data]
                except KeyError:
                    pass
            attrs = parent_tag.__dict__['attrs']
            for attr in attrs:
                child[attr] = attrs[attr]
            return soup

        for soup in soups:
            def try_get_from(element):
                try:
                    return element.has_attr('from')
                except:
                    return False
            children = filter(try_get_from,
                soup.__dict__['contents'])
            for child in children:
                soup = make_child(child, soup)
            print soup

        if len(soups) == 1:
            return soups[0]
        else:
            return soups


if __name__ == '__main__':
    args = docopt(__doc__, version='Sugarcoat 0.1')
    if args['compile']:
        Sugarcoat(args['<template>'])
