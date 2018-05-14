import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, ClusterMixin
import networkx as nx

def _hill_climb(x_t, X, W=None, h=0.1, eps=1e-7):

    error = 99.
    prob = 0.
    x_l1 = np.copy(x_t)


    radius_new = 0.
    radius_old = 0.
    radius_twiceold = 0.
    iters = 0.
    while True:
        radius_thriceold = radius_twiceold
        radius_twiceold = radius_old
        radius_old = radius_new
        x_l0 = np.copy(x_l1)
        x_l1, density = _step(x_l0, X, W=W, h=h)
        error = density - prob
        prob = density
        radius_new = np.linalg.norm(x_l1 - x_l0)
        radius = radius_thriceold + radius_twiceold + radius_old + radius_new
        iters += 1
        if iters > 3 and error < eps:
            break
    return [x_l1, prob, radius]


def _step(x_l0, X, W=None, h=0.1):
    n = X.shape[0]
    d = X.shape[1]
    superweight = 0.
    x_l1 = np.zeros((1, d))
    if W is None:
        W = np.ones((n, 1))
    else:
        W = W
    for j in range(n):
        kernel = kernelize(x_l0, X[j], h, d)
        kernel = kernel * W[j] / (h ** d)
        superweight = superweight + kernel
        x_l1 = x_l1 + (kernel * X[j])
    x_l1 = x_l1 / superweight
    density = superweight / np.sum(W)
    return [x_l1, density]


def kernelize(x, y, h, degree):
    kernel = np.exp(-(np.linalg.norm(x - y) / h) ** 2. / 2.) / ((2. * np.pi) ** (degree / 2))
    return kernel


class DENCLUE(BaseEstimator, ClusterMixin):


    def __init__(self, h=None, eps=1e-8, min_density=0., metric='euclidean'):
        self.h = h
        self.eps = eps
        self.min_density = min_density
        self.metric = metric

    def fit(self, X, y=None, sample_weight=None):
        if not self.eps > 0.0:
            raise ValueError("eps must be positive.")
        self.n_samples = X.shape[0]
        self.n_features = X.shape[1]
        density_attractors = np.zeros((self.n_samples, self.n_features))
        radii = np.zeros((self.n_samples, 1))
        density = np.zeros((self.n_samples, 1))


        if self.h is None:
            self.h = np.std(X) / 5
        if sample_weight is None:
            sample_weight = np.ones((self.n_samples, 1))
        else:
            sample_weight = sample_weight


        labels = -np.ones(X.shape[0])


        for i in range(self.n_samples):
            density_attractors[i], density[i], radii[i] = _hill_climb(X[i], X, W=sample_weight,
                                                                      h=self.h, eps=self.eps)


        cluster_info = {}
        num_clusters = 0
        cluster_info[num_clusters] = {'instances': [0],
                                      'centroid': np.atleast_2d(density_attractors[0])}
        g_clusters = nx.Graph()
        for j1 in range(self.n_samples):
            g_clusters.add_node(j1, attr_dict={'attractor': density_attractors[j1], 'radius': radii[j1],
                                               'density': density[j1]})


        for j1 in range(self.n_samples):
            for j2 in (x for x in range(self.n_samples) if x != j1):
                if g_clusters.has_edge(j1, j2):
                    continue
                diff = np.linalg.norm(g_clusters.node[j1]['attractor'] - g_clusters.node[j2]['attractor'])
                if diff <= (g_clusters.node[j1]['radius'] + g_clusters.node[j1]['radius']):
                    g_clusters.add_edge(j1, j2)


        clusters = list(nx.connected_component_subgraphs(g_clusters))
        num_clusters = 0


        for clust in clusters:


            max_instance = max(clust, key=lambda x: clust.node[x]['density'])
            max_density = clust.node[max_instance]['density']
            max_centroid = clust.node[max_instance]['attractor']


            complete = False
            c_size = len(clust.nodes())
            if clust.number_of_edges() == (c_size * (c_size - 1)) / 2.:
                complete = True


            cluster_info[num_clusters] = {'instances': clust.nodes(),
                                          'size': c_size,
                                          'centroid': max_centroid,
                                          'density': max_density,
                                          'complete': complete}


            if max_density >= self.min_density:
                labels[clust.nodes()] = num_clusters
            num_clusters += 1

        self.clust_info_ = cluster_info
        self.labels_ = labels
        return self

    def get_density(self, x, X, y=None, sample_weight=None):
        superweight = 0.
        n_samples = X.shape[0]
        n_features = X.shape[1]
        if sample_weight is None:
            sample_weight = np.ones((n_samples, 1))
        else:
            sample_weight = sample_weight
        for y in range(n_samples):
            kernel = kernelize(x, X[y], h=self.h, degree=n_features)
            kernel = kernel * sample_weight[y] / (self.h ** n_features)
            superweight = superweight + kernel
        density = superweight / np.sum(sample_weight)
        return density

    def set_minimum_density(self, min_density):
        self.min_density = min_density
        labels_copy = np.copy(self.labels_)
        for k in self.clust_info_.keys():
            if self.clust_info_[k]['density'] < min_density:
                labels_copy[self.clust_info_[k]['instances']] = -1
            else:
                labels_copy[self.clust_info_[k]['instances']] = k
        self.labels_ = labels_copy
        return self


data = pd.read_csv('iris.csv')
data = np.array(data)
samples = np.mat(data[:,0:2])
true_labels=data[:,-1]
labels=list(set(true_labels))
true_ID=np.zeros((3,50))
index=range(len(true_labels))

for i in range(len(labels)):
    true_ID[i]=[j for j in index if true_labels[j]==labels[i]]
d = DENCLUE(0.25, 0.0001)
d.fit(samples)
right_num=0

for i in range(len(d.clust_info_)):
    bestlens=0
    clust_set = set(d.clust_info_[i]['instances'])
    for j in range(len(labels)):
        true_set=set(true_ID[j])
        and_set= clust_set&true_set
        if len(list(and_set))>bestlens:
            bestlens=len(list(and_set))
    right_num+=bestlens

print (d.clust_info_,float(right_num)/len(samples))





