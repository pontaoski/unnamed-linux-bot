#!/usr/bin/env python
import asyncio

class Timer:
    def __init__(self, timeout, callback):
        self._timeout = timeout
        self._callback = callback
        self._task = asyncio.ensure_future(self._job())
        
    async def _job(self):
        await asyncio.sleep(self._timeout)
        await self._callback()

    def cancel(self):
        self._task.cancel()

def get_content(string, trim_words=2):
    array = string.split()
    return " ".join(array[trim_words:])

def default(get, default):
    if get is False:
        return default
    elif get is None:
        return default
    else:
        return get