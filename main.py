"""n = 5
m = 5
table = [[0] * 5 for _ in range(5)]

for i in range(5):
    for j in range(5):
        if i == j:
            table[i][j] = 1
        else:
            table[i][j] = i + j
print(table)"""
import random

"""t = "я я я лучший крутой дерево пень"

t.split()

dictionary = {}

for word in t.split():
    if word in dictionary:
        dictionary[word] += 1
    else:
        dictionary[word] = 1
for word, count in dictionary.items():
    print(word, count)"""


"""K = 0.1

import asyncio

async def loundary():
    print("Начали стирку")
    await asyncio.sleep(70*K)
    print("Закончили стирку")

async def soup():
    print("Начали варить")
    await asyncio.sleep(60*K)
    print("Закончили варить")

async def tea():
    print("Начали чайник")
    await asyncio.sleep(15*K)
    print("Закончили чайник")

async def async_main():
    await asyncio.gather(loundary(), soup(), tea())

asyncio.run(async_main())"""


"""import asyncio
import aiohttp

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

url = 'https://api.thecatapi.com/v1/images/search?limit=10'

async def download_cat(session: aiohttp.ClientSession, url: str, n: int):
    print(f"Котенок номер {n} скачивается")
    response = await session.get(url)
    response_bytes = await response.read()
    file = open(f'cat{n}.jpg', 'wb')
    file.write(response_bytes)
    file.close()
    print(f"Котенок номер {n} скачался")

async def async_main():
    session = aiohttp.ClientSession()
    response = await session.get(url)
    response_json = await response.json()
    url_cats = []
    for data in response_json:
        url_cats.append(data['url'])
    tasks = []
    for i in range(10):
        tasks.append(download_cat(session, url_cats[i], i))
    await asyncio.gather(*tasks)
    await session.close()

asyncio.run(async_main())"""


"""class Human:
    genom_count = 46

    def __init__(self, name: str, age: int, description: str):
        self.name = name
        self.age = age
        self.description = description

    def show_description(self):
        print(f'{self.name} {self.description}, {self.age} лет')

    @classmethod
    def get_genom_count(cls):
        return cls.genom_count

    @classmethod
    def set_genom_count(cls, count: int):
        cls.genom_count = count

human = Human("Иван", 16, "Кто")"""


"""class Ingridients:
    def __init__(self, calories: float, mass: float):
        self.calories = calories
        self.mass = mass

    def prepare(self) -> float:
        return self.calories

    def get_calories(self) -> float:
        return self.calories

    def get_mass(self) -> float:
        return self.mass

class Bread(Ingridients):
    def prepare(self) -> float:
        self.calories += 10
        self.mass *= 0.8
        return super().prepare()

class Tomato(Ingridients):
    def __init__(self, calories: float, mass: float, color: str) -> None:
        print("Вызывается метод __init__ у Tomato")
        self.color = color
        super().__init__(calories, mass)

    def prepare(self) -> float:
        self.mass -= 10
        return super().prepare()

class Soup(Ingridients):
    def __init__(self, calories: float, salinity: float) -> None:
        print("Вызывается метод __init__ у суп")
        self.salinity = salinity
        super().__init__(calories, mass)

def cook(ings: list[Ingridients]):
    for ing in ings:
        print(type(ing))
        print(ing.prepare())
        print(ing.get_mass())

def main():
    bread = Bread(100, 50)
    soup = Soup(200, 100, 0.5)
    tomato = Tomato(100, 100, "RED")
    cook([bread, soup, tomato])"""