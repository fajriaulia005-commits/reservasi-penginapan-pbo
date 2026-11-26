class Reservasi:
    """Menyimpan data reservasi dan mengatur statusnya."""

    def __init__(
        self, id_reservasi, id_tamu, nomor_kamar,
        tgl_checkin, tgl_checkout, total_biaya,
        status="DIPESAN", metode_pembayaran=""
    ):
        self._id_reservasi = str(id_reservasi)
        self._id_tamu = str(id_tamu)
        self._nomor_kamar = str(nomor_kamar)
        self._tgl_checkin = str(tgl_checkin)
        self._tgl_checkout = str(tgl_checkout)
        self._total_biaya = int(total_biaya)
        self._status = status
        self._metode_pembayaran = metode_pembayaran

    @property
    def id_reservasi(self):
        return self._id_reservasi

    @property
    def id_tamu(self):
        return self._id_tamu

    @property
    def nomor_kamar(self):
        return self._nomor_kamar

    @property
    def tgl_checkin(self):
        return self._tgl_checkin

    @property
    def tgl_checkout(self):
        return self._tgl_checkout

    @property
    def total_biaya(self):
        return self._total_biaya

    @property
    def status(self):
        return self._status

    @property
    def metode_pembayaran(self):
        return self._metode_pembayaran

    def selesaikan(self, metode):
        if self.status != "DIPESAN":
            raise ValueError("Hanya reservasi DIPESAN yang dapat di-check-out.")
        metode = metode.upper().strip()
        if metode not in ("TUNAI", "TRANSFER", "KARTU"):
            raise ValueError("Metode pembayaran harus TUNAI, TRANSFER, atau KARTU.")
        self._status = "SELESAI"
        self._metode_pembayaran = metode

    def ke_dict(self):
        return {
            "id_reservasi": self.id_reservasi,
            "id_tamu": self.id_tamu,
            "nomor_kamar": self.nomor_kamar,
            "tgl_checkin": self.tgl_checkin,
            "tgl_checkout": self.tgl_checkout,
            "total_biaya": self.total_biaya,
            "status": self.status,
            "metode_pembayaran": self.metode_pembayaran
        }
