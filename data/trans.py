import asyncio
import json
import os
from typing import Dict, List

import aiofiles
import aiohttp
from aiohttp import ClientSession

INPUT_PATH = "engword.json"
OUTPUT_PATH = "rusword.json"
CACHE_PATH = "translation_cache.json"

# Настройки
BATCH_SIZE = 200
CONCURRENCY = 10
API_URL = "https://translate.googleapis.com/translate_a/single"


async def translate_text(
    session: ClientSession, text: str, source="en", target="ru"
) -> str:
    params = {"client": "gtx", "sl": source, "tl": target, "dt": "t", "q": text}
    async with session.get(API_URL, params=params) as resp:
        data = await resp.json(content_type=None)
        return data[0][0][0].lower()


async def load_json(path: str) -> List[str]:
    async with aiofiles.open(path, "r", encoding="utf-8") as f:
        return json.loads(await f.read())


async def save_json(data, path: str):
    async with aiofiles.open(path, "w", encoding="utf-8") as f:
        await f.write(json.dumps(data, ensure_ascii=False, indent=2))


async def process_batch(
    session: ClientSession, batch: List[str], cache: Dict[str, str]
) -> Dict[str, str]:
    results = {}
    tasks = []
    for word in batch:
        if word in cache:
            continue
        tasks.append(asyncio.create_task(translate_text(session, word)))

    translations = await asyncio.gather(*tasks, return_exceptions=True)

    for word, tr in zip([w for w in batch if w not in cache], translations):
        if isinstance(tr, Exception):
            continue
        cache[word] = tr
        results[word] = tr

    return results


async def main():
    print("Загрузка входных данных...")
    words = await load_json(INPUT_PATH)
    print(f"Всего слов: {len(words)}")

    if os.path.exists(CACHE_PATH):
        cache = await load_json(CACHE_PATH)
        print(f"Кэш загружен: {len(cache)} записей")
    else:
        cache = {}

    seen = set()
    final = []

    async with aiohttp.ClientSession() as session:
        for i in range(0, len(words), BATCH_SIZE):
            batch = words[i : i + BATCH_SIZE]
            print(f"Перевод батча {i}–{i+len(batch)-1}...")

            results = await process_batch(session, batch, cache)

            for word in batch:
                tr = cache.get(word)
                if not tr:
                    continue
                if " " in tr:
                    continue
                if tr in seen:
                    continue
                seen.add(tr)
                final.append(tr)

            if i % (BATCH_SIZE * 5) == 0:
                await save_json(cache, CACHE_PATH)

    print(f"Финальный список: {len(final)} слов")
    await save_json(final, OUTPUT_PATH)
    await save_json(cache, CACHE_PATH)
    print(f"✅ Перевод завершён. Файл сохранён: {OUTPUT_PATH}")


if __name__ == "__main__":
    asyncio.run(main())
