import asyncio

async def get_values_from_io():
    await asyncio.sleep(1)
    return list(range(10))


vals = []

async def fetcher():
    while True:
        io_vals = await get_values_from_io()

        for val in io_vals:
            await vals.append(val)


async def monitor():
    while True:
      print(len(vals))

      await asyncio.sleep(1)


async def counter(name: str):
  for i in range(0, 100):
    print(f"{name}: {i!s}")
    await asyncio.sleep(0)


async def main():
  tasks = []
  for n in range(0, 4):
    tasks.append(asyncio.create_task(counter(f"task{n}")))

  while True:
    tasks = [t for t in tasks if not t.done()]
    if len(tasks) == 0:
      return

    await tasks[0]


# async def main():
#   t1 = asyncio.create_task(fetcher())
#   t2 = asyncio.create_task(monitor())
#   await asyncio.gather(t1, t2)


asyncio.run(main())
