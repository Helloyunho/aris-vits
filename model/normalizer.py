from pathlib import Path
import subprocess

for p in Path("./data").glob("*.wav"):
    converted_path = p.with_stem(p.stem + "_norm")
    if converted_path.exists():
        continue
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(p),
            "-acodec",
            "pcm_s16le",
            "-ac",
            "1",
            "-ar",
            "44100",
            str(converted_path),
        ],
        check=True,
    )

    p.unlink()
    converted_path.rename(p)
    if p.with_suffix(".spec.pt").exists():
        p.with_suffix(".spec.pt").unlink()
