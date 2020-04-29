#!/usr/bin/env python3

import json
import glob
import argparse

def generate_dependency_name(finding):
    name_string = ""
    for n in finding['trigger']['componentFacts'][0]['displayName']['parts']:
        if ':' not in n['value']:
            if name_string != "":
                name_string = name_string + ":" + n['value']
            else:
                name_string = n['value']
    return name_string

parser = argparse.ArgumentParser(description='Map IQ Findings to Gradle Dependencies')
parser.add_argument('-r', '--results-file', nargs=1, dest='results_file', action='store', help='IQ JSON Results File')
parser.add_argument('-d', '--debug', dest='debug', action='store_true', help='Print Debug Information')
args = parser.parse_args()
debug = args.debug

with open( args.results_file[0], 'r') as f:
    res=f.read()

jres = json.loads(res)

if debug:
    print("Found {} total findings with status of {}".format(
        len(jres['policyEvaluationResult']['alerts']),
        jres['policyAction']))

# collect the failures
fails = []
for i in jres['policyEvaluationResult']['alerts']:
    if 'fail' in i['actions'][0]['actionTypeId']:
        fails.append(i)

if debug:
    print("Found {} packages in violation".format(
        len(fails)))

if debug:
    print("\nDependencies in violation:")
    for f in fails:
        print(generate_dependency_name(f))
    print()

# get list of build.gradle files for the project
gradle_files = glob.glob("./**/*.gradle")
depends = {}

if debug:
    print("Found {} build.gradle files".format(len(gradle_files)))
    print("\nFound build files")
    for g in gradle_files:
        print(g)
    print()

# for each gradle file, grab the compile lines
for f in gradle_files:
    if debug:
        print("Scanning {} for dependencies".format(f))
    with open(f, 'r') as gf:
        lines = gf.readlines()
        for text in lines:
            if 'compile(' in text:
                text = text.strip()
                try:
                    text = text.split("\"")[1]
                except:
                    text = text.split("\'")[1]
                depends[text] = f

if debug:
    print("\nFound {} direct dependencies in project\n".format(
        len(depends)))
    
name_strings = []
for f in fails:
    name_strings.append(generate_dependency_name(f))

direct_dependencies = []
for n in name_strings:
    try:
        f = depends[n]
        dependency = { "dependency": n, "filepath": f}
        direct_dependencies.append(dependency)
    except:
        pass

for d in direct_dependencies:
    print("Direct Dependency: {} in {}".format(
        d['dependency'], d['filepath']
    ))
