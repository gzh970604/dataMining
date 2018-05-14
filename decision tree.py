import sys
from math import log
import operator
from numpy import mean


def get_labels(train_file):

    labels = []
    for index, line in enumerate(open(train_file, 'rU').readlines()):
        label = line.strip().split(',')[-1]
        labels.append(label)
    return labels


def format_data(dataset_file):

    dataset = []
    for index, line in enumerate(open(dataset_file, 'rU').readlines()):
        line = line.strip()
        fea_and_label = line.split(',')
        dataset.append(
            [float(fea_and_label[i]) for i in range(len(fea_and_label) - 1)] + [fea_and_label[len(fea_and_label) - 1]])


    features = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
    return dataset, features


def split_dataset(dataset, feature_index, labels):

    dataset_less = []
    dataset_greater = []
    label_less = []
    label_greater = []
    datasets = []
    for data in dataset:
        datasets.append(data[0:4])
    mean_value = mean(datasets, axis=0)[feature_index]
    for data in dataset:
        if data[feature_index] > mean_value:
            dataset_greater.append(data)
            label_greater.append(data[-1])
        else:
            dataset_less.append(data)
            label_less.append(data[-1])
    return dataset_less, dataset_greater, label_less, label_greater


def cal_entropy(dataset):

    n = len(dataset)
    label_count = {}
    for data in dataset:
        label = data[-1]
        if label_count.has_key(label):
            label_count[label] += 1
        else:
            label_count[label] = 1
    entropy = 0
    for label in label_count:
        prob = float(label_count[label]) / n
        entropy -= prob * log(prob, 2)
    # print 'entropy:',entropy
    return entropy


def cal_info_gain(dataset, feature_index, base_entropy):

    datasets = []
    for data in dataset:
        datasets.append(data[0:4])
    # print datasets
    mean_value = mean(datasets, axis=0)[feature_index]
    # print mean_value
    dataset_less = []
    dataset_greater = []
    for data in dataset:
        if data[feature_index] > mean_value:
            dataset_greater.append(data)
        else:
            dataset_less.append(data)

    condition_entropy = float(len(dataset_less)) / len(dataset) * cal_entropy(dataset_less) + float(
        len(dataset_greater)) / len(dataset) * cal_entropy(dataset_greater)
    # print 'info_gain:',base_entropy - condition_entropy
    return base_entropy - condition_entropy


def cal_info_gain_ratio(dataset, feature_index):

    base_entropy = cal_entropy(dataset)
    '''
    if base_entropy == 0:
        return 1
    '''
    info_gain = cal_info_gain(dataset, feature_index, base_entropy)
    info_gain_ratio = info_gain / base_entropy
    return info_gain_ratio


def choose_best_fea_to_split(dataset, features):

    # base_entropy = cal_entropy(dataset)
    split_fea_index = -1
    max_info_gain_ratio = 0.0
    for i in range(len(features)):
        # info_gain = cal_info_gain(dataset,i,base_entropy)
        # info_gain_ratio = info_gain/base_entropy
        info_gain_ratio = cal_info_gain_ratio(dataset, i)
        if info_gain_ratio > max_info_gain_ratio:
            max_info_gain_ratio = info_gain_ratio
            split_fea_index = i
    return split_fea_index


def most_occur_label(labels):

    label_count = {}
    for label in labels:
        if label not in label_count.keys():
            label_count[label] = 1
        else:
            label_count[label] += 1
    sorted_label_count = sorted(label_count.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sorted_label_count[0][0]


def build_tree(dataset, labels, features):

    if len(labels) == 0:
        return 'NULL'

    if len(labels) == len(labels[0]):
        return labels[0]

    if len(features) == 0:
        return most_occur_label(labels)

    if cal_entropy(dataset) == 0:
        return most_occur_label(labels)
    split_feature_index = choose_best_fea_to_split(dataset, features)
    split_feature = features[split_feature_index]
    decesion_tree = {split_feature: {}}

    if cal_info_gain_ratio(dataset, split_feature_index) < 0.3:
        return most_occur_label(labels)
    del (features[split_feature_index])
    dataset_less, dataset_greater, labels_less, labels_greater = split_dataset(dataset, split_feature_index, labels)
    decesion_tree[split_feature]['<='] = build_tree(dataset_less, labels_less, features)
    decesion_tree[split_feature]['>'] = build_tree(dataset_greater, labels_greater, features)
    return decesion_tree


def store_tree(decesion_tree, filename):

    import pickle
    writer = open(filename, 'w')
    pickle.dump(decesion_tree, writer)
    writer.close()


def read_tree(filename):

    import pickle
    reader = open(filename, 'rU')
    return pickle.load(reader)


def classify(decesion_tree, features, test_data, mean_values):

    first_fea = decesion_tree.keys()[0]
    fea_index = features.index(first_fea)
    if test_data[fea_index] <= mean_values[fea_index]:
        sub_tree = decesion_tree[first_fea]['<=']
        if type(sub_tree) == dict:
            return classify(sub_tree, features, test_data, mean_values)
        else:
            return sub_tree
    else:
        sub_tree = decesion_tree[first_fea]['>']
        if type(sub_tree) == dict:
            return classify(sub_tree, features, test_data, mean_values)
        else:
            return sub_tree


def get_means(train_dataset):

    dataset = []
    for data in train_dataset:
        dataset.append(data[0:4])
    mean_values = mean(dataset, axis=0)
    return mean_values


def run(train_file, test_file):

    labels = get_labels(train_file)
    train_dataset, train_features = format_data(train_file)
    decesion_tree = build_tree(train_dataset, labels, train_features)
    print 'decesion_tree :', decesion_tree
    store_tree(decesion_tree, 'decesion_tree')
    mean_values = get_means(train_dataset)
    test_dataset, test_features = format_data(test_file)
    n = len(test_dataset)
    correct = 0
    for test_data in test_dataset:
        label = classify(decesion_tree, test_features, test_data, mean_values)
        # print 'classify_label  correct_label:',label,test_data[-1]
        if label == test_data[-1]:
            correct += 1
    print "zun: ", correct / float(n)



if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "please use: python decision.py train_file test_file"
        sys.exit()
    train_file = sys.argv[1]
    test_file = sys.argv[2]
    run(train_file, test_file)