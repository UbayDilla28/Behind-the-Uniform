## =========================================================
## SCRIPT REN'PY - "MISTERI SEKOLAH"
## Adaptasi naskah asli, tokoh "Herssen" diganti menjadi "Tama"
## Ditambahkan branching dialogue: sikap player (dingin/ramah)
## terhadap Tama akan memengaruhi kemauan Tama untuk bekerja sama
## =========================================================

## -----------------------
## DEFINISI KARAKTER
## -----------------------
define narrator = Character(None, kind=nvl)
define radio = Character("Radio", color="#8a8a8a")
define guru = Character("Guru Wali Kelas", color="#c9a15a")
define tama = Character("Tama", color="#5ab0e0")
define mc = Character("[player_name]", color="#e08ab0")
define maria = Character("Maria", color="#e05a5a")
define paksapto = Character("Pak Sapto", color="#7a8a5a")
define paksunar = Character("Pak Sunar", color="#5a6a8a")

## -----------------------
## VARIABEL GLOBAL
## -----------------------
default player_name = "Akur"
default tama_trust = 0
default maria_trust = 0
## tama_trust > 0  = Tama merasa nyaman / percaya ke player
## tama_trust < 0  = Tama merasa waspada / enggan ke player
## tama_trust == 0 = netral (default sebelum interaksi taman)
## maria_trust mengikuti pola yang sama, dipakai mulai Day 4

## -----------------------
## IMAGE & AUDIO PLACEHOLDER
## Ganti path di bawah ini dengan aset asli kalian
## -----------------------
image bg radio room = "bg_radio_room.png"
image bg classroom = "bg_classroom.png"
image bg park = "bg_park.png"

image tama normal = "tama_normal.png"
image tama nervous = "tama_nervous.png"
image tama relieved = "tama_relieved.png"
image tama guarded = "tama_guarded.png"
image tama happy = "tama_happy.png"
image tama scared = "tama_scared.png"
image tama gelisah = "tama_gelisah.png"
image tama menyesal = "tama_menyesal.png"

image maria sinis = "maria_sinis.png"
image maria marah = "maria_marah.png"
image maria panik = "maria_panik.png"

image paksapto ramah = "paksapto_ramah.png"
image paksunar tegas = "paksunar_tegas.png"

image bg lorong = "bg_lorong.png"
image bg gerbang = "bg_gerbang.png"
image bg markas = "bg_markas.png"
image bg kelas hujan = "bg_kelas_hujan.png"
image bg keramaian = "bg_keramaian.png"

audio radio_static = "audio/radio_static.ogg"
audio sfx_bell = "audio/bell.ogg"
audio sfx_bruukk = "audio/bruukk.ogg"
audio sfx_hujan = "audio/hujan.ogg"


## =========================================================
## SISTEM INVENTORI
## =========================================================
## default inventory: dict {item_id: True} berisi barang yang
## sudah dimiliki player. Data detail tiap barang (nama,
## deskripsi, gambar, tipe) disimpan terpisah di item_data
## supaya save file tetap ringan.
## -----------------------------------------------------------
default inventory = []

init python:

    # -----------------------------------------------------
    # DATABASE BARANG
    # type "evidence"   = bukti permanen, tersimpan terus untuk
    #                      dicocokkan / ditunjukkan ke NPC lain.
    # type "consumable" = barang sekali pakai, otomatis hilang
    #                      dari inventori setelah dipakai lewat
    #                      use_item().
    # -----------------------------------------------------
    item_data = {

        "kertas_kode": {
            "name": "Kertas Kode Misterius",
            "description": "Secarik kertas berisi deretan angka acak yang ditemukan tergeletak di lorong sepi. Sepertinya berhubungan dengan kasus siswa yang menghilang.",
            "image": "item_kertas_kode.png",
            "type": "evidence",
        },

        "petunjuk_tama": {
            "name": "Catatan Rahasia Tama",
            "description": "Beberapa lembar catatan milik Tama yang berisi kejanggalan-kejanggalan yang ia amati sendiri di sekolah. Bisa jadi petunjuk penting.",
            "image": "item_catatan_tama.png",
            "type": "evidence",
        },

        "senter_kecil": {
            "name": "Senter Kecil",
            "description": "Senter kecil dengan baterai yang sudah agak lemah. Hanya cukup untuk sekali pemakaian di tempat gelap.",
            "image": "item_senter.png",
            "type": "consumable",
        },

        "tas_tama": {
            "name": "Tas Sekolah Tama",
            "description": "Tas sekolah milik Tama yang ditemukan tercecer oleh Maria, lengkap dengan noda darah di talinya. Kemungkinan berisi petunjuk lain di dalamnya.",
            "image": "item_tas_tama.png",
            "type": "evidence",
        },

    }

    def add_item(item_id):
        """Menambahkan barang ke inventori jika belum dimiliki."""
        if item_id not in inventory:
            inventory.append(item_id)
            data = item_data[item_id]
            renpy.notify("Barang didapatkan: %s" % data["name"])
        else:
            renpy.notify("%s sudah ada di inventorimu." % item_data[item_id]["name"])

    def has_item(item_id):
        """Mengecek apakah suatu barang sudah dimiliki player."""
        return item_id in inventory

    def use_item(item_id):
        """
        Memakai barang. Barang bertipe 'consumable' akan otomatis
        dihapus dari inventori setelah dipakai. Barang bertipe
        'evidence' tetap disimpan (dianggap 'ditunjukkan', bukan
        dihabiskan).
        """
        if item_id not in inventory:
            return False
        if item_data[item_id]["type"] == "consumable":
            inventory.remove(item_id)
            renpy.notify("%s telah digunakan." % item_data[item_id]["name"])
        return True


## -----------------------------------------------------------
## SCREEN: tombol pembuka inventori, tampil terus di pojok layar
## -----------------------------------------------------------
screen inventory_button():
    zorder 100

    frame:
        xalign 1.0
        yalign 0.0
        xoffset -20
        yoffset 20
        background "#000000aa"
        padding (14, 8)

        textbutton "🎒 Inventori ([len(inventory)])":
            text_color "#ffffff"
            action Show("inventory_screen")


## -----------------------------------------------------------
## SCREEN: isi inventori
## -----------------------------------------------------------
screen inventory_screen():
    modal True
    zorder 200

    frame:
        align (0.5, 0.5)
        xsize 900
        ysize 560
        background "#1a1a1aee"

        vbox:
            spacing 10
            xfill True

            text "INVENTORI & BUKTI" size 34 color "#ffffff" xalign 0.5

            null height 10

            viewport:
                xsize 860
                ysize 400
                scrollbars "vertical"
                mousewheel True
                draggable True

                vbox:
                    spacing 18

                    if not inventory:
                        text "Belum ada barang atau bukti yang dikumpulkan." italic True color "#aaaaaa"

                    for _item_id in inventory:
                        $ _data = item_data[_item_id]
                        frame:
                            background "#2a2a2add"
                            xfill True
                            padding (16, 12)
                            hbox:
                                spacing 16
                                add _data["image"] xsize 90 ysize 90
                                vbox:
                                    spacing 4
                                    text _data["name"] size 24 bold True color "#ffffff"
                                    text _data["description"] size 16 color "#cccccc" xsize 620
                                    if _data["type"] == "consumable":
                                        text "(Barang sekali pakai)" size 14 color "#e0a05a"
                                    else:
                                        text "(Bukti permanen)" size 14 color "#5ab0e0"

            textbutton "Tutup":
                xalign 0.5
                text_size 22
                action Hide("inventory_screen")


## =========================================================
## OPENING
## =========================================================
label start:

    show screen inventory_button

    scene bg radio room
    play sound radio_static

    narrator "*suara gemerisik*"

    radio "Sebuah radio layanan informasi darurat dalam tiga bulan terakhir menyiarkan tentang beberapa siswa yang dinyatakan menghilang di sebuah sekolah yang berjarak tak jauh dari sebuah taman."

    radio "Pihak sekolah menyatakan dan menyangkal tentang rumor menghilangnya beberapa siswa dalam sekolah tersebut dengan mengatakan bahwa siswa-siswi yang dinyatakan menghilang tersebut hanya pindah sekolah."

    radio "Hal ini menuai banyak sekali kritik tajam dari beberapa siswa-siswi di sekolah itu maupun pihak keluarga yang mengaku bahwa siswa-siswi yang menghilang sama sekali tidak bisa dihubungi ataupun melihat nama mereka dalam daftar murid di sekolah lain."

    narrator "(gemerisik)"

    radio "Pada akhir pernyataan pihak sekolah, mereka menghimbau kepada seluruh siswa-siswi untuk tetap waspada dan menjaga diri dari hal apapun yang membahayakan keselamatan."

    mc "Ini situasinya mendesak ya? Sekolah yang seharusnya menjadi lingkungan yang sehat untuk belajar dan menambah wawasan malah menjadi tempat kejahatan yang seharusnya tidak pernah terjadi."

    mc "Sepertinya aku harus turun tangan untuk mengusutnya. Sebenarnya banyak sekali celah dan hal janggal yang mencurigakan, untuk saat ini sebaiknya aku berfokus untuk mengumpulkan bukti-bukti dan memperkuat dugaanku."

    mc "Aku harus menyamar."

    jump day1


## =========================================================
## DAY 1
## =========================================================
label day1:

    scene bg classroom
    play sound sfx_bell

    narrator "Pagi telah tiba, murid memasuki kelas dan terdengar bunyi bel."

    guru "Selamat pagi, anak-anak! Di pagi yang cerah dan bahagia ini seharusnya kalian sudah tahu bahwa hari ini kita kedatangan murid baru."

    guru "Silahkan masuk, nak. Ayo, perkenalkan dirimu di depan kelas."

    mc "Halo semuanya, saya [player_name]. Saya pindahan dari SMK Bangsa Indah dan tinggal di Jl. Mawar Indah blok C."

    mc "Alasan kepindahan saya adalah karena pekerjaan orang tua saya yang membuat kami sekeluarga akhirnya pindah ke daerah ini. Salam kenal semuanya."

    guru "Baik, nak [player_name], terima kasih atas perkenalannya dan selamat datang di kelas ini. Untuk bangkumu, kamu duduk di sebelah Tama ya, nak."

    mc "Baik, Bu. Terima kasih."

    # duduk di tempat
    show tama normal

    mc "Hi, nama kamu Tama ya? Salam kenal ya, aku [player_name]."

    show tama nervous

    tama "I-iya, salam kenal, s-semoga kita bisa berkenal akrab."

    hide tama

    jump park_scene


## =========================================================
## SKIP ISTIRAHAT - ADEGAN TAMAN
## =========================================================
label park_scene:

    scene bg park

    narrator "Tama duduk di taman sambil panik saat dihampiri oleh [player_name]."

    show tama nervous

    mc "Eh, loh, tunggu dulu, Tama."

    tama "Kamu mau apa?! (panik)"

    ## -------------------------------------------------
    ## PERCABANGAN UTAMA: sikap player terhadap Tama
    ## -------------------------------------------------
    menu:
        "Bagaimana [player_name] menanggapi Tama?"

        "Jangan takut, aku cuma mau makan bareng.":
            $ tama_trust += 1
            jump park_friendly

        "(bersikap dingin) Santai aja, aku ga tertarik sama urusanmu kok.":
            $ tama_trust -= 1
            jump park_cold


## ---------------------------------------------------------
## CABANG RAMAH
## ---------------------------------------------------------
label park_friendly:

    mc "Jangan takut, aku cuma mau makan bareng, loh."

    show tama relieved

    tama "Oh... gitu ya... (wajah lega)"

    narrator "[player_name] akhirnya duduk di sebelah Tama."

    mc "Kamu kenapa? Kelihatannya waspada banget."

    show tama nervous

    tama "Oh, gapapa kok. Aku cuma... (bergumam lalu diam)"

    mc "Cuma...? (wajah penasaran)"

    tama "Engga, gapapa. Kayaknya kalaupun dijelaskan kamu juga ga bakalan ngerti."

    mc "Iya jelas aku ga bakalan ngerti, kamu aja belum jelasin kok."

    tama "(menggeleng dan menyerahkan sesuatu) Ya pokoknya sulit, deh. Aku duluan."

    narrator "Tama buru-buru mengemas barangnya."

    mc "Loh, Tama! Tunggu—"

    hide tama
    narrator "Tama pergi tanpa menoleh lagi."

    mc "(terdiam sejenak) ...Aneh banget. Sebenernya dia mau nyampein apa, sih?"

    jump classroom_scene


## ---------------------------------------------------------
## CABANG DINGIN
## Sikap dingin membuat Tama semakin waspada dan tertutup
## ---------------------------------------------------------
label park_cold:

    mc "(nada datar) Santai aja, aku ga tertarik sama urusanmu kok."

    show tama guarded

    tama "...oh. (menatap curiga) Ya udah kalau gitu."

    narrator "Tama tetap menjaga jarak, raut wajahnya semakin tertutup."

    mc "(dingin) Aku cuma kebetulan lewat sini kok."

    tama "(pelan) ...kirain mau ngapa-ngapain. Ya udah, aku duluan aja."

    narrator "Tama buru-buru berdiri dan pergi tanpa menoleh lagi, kali ini lebih cepat dari sebelumnya."

    hide tama

    mc "(menghela nafas) ...harusnya tadi aku ga usah sedingin itu."

    jump classroom_scene


## =========================================================
## KEMBALI KE KELAS
## =========================================================
label classroom_scene:

    scene bg classroom

    narrator "Setelah masuk ke kelas, pelajaran akhirnya dimulai kembali."

    guru "...jadi, pada dasarnya nilai praksis yang terkandung dalam nilai-nilai Pancasila mencakup..."

    show tama normal

    mc "(berbisik) Tama, kamu ada penghapus tidak? Boleh aku pinjam?"

    ## -------------------------------------------------
    ## Reaksi Tama tergantung tama_trust dari adegan taman
    ## -------------------------------------------------
    if tama_trust >= 1:
        jump eraser_friendly
    else:
        jump eraser_cold


## ---------------------------------------------------------
## Jika Tama masih percaya / nyaman -> mau berbagi & akrab
## ---------------------------------------------------------
label eraser_friendly:

    tama "Hah? Penghapus? Ada, lah. Nih. (memberikan penghapus)"

    mc "(menerima, tapi kemudian ia terdiam dan menunjuk ke arah bentuk penghapusnya) Eh, kamu juga suka main game ini ya? Aku suka sama karakter ini, loh."

    show tama happy

    tama "Eh? Serius?"

    narrator "Mulai dari percakapan sederhana itu, tak terasa mereka perlahan-lahan mulai akrab."

    jump end_day1


## ---------------------------------------------------------
## Jika Tama enggan / trust negatif -> menolak bekerja sama
## ---------------------------------------------------------
label eraser_cold:

    show tama guarded

    tama "(ragu-ragu) ...ga punya."

    mc "Yakin? Sepertinya tadi aku lihat kamu—"

    tama "(memotong, singkat) Udah bilang ga punya."

    narrator "Tama kembali fokus ke buku catatannya, enggan melanjutkan obrolan."

    mc "(dalam hati) ...sepertinya dia masih belum mau membuka diri ke aku. Mungkin sikapku tadi salah."

    narrator "Sikap dingin [player_name] di taman membuat Tama semakin menjaga jarak dan enggan bekerja sama untuk saat ini."

    jump end_day1


## =========================================================
## PENUTUP HARI 1
## =========================================================
label end_day1:

    scene bg classroom with dissolve

    if tama_trust >= 1:
        narrator "Hubungan [player_name] dan Tama mulai terjalin baik. Mungkin ke depannya Tama akan lebih terbuka untuk bekerja sama mengungkap misteri sekolah ini."
    else:
        narrator "Tama masih menyimpan jarak dengan [player_name]. Kepercayaannya harus dibangun kembali sebelum ia mau bekerja sama."

    jump day2


## =========================================================
## DAY 2
## =========================================================
label day2:

    scene bg lorong

    narrator "[player_name] dan Tama berjalan bersama sembari mengobrol tentang game yang mereka senangi. Tanpa sadar mereka berjalan melewati lorong yang lumayan sepi dan tidak sengaja melihat beberapa orang."

    play sound sfx_bruukk
    narrator "*bruukk*"

    show maria sinis

    maria "Pfft, serius kamu mau macem-macem sama kita? Kamu beneran mau menghilang kayak mereka ya? Hahahahaha!"

    narrator "Merasa kesal karena ucapan siswi itu, [player_name] dan Tama menghampiri mereka."

    mc "(kesal) Kamu beneran ga tau malu ya? Merundung siswi lain dan sok berkuasa begitu. Dan soal menghilangnya siswa-siswi… bisa ga, ga usah kamu ungkit-ungkit? Bikin muak, tau, ga?"

    show tama scared

    tama "U-udah, [player_name], jangan bikin urusan dengan dia."

    show maria marah

    maria "Lu gatau gua siapa ya, kampung. Gua anak dari pejabat yang mendonatur sekolah ini, siapa yang berani sama gua, habis di tangan gua, haha."

    mc "Kamu siapa sih? Jabatan ayahmu ga bikin kita takut. Kamu sadar ga sikapmu ini sangat mempermalukan keluargamu? Keluargamu ngajarin kamu jadi kayak gini ya? Sikap sombong dan berkuasa?"

    mc "(dalam hati) Dia pasti satu komplotan dengan kasus itu."

    maria "Sok ngatur banget sih lu?! Lo kalau ga tau apa-apa soal gua ga usah nyolot! Mana sok tau banget lagi. Gue Maria, kalau lo mau tau."

    maria "(menunjuk-nunjuk) Dan kalau lo emang mau ikut campur urusan gua dan nyari perkara sama gua, boleh aja. Gua tandain muka lo!"

    narrator "Maria pergi sembari menyenggol bahu [player_name]."

    hide maria

    mc "Cuma anak pejabat tapi gayanya udah kayak yang punya Bumi aja."

    show tama nervous

    tama "Sebaiknya kamu jangan pernah cari masalah ke dia, deh."

    mc "Kenapa? Justru orang kaya gitu perlu dikasih pelajaran, tau."

    show tama scared

    tama "JANGAN, o-orang itu cukup menakutkan, pernah ada… (terdiam)"

    tama "Ah, lupakan, seharusnya kamu gaperlu tau."

    mc "Kenapa?"

    tama "Gapapa, itu topik yang agak sensitif buat dibahas."

    tama "Yuk balik kelas aja, bentar lagi pelajaran matematika, nih."

    narrator "Tama berjalan lebih dulu, meninggalkan [player_name] yang menatap punggung Tama dengan curiga."

    hide tama

    mc "(heran) Perasaan ngehindar mulu, dia-nya."

    narrator "Di saat hendak kembali, [player_name] menemukan sebuah kertas berisi angka yang ditulis acak seperti sebuah kode."

    mc "Hah? Apa ini?"

    $ add_item("kertas_kode")

    show tama normal

    tama "Hei, kenapa melamun, ayo kembali."

    mc "Eh, iya, sebentar, aku menjatuhkan uang sakuku."

    jump satpam_scene


## ---------------------------------------------------------
## BERTEMU PAK SAPTO
## ---------------------------------------------------------
label satpam_scene:

    scene bg lorong

    show paksapto ramah

    mc "Selamat pagi, Pak."
    tama "Selamat pagi, Pak."

    paksapto "Hoho, pagi, cah. Loh, sek. Kamu cah baru, to?"

    mc "Iya, Pak."

    paksapto "Semoga nyaman yo di sekolah ini, temen-temene enak, to?"

    mc "Baik, Pak, siap. Kalau gitu saya dan Tama izin kembali ke kelas ya, Pak."

    paksapto "O ya, semangat belajarnya yo."

    mc "Wokay, siap, Pak."

    hide paksapto

    scene bg classroom

    narrator "Tiba di depan pintu kelas, [player_name] mencekal tangan Tama, menghentikannya yang belum sempat membuka pintu."

    mc "Tama, kamu nyadar ga tadi tangan Pak Sapto bau amis?"

    show tama scared

    tama "Ee… iya, habis makan daging—(terlihat ketakutan)"

    tama "Eh, maksudnya habis makan ikan kayaknya."

    narrator "Ucapan Tama membuat [player_name] kembali curiga."

    hide tama

    narrator "Dan mereka pun akhirnya kembali ke kelas dan mengikuti pelajaran seperti biasa. Saat pelajaran telah selesai, [player_name] berjalan menuju ke gerbang sekolah untuk pulang."

    scene bg gerbang

    show maria sinis

    maria "Woy, kampung. Belum pulang ya, ternyata. Hati-hati di jalan, siapa tau besok lu ga berangkat sampai kapanpun itu, hahahahaha."

    hide maria

    mc "(emosi) Ck."

    jump day3


## =========================================================
## DAY 3
## =========================================================
label day3:

    scene bg kelas hujan
    play sound sfx_hujan

    narrator "Siang itu hujan datang, mengguyur seisi kota dengan begitu derasnya. [player_name] yang sedang bersiap-siap untuk pulang tidak sengaja melihat Tama berdiri dengan gelisah sendirian di dekat jendela kelas."

    narrator "Suasana di kelas cukup sepi karena hampir seisi kelas sudah pulang. Karena merasa ada yang tidak beres, [player_name] tanpa mengatakan apapun, langsung menyeretnya ke pojok belakang kelas dan mulai bertanya."

    show tama gelisah

    mc "Tama, kamu lagi apa? (menepuk bahu Tama tiba-tiba)"

    tama "(tersentak kaget) Eh! Oh… kamu bikin aku kaget aja."

    mc "Santai aja kali, kenapa? Masih kepikiran soal omongan Maria kemarin ya?"

    tama "(menggeleng) Bukan kok, (menunduk) aku cuma ngerasa waktu pulang sekolah kemarin perasaanku makin ga enak."

    mc "Ga enak gimana? Oh, dan soal tangan Pak Sapto yang bau amis itu. Kamu sebenernya tau sesuatu kan? Aku selalu ngerasa kamu ngehindarin aku setiap aku nanya soal itu. Sebenarnya kamu kenapa, sih?"

    narrator "Tama terdiam, ia melirik ke arah lorong dan melihat Pak Sapto melewati kelas mereka dengan menyeret tempat sampah beroda dengan perlahan."

    tama "Disini rasanya ga ada tempat yang aman. Semenjak siswa-siswi menghilang, aku merasa kayak terus diawasi dan juga… gerak-gerik beberapa orang di sekolah ini mulai terasa aneh."

    mc "Oh, jadi perasaanku selama ini bener, ya? Kamu beneran ada nyembunyiin sesuatu. Kertas angka acak yang kemarin kutemui di lorong sepi itu… juga ada hubungannya sama kamu, kan?"

    show tama scared

    tama "(melebarkan matanya) Loh, astaga! Kamu yang ambil kertas itu?!!..."

    mc "I-iya, aku nemu pas hari itu, pas abis ketemu Maria di lorong. Kenapa emangnya? Kamu tau soal ini?"

    narrator "Tama terdiam cukup lama, matanya bergerak gelisah mengawasi lorong lewat kaca jendela. Tangannya meremas ujung baju seragamnya sendiri."

    show tama gelisah

    tama "Itu… itu bukan angka biasa. Itu semacam… (berhenti, menggigit bibir) ah, susah jelasinnya."

    mc "Coba aja dulu, sedikit juga gapapa. Tama, please."

    tama "(menghela nafas pelan) Beberapa bulan lalu, aku sempet nemuin kertas yang sama di loker aku. Awalnya aku pikir itu cuma iseng, tapi terus… (diam sejenak, seperti menahan sesuatu) terus mulai ada yang hilang."

    mc "Maksudnya? Itu kayak… kode buat nentuin siapa yang bakal jadi korban selanjutnya?"

    tama "Aku—aku juga ga yakin, tapi setiap kali kertas kayak gitu muncul, ga lama abis itu pasti ada yang hilang. Makanya pas kamu bilang nemu kertas serupa, aku… (menutup mulut, terlihat panik)"

    mc "Tama, kalo kamu tau siapa yang naruh kertas itu, atau ada hubungannya sama siapa, tolong—"

    show tama scared

    tama "(memotong, suaranya bergetar) Aku ga bisa cerita semuanya sekarang. Ini… ini lebih rumit dari yang kamu kira, [player_name]. Kalo aku ngomong sembarangan, bisa bahaya buat—"

    narrator "Tama tiba-tiba terdiam, seolah baru sadar sudah kebablasan bicara. Ia menoleh cepat ke arah lorong yang sepi, lalu menatap [player_name] dengan raut wajah campur aduk antara takut dan menyesal."

    show tama menyesal

    tama "…lupain aja yang barusan. Aku cuma capek aja, kepikiran macem-macem gara-gara hujan."

    narrator "Tama masih terlihat ragu, seperti menimbang apakah ia harus benar-benar mempercayai [player_name] atau tidak. Ini mungkin kesempatan untuk meyakinkannya."

    ## -------------------------------------------------
    ## MEKANIK: pilih dialog yang tepat untuk meyakinkan
    ## Tama agar mau memberikan barang buktinya.
    ## Opsi "tunjukkan kertas kode" hanya muncul kalau
    ## player sudah punya item "kertas_kode".
    ## -------------------------------------------------
    menu:
        "Bagaimana [player_name] coba meyakinkan Tama?"

        "Tunjukkan kertas kode yang kutemukan kemarin sebagai bukti niat baik." if has_item("kertas_kode"):
            jump tama_convince_evidence

        "Aku janji bakal rahasiain apapun yang kamu ceritain ke aku.":
            jump tama_convince_promise

        "(memaksa) Kamu harus cerita semuanya sekarang, atau aku laporin ke guru!":
            jump tama_convince_force


## ---------------------------------------------------------
## OPSI 1 - Menunjukkan bukti (paling meyakinkan)
## ---------------------------------------------------------
label tama_convince_evidence:

    mc "Tama, coba lihat ini. (menunjukkan kertas kode) Aku ga bakal cari masalah, aku cuma pengen bantu. Anggap ini bukti kalau aku serius mau bantu nyelesain masalah ini bareng-bareng."

    show tama gelisah

    tama "(menatap kertas itu lama) ...kamu benar-benar serius, ya?"

    $ tama_trust += 1
    $ add_item("petunjuk_tama")

    jump tama_convince_success


## ---------------------------------------------------------
## OPSI 2 - Janji menjaga rahasia
## Hasilnya tergantung tama_trust yang sudah terkumpul
## sejak Day 1 (dari sikap ramah/dingin di taman).
## ---------------------------------------------------------
label tama_convince_promise:

    mc "Aku janji bakal rahasiain apapun yang kamu ceritain ke aku. Kamu bisa percaya aku, Tama."

    if tama_trust >= 1:
        show tama gelisah
        tama "(menghela nafas panjang) ...oke. Aku percaya kamu."
        $ add_item("petunjuk_tama")
        jump tama_convince_success
    else:
        show tama guarded
        tama "(menggeleng pelan) ...maaf, aku belum bisa percaya segampang itu. Apalagi sama kamu."
        jump tama_convince_partial


## ---------------------------------------------------------
## OPSI 3 - Memaksa (salah, membuat Tama makin tertutup)
## ---------------------------------------------------------
label tama_convince_force:

    mc "(memaksa) Kamu harus cerita semuanya sekarang, atau aku laporin ke guru!"

    show tama scared

    tama "(mundur selangkah, matanya berkaca-kaca) ...kenapa kamu jadi kayak gini? Aku kira kamu beda."

    $ tama_trust -= 1

    jump tama_convince_fail


## ---------------------------------------------------------
## HASIL: BERHASIL - Tama memberikan barang buktinya
## ---------------------------------------------------------
label tama_convince_success:

    show tama menyesal

    tama "Mungkin aku akan memberikanmu beberapa item yang mengganggu aku kali ini, mungkin ini bisa saja menjadi sebuah petunjuk lebih detail untuk menangani kasus ini."

    tama "Aku tau kamu masuk ke sekolah ini demi memecahkan kasus, sudah dari awal aku sudah menyadarinya."

    narrator "Tama menyerahkan sebuah catatan berisi kejanggalan-kejanggalan yang selama ini ia simpan sendiri."

    jump tama_after_convince


## ---------------------------------------------------------
## HASIL: SETENGAH BERHASIL - Tama tidak kasih barang,
## tapi masih mau kasih sedikit petunjuk lisan.
## ---------------------------------------------------------
label tama_convince_partial:

    tama "(menatap ragu, agak menjaga jarak) ...tapi aku masih belum yakin bisa sepenuhnya percaya sama kamu. Sikapmu ke aku beberapa hari ini juga bikin aku susah buat terbuka."

    tama "Meski begitu... mungkin aku akan kasih sedikit petunjuk. Cuma sedikit. Aku tau kamu masuk ke sekolah ini demi memecahkan kasus, dari awal aku juga udah sadar."

    narrator "Tama tidak memberikan barang apapun kali ini, hanya sepotong informasi lisan yang samar."

    jump tama_after_convince


## ---------------------------------------------------------
## HASIL: GAGAL - Tama menolak sepenuhnya
## ---------------------------------------------------------
label tama_convince_fail:

    tama "(suara bergetar) ...aku ga akan cerita apa-apa kalo caranya kayak gini."

    narrator "Tama menutup diri sepenuhnya. Ia tidak memberikan barang maupun informasi apapun kali ini, dan kepercayaannya terhadap [player_name] semakin menipis."

    jump tama_after_convince


## ---------------------------------------------------------
## KELANJUTAN BERSAMA, APAPUN HASIL PERCAKAPAN DI ATAS
## ---------------------------------------------------------
label tama_after_convince:

    mc "Tama, kamu jangan bohong lagi deh sama aku."

    tama "(memaksakan senyum tipis) Besok aja ya, aku cerita lebih jelas kalo emang udah waktunya. Sekarang udah sore banget, mendingan kita pulang duluan."

    narrator "Tama buru-buru mengambil tasnya dan berjalan keluar kelas lebih dulu, meninggalkan [player_name] yang masih berdiri termenung menatap punggungnya menghilang di ujung lorong yang gelap karena hujan."

    hide tama

    mc "(dalam hati) Besok, katanya… semoga aja beneran sempet."

    show paksunar tegas

    paksunar "Loh, kalian kok belum pulang, sudah jam segini loh, waktu sudah hampir petang, segera pulang ke rumah!"

    show tama scared

    tama "(panik) I-iya, Pak, kami akan segera pulang."

    paksunar "Ya sudah, saya pulang dulu!"

    hide paksunar
    hide tama

    jump markas_scene


## =========================================================
## MARKAS - MENGUMPULKAN BUKTI
## =========================================================
label markas_scene:

    scene bg markas

    narrator "[player_name] mengeluarkan beberapa barang yang telah terkumpul."

    mc "Ini sudah banyak bukti yang dapat dicocoklogikan, namun aku masih tetap butuh bukti yang akurat."

    mc "Kebanyakan di sekolah itu orangnya sangat mencurigakan semuanya."

    jump day4


## =========================================================
## DAY 4
## =========================================================
label day4:

    scene bg keramaian

    narrator "Suasana pagi itu ramai sekali oleh kerumunan siswa yang berbisik-bisik di depan mading sekolah."

    mc "Kenapa semua orang sangat ramai disini, apa yang sedang terjadi?"

    narrator "[player_name] menghampiri dan membaca sebuah pengumuman berisi info orang hilang."

    mc "TAMAAA??? Dia kemana, kenapa tiba-tiba menghilang, ada sesuatu yang tidak beres. Kemarin apakah kita dipantau?"

    play sound sfx_bell

    scene bg classroom

    narrator "Suara bel berbunyi dan [player_name] bergegas masuk ke kelas."

    guru "Anak-anak, tetap jaga diri kalian ya. Semoga teman kita Tama segera ditemukan. Ibu sangat khawatir, dikarenakan tadi semalam orang tua Tama menghubungi ibu karena Tama tidak kunjung pulang ke rumah hingga saat ini."

    narrator "\"Baik, Bu,\" jawab murid-murid serempak."

    mc "(dalam hati) Aku harus mencari tahu nanti."

    jump park_day4


## ---------------------------------------------------------
## ISTIRAHAT - MARIA MENGHAMPIRI DENGAN PANIK
## ---------------------------------------------------------
label park_day4:

    scene bg park

    narrator "Bel istirahat berbunyi. Maria menghampiri [player_name] dengan panik di taman."

    show maria panik

    maria "[player_name]! SINI, ADA SESUATU YANG PENTING!"

    mc "Kenapa kamu panik? Biasanya jadi seorang pembully, sekarang kok mental ciut."

    maria "Diam, ini bukan saat yang tepat untuk kamu membenciku!"

    maria "Semalam aku pergi ke cafe, namun aku melihat Tama pulang sendirian. Sudah biasa aku melihatnya, namun di saat aku menikmati seteguk kopi, aku mendengar jeritan Tama yang hanya aku dengar."

    maria "Aku pergi keluar dan di sana ada cucuran darah beserta tas sekolah Tama yang ditinggal. Aku bawa pulang, namun aku tak melihat Tama di mana. Kota di sini sangat menyeramkan."

    narrator "Maria terlihat gemetar, matanya berkaca-kaca menahan tangis. Bagaimana [player_name] meresponnya mungkin akan menentukan seberapa jauh Maria mau bekerja sama."

    ## -------------------------------------------------
    ## MEKANIK: pilihan dialog menentukan apakah Maria
    ## mau memberi barang tambahan (bonus) sekarang.
    ## -------------------------------------------------
    menu:
        "Bagaimana [player_name] merespon Maria?"

        "Tenang, Maria. Cerita pelan-pelan, aku dengerin kok.":
            $ maria_trust += 1
            jump maria_respond_empati

        "(dingin) Kenapa aku harus percaya omongan seorang pembully kayak kamu?":
            $ maria_trust -= 1
            jump maria_respond_dingin


## ---------------------------------------------------------
## RESPON EMPATI - Maria jadi lebih percaya & memberi bonus
## ---------------------------------------------------------
label maria_respond_empati:

    show maria panik

    maria "(menghela nafas, sedikit lebih tenang) ...makasih. Aku emang lagi takut banget, ga tau lagi harus cerita ke siapa."

    maria "Nih, sebelum kamu pulang, bawa ini aja. (menyerahkan sebuah senter kecil) Aku selalu bawa-bawa ini buat jaga-jaga, tapi kayaknya kamu yang lebih butuh sekarang."

    $ add_item("senter_kecil")

    jump maria_after_respond


## ---------------------------------------------------------
## RESPON DINGIN - Maria kesal, tidak ada bonus barang
## ---------------------------------------------------------
label maria_respond_dingin:

    show maria marah

    maria "(menatap tajam, suaranya bergetar menahan marah) ...ya udah kalo gitu, terserah kamu mau percaya apa nggak. Aku cuma coba jujur ke kamu."

    narrator "Maria memilih untuk tidak membagikan hal lain kepada [player_name] selain ceritanya barusan."

    jump maria_after_respond


## ---------------------------------------------------------
## KELANJUTAN BERSAMA
## ---------------------------------------------------------
label maria_after_respond:

    mc "Lalu di mana tas tersebut? Kamu bawa?"

    maria "TENTU TIDAK, aku akan memberikanmu tas Tama ke rumahku. Di sini sangat tidak aman, aku takut ada orang yang mengintaiku."

    mc "Baiklah, aku tunggu pulang sekolah."

    hide maria

    ## NOTE untuk kelanjutan (Day 5):
    ## Saat adegan penyerahan tas benar-benar terjadi di rumah
    ## Maria, tambahkan baris berikut di titik yang tepat:
    ##     $ add_item("tas_tama")
    ## Nilai maria_trust dari Day 4 ini bisa dipakai untuk
    ## menentukan seberapa kooperatif/detail Maria saat itu.

    narrator "TO BE CONTINUED..."

    return
