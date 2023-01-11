# SPDX-License-Identifier: LGPL-3.0-or-later
# Copyright (C) 2021 Intel Corporation
#                    Andrey Morkovkin <andrey.morkovkin@intel.com>


from timeit import default_timer as timer
import pandas as pd

from sklearnex import patch_sklearn
patch_sklearn()

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from sklearn.metrics import davies_bouldin_score

def main():
    X = pd.read_csv('data/X.csv')
    y = pd.read_csv('data/y.csv')

    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=123)

    scaler_x = MinMaxScaler()
    scaler_x.fit(x_train)
    x_train = scaler_x.transform(x_train)
    x_test = scaler_x.transform(x_test)

    params = {
        'n_clusters': 10,
        'random_state': 123,
        'copy_x': False,
    }

    start = timer()
    model = KMeans(**params).fit(x_train, y_train)
    train_patched = timer() - start
    print(f'Intel extension for Scikit-learn train time: {train_patched:.3f} s')

    inertia_opt = model.inertia_
    n_iter_opt = model.n_iter_
    print(f'Intel extension for Scikit-learn inertia: {inertia_opt:.3f}')
    print(f'Intel extension for Scikit-learn number of iterations: {n_iter_opt}')

    davies_bouldin_value = davies_bouldin_score(x_train, model.labels_)
    print(f'Intel extension for Scikit-learn Davies-Bouldin metric on train data: {davies_bouldin_value:.3f}')

    start = timer()
    predicted_labels = model.predict(x_test)
    test_time = timer() - start
    print(f'Intel extension for Scikit-learn predict time: {test_time:.3f} s')

    davies_bouldin_value = davies_bouldin_score(x_test, predicted_labels)
    print(f'Intel extension for Scikit-learn Davies-Bouldin metric on test data: {davies_bouldin_value:.3f}')
    print('Kmeans example finished')

if __name__ == '__main__':
    main()
