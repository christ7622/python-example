#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import threading


def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper


class FTX(object):
    """docstring for FTX"""

    def __init__(self):
        super(FTX, self).__init__()

    def inclass_function(self, market_price):
        return market_price*1.1

    @threaded
    def func_to_be_threaded(self, stop_event, coin):
        loop_count = 1
        # get the pre-threaded defined data
        market_info = list(filter(lambda market: market["coin"] == coin, self.markets))[0]
        market_price = market_info['price']
        market_msg = market_info["msg"]

        while not stop_event.wait(1):
            print("[!] You earned {loop_count} {coin}, now a {coin} is worth ${market_price:.2f}".format(
                loop_count=loop_count, coin=coin, market_price=market_price))

            print("  News: {market_msg}.".format(market_msg=market_msg))
            # call an inclass function
            market_price = self.inclass_function(market_price)

            loop_count = loop_count + 1
            time.sleep(1)
        print("[WARN] YOUR {coin} is 0.".format(coin=coin))

    def run(self):
        stop_event = threading.Event()
        threads = []

        coins = ["DOGE", "BTC"]
        self.markets = [{"coin": "DOGE", "price": 0.1, "msg": "DOGE to $1"},
                        {"coin": "BTC", "price": 50000, "msg": "BTC to $1,000,000"}]

        for market in self.markets:
            threads.append(self.func_to_be_threaded(stop_event, market["coin"]))

        try:
            while 1:
                time.sleep(2)
        except KeyboardInterrupt:
            stop_event.set()
            print("\nWEN RUG?")

        for thread in threads:
            thread.join()

        print("\nALL DONE.")


if __name__ == '__main__':
    ftx = FTX()
    ftx.run()
