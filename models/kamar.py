from abc import ABC, abstractmethod


class Kamar(ABC):
    "Class abstrak yang menjadi dasar semua jenis kamar."

    def __init__(self, nomor, tarif):
        if not nomor:
            raise ValueError("Nomor kamar tidak boleh kosong.")
        if tarif <= 0:
            raise ValueError("Tarif kamar harus lebih dari nol.")

        self._nomor = str(nomor)
        self._tarif = int(tarif)

    @property
    def nomor(self):
        return self._nomor

    @property
    def tarif(self):
        return self._tarif

    @property
    @abstractmethod
    def tipe(self):
        pass

    @abstractmethod
    def hitung_biaya(self, jumlah_malam):
        pass

    def ke_dict(self):
        return {
            "nomor": self.nomor,
            "tipe": self.tipe,
            "tarif": self.tarif
        }


class KamarStandar(Kamar):
    @property
    def tipe(self):
        return "Standar"

    def hitung_biaya(self, jumlah_malam):
        if jumlah_malam <= 0:
            raise ValueError("Jumlah malam harus lebih dari nol.")
        return self.tarif * jumlah_malam


class KamarDeluxe(Kamar):
    BIAYA_SARAPAN = 50000

    @property
    def tipe(self):
        return "Deluxe"

    def hitung_biaya(self, jumlah_malam):
        if jumlah_malam <= 0:
            raise ValueError("Jumlah malam harus lebih dari nol.")
        return (self.tarif + self.BIAYA_SARAPAN) * jumlah_malam


def kamar_dari_dict(data):
    """Membentuk objek kamar dari data JSON."""
    if data["tipe"] == "Standar":
        return KamarStandar(data["nomor"], data["tarif"])
    if data["tipe"] == "Deluxe":
        return KamarDeluxe(data["nomor"], data["tarif"])
    raise ValueError(f"Jenis kamar tidak dikenal: {data['tipe']}")
