import ccxt
import time
import requests

print("Bot Start")

def send_telegram_message(text):
    bot_token = '7437512729:AAFBCqInl9ra4jAxpzVBlz6-GM2EqB_gGVo'
    chat_id = '-4279557624'
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={text}"
    
    response = requests.get(url)
    data = response.json()
    print(data)


def get_asks_and_bids(exchange, symbol, balance):
    exchange_obj = getattr(ccxt, exchange)()
    try:
        exchange_obj.load_markets()
        orders = exchange_obj.fetch_order_book(symbol, limit=20)
        asks_ = orders['asks'][:20]
        bids_ = orders['bids'][:20]

        qty_ask = balance / asks_[0][0]
        qty_bid = balance / bids_[0][0]

        total_qty_ask, total_value_ask, total_qty_bid, total_value_bid = 0, 0, 0, 0
        orders_count_ask, orders_count_bid = 0, 0

        for ask in asks_:
            ask_price, ask_qty = ask
            if qty_ask > ask_qty:
                total_qty_ask += ask_qty
                total_value_ask += ask_qty * ask_price
                qty_ask -= ask_qty
                orders_count_ask += 1
            else:
                total_qty_ask += qty_ask
                total_value_ask += qty_ask * ask_price
                orders_count_ask += 1
                break

        for bid in bids_:
            bid_price, bid_qty = bid
            if qty_bid > bid_qty:
                total_qty_bid += bid_qty
                total_value_bid += bid_qty * bid_price
                qty_bid -= bid_qty
                orders_count_bid += 1
            else:
                total_qty_bid += qty_bid
                total_value_bid += qty_bid * bid_price
                orders_count_bid += 1
                break

        average_price_ask = total_value_ask / total_qty_ask if total_qty_ask != 0 else 0
        average_price_bid = total_value_bid / total_qty_bid if total_qty_bid != 0 else 0

        return {
            'exchange': exchange,
            'symbol': symbol,
            'average_price_ask': average_price_ask,
            'total_qty_ask': total_qty_ask,
            'orders_count_ask': orders_count_ask,
            'average_price_bid': average_price_bid,
            'total_qty_bid': total_qty_bid,
            'orders_count_bid': orders_count_bid
        }
    except Exception as e:
        print(f"An error occurred for {exchange}: {e}")
        return None

symbols = ["BTC/USDT", "XRP/USDT", "SOL/USDT"]
exchanges = ["binance", "kucoin", "mexc", 'huobi', 'bybit', 'woo', 'gate']
balance = 1000

def main():
    results = []
    for symbol in symbols:
        exchange_results = []
        print(f"Symbol: {symbol}")
        for exchange in exchanges:
            result = get_asks_and_bids(exchange, symbol, balance)
            if result:
                exchange_results.append(result)
        
                # Compare average_price_ask and average_price_bid between exchanges
                for i in range(len(exchange_results)):
                    for j in range(i + 1, len(exchange_results)):
                        price_ask_1 = exchange_results[i]['average_price_ask']
                        price_ask_2 = exchange_results[j]['average_price_ask']
                        price_bid_1 = exchange_results[i]['average_price_bid']
                        price_bid_2 = exchange_results[j]['average_price_bid']
                        
                        if abs(price_ask_1 - price_ask_2) / min(price_ask_1, price_ask_2) >= 0.005 or \
                            abs(price_bid_1 - price_bid_2) / min(price_bid_1, price_bid_2) >= 0.005:
                                price_ask = exchange_results[i]['average_price_ask']
                                price_bid = exchange_results[j]['average_price_bid']
                                send_telegram_message(f"""
{symbol}:

|{exchange_results[i]['exchange']}|
Ціна: {exchange_results[i]['average_price_ask']}$
Обєм: {exchange_results[i]['total_qty_ask']:.5f}, {exchange_results[i]['orders_count_ask']} Ордер

|{exchange_results[j]['exchange']}|
Ціна: {exchange_results[j]['average_price_bid']}$
Обєм: {exchange_results[j]['total_qty_bid']:.5f}, {exchange_results[j]['orders_count_bid']} Ордер

!КомісіЇ: 0.4%
*Для Баланса: {balance}$
*Різниця: {((exchange_results[i]['average_price_ask'] - exchange_results[j]['average_price_bid']) / exchange_results[j]['average_price_bid'] * 100):.3f}%
""")




if __name__ == "__main__":
    while(1):
        try:
            time.sleep(600)
            main()
        except:
            pass
