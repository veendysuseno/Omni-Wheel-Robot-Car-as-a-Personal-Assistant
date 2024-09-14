#import necessary modules
import csv

# Menggunakan slash agar lebih aman
with open('D:/A/Car-Mobil-PA-Omni-Wheel/doc/barcodes.csv', 'rt') as f:
    data = csv.reader(f)
    for row in data:
        print(row)
