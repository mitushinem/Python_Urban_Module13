import asyncio


async def start_strongman(name, power):
    print(f'Силач {name} начал соревнования.')

    for i in range(1, 6):
        print(f'Силач {name} поднял {i} шар')
        await asyncio.sleep(power)

    print(f'Силач {name} закончил соревнования.')


async def start_tournament():
    strongman_1 = asyncio.create_task(start_strongman('Pasha', 3))
    strongman_2 = asyncio.create_task(start_strongman('Denis', 4))
    strongman_3 = asyncio.create_task(start_strongman('Apollon', 5))

    await asyncio.gather(strongman_1, strongman_2, strongman_3)
    # await strongman_1
    # await strongman_2
    # await strongman_3


if __name__ == '__main__':
    asyncio.run(start_tournament())
