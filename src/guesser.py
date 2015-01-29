"""
I mean, we can only really call this a guesser.  Let's categorize some contestants.
"""

from sklearn import tree
import json


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

    ret_data = dict({"ethnicity": ethnicity[in_vals['ethnicity']],
                     "hair_color": hair_color[in_vals['hair_color']],
                     "hair_length": hair_length[in_vals['hair_length']],
                     "hair_wavy": hair_wavy[in_vals['hair_wavy']]})

    return ret_data


def data_formatter(in_file):
    """
    do stuff
    :return:
    """
    file_p = file(in_file, 'r')
    in_json = json.load(file_p)
    file_p.close()

    print in_json

    ret_vals = list()
    ## a list of lists: each of which is a classified value and a set of numerical features
    ## i.e. [ [1, [2,3,4,5] ], [0, [2,3,4,3] ] ] where 1 is stays and 0 is goes (or vice versa)

    #TODO: Convert inputs to numbers.
    # categories?  or is everything continuous?

    return ret_vals


if __name__ == "__main__":
    tgt_file = "../feature_data/contestants_27jan2015.json"
    learn_values= data_formatter(tgt_file)

    # These next two lines courtesy of:
    # http://scikit-learn.org/stable/modules/tree.html
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(X, Y)

    # clf.predict( some values here )

    ## some awesome output code here