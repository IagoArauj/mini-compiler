import re
import json
import sys

input_file = sys.argv[1]

if sys.argv.count('-o') == 1:
    output_file = sys.argv[sys.argv.index('-o') + 1]
else:
    output_file = input_file + '.out'

if sys.argv.count('-conf') == 1:
    config_file = sys.argv[sys.argv.index('-conf') + 1]
else:
    config_file = "./config.json"

config = json.load(open(config_file, "r"))

tokens_list = config['tokens']

tokens = dict()

for token in tokens_list:
    token = dict(token)
    token_key = list(token.keys())[0]
    tokens[token_key] = token.get(token_key)


line = 1
pos = 0
tokens_out = [["token", "type", "line", "position"]]
identifiers = []
errors = []
res_words = tokens['reserved_keywords']
del tokens['reserved_keywords']

with open(sys.argv[1]) as file:
    sep_regex = re.compile(tokens['sep']['regex'])
    block_regex = re.compile(tokens['block_sep']['regex'])
    arith_regex = re.compile(tokens['arith_op']['regex'])
    logical_regex = re.compile(tokens['log_op']['regex'])
    comment_regex = re.compile(tokens['comment']['regex'])
    number_regex = re.compile(tokens['number']['regex'])
    identifier_regex = re.compile(tokens['identifier']['regex'])
    del tokens['comment']
    del tokens['block_sep']
    del tokens['sep']
    del tokens['identifier']

    while True:
        char = file.read(1)
        pos += 1

        if not char or char == '':
            break
        elif char == '\n':
            line += 1
            pos = 0
        else:
            if re.search(sep_regex, char):
                continue
            elif re.search(block_regex, char):
                tokens_out.append([char, "block_sep", str(line), str(pos - len(char) + 1)])
                continue

            word = char

            flag = False
            arith_flag = False
            while True:
                char = file.read(1)
                if not char or char == '' or char == '\n':
                    line += 1
                    pos = 0
                    break
                elif (re.search(sep_regex, char) and not re.search(comment_regex, word))\
                        or re.search(block_regex, char):
                    file.seek(file.tell() - 1)
                    break
                elif re.search(arith_regex, char) or re.search(logical_regex):
                    if re.search(identifier_regex, word) or re.search(number_regex, word):
                        file.seek(file.tell() - 1)
                        break
                    elif re.search(arith_regex, word) or re.search(logical_regex):
                        if arith_flag and word in tokens['arith_op']['tokens']:
                            file.seek(file.tell() - 1)
                            break
                        else:
                            arith_flag = True

                word += char
                pos += 1

            if re.search(comment_regex, word):
                tokens_out.append([word, "comment", str(line), str(pos - len(word) + 1)])
                continue

            for key in tokens.keys():
                regex = re.compile(tokens[key]['regex'])
                if re.search(regex, word):
                    if "tokens" in tokens[key]:
                        if word in tokens[key]['tokens']:
                            tokens_out.append([word, key, str(line), str(pos - len(word) + 1)])
                            flag = True
                            break
                        else:
                            continue
                    else:
                        tokens_out.append([word, key, str(line), str(pos - len(word) + 1)])
                        flag = True
                        break

            if not flag:
                if word in res_words:
                    tokens_out.append([word, "reserved_keyword", str(line), str(pos - len(word) + 1)])
                else:
                    if re.search(identifier_regex, word):
                        tokens_out.append([word, "identifier", str(line), str(pos - len(word) + 1)])
                        if word not in identifiers:
                            identifiers.append(word)
                    else:
                        errors.append("Unknown token \"{}\" in position {}:{}".format(word, line, pos - len(word) + 1))

if len(errors) != 0:
    [print(err) for err in errors]
    exit(0)

del token
with open('./out/lexical_analyzer.tsv', 'w') as output:
    for token in tokens_out:
        output.write("\t".join(token))
        output.write('\n')
with open('./out/identifiers.tsv', 'w') as output:
    for token in identifiers:
        output.write(token)
        output.write('\n')
print('Done')
