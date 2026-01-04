# constants.py

# ID2LABEL: Modelin sayıları kelimeye çevirdiği sözlük
# DİKKAT: Buradaki isimler (value), INFO_MAP'teki anahtarlarla AYNI olmalı.
ID2LABEL = {
    0: "shipping",            # Kargo
    1: "discount_campaign",   # İndirim ve Kampanya
    2: "product_stock",       # Stok (Eskiden stock_availability idi, artık product_stock)
    3: "account_payment",     # Hesap ve Ödeme
    4: "return_cancel",       # İade ve İptal
    5: "customer_support"     # Müşteri Hizmetleri
}

# INFO_MAP: Chatbot'un vereceği hazır cevaplar
# DİKKAT: Buradaki anahtarlar (keys), yukarıdaki ID2LABEL isimleriyle BİREBİR aynı olmalı.
INFO_MAP = {
    "shipping": "Siparişinizin durumunu 'Siparişlerim' sayfasından takip edebilirsiniz. Kargo takip numarası, paketiniz kargoya verildiğinde SMS ve e-posta ile iletilir.",

    "discount_campaign": "İndirim kuponunuzu ödeme ekranındaki 'Kupon Kodu' alanına girebilirsiniz. Kampanyalarımız dönemsel olarak değişmektedir.",

    # DİKKAT: Burası 'product_stock' olmalı, çünkü ID2LABEL[2] böyle diyor.
    "product_stock": "Stokta olmayan ürünler için 'Gelince Haber Ver' butonunu kullanabilirsiniz. Ön sipariş ürünleri hakkında bilgi ürün detay sayfasında yer almaktadır.",

    "account_payment": "Hesap oluşturmak için sağ üstteki 'Giriş Yap / Üye Ol' menüsünü kullanabilirsiniz. Ödemelerinizi güvenle yapabilirsiniz.",

    "return_cancel": "Satın aldığınız ürünü 14 gün içinde koşulsuz iade edebilirsiniz. İade talebi oluşturmak için 'Siparişlerim' sayfasına gidip 'Kolay İade' butonuna tıklayın.",

    "customer_support": "Size yardımcı olmak için buradayız! Hafta içi 09:00-18:00 saatleri arasında bize ulaşabilirsiniz."
}
