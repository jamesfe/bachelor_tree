"""
I mean, we can only really call this a guesser.  Let's categorize some contestants.
"""

from sklearn import tree
import json


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