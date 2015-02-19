"""
We can only really call this a guesser.  Let's categorize some contestants.
"""

from sklearn import tree, svm
import json
from collections import OrderedDict
import random
from operator import itemgetter

MAXWEEK = 8


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

    try:
        feat_num = in_vals['featured_num']
    except KeyError:
        feat_num = -999

    ret_data = OrderedDict({"ethnicity": ethnicity[in_vals['ethnicity']],
                            "hair_color": hair_color[in_vals['hair_color']],
                            "hair_length": hair_length[in_vals['hair_length']],
                            "hair_wavy": hair_wavy[in_vals['hair_wavy']],
                            "age": in_vals['age'],
                            "tattoos": in_vals['num_tattoos'],
                            "height": in_vals['height_inches'],
                            "featured_num": feat_num,
                            "intro_order": in_vals['intro_order'],
                            "pop_2013": in_vals['hometown_pop_2013']})

    return ret_data


def data_formatter(in_json, eliminations, tgt_week):
    """
    do stuff
    :return:
    """
    num_vals = dict()
    for indiv in in_json:
        elim = 0
        for i in range(1, tgt_week + 1):
            k = str(i)
            if indiv['name'] in eliminations[k]:
                elim = 1
        in_vals = textvals_to_numbers(indiv)
        num_vals[indiv['name']] = [in_vals.values(), elim]

    return num_vals


def week_predict(tgt_data, elims, tgt_week, sc_learn):
    """
    Given some data, make some predictions and return the average accuracy.
    :param tgt_data: json structure of data to be formatted
    :param elims: eliminated
    :param tgt_week:
    :param sc_learn:
    :return:
    """

    learn_values = data_formatter(tgt_data, elims, tgt_week)
    x = list()
    y = list()
    samples = set()
    while len(samples) < (len(learn_values) * 0.25):
        samples.add(random.randint(0, len(learn_values) - 1))
    learn_arr = learn_values.values()
    # print "Sample selection: ", samples
    for index in samples:
        x.append(learn_arr[index][0])
        y.append(learn_arr[index][1])

    # These next two lines courtesy of:
    # http://scikit-learn.org/stable/modules/tree.html
    clf = sc_learn
    try:
        clf = clf.fit(x, y)
    except ValueError:
        # Sometimes we try to train with 0 classes.
        return dict({"accuracy": 0, "departures": []})
    c = 0
    departures = list()
    for item in learn_values:
        if clf.predict(learn_values[item][0]) != learn_values[item][1]:
            c += 1
            if learn_values[item][1] == 0:  # if they aren't eliminated
                departures.append(item)
    accuracy = round((len(learn_values) - c) / float(len(learn_values)) * 100, 2)
    ret_val = dict({"accuracy": accuracy,
                    "departures": departures})
    return ret_val

if __name__ == "__main__":
    ELIMS = json.load(file('../feature_data/eliminations.json', 'r'))
    TGT_FILE = json.load(file("../feature_data/contestants.json", 'r'))

    # learner = tree.DecisionTreeClassifier()
    learner = svm.SVC()

    dt = dict()

    tot_att = 5000
    departure_count = dict()
    for att in range(0, tot_att):
        accs = list()
        week = MAXWEEK
        predict = week_predict(TGT_FILE, ELIMS, week, learner)
        accs.append(predict['accuracy'])
        for i in predict['departures']:
            if i in departure_count:
                departure_count[i] += 1
            else:
                departure_count[i] = 1
        for indiv in TGT_FILE:
            name = indiv['name']
            if name not in dt:
                dt[name] = [0]
            # print indiv, predict['departures']
            if name in predict['departures']:
                dt[name].append(dt[name][-1] + 1)
            else:
                dt[name].append(dt[name][-1])

    # fp = file("csv_out.csv", 'w')
    # for indiv in dt:
    #     fp.write(indiv + ", ")
    #     for i in dt[indiv]:
    #         fp.write(str(i) + ", ")
    #     fp.write("\n")
    # fp.close()

    print sum(accs) / len(accs)
    dc = sorted(zip(departure_count.keys(), departure_count.values()), key=itemgetter(1), reverse=True)

    for i in dc:
        print "Departing: ", i[0] + ": ", i[1]
