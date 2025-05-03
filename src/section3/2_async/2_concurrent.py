import asyncio


async def long_task():
    print("Starting long task...")
    await asyncio.sleep(2)
    print("Long task completed!")


async def concurrent():
    print("Running tasks concurrently...")

    # タスクのリストを作成（タスクがまだawaitされていない点に注意）
    tasks = [long_task() for _ in range(5)]

    # タスクを並行して実行
    await asyncio.gather(*tasks)

    print("All tasks completed!")


async def sequential():
    print("Running task sequentially...")

    # タスクを順番に実行
    for _ in range(5):
        await long_task()

    print("All tasks completed!")


async def main():
    # 2秒かかるタスクを5回実行するので、合計10秒かかる
    await sequential()

    # 2秒かかるタスクを並行で実行するので、いくつ実行してもおよそ合計2秒で済む
    await concurrent()


if __name__ == "__main__":
    asyncio.run(main())
