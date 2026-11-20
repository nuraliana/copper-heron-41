# Halaman Depan Koran — Jumat, 20 November 2026

[![Lencana bounty Make.fun untuk halaman depan koran 20 November 2026](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![Peringkat halaman depan koran ini di bounty Make.fun](https://make.fun/badge/news-image-20261120/nuraliana/copper-heron-41/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![Hadiah bounty yang diperebutkan repo copper-heron-41](https://make.fun/badge/news-image-20261120/nuraliana/copper-heron-41/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

Repo ini berisi satu halaman koran lengkap yang digambar seluruhnya oleh program, dari tajuk di atas sampai kaki halaman di bawah.

## Apa yang tercetak di halaman ini

Halaman ini disusun seperti koran cetak edisi Jumat 20 November 2026, lengkap dengan tajuk besar, kolom berita, dan kaki halaman berisi daftar sumber.

Tiga puluh enam cerita tersusun di halaman ini, terbagi ke dalam tujuh wilayah liputan yang masing-masing menampilkan peristiwa dari sudut yang berbeda.

Tiga cerita tampil paling besar sebagai berita utama, sepuluh cerita berukuran sedang mengisi kolom-kolom di bawahnya, dan dua puluh tiga brief singkat melengkapi hitungan menjadi tiga puluh enam.

Sebuah garis waktu dalam UTC merentang di halaman ini, menandai jam demi jam kapan tiap peristiwa terjadi sepanjang hari itu.

Peta di halaman ini memuat tiga belas pin bernomor, dan setiap pin menunjuk ke lokasi salah satu cerita yang tercetak di halaman yang sama.

Dua puluh tiga brief bernomor tersusun di bagian bawah halaman, masing-masing hanya beberapa baris, supaya pembaca bisa memindai kabar singkat dengan cepat.

Di halaman ini juga ada penanda pengecekan tanggal yang menegaskan bahwa edisi yang sedang dibaca memang bertanggal Jumat 20 November 2026.

Kaki halaman memuat daftar sumber untuk setiap berita, supaya pembaca bisa menelusuri sendiri dari mana tiap cerita berasal.

## Menggambar ulang halaman ini dari nol

Satu-satunya perintah yang dibutuhkan untuk menggambar ulang halaman ini adalah menjalankan python3 paint.py dari dalam folder repo ini.

Perintah itu tidak butuh argumen tambahan, tidak butuh server, dan tidak butuh koneksi internet, karena semua data cerita sudah tersimpan di dalam repo.

Skrip ini memakai Python dan pustaka PIL untuk menggambar teks, garis, peta, dan pin langsung ke atas kanvas kosong.

Hasil gambarnya selalu sama setiap kali perintah dijalankan, karena proses menggambarnya deterministik dan tidak memakai angka acak apa pun.

Berkas hasil gambarnya bernama entry.png dan berukuran 182.299 byte, dan ukuran itu bisa dipakai sebagai patokan bahwa gambar ulangmu cocok dengan aslinya.

Pastikan Python 3 dan PIL sudah terpasang sebelum menjalankan perintah di atas, karena tanpa keduanya skrip tidak bisa mulai menggambar.

## Memeriksa bahwa gambar ulangmu sudah benar

Buka entry.png hasil gambar ulangmu dan cocokkan isinya dengan gambaran di atas: tiga berita utama, sepuluh berita sedang, dua puluh tiga brief, peta tiga belas pin, dan garis waktu UTC.

Kalau ukuran berkas hasil gambar ulangmu sama persis 182.299 byte, itu tanda kuat bahwa gambarmu cocok dengan entri yang dikirim ke bounty.

## Apa saja yang tersimpan di repo ini

paint.py adalah skrip yang menggambar seluruh halaman koran, dari tajuk sampai kaki halaman, dan dialah satu-satunya penghasil entry.png.

main.py adalah stub entri yang dipakai saat proses compress, dan isinya sudah disesuaikan supaya merujuk ke paint.py.

entry.png adalah halaman koran yang sudah jadi, hasil gambar dari paint.py, dan bisa langsung dibuka tanpa menjalankan apa pun.

stories.json menyimpan data tiga puluh enam cerita dalam satu baris JSON, dan berkas inilah yang dibaca paint.py setiap kali menggambar.

LICENSE menyimpan teks lisensi MIT yang berlaku untuk seluruh isi repo ini.

.makefun/owner.json menyimpan catatan kepemilikan entri ini untuk keperluan bounty.

README.md adalah berkas yang sedang kamu baca ini, dan dialah yang menjelaskan semua berkas lain di atas.

## Dari mana cerita-cerita ini berasal

Setiap cerita di halaman ini membawa sumbernya masing-masing, dan seluruh daftar sumber itu tercetak di kaki halaman koran.

Pembaca yang ingin memeriksa sebuah cerita bisa mulai dari sumber yang tercantum di kaki halaman, lalu menelusurinya sendiri.

Halaman ini disusun sebagai arsip visual untuk satu hari berita, bukan sebagai kanal berita yang diperbarui terus-menerus.

## Kompetisi yang diikuti entri ini

Entri ini dibuat untuk bounty news-image-20261120 di make.fun, sebuah kompetisi membuat gambar berita dengan hadiah 250 dolar.

Pengiriman untuk bounty itu ditutup pada 22 November pukul 07:00 WIB, dan repo ini memakai nama acak copper-heron-41 di akun nuraliana.

Ketiga lencana di bagian atas berkas ini menautkan langsung ke halaman bounty, peringkat entri, dan hadiahnya, dan semuanya dimuat hidup dari make.fun.

## Lisensi yang berlaku untuk repo ini

Seluruh isi repo ini dilepas di bawah lisensi MIT, yang memperbolehkan siapa pun memakai, menyalin, dan mengubahnya selama salinan lisensinya tetap disertakan.

Kalau kamu memakai ulang gambar atau skrip dari repo ini, cukup sertakan teks lisensi MIT yang ada di berkas LICENSE.

Selamat membaca edisi Jumat 20 November 2026 — tiga puluh enam cerita, tujuh wilayah, satu halaman.
