from pathlib import Path
import random

filelist = Path("./data/filelist.txt").read_text().splitlines()
random.shuffle(filelist)

train = filelist[: int(len(filelist) * 0.9)]
valid = filelist[int(len(filelist) * 0.9) :]
Path("./data/train.txt").write_text("\n".join(train))
Path("./data/valid.txt").write_text("\n".join(valid))
