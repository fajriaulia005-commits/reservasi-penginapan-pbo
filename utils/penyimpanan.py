import json
from pathlib import Path


class PenyimpananJSON:
    """Satu tempat untuk membaca dan menulis tiga file JSON."""

    NAMA_FILE = {
        "kamar": "kamar.json",
        "tamu": "tamu.json",
        "reservasi": "reservasi.json"
    }

    def __init__(self, folder):
        self.folder = Path(folder)
        self.folder.mkdir(parents=True, exist_ok=True)

        for nama in self.NAMA_FILE.values():
            path = self.folder / nama
            if not path.exists():
                path.write_text("[]", encoding="utf-8")

    def baca(self, jenis):
        if jenis not in self.NAMA_FILE:
            raise ValueError("Jenis data tidak dikenal.")
        path = self.folder / self.NAMA_FILE[jenis]
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def simpan(self, jenis, data):
        if jenis not in self.NAMA_FILE:
            raise ValueError("Jenis data tidak dikenal.")
        path = self.folder / self.NAMA_FILE[jenis]
        sementara = path.with_suffix(".tmp")
        with sementara.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        sementara.replace(path)
