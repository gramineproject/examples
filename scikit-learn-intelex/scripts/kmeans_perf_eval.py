# SPDX-License-Identifier: LGPL-3.0-or-later
# Copyright (c) 2021 Intel Corporation
#                    Andrey Morkovkin <andrey.morkovkin@intel.com>

from timeit import default_timer as timer
import pandas as pd

def run(X, y, is_patched):
    if is_patched:
        from sklearnex import patch_sklearn
        patch_sklearn()

    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import MinMaxScaler
    from sklearn.cluster import KMeans
    from sklearn.metrics import davies_bouldin_score

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
    model = KMeans(**params).fit(x_train)
    train_time = timer() - start
    print(f'Train time: {train_time:.3f} s')

    inertia_opt = model.inertia_
    n_iter_opt = model.n_iter_
    davies_bouldin_value = davies_bouldin_score(x_train, model.labels_)
    print(f'Inertia: {inertia_opt:.3f}')
    print(f'Number of iterations: {n_iter_opt}')
    print(f'Davies-Bouldin metric on train data: {davies_bouldin_value:.3f}')

    start = timer()
    predicted_labels = model.predict(x_test)
    test_time = timer() - start
    print(f'Predict time: {test_time:.3f} s')

    davies_bouldin_value = davies_bouldin_score(x_test, predicted_labels)
    print(f'Davies-Bouldin metric on test data: {davies_bouldin_value:.3f}')


def main():
    X = pd.read_csv('data/X.csv')
    y = pd.read_csv('data/y.csv')

    print('*** Stock Scikit-learn ***')
    run(X, y, is_patched=False)
    print('*** Intel® extension for Scikit-learn ***')
    run(X, y, is_patched=True)
    print('Kmeans perf evaluation finished')

if __name__ == '__main__':
    main()
