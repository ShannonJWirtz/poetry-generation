from flask import Flask, request
from datetime import datetime
import re
from poetrygenerator import *
app = Flask(__name__)

@app.route('/')
def homepage():

    profile = [stresses, nostresses]*4
    gen_dict = dictionary[:30000]
    rhyme = get_pronunciation_end('traitor', dictionary)[0]
    lines = 10

    user = request.args.get('user')

    if request.args.get('pr'):
        pr = request.args.get('pr')
        repeats = int(re.findall('\d+', pr)[0])
        foot = list(re.findall('[a-z]+', pr)[0])
        foot = [stresses if e=='s' else nostresses for e in foot]
        profile = foot * repeats

    if request.args.get('n'):
        n = int(request.args.get('n'))
        get_dict = dictionary[:n]

    if request.args.get('r'):
        r = request.args.get('r')
        rhyme=get_pronunciation_end(r, dictionary)[0]
        rhyme_indices = get_rhymes(dictionary,
                                   profile,
                                   rhyme,
                                   match_consonants=True)
        rhyme_indices.sort()
        to_keep = rhyme_indices[2] if len(rhyme_indices) >= 3 else rhyme_indices[-1]
        gen_dict = dictionary[:(to_keep+1)]

    if request.args.get('l'):
        l = int(request.args.get('l'))
        lines = l

    output = generate(gen_dict,
             profile,
             rhyme,
             lines)
    output = output
    start = """
    <h1>Nonesense Poetry Generator</h1>
    """
    middle = ''
    for line in output:
        middle += "<p>" + line + "</p>"

    end = """
    </br>
    ---------------------------------------------------------
    </br>
    <pr> query parameters:
    </br>n: top n entries from dictionary.
    </br>pr: profile, in the format 'sns2' or 'ns5', with 's' meaning stress, 'n' meaning no stress, and the ending number is the repeats of that pattern of stresses and nostresses
    </br>r: the rhyming word.
    </br>l: the number of lines.
    </br> e.g. ?pr=ns5&r=spoiled&l=10 returns 10 lines in iambic pentameter which rhyme with 'spoiled'
    """
    return start + middle + end

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
