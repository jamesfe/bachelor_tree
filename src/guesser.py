"""
We can only really call this a guesser.  Let's categorize some contestants.
"""

from sklearn import tree
import json
from collections import OrderedDict


def textvals_to_numbers(in_vals):
    """
    hair length
    :param in_vals: dictionary of attributes and text values
    :return:
    """
    hair_length = dict({"neck": 1,
                        "shoulder": 2,
                        "chest": 3,
                        "stomach": 4})

    hair_color = dict({"light": 1,
                       "medium": 2,
                       "mixed": 3,
                       "medium-dark": 4,
                       "dark": 5})

    hair_wavy = dict({"straight": 1,
                      "straight-medium": 2,
                      "medium": 3,
                      "curly-medium": 4,
                      "curly": 5})

    ethnicity = dict({"asian": 1,
                      "caucasian": 2,
                      "african-american": 3})

    ret_data = OrderedDict({"ethnicity": ethnicity[in_vals['ethnicity']],
                            "hair_color": hair_color[in_vals['hair_color']],
                            "hair_length": hair_length[in_vals['hair_length']],
                            "hair_wavy": hair_wavy[in_vals['hair_wavy']],
                            "age": in_vals['age']})

    return ret_data


def data_formatter(in_file):
    """
    do stuff
    :return:
    """
    file_p = file(in_file, 'r')
    in_json = json.load(file_p)
    file_p.close()

    num_vals = dict()
    for item in in_json:
        if item['eliminated']:
            elim = 1
        else:
            elim = 0
        in_vals = textvals_to_numbers(item)
        num_vals[item['name']] = [in_vals.values(), elim]

    return num_vals


if __name__ == "__main__":
    tgt_file = "../feature_data/contestants_27jan2015.json"
    learn_values = data_formatter(tgt_file)

    x = list()
    y = list()

    for index, item in enumerate(learn_values.values()):
        x.append(item[0])
        y.append(item[1])
        if index > len(learn_values)*0.3:
            break

    print x, y


    # These next two lines courtesy of:
    # http://scikit-learn.org/stable/modules/tree.html
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(x, y)

    for item in learn_values:
        print item, clf.predict(learn_values[item][0]), learn_values[item][1]

    ## some awesome output code here