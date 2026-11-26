class Tamu:
    """Menyimpan identitas seorang tamu."""

    def __init__(self, id_tamu, nama, no_telepon):
        nama = str(nama).strip()
        no_telepon = str(no_telepon).strip()

        if not nama:
            raise ValueError("Nama tamu tidak boleh kosong.")
        if not no_telepon.isdigit():
            raise ValueError("Nomor telepon hanya boleh berisi angka.")

        self._id_tamu = str(id_tamu)
        self._nama = nama
        self._no_telepon = no_telepon

    @property
    def id_tamu(self):
        return self._id_tamu

    @property
    def nama(self):
        return self._nama

    @property
    def no_telepon(self):
        return self._no_telepon

    def ke_dict(self):
        return {
            "id_tamu": self.id_tamu,
            "nama": self.nama,
            "no_telepon": self.no_telepon
        }
