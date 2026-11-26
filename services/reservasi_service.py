from datetime import date
from models.kamar import kamar_dari_dict
from models.tamu import Tamu
from models.reservasi import Reservasi


class ReservasiService:
    """Mengatur proses bisnis dan menghubungkan model dengan JSON."""

    def __init__(self, penyimpanan):
        self.penyimpanan = penyimpanan

    def daftar_kamar(self):
        return [
            kamar_dari_dict(item)
            for item in self.penyimpanan.baca("kamar")
        ]

    def daftar_tamu(self):
        return [
            Tamu(**item)
            for item in self.penyimpanan.baca("tamu")
        ]

    def riwayat_reservasi(self):
        return [
            Reservasi(**item)
            for item in self.penyimpanan.baca("reservasi")
        ]

    def tambah_tamu(self, nama, no_telepon):
        data = self.penyimpanan.baca("tamu")
        nomor_baru = len(data) + 1
        tamu = Tamu(f"TMU-{nomor_baru:03d}", nama, no_telepon)
        data.append(tamu.ke_dict())
        self.penyimpanan.simpan("tamu", data)
        return tamu

    def buat_reservasi(self, id_tamu, nomor_kamar, tgl_masuk, tgl_keluar):
        tamu_dikenal = any(
            t.id_tamu == id_tamu for t in self.daftar_tamu()
        )
        if not tamu_dikenal:
            raise ValueError("ID tamu tidak ditemukan.")

        kamar = next(
            (k for k in self.daftar_kamar() if k.nomor == nomor_kamar),
            None
        )
        if kamar is None:
            raise ValueError("Nomor kamar tidak ditemukan.")

        try:
            masuk = date.fromisoformat(tgl_masuk)
            keluar = date.fromisoformat(tgl_keluar)
        except ValueError:
            raise ValueError("Tanggal harus menggunakan format YYYY-MM-DD.")

        if masuk < date.today():
            raise ValueError("Tanggal check-in tidak boleh sebelum hari ini.")
        if keluar <= masuk:
            raise ValueError("Tanggal check-out harus setelah check-in.")

        # Dua rentang tanggal bertabrakan jika awal rentang baru
        # sebelum akhir lama DAN akhir baru setelah awal lama.
        for lama in self.riwayat_reservasi():
            if lama.nomor_kamar == nomor_kamar and lama.status == "DIPESAN":
                awal_lama = date.fromisoformat(lama.tgl_checkin)
                akhir_lama = date.fromisoformat(lama.tgl_checkout)
                if masuk < akhir_lama and keluar > awal_lama:
                    raise ValueError("Kamar sudah dipesan pada rentang tanggal tersebut.")

        jumlah_malam = (keluar - masuk).days
        total = kamar.hitung_biaya(jumlah_malam)

        data = self.penyimpanan.baca("reservasi")
        id_baru = f"RSV-{len(data) + 1:03d}"
        reservasi = Reservasi(
            id_baru, id_tamu, nomor_kamar,
            masuk.isoformat(), keluar.isoformat(), total
        )
        data.append(reservasi.ke_dict())
        self.penyimpanan.simpan("reservasi", data)
        return reservasi

    def check_out(self, id_reservasi, metode):
        data = self.penyimpanan.baca("reservasi")
        for index, item in enumerate(data):
            if item["id_reservasi"] == id_reservasi:
                reservasi = Reservasi(**item)
                reservasi.selesaikan(metode)
                data[index] = reservasi.ke_dict()
                self.penyimpanan.simpan("reservasi", data)
                return reservasi
        raise ValueError("ID reservasi tidak ditemukan.")
