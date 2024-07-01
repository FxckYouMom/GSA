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

symbols = ["BNB/USDT", "XRP/USDT", "SOL/USDT", "ADA/USDT", "DOGE/USDT", "TRX/USDT", "LINK/USDT", "TONCOIN/USDT", "MATIC/USDT", "DOT/USDT", "AVAX/USDT", "LTC/USDT", "DAI/USDT", "SHIB/USDT", "BCH/USDT", "LEO/USDT", "OKB/USDT", "ATOM/USDT", "XLM/USDT", "TUSD/USDT", "UNI/USDT", "XMR/USDT", "ETC/USDT", "CRO/USDT", "FIL/USDT", "HBAR/USDT", "LDO/USDT", "ICP/USDT", "APT/USDT", "BUSD/USDT", "NEAR/USDT", "VET/USDT", "OP/USDT", "ARB/USDT", "INJ/USDT", "AAVE/USDT", "IMX/USDT", "QNT/USDT", "GRT/USDT", "MKR/USDT", "FTT/USDT",
                     "STX/USDT", "FTM/USDT", "SAND/USDT", "AXS/USDT", "XTZ/USDT", "NEO/USDT", "MANA/USDT", "EOS/USDT", "HAVVEN/USDT", "SNX/USDT", "XDCE/USDT", "KAVA/USDT", "FLOW/USDT", "MINA/USDT", "XEC/USDT", "CHZ/USDT", "CFX/USDT", "GALA/USDT", "DYDX/USDT", "KCS/USDT", "MIOTA/USDT", "SUI/USDT", "CRV/USDT", "TWT/USDT", "KLAY/USDT", "APE/USDT", "HT/USDT", "ZEC/USDT", "CAKE/USDT", "LUNC/USDT", "ROSE/USDT", "AR/USDT", "PAX/USDT", "BTTC/USDT", "CSPR/USDT", "COMP/USDT", "ASTR/USDT", "ZRX/USDT", "NEXO/USDT", "ZIL/USDT", "GNO/USDT", "1INCH/USDT", "DASH/USDT", "BAT/USDT", "FET/USDT", "QTUM/USDT", "GMT/USDT", "XEM/USDT", "LRC/USDT", "NFT/USDT",
                     "AGI/USDT", "EDO/USDT", "YFI/USDT", "TFUEL/USDT", "CELO/USDT", "FLOKI/USDT", "JST/USDT", "SFP/USDT", "HOT/USDT", "MASK/USDT", "STORJ/USDT", "HNT/USDT", "ICX/USDT", "BTG/USDT", "JASMY/USDT", "IOTX/USDT", "ANKR/USDT", "ELF/USDT", "XCH/USDT", "RVN/USDT", "WAVES/USDT", "GLM/USDT", "DCR/USDT", "SUSHI/USDT", "KSM/USDT", "ANT/USDT", "AUDIO/USDT", "SC/USDT", "WAX/USDT", "GLMR/USDT", "BAL/USDT", "TRB/USDT", "SXP/USDT", "BAND/USDT", "ONE/USDT", "ONT/USDT", "HIVE/USDT", "IOST/USDT", "BNT/USDT", "SNT/USDT", "ZEN/USDT", "LOOM/USDT", "KDA/USDT", "CKB/USDT", "SKL/USDT", "ZEL/USDT", "LSK/USDT", "STRAX/USDT", "MCO/USDT",
                     "ORBS/USDT", "DGB/USDT", "UMA/USDT", "PUNDIX/USDT", "RSR/USDT", "DREP/USDT", "TNC/USDT", "BTT/USDT", "ARK/USDT", "POLY/USDT", "TRIBE/USDT", "STPT/USDT", "API3/USDT", "ONG/USDT", "CTSI/USDT", "MTL/USDT", "DEXE/USDT", "CELR/USDT", "POWR/USDT", "STEEM/USDT", "STG/USDT", "C98/USDT", "LYXE/USDT", "KEEP/USDT", "TOMO/USDT", "XVS/USDT", "RIF/USDT", "CVC/USDT", "DAO/USDT", "BLZ/USDT", "VTHO/USDT", "NANO/USDT", "RDNT/USDT", "ARDR/USDT", "SLP/USDT", "CDT/USDT", "OGN/USDT", "CHR/USDT", "STORM/USDT", "STMX/USDT", "OMG/USDT", "RLC/USDT", "ERG/USDT", "RAY/USDT", "NMR/USDT", "IQ/USDT", "GAS/USDT", "POND/USDT", "REQ/USDT", "DENT/USDT",
                     "MED/USDT", "PROM/USDT", "CQT/USDT", "VRA/USDT", "BADGER/USDT", "SYS/USDT", "SFUND/USDT", "DODO/USDT", "OXT/USDT", "NKN/USDT", "GTC/USDT", "MBL/USDT", "META/USDT", "ALPHA/USDT", "QKC/USDT", "DUSK/USDT", "XVG/USDT", "COTI/USDT", "CEL/USDT", "PHA/USDT", "SNM/USDT", "GODS/USDT", "LINA/USDT", "ARPA/USDT", "NA/USDT", "REN/USDT", "EFI/USDT", "FX/USDT", "MDX/USDT", "ALICE/USDT", "MBOX/USDT", "FUN/USDT", "UNFI/USDT", "ENV/USDT", "MXM/USDT", "SUPER/USDT", "BETA/USDT", "KIN/USDT", "TLM/USDT", "CTK/USDT", "TRU/USDT", "XYO/USDT", "FORTH/USDT", "MOVR/USDT", "WRX/USDT", "GRS/USDT", "COCOS/USDT", "TKO/USDT", "ABBC/USDT", "DAR/USDT",
                     "GHST/USDT", "FLM/USDT", "PERP/USDT", "ATA/USDT", "BAKE/USDT", "BEL/USDT", "WAN/USDT", "BQX/USDT", "YFII/USDT", "BSW/USDT", "REEF/USDT", "UPP/USDT", "LAT/USDT", "POLS/USDT", "KP3R/USDT", "DEGO/USDT", "ERN/USDT", "KMD/USDT", "IRIS/USDT", "UTK/USDT", "SUSD/USDT", "LIT/USDT", "ETN/USDT", "BLOK/USDT", "CREAM/USDT", "MDT/USDT", "JNT/USDT", "DIA/USDT", "KEY/USDT", "CLV/USDT", "CTXC/USDT", "TNT/USDT", "LTO/USDT", "FRONT/USDT", "DATA/USDT", "COS/USDT", "AVA/USDT", "QUICK/USDT", "ALPACA/USDT", "SAMO/USDT", "BTM/USDT", "MONA/USDT", "AKRO/USDT", "WING/USDT", "DNT/USDT", "XZC/USDT",
                     "ELA/USDT", "AMB/USDT", "KISHU/USDT", "ORN/USDT", "VELO/USDT", "ADX/USDT", "TROY/USDT", "BMX/USDT", "NULS/USDT", "FIDA/USDT", "WWB/USDT", "PSG/USDT", "CHESS/USDT", "OG/USDT", "FIS/USDT", "HARD/USDT", "BURGER/USDT", "UBT/USDT", "UBT/USDT", "OM/USDT", "OM/USDT", "HERO/USDT", "AST/USDT",  "PIVX/USDT",  "DOCK/USDT", "FSN/USDT", "SRM/USDT", "VITE/USDT", "WTC/USDT", "JUV/USDT", "SOUL/USDT", "EPS/USDT", "OAX/USDT", "VR/USDT", "TIME/USDT",  "BCD/USDT", "NCT/USDT", "UMEE/USDT", "PNT/USDT", "DORA/USDT", "HNS/USDT", "ACM/USDT",
                     "PPC/USDT", "ATM/USDT", "OOKI/USDT", "CVP/USDT",  "ABT/USDT", "UFT/USDT", "PROS/USDT", "PERL/USDT", "GBYTE/USDT", "INSTAR/USDT", "DMD/USDT", "FCT/USDT", "ASR/USDT", "AE/USDT", "REP/USDT", "XCP/USDT", "MAN/USDT", "NEX/USDT", "AKITA/USDT", "BCN/USDT", "DBC/USDT", "GO/USDT", "PDEX/USDT", "KASTA/USDT", "VIT/USDT", "CERE/USDT", "SENSO/USDT", "DX/USDT", "UKG/USDT", "RVR/USDT", "BEAM/USDT", "BTCST/USDT", "COIN/USDT", "VTC/USDT", "SALT/USDT", "HC/USDT", "QSP/USDT", "HDAO/USDT", "GRIN/USDT", "KINE/USDT", "QLC/USDT",  "GAME/USDT", "MTH/USDT",  "PPT/USDT", "CPX/USDT"]
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
