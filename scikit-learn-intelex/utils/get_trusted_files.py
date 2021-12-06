import sys
import os

required_parts = ['numpy', 'numpy.libs', 'joblib', 'pandas', 'onedal', 'scipy', 'scipy.libs',
        'sklearn', 'sklearnex', 'daal4py', 'scikit_learn.libs',
        'psutil', 'dateutil', 'joblib', 'threadpoolctl.py']


def main():
    result = []
    for part in required_parts:
        for folder in sys.path:
            path_to_check = os.path.join(folder, part)
            postfix = ''
            if path_to_check.split('/')[1] == 'usr' and os.path.exists(path_to_check):
                if os.path.isdir(path_to_check):
                    postfix = '/'
                result.append(f'\\"file:{path_to_check}{postfix}\\",')
                break
    print('\n'.join(result))


if __name__ == '__main__':
    main()

