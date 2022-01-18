import asyncio

class Client():
    def loop(func):
        async_loop = asyncio.get_event_loop()
        try:
            asyncio.ensure_future(func)
            async_loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            print("Closing Loop")
            async_loop.close()
