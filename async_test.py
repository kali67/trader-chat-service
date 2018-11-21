import asyncio

loop = asyncio.get_event_loop()


async def hello():
    print("Hello")
    await asyncio.sleep(3)
    print("World!")


async def main():
    tasks = []
    for i in range(10):
        tasks.append(asyncio.ensure_future(hello()))  # create 10 tasks
    await asyncio.wait(tasks)

if __name__ == "__main__":
    loop.run_until_complete(main())
