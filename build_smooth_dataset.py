import argparse
import h5py
import numpy as np

from nasdaq.core.database import Database
from nasdaq.analyzer.utils.window import scaled_window


def main(args):
    db = Database()

    root = h5py.File(args.output, 'w')
    root.create_dataset('windows', shape=(0, args.window, 4),
                        maxshape=(None, args.window, 4), dtype=np.float32)

    for target in args.target:
        df = db.get_daily_price(
            target, '1900-01-01')[['open', 'high', 'low', 'close']]

        step = 1 if args.overlap else args.window

        windows = []
        for i in range(1, len(df), step):
            criteria = df.iloc[i-1]['close']
            window = df.iloc[i:i+args.window].to_numpy()

            if window.shape[0] != args.window:
                break

            window = scaled_window(window, criteria)
            windows.append(window)

        orig_len = root['windows'].shape[0]
        length = len(windows)

        windows = np.array(windows)

        root['windows'].resize(orig_len+length, axis=0)
        root['windows'][orig_len:orig_len+length] = windows

    root.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=str, required=True,
                        help='the path of created database file')
    parser.add_argument('--target', nargs='+',
                        required=True, help='the target names')
    parser.add_argument('--window', type=int, required=True,
                        help='the size of window')
    parser.add_argument('--overlap', action='store_true',
                        help='create data with allowing overlap')

    args = parser.parse_args()
    main(args)
