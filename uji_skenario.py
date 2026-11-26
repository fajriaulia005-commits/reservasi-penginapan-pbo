"""Pengujian sederhana: 5 skenario positif dan 1 skenario input tidak valid."""

import tempfile
import unittest
from pathlib import Path

from utils.penyimpanan import PenyimpananJSON
from services.reservasi_service import ReservasiService


class UjiReservasi(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.store = PenyimpananJSON(self.folder.name)
        # Data kamar awal untuk pengujian terisolasi.
        self.store.simpan("kamar", [
            {"nomor": "101", "tipe": "Standar", "tarif": 250000},
            {"nomor": "201", "tipe": "Deluxe", "tarif": 400000}
        ])
        self.service = ReservasiService(self.store)

    def tearDown(self):
        self.folder.cleanup()

    def siapkan_tamu_dan_reservasi(self):
        tamu = self.service.tambah_tamu("Budi", "081234567890")
        reservasi = self.service.buat_reservasi(
            tamu.id_tamu, "101", "2027-01-10", "2027-01-12"
        )
        return tamu, reservasi

    def test_1_tambah_tamu(self):
        tamu = self.service.tambah_tamu("Budi", "081234567890")
        self.assertEqual(tamu.nama, "Budi")
        self.assertEqual(len(self.store.baca("tamu")), 1)

    def test_2_reservasi_kamar_standar(self):
        tamu = self.service.tambah_tamu("Budi", "081234567890")
        reservasi = self.service.buat_reservasi(
            tamu.id_tamu, "101", "2027-01-10", "2027-01-12"
        )
        self.assertEqual(reservasi.total_biaya, 500000)
        self.assertEqual(reservasi.status, "DIPESAN")

    def test_3_reservasi_kamar_deluxe(self):
        tamu = self.service.tambah_tamu("Siti", "081234567891")
        reservasi = self.service.buat_reservasi(
            tamu.id_tamu, "201", "2027-01-10", "2027-01-12"
        )
        self.assertEqual(reservasi.total_biaya, 900000)

    def test_4_check_out_dan_pembayaran(self):
        _, reservasi = self.siapkan_tamu_dan_reservasi()
        selesai = self.service.check_out(reservasi.id_reservasi, "TUNAI")
        self.assertEqual(selesai.status, "SELESAI")
        self.assertEqual(selesai.metode_pembayaran, "TUNAI")

    def test_5_data_tetap_tersimpan_setelah_service_dibuat_ulang(self):
        tamu, reservasi = self.siapkan_tamu_dan_reservasi()
        service_baru = ReservasiService(PenyimpananJSON(self.folder.name))
        self.assertEqual(service_baru.daftar_tamu()[0].nama, "Budi")
        self.assertEqual(
            service_baru.riwayat_reservasi()[0].id_reservasi,
            reservasi.id_reservasi
        )

    def test_input_tidak_valid_ditolak(self):
        with self.assertRaises(ValueError):
            self.service.tambah_tamu(" ", "08AB")


if __name__ == "__main__":
    unittest.main(verbosity=2)
