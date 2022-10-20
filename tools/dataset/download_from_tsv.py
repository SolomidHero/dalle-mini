from pathlib import Path
import requests
import argparse
import hashlib
from tqdm.auto import tqdm


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        'meta_paths', type=Path, nargs='+',
        help='paths to .tsv files with (img_url, caption) pairs'
    )

    parser.add_argument(
        '--data_dir', type=Path,
        help='path to store downloaded images and captions'
    )

    return parser.parse_args()


def download_image(url, data_dir):
    try:
        r = requests.get(url, timeout=5)
    except:
        return None
    if r.status_code != 200:
        return None
    img_data = r.content
    filepath = hashlib.md5(url.encode()).hexdigest()
    filepath = (data_dir / filepath).with_suffix('.jpg')
    with open(filepath, 'wb') as f:
        f.write(img_data)
    return filepath


def process_meta(meta_path: Path, data_dir: Path):
    with open(meta_path) as meta:
        for line in tqdm(meta):
            url, caption = line.split('\t', 1)
            filepath = download_image(url, data_dir)
            if filepath is None:
                continue
            with open(Path(filepath).with_suffix('.txt'), 'w') as f:
                f.write(caption.strip())


if __name__ == "__main__":
    args = parse_args()
    meta_paths = [Path(meta_path) for meta_path in args.meta_paths]

    Path(args.data_dir).mkdir(exist_ok=True, parents=True)
    for meta_path in meta_paths:
        process_meta(meta_path, args.data_dir)
