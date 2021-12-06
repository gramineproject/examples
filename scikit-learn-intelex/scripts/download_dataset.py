from sklearn.datasets import fetch_openml

def main():
    X, y = fetch_openml(name='mnist_784', version=1, return_X_y=True, data_home='data')
    X.to_csv('data/X.csv', index=False)
    y.to_csv('data/y.csv', index=False)

if __name__ == '__main__':
    main()