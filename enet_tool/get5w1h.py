from allennlp.predictors.predictor import Predictor
import re
import copy
predictor = Predictor.from_path("https://storage.googleapis.com/allennlp-public-models/bert-base-srl-2020.03.24.tar.gz")

def checkarg0(sen):
    try:
        comps = predictor.predict(sentence=sen)
    except:
        return False
    if comps['verbs'] == []:
        return False
    p = re.compile(r'\[(.*?)\]', re.S)
    comps = re.findall(p, comps['verbs'][0]['description'])
    for i in comps:
        if 'ARG0' in i:
            return True
    return False
def checkverb(sen):
    try:
        comps = predictor.predict(sentence=sen)
    except:
        return False
    if comps['verbs'] == []:
        return False
    p = re.compile(r'\[(.*?)\]', re.S)
    comps = re.findall(p, comps['verbs'][0]['description'])
    for i in comps:
        if 'V' in i:
            return True
    return False
def fill(tri):
    i = copy.deepcopy(tri)
    if checkarg0(i[2]):
        return
    if i[1] == 'xWant':
        if i[2].split(' ', 1)[0] == 'to':
            i[2] = 'PersonX want ' + i[2]
        else:
            i[2] = 'PersonX want to ' + i[2]
    elif i[1] == 'xNeed':
        if i[2].split(' ', 1)[0] == 'to':
            i[2] = 'PersonX need ' + i[2]
        else:
            i[2] = 'PersonX need to ' + i[2]
    elif i[1] == 'xIntent':
        if i[2].split(' ', 1)[0] == 'to':
            i[2] = 'PersonX intent ' + i[2]
        else:
            i[2] = 'PersonX intent to ' + i[2]
    elif i[1] == 'xAttr':
        if checkverb(i[2]):
            i[2] = 'PersonX ' + i[2]
        i[2] = 'PersonX is ' + i[2]
    elif i[1] == 'xEffect': 
        i[2] = 'PersonX ' + i[2]
    elif i[1] == 'xReact':
        i[2] = 'PersonX feel ' + i[2]
    elif i[1] == 'oWant':
        if i[2].split(' ', 1)[0] == 'to':
            i[2] = 'Others want ' + i[2]
        else:
            i[2] = 'Others want to ' + i[2]
    elif i[1] == 'oReact': 
        i[2] = 'Others feel ' + i[2]
    elif i[1] == 'oEffect': 
        i[2] = 'Others ' + i[2]
######################################################################
######################################################################
# The 5w1h does not contain all the references in ATOMIC, meeting such references
# We use else:5w1h in it
    else:
        i[2] = '5w1htest ' + i[2]
######################################################################
######################################################################
    return i


def srlto5w1h(i):
    comps = []
    p = re.compile(r'\[(.*?)\]', re.S)
    s = predictor.predict(sentence=i)
    one = ['','','','','','','','','False']
    if s['verbs'] == []:
        return one
    comps = re.findall(p, s['verbs'][0]['description'])
    output = []
    for l in comps:
        if 'ARG0' in l:
            one[4] = l.split(' ', 1)[1]
        elif 'ARG1' in l:
            one[1] = l.split(' ', 1)[1]
        elif 'ARGM-TMP' in l:
            one[3] = l.split(' ', 1)[1]
        elif 'ARGM-CAU' in l or 'ARGM-PRP' in l or 'ARGM-MNR' in l or 'ARGM-COM' in l or 'ARGM-EXT' in l:
            one[6] = l.split(' ', 1)[1]
        elif 'V' in l:
            one[0] = l.split(' ', 1)[1]
        elif 'ARGM-LOC' in l or 'ARG4' in l:
            one[2] = l.split(' ', 1)[1]
        elif 'ARG2' in l or 'ARG3' in l or 'C-ARG0' in l:
            one[5] = l.split(' ', 1)[1]
        elif 'ARGM-NEG' in l:
            one[7] = 'True'
    return one
def get5w1h(tri):
    a = fill(tri)
    output = []
    output += srlto5w1h(a[0])
    output.append(a[1])
    output += srlto5w1h(a[2])
    return output


