'''
Copyright (C) 2020-2023  Bryant Moscon - bmoscon@gmail.com
Please see the LICENSE file for the terms and conditions
associated with this software.
'''
from decimal import Decimal
from itertools import zip_longest, chain
import time
import zlib

from order_book import OrderBook


def sample_orderbook(**kwargs):
    asks = [
        ["0.003385", "142011.0"],
        ["0.003395", "221850.0"],
        ["0.0034", "120.0"],
        ["0.003405", "149119.0"],
        ["0.003415", "3.0"],
        ["0.003425", "46851.0"],
        ["0.00343", "162552.0"],
        ["0.003445", "0.0000034"],
        ["0.003455", "182323.0"],
        ["0.003465", "123.0"],
        ["0.003475", "171058.0"],
        ["0.00348", "0.0000000048"],
        ["0.0035", "3.0"],
        ["0.003515", "3.0"],
        ["0.00352", "17.0"],
        ["0.00353", "120.0"],
        ["0.003535", "3.0"],
        ["0.00355", "196293.0"],
        ["0.003565", "168196.0"],
        ["0.00357", "4.0"],
        ["0.003585", "3.0"],
        ["0.003595", "120.0"],
        ["0.003605", "3.0"],
        ["0.00361", "1.0"],
        ["0.003615", "354598.0"],
        ["0.00362", "3.0"],
        ["0.003635", "5.0"],
        ["0.00364", "181628.0"],
        ["0.00365", "4.0"],
        ["0.003655", "3.0"],
        ["0.00366", "121.0"],
        ["0.003675", "8.0"],
        ["0.00368", "202178.0"],
        ["0.00369", "3.0"],
        ["0.0037", "179932.0"],
        ["0.00371", "295577.0"],
        ["0.003725", "123.0"],
        ["0.003745", "3.0"],
        ["0.00375", "1.0"],
        ["0.00376", "3.0"],
        ["0.003775", "208662.0"],
        ["0.00378", "3.0"],
        ["0.00379", "120.0"],
        ["0.003795", "3.0"],
        ["0.0038", "1.0"],
        ["0.003815", "3.0"],
        ["0.003825", "16.0"],
        ["0.00383", "3.0"],
        ["0.00385", "4.0"],
        ["0.003855", "120.0"],
        ["0.003865", "3.0"],
        ["0.003885", "3.0"],
        ["0.00389", "1.0"],
        ["0.0039", "876.0"],
        ["0.00392", "123.0"],
        ["0.003935", "3.0"],
        ["0.00394", "1.0"],
        ["0.003955", "3.0"],
        ["0.00397", "3.0"],
        ["0.00398", "5.0"],
        ["0.003985", "120.0"],
        ["0.00399", "4.0"],
        ["0.004005", "3.0"],
        ["0.00402", "3.0"],
        ["0.00403", "3.0"],
        ["0.00405", "120.0"],
        ["0.00406", "3.0"],
        ["0.00409", "3.0"],
        ["0.004115", "120.0"],
        ["0.00412", "3.0"],
        ["0.004135", "5.0"],
        ["0.00414", "1764.0"],
        ["0.00415", "3.0"],
        ["0.00418", "123.0"],
        ["0.00421", "3.0"],
        ["0.00424", "3.0"],
        ["0.004245", "120.0"],
        ["0.00427", "3.0"],
        ["0.00429", "16.0"],
        ["0.0043", "3.0"],
        ["0.00431", "120.0"],
        ["0.00433", "3.0"],
        ["0.00436", "3.0"],
        ["0.004375", "120.0"],
        ["0.00439", "3.0"],
        ["0.00442", "3.0"],
        ["0.00443", "147145.0"],
        ["0.00444", "120.0"],
        ["0.004445", "16.0"],
        ["0.00445", "3.0"],
        ["0.00448", "3.0"],
        ["0.004505", "120.0"],
        ["0.004515", "3.0"],
        ["0.004545", "3.0"],
        ["0.00457", "120.0"],
        ["0.004575", "3.0"],
        ["0.004595", "16.0"],
        ["0.004605", "3.0"],
        ["0.004635", "123.0"],
        ["0.004665", "3.0"]
    ]

    bids = [
        ["0.00336", "3.0"],
        ["0.00335", "39492.0"],
        ["0.003345", "3.0"],
        ["0.00334", "219821.0"],
        ["0.00333", "17115.0"],
        ["0.003325", "205654.0"],
        ["0.003315", "8049.0"],
        ["0.00331", "602.0"],
        ["0.00329", "4.0"],
        ["0.00328", "7.0"],
        ["0.003275", "509455.0"],
        ["0.00327", "120.0"],
        ["0.003265", "148571.0"],
        ["0.003255", "3.0"],
        ["0.00324", "4.0"],
        ["0.003235", "612.0"],
        ["0.00322", "148150.0"],
        ["0.003215", "169503.0"],
        ["0.00321", "16.0"],
        ["0.003205", "184421.0"],
        ["0.0032", "1.0"],
        ["0.003185", "3.0"],
        ["0.00317", "3.0"],
        ["0.00315", "8575.0"],
        ["0.003145", "247853.0"],
        ["0.003135", "3.0"],
        ["0.00312", "3060.0"],
        ["0.003115", "186021.0"],
        ["0.00311", "1.0"],
        ["0.003105", "229810.0"],
        ["0.0031", "3.0"],
        ["0.003095", "206811.0"],
        ["0.00308", "3.0"],
        ["0.003065", "3.0"],
        ["0.003055", "16.0"],
        ["0.003045", "3.0"],
        ["0.00303", "3.0"],
        ["0.00301", "288639.0"],
        ["0.003", "272946.0"],
        ["0.002995", "3.0"],
        ["0.002975", "212459.0"],
        ["0.002965", "244636.0"],
        ["0.00296", "3.0"],
        ["0.00294", "3.0"],
        ["0.002925", "3.0"],
        ["0.002905", "19.0"],
        ["0.00289", "3.0"],
        ["0.00287", "3.0"],
        ["0.002855", "3.0"],
        ["0.00284", "3.0"],
        ["0.00282", "3.0"],
        ["0.002805", "3.0"],
        ["0.002785", "3.0"],
        ["0.00277", "3.0"],
        ["0.00275", "3.0"],
        ["0.002735", "3.0"],
        ["0.002715", "3.0"],
        ["0.0027", "3.0"],
        ["0.00268", "3.0"],
        ["0.002665", "3.0"],
        ["0.002645", "3.0"],
        ["0.00263", "3.0"],
        ["0.00261", "3.0"],
        ["0.002595", "3.0"],
        ["0.002575", "3.0"],
        ["0.00256", "3.0"],
        ["0.002555", "147658.0"],
        ["0.00254", "3.0"],
        ["0.002525", "3.0"],
        ["0.002505", "3.0"],
        ["0.00249", "3.0"],
        ["0.00247", "3.0"],
        ["0.002455", "3.0"],
        ["0.002435", "3.0"],
        ["0.00242", "3.0"],
        ["0.0024", "3.0"],
        ["0.002385", "3.0"],
        ["0.002365", "3.0"],
        ["0.00235", "3.0"],
        ["0.00233", "3.0"],
        ["0.002315", "3.0"],
        ["0.0023", "3.0"],
        ["0.002035", "3440.0"],
        ["0.0015", "1333.0"],
        ["0.0012", "5010.0"],
        ["0.00033", "303030.0"],
        ["0.00003", "371115.0"]
    ]

    ob = OrderBook(**kwargs)
    for a in asks:
        ob.asks[Decimal(a[0])] = Decimal(a[1])

    for b in bids:
        ob.bids[Decimal(b[0])] = Decimal(b[1])

    return ob


def kraken_checksum(book):
    combined = ""
    for side in (book.asks, book.bids):
        d = list(side)[:10]
        sizes = [str(side[price]).replace('.', '').lstrip('0').split('E')[0] for price in d]
        prices = [str(price).replace('.', '').lstrip('0').split('E')[0] for price in d]
        combined += ''.join([b for a in zip(prices, sizes) for b in a])

    return zlib.crc32(combined.encode())


def ftx_checksum(book):
    n = 100
    def fmt(x): return str(float(x))

    bids = [f"{fmt(price)}:{fmt(book.bids[price])}" for price in list(book.bids)[:n]]
    asks = [f"{fmt(price)}:{fmt(book.asks[price])}" for price in list(book.asks)[:n]]

    combined = ":".join([x for x in chain(*zip_longest(bids, asks)) if x is not None])
    return zlib.crc32(combined.encode())


def okx_checksum(book):
    n = 25
    def fmt(x): return format(x, 'f')

    bids = [f"{fmt(price)}:{fmt(book.bids[price])}" for price in list(book.bids)[:n]]
    asks = [f"{fmt(price)}:{fmt(book.asks[price])}" for price in list(book.asks)[:n]]

    combined = ":".join([x for x in chain(*zip_longest(bids, asks)) if x is not None])
    return zlib.crc32(combined.encode())


def bitget_checksum(book):
    n = 25
    def fmt(x): return str(x)

    bids = [f"{fmt(price)}:{fmt(book.bids[price])}" for price in list(book.bids)[:n]]
    asks = [f"{fmt(price)}:{fmt(book.asks[price])}" for price in list(book.asks)[:n]]

    combined = ":".join([x for x in chain(*zip_longest(bids, asks)) if x is not None])
    return zlib.crc32(combined.encode())


def compare(fmt, reference, n=1000):
    print(fmt)

    ob = sample_orderbook(checksum_format=fmt)

    start = time.time()
    for i in range(n):
        reference_checksum = reference(ob)
    duration = time.time() - start
    print(f'  Python: {1e6*duration/n:g} us/checksum')

    start = time.time()
    for i in range(n):
        checksum = ob.checksum()
    duration = time.time() - start
    print(f'  C: {1e6*duration/n:g} us/checksum')

    assert checksum == reference_checksum


def main():
    compare('KRAKEN', kraken_checksum)
    compare('FTX', ftx_checksum)
    compare('OKX', okx_checksum)
    compare('BITGET', bitget_checksum)


if __name__ == '__main__':
    main()
