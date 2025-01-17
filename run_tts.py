import torch
from scipy.io.wavfile import write

import commons
import utils
import socket
import signal
from models import SynthesizerTrn
from text.symbols import symbols
from text import text_to_sequence
from tempfile import NamedTemporaryFile
from scipy.io.wavfile import write
from threading import Thread

SOCKET_PATH = "/tmp/aris.sock"


def get_text(text, hps):
    text_norm = text_to_sequence(text, hps.data.text_cleaners)
    if hps.data.add_blank:
        text_norm = commons.intersperse(text_norm, 0)
    text_norm = torch.LongTensor(text_norm)
    return text_norm


hps = utils.get_hparams_from_file("./model/aris_ms_istft_vits.json")
hps.model_dir = "/Users/helloyunho/Documents/aris"


net_g = SynthesizerTrn(
    len(symbols),
    hps.data.filter_length // 2 + 1,
    hps.train.segment_size // hps.data.hop_length,
    **hps.model
)
_ = net_g.eval()

_ = utils.load_checkpoint(
    utils.latest_checkpoint_path(hps.model_dir, "G_*.pth"), net_g, None
)

server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server.bind(SOCKET_PATH)
server.listen(1)


def handle_connection(connection):
    buf = b""
    try:
        while True:
            data = connection.recv(1024)
            if not data:
                break

            buf += data
            if buf.endswith(b"\n"):
                text = buf.decode("utf-8").strip()
                buf = b""

                stn_tst = get_text(text, hps)
                with torch.no_grad():
                    x_tst = stn_tst.unsqueeze(0)
                    x_tst_lengths = torch.LongTensor([stn_tst.size(0)])
                    audio = (
                        net_g.infer(
                            x_tst,
                            x_tst_lengths,
                            noise_scale=0.667,
                            noise_scale_w=0.8,
                            length_scale=1,
                        )[0][0, 0]
                        .data.float()
                        .numpy()
                    )
                with NamedTemporaryFile(delete=False) as tmp:
                    write(tmp, hps.data.sampling_rate, audio)
                    tmp.seek(0)
                    connection.send(tmp.name.encode())
                    break
    finally:
        connection.close()


def cleanup(_, __):
    server.close()
    import os

    os.unlink(SOCKET_PATH)


signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGQUIT, cleanup)
signal.signal(signal.SIGABRT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

while True:
    connection, client_address = server.accept()
    thread = Thread(target=handle_connection, args=(connection,))
    thread.daemon = True
    thread.start()
