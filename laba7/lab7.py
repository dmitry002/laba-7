import csv
import sys
import numpy as np
import matplotlib.pyplot as plt

file_name = "ea7b47a8-b4f7-40a5-b22f-59282570c9b1_Data.csv"
indicator = "Population, total"

countries = []
values = {}
years = []

try:
    with open(file_name, "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader)
        for col in header[4:]:
            years.append(int(col[:4]))
        for row in reader:
            if len(row) < 5 or row[0] == "" or row[3] == "":
                continue
            name = row[0]
            nums = []
            for v in row[4:]:
                if v == ".." or v == "":
                    nums.append(0)
                else:
                    nums.append(float(v))
            countries.append(name)
            values[name] = np.array(nums)
except FileNotFoundError:
    print("Файл", file_name, "не знайдено")
    sys.exit()
except ValueError:
    print("Помилка читання даних з файлу")
    sys.exit()
except Exception as e:
    print("Помилка:", e)
    sys.exit()

years = np.array(years)
country1 = "Ukraine"
country2 = "France"
if country1 not in values or country2 not in values:
    print("У файлі немає даних для", country1, "або", country2)
    sys.exit()
ukraine = values[country1]
france = values[country2]

print("Завантажені країни:", countries)
print("Роки:", years)

plt.figure(figsize=(8, 5))
plt.plot(years, ukraine, label=country1, marker="o")
plt.plot(years, france, label=country2, marker="o")
plt.title(indicator + " (" + country1 + " and " + country2 + ")", fontsize=15)
plt.xlabel("Year", fontsize=12)
plt.ylabel("Population", fontsize=12)
plt.xticks(years)
plt.legend()
plt.grid(True)
plt.show()

country = input("Введіть назву країни (" + country1 + " або " + country2 + "): ").strip()
while country not in countries:
    print("Країни", country, "немає в даних. Доступні:", countries)
    country = input("Введіть назву країни: ").strip()

plt.figure(figsize=(8, 5))
plt.bar(years, values[country], color="teal")
plt.title(indicator + " - " + country, fontsize=15)
plt.xlabel("Year", fontsize=12)
plt.ylabel("Population", fontsize=12)
plt.xticks(years)
plt.grid(True, axis="y")
plt.show()

year = 0
while year not in years:
    try:
        year = int(input("Введіть рік (" + str(years[0]) + "-" + str(years[-1]) + "): "))
        if year not in years:
            print("Такого року немає в даних")
    except ValueError:
        print("Рік має бути числом")

i = list(years).index(year)
data = np.array([ukraine[i], france[i]])
labels = np.array([country1, country2])


def func(pct, allvals):
    absolute = int(np.round(pct / 100 * np.sum(allvals)))
    return f"{pct:.1f}%\n({absolute})"


plt.figure(figsize=(6, 6))
wedges, texts, autotexts = plt.pie(data, labels=labels, autopct=lambda pct: func(pct, data))
plt.title(indicator + " (" + str(year) + ")", fontsize=15)
plt.setp(autotexts, size=9, weight="bold")
plt.show()