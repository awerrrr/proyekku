# E-commerce Sales Analysis Dashboard
----
Proyek ini dibuat bertujuan untuk mengisi tugas di kelas Dicoding "Belajar Analisis data dengan Python". Analisis yang dilakukan dalam proyek ini guna mengidentifikasi pola pembelian pelanggan, metode pembayaran yang paling sering digunakan, serta tren penjualan dari waktu ke waktu.

## Datasets
----
Pemrosesan data-data yang akan digunakan:
1. Sumber Dataset: E-Commerce Public Dataset.
2. Struktur Datasets:
   - customers_dataset.csv
   - geolocation_dataset.csv
   - order_items_dataset.csv
   - order_payments_dataset.csv
   - order_reviews_dataset.csv
   - orders_dataset.csv
   - product_category_name_translation.csv
   - products_dataset.csv
   - sellers_dataset.csv
3. Persiapan Datasets:
   - Mengisi nilai yang hilang pada tabel order_reviews, orders dan products.
   - Menghapus nilai duplikat pada tabel geolocation.
   - Mengkonversi kolom-kolom yang mengalami *inaccurate values* pada tabel orders, order_items dan order_reviews.

## Project Cycle
----
1. Pertanyaan Bisnis:
   - Produk apa yang paling sering dibeli pelanggan?
   - Apakah ada pola pembayaran tertentu yang lebih sering digunakan pelanggan?
   - Bagaimana tren penjualan dari waktu ke waktu?
2. Metode Analisis:
+ Data Wrangling:
    
   - Nilai yang Hilang:
     - order_reviews
       - Pada kolom *review_comment_title* dan *review_comment_message* kita melakukan pengisian untuk *missing value* dengan memberikan nilai kosong jika *customer* tidak memberikan reviews.
     - orders
       - Pada data *orders* kita membuat kolom baru untuk membantu menandai pesanan yang hilang, hal ini dikarenakan kita tidak bisa sembarangan mengisi data pada kolom kolom yang mengalami *missing value* yang dimana kesalahan ini bisa di akibatkan oleh pesanan yang belum diproses atau data yang tidak tercatat.
    -  products
      - Di dalam *datasets products* harus dilakukan pengisian nilai kosong/hilang pada kolom *product_category_name* dan beberapa kolom yang berisi nilai numeric pada *datasets products*.
    
    - Duplikasi Data:
      - geolocation
        - Pada *datasets* *geolocation* kita melakukan penghapusan duplikat data secara total untuk menghasilkan data yang mudah dibaca dan tentunya lebih bersih.
    
    - Kesalahan Akurasi Nilai:
      - order_reviews
        - Melakukan perubahan tipe data pada kolom *review_creation_date* dan *review_answer_timestamp* menjadi tipe data *datetime*.
      - orders
        - Melakukan perubahan yang sama seperti pada kolom *order_reviews*.
      - order_items
        - Melakukan perubahan yang sama seperti padda kolom-kolom sebelumnya.
    
+ Exploratory Data Analysis (EDA):
Kita akan mengeksplorasi data untuk keperluan fitur-fitur pada datasets dan menjawab pertanyaan-pertanyaan bisnis yang telah kita tetapkan. Dan menghasilkan *insight* seperti ini:
  - Scatterplot antara geolocation_lat dan geolocation_lng menunjukkan distribusi titik yang membentuk pola wilayah geografis.
  - Hubungan antara geolocation_zip_code_prefix dan koordinat geografis (lat & lng) menunjukkan pola tertentu. Ini berarti kode pos memiliki hubungan kuat dengan lokasi geografis tertentu.

+ Data Visualization
Menggunakan Matplotlib dan Seaborn untuk membuat grafik yang baik dan menampilkan data yang mudah dibaca.

+ Dashboard
Presentasi yang akan kita lakukan setelah mendapatkan semua jawaban dari pertanyaan-pertanyaan bisnis dan menampilkan hasil final dari data EDA yang telah kita dapatkan.

# Setting Environment - Anaconda
'''
conda create --name main-subdic python=3.9
conda activate main-subdic
pip install -r requirements.txt
'''

# Setup Environment - Terminal
'''
mkdir Submission_Dicoding
cd Submission_Dicoding
pipenv install
pipenv shell
pip install -r requirements.txt
'''

# Run Streamlit App
'''
streamlit run dashboard.py
'''
