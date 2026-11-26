from datetime import date
from models.kamar import KamarStandar, KamarDeluxe
from services.reservasi_service import ReservasiService
from utils.penyimpanan import PenyimpananJSON


def buat_aplikasi():
    penyimpanan = PenyimpananJSON("data")
    service = ReservasiService(penyimpanan)
    return service


def tampilkan_menu():
    print("\n=== SISTEM RESERVASI PENGINAPAN ===")
    print("1. Lihat daftar kamar")
    print("2. Tambah data tamu")
    print("3. Buat reservasi")
    print("4. Check-out dan pembayaran")
    print("5. Lihat riwayat reservasi")
    print("0. Keluar")


def main():
    service = buat_aplikasi()

    while True:
        tampilkan_menu()
        pilihan = input("Pilih menu: ").strip()

        try:
            if pilihan == "1":
                for kamar in service.daftar_kamar():
                    print(
                        f"{kamar.nomor} | {kamar.tipe} | "
                        f"Rp{kamar.tarif:,}/malam"
                    )

            elif pilihan == "2":
                nama = input("Nama tamu: ").strip()
                telepon = input("Nomor telepon: ").strip()
                tamu = service.tambah_tamu(nama, telepon)
                print(f"Tamu berhasil ditambahkan. ID: {tamu.id_tamu}")

            elif pilihan == "3":
                print("\nDaftar tamu:")
                for tamu in service.daftar_tamu():
                    print(f"{tamu.id_tamu} - {tamu.nama}")

                print("\nDaftar kamar:")
                for kamar in service.daftar_kamar():
                    print(f"{kamar.nomor} - {kamar.tipe} - Rp{kamar.tarif:,}")

                id_tamu = input("ID tamu: ").strip()
                nomor = input("Nomor kamar: ").strip()
                masuk = input("Tanggal check-in (YYYY-MM-DD): ").strip()
                keluar = input("Tanggal check-out (YYYY-MM-DD): ").strip()

                reservasi = service.buat_reservasi(
                    id_tamu, nomor, masuk, keluar
                )
                print(
                    f"Reservasi berhasil: {reservasi.id_reservasi}. "
                    f"Total biaya: Rp{reservasi.total_biaya:,}"
                )

            elif pilihan == "4":
                id_reservasi = input("ID reservasi: ").strip()
                metode = input("Metode pembayaran (TUNAI/TRANSFER/KARTU): ").strip()
                reservasi = service.check_out(id_reservasi, metode)
                print(
                    f"Check-out berhasil. Total Rp{reservasi.total_biaya:,}; "
                    f"metode: {reservasi.metode_pembayaran}"
                )

            elif pilihan == "5":
                riwayat = service.riwayat_reservasi()
                if not riwayat:
                    print("Belum ada reservasi.")
                for item in riwayat:
                    print(
                        f"{item.id_reservasi} | Tamu: {item.id_tamu} | "
                        f"Kamar: {item.nomor_kamar} | "
                        f"{item.tgl_checkin} s.d. {item.tgl_checkout} | "
                        f"Rp{item.total_biaya:,} | {item.status}"
                    )

            elif pilihan == "0":
                print("Terima kasih. Program selesai.")
                break
            else:
                print("Pilihan menu tidak tersedia.")

        except (ValueError, KeyError) as error:
            print(f"Terjadi kesalahan: {error}")


if __name__ == "__main__":
    main()
