import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Загружаем JSON с текстами
json_path = "../../data/fomc_minutes.json"
with open(json_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# Преобразуем JSON в DataFrame
df = pd.DataFrame(data)

# Добавляем колонку с длиной текста
df["length"] = df["text"].apply(len)

# Преобразуем дату в формат datetime и извлекаем год
df["year"] = pd.to_datetime(df["date"]).dt.year

# Убираем фон
sns.set(style="white", rc={"axes.facecolor": (0, 0, 0, 0)})

# Создаём фигуру и оси
fig, ax = plt.subplots(figsize=(8, 6))

# Делаем KDE plot с эффектом Ridgeline
sns.kdeplot(
    data=df, x="length", hue="year", fill=True, multiple="stack",
    palette="Blues", alpha=0.8, linewidth=1.2
)

# Настройки осей
ax.set_xlabel("Длина текста (символы)", fontsize=12)
ax.set_ylabel("Год", fontsize=10)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Добавляем подписи годов слева
years = sorted(df["year"].unique(), reverse=True)
for i, y in enumerate(years):
    ax.text(df["length"].min(), i * (df["length"].max() - df["length"].min()) / len(years),
            str(y), fontsize=8, ha="right", va="center")

plt.title("Распределение длин текстов по годам", fontsize=14)
plt.show()
