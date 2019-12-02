# Author: Amogh Jalihal
# Date: 2019-12-02
# Description: TODO

import os
import sys
import yaml
import bibtexparser as bp
from optparse import OptionParser


def initialize_graph(bibpath, yamlpath):
    with open(bibpath, 'r') as bibfile:
        bib = bp.load(bibfile)

    bibkeydict = {e['ID']:[] for e in bib.entries}
    
    with open(yamlpath, 'w') as yamlfile:
        yaml.dump(bibkeydict, yamlfile)

def update_graph(bibpath, yamlpath):
    with open(bibpath, 'r') as bibfile:
        bib = bp.load(bibfile)

    bibkeyset = set([e['ID'] for e in bib.entries])
    with open(yamlpath, 'r') as yamlfile:
        citedict = yaml.safe_load(yamlfile)
        
    existingkeys = set(citedict.keys())
    newkeys = bibkeyset.difference(existingkeys)
    print(newkeys)
    citedict.update({nk:[] for nk in newkeys})
    
    with open(yamlpath, 'w') as yamlfile:
        yaml.dump(citedict, yamlfile)        

def add_edge(yamlpath, head, tail):
    """
    Add edge between HEAD and TAIL if HEAD
    in graph
    """
    with open(yamlpath, 'r') as yamlfile:
        citedict = yaml.safe_load(yamlfile)

    if head in citedict.keys():
        citedict[head].append(tail)
        with open(yamlpath, 'w') as yamlfile:
            yaml.dump(citedict, yamlfile)                
    else:
        print('key does not exist. please run --update first.')
        sys.exit()
    
def get_opts():
    parser = OptionParser()
    parser.add_option('-i','--initialize',
                      action='store_true',
                      default=False,
                      help="Create yaml file with entries in bib file. Required step.")
    parser.add_option('-u','--update',
                      action='store_true',
                      default=False,
                      help="update yaml file with new entries in bib file")    
    parser.add_option('-b','--bib-path',
                      type='str',
                      help="path to yaml file")    
    parser.add_option('-y','--yaml-path',
                      type='str',
                      help="path to yaml file")
    parser.add_option('-a','--add-edge',
                      action='store_true',
                      default=False,
                      help='Add edge between head and tail')
    parser.add_option('','--head',
                      type='str',
                      help="bib key of head. this is the paper that cites.")
    parser.add_option('','--tail',
                      type='str',
                      help="bib key of tail. this is the paper that is cited")
    opts, args = parser.parse_args()

    if opts.yaml_path is None:
        print('please specify yaml path!')
        sys.exit()
    else:
        if not os.path.exists(opts.yaml_path):
            print('yaml path is incorrect or doesnt exist. Please run --initialize first.')
            sys.exit()
    
    return opts, args
    
def main():
    opts, args = get_opts()
    if opts.initialize:
        initialize_graph(opts.bib_path, opts.yaml_path)

    if opts.update:
        update_graph(opts.bib_path, opts.yaml_path)

    if opts.add_edge:
        if opts.head is not None and opts.tail is not None:
            print(f"adding edge between {opts.head} and {opts.tail}")
            add_edge(opts.yaml_path, opts.head, opts.tail)
        else:
            print('head or tail misspecified')


if __name__ == '__main__':
    main()
