# Домашнее задание по теме "Асинхронность на практике".
# Задача "Асинхронные силачи".

import asyncio


async def start_strongman(name, power):
    print(f"Силач {name} начал соревнования.")
    for ball_number in range(1, 6):
        # Рассчитываем задержку, обратно пропорциональную силе
        delay = 1 / power
        await asyncio.sleep(delay)
        print(f"Силач {name} поднял {ball_number} шар.")
    print(f"Силач {name} закончил соревнования.")


async def start_tournament():
    # Создаем задачи для трёх силачей
    tasks = [
        start_strongman("Pasha", 3),
        start_strongman("Denis", 4),
        start_strongman("Apollon", 5)
    ]

    # Ждем выполнения всех задач
    await asyncio.gather(*tasks)


# Запускаем асинхронную функцию
asyncio.run(start_tournament())

