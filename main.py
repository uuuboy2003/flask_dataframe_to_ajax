# Flask中使用AJax进行前后端数据的传递处理——【实现Python有道翻译】
# https://blog.csdn.net/EchoooZhang/article/details/104491914
from flask import Flask, render_template, Response, jsonify, request
import json
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

def queryWords(word):
    ''' 利用有道翻譯查詢單詞 '''
    url = 'http://dict.youdao.com/w/{}/'.format(word)
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    trans_container = soup.find(class_='trans-container')

    if not trans_container:
        ''' not found the translation '''
        return [word]
    trans_li = trans_container.find_all('li')
    trans_data = [li.text.strip() for li in trans_li]
    print(trans_data)
    return trans_data

@app.route('/trans', methods=['GET','POST'])
def trans():
    a = request.form.get('mydata')
    print(a)
    print('-------------------------')
    word = str(a)
    word_after_trans = queryWords(word)
    data={"word":word,"trans":'\n'.join(word_after_trans)}
    print(word_after_trans)
    # 这块需要注意，不可以直接用jsonify，会失败QAQ。
    # 用json.dumps(data)可把字典形式转为json可用，可以成功，
    return json.dumps(data)

@app.route('/')
def search():
    return render_template('index.html')

# 傳dict給ajax生成表格
@app.route('/test1', methods=['GET','POST'])
def test1():
    print('test1.............................')
    print(request.method)
    if request.method == 'GET':
        word = request.args.get('mydata') # 可以用傳參 /get_df?mydata=bybit
        print(word)
        print('-----------------')
        name = '交易幣種'
        price = '即時價格'
        return render_template('test1.html', name=name, price=price)
    elif request.method == 'POST':
        word = request.form.get('mydata') # 可以用傳參 /get_df?mydata=bybit
        print(word)
        print('-----------------')
        if word == 'okex':
            table_data = {1:['ETH', 1200], 2:['BTC', 18000], 3:['XRP', 0.1526]}
        elif word == 'bybit':
            table_data = {1:['LINK', 1200], 2:['SOL', 18000], 3:['RVN', 0.1526]}
        else:
            table_data = {}
        return table_data
    
@app.route('/test2', methods=['GET','POST'])
def test2():
    print('test2.............................')
    print(request.method)
    if request.method == 'GET':
        word = request.args.get('mydata') # 可以用傳參 /get_df?mydata=bybit
        print(word)
        print('-----------------')
        column_list = ['name', 'price']
        name = 'ETH'
        code = "<thead><tr><td><b>交易幣種</b></td><td><b>即時價格</b></td></tr></thead>"
        return render_template('test2.html', column_list=column_list, name=name, code=code)
    elif request.method == 'POST':
        word = request.form.get('mydata') # 可以用傳參 /get_df?mydata=bybit
        print(word)
        print('-----------------')

        # 傳list用這些
        if word == 'okex':
            table_data = [{'name': 'NEO-USD-SWAP', 'price': 0.0137,},
                          {'name': 'LINK-USD-SWAP', 'price': 0.0133},
                          {'name': 'DASH-USD-SWAP', 'price': 0.0136}]
        elif word == 'bybit':
            table_data = [{'name': 'NEO-USD-SWAP', 'price': 0.0137},
                          {'name': 'LINK-USD-SWAP', 'price': 0.0133},
                          {'name': 'DASH-USD-SWAP', 'price': 0.0136}]
        else:
            table_data = {}
        return jsonify(table_data)

@app.route('/test3', methods=['GET','POST'])
def test3():
    print('test3.............................')
    print(request.method)
    if request.method == 'GET':
        word = request.args.get('mydata') # 可以用傳參 /get_df?mydata=bybit
        print(word)
        print('-----------------')
        if word == 'okex':
            instruments = [{'instrument_id': 'NEO-USD-SWAP', 'funding': 0.0137, 'exchange': 'OKEX'},
                                {'instrument_id': 'LINK-USD-SWAP', 'funding': 0.0133, 'exchange': 'OKEX'},
                                {'instrument_id': 'DASH-USD-SWAP', 'funding': 0.0136, 'exchange': 'OKEX'}]
        elif word == 'bybit':
            instruments = [{'instrument_id': 'NEO-USD-SWAP', 'funding': 0.0137, 'exchange': 'BYBIT'},
                            {'instrument_id': 'LINK-USD-SWAP', 'funding': 0.0133, 'exchange': 'BYBIT'},
                            {'instrument_id': 'DASH-USD-SWAP', 'funding': 0.0136, 'exchange': 'BYBIT'}]
        else:
            instruments = {}
        return render_template('test3.html', instruments=instruments)
    elif request.method == 'POST':
        word = request.form.get('mydata') # 可以用傳參 /get_df?mydata=bybit
        print(word)
        print('-----------------')
        if word == 'okex':
            instruments = [{'instrument_id': 'NEO-USD-SWAP', 'funding': 0.0137, 'exchange': 'OKEX'},
                            {'instrument_id': 'LINK-USD-SWAP', 'funding': 0.0133, 'exchange': 'OKEX'},
                            {'instrument_id': 'DASH-USD-SWAP', 'funding': 0.0136, 'exchange': 'OKEX'}]
        elif word == 'bybit':
            instruments = [{'instrument_id': 'NEO-USD-SWAP', 'funding': 0.0137, 'exchange': 'BYBIT'},
                            {'instrument_id': 'LINK-USD-SWAP', 'funding': 0.0133, 'exchange': 'BYBIT'},
                            {'instrument_id': 'DASH-USD-SWAP', 'funding': 0.0136, 'exchange': 'BYBIT'}]
        else:
            instruments = [{'instrument_id': 'NEO-USD-SWAP', 'funding': 0.0137, 'exchange': 'BINANCE'}]
        return jsonify(instruments)
        # return instruments #render_template('test3.html', instruments=instruments)

@app.route('/test4', methods=['GET','POST'])
def test4():
    print('test4.............................')
    print(request.method)
    if request.method == 'GET':
        word = request.args.get('mydata') # 可以用傳參 /get_df?mydata=bybit
        print(word)
        print('-----------------')
        instruments = [{'instrument_id': 'XRP-USD-SWAP', 'funding': 0.0137, 'exchange': 'BYBIT'},
                        {'instrument_id': 'LINK-USD-SWAP', 'funding': 0.0133, 'exchange': 'BYBIT'},
                        {'instrument_id': 'DASH-USD-SWAP', 'funding': 0.0136, 'exchange': 'BYBIT'}]
        # return jsonify(instruments)
        column_list = ['交易對', '資金費率', '交易所']
        column_dict = { 0: '交易對', 1: '資金費率', 2: '交易所' }
        return render_template('test4.html', column_list=column_list, column_dict=column_dict)
    elif request.method == 'POST':
        word = request.form.get('mydata') # 可以用傳參 /get_df?mydata=bybit
        print(word)
        print('-----------------')
        if word == 'okex':
            instruments = [{'instrument_id': 'NEO-USD-SWAP', 'funding': 0.0137, 'exchange': 'OKEX'},
                            {'instrument_id': 'LINK-USD-SWAP', 'funding': 0.0133, 'exchange': 'OKEX'},
                            {'instrument_id': 'DASH-USD-SWAP', 'funding': 0.0136, 'exchange': 'OKEX'}]
        elif word == 'bybit':
            instruments = [{'instrument_id': 'NEO-USD-SWAP', 'funding': 0.0137, 'exchange': 'BYBIT'},
                            {'instrument_id': 'LINK-USD-SWAP', 'funding': 0.0133, 'exchange': 'BYBIT'},
                            {'instrument_id': 'DASH-USD-SWAP', 'funding': 0.0136, 'exchange': 'BYBIT'}]
        else:
            instruments = [{'instrument_id': 'NEO-USD-SWAP', 'funding': 0.0137, 'exchange': 'BINANCE'}]
        return jsonify(instruments)

# 直接展示css處理過的dataframe
@app.route('/test5', methods=['GET'])
def test5():
    print('test5.............................')
    print(request.method)
    if request.method == 'GET':
        word = request.args.get('mydata') # 可以用傳參 /get_df?mydata=bybit
        print(word)
        print('-----------------')
        instruments = [{'名稱': 'BTCUSDT', '周期': '2h', '張數': '5', '方向': 0},
                        {'名稱': 'ETHUSDT', '周期': '1h', '張數': '3', '方向': 1},
                        {'名稱': 'SOLUSDT', '周期': '5m', '張數': '6', '方向': -1}, 
                        {'名稱': 'AXSUSDT', '周期': '30m', '張數': '7', '方向': 0}, 
                        {'名稱': 'RVNUSDT', '周期': '15m', '張數': '21', '方向': 1}]
        # return jsonify(instruments)
        column_list = ['交易對', '資金費率', '交易所']
        column_dict = { 0: '交易對', 1: '資金費率', 2: '交易所' }
        return render_template('test5.html')

# columns 寫死在 html 裡
@app.route('/test6', methods=['GET','POST'])
def test6():
    print('test6.............................')
    print(request.method)
    if request.method == 'GET':
        word = request.args.get('mydata') # 可以用傳參 /get_df?mydata=bybit
        print(word)
        print('-----------------')
        exchanges = ['OKEX', 'BYBIT']
        symbols = ['BTC', 'ETH', 'BNB', 'SOL', 'AXS']
        return render_template('test6.html', exchanges=exchanges, symbols=symbols)

    elif request.method == 'POST':
        import random
        word = request.form.get('mydata') # 可以用傳參 /get_df?mydata=bybit
        word2 = request.form.get('mydata2')
        print(word)
        print(word2)
        print('-----------------')
        instruments = [{'名稱': f'{word} / {word2}', '周期': random.choice(['15m', '30m', '1h', '2h']), '張數': random.randint(1, 20), '方向': random.choice([1, 0, -1])} for i in range(10)]
        return jsonify(instruments)

# columns 從 flask 傳到 ajax 裡顯示 table
@app.route('/test7', methods=['GET','POST'])
def test7():
    print('test7.............................')
    print(request.method)
    if request.method == 'GET':
        word = request.args.get('mydata') # 可以用傳參 /get_df?mydata=bybit
        print(word)
        print('-----------------')
        exchanges = ['OKEX', 'BYBIT']
        symbols = ['BTC', 'ETH', 'BNB', 'SOL', 'AXS']
        columns = ['名稱', '周期', '張數', '方向']
        return render_template('test7.html', exchanges=exchanges, symbols=symbols, columns=columns)

    elif request.method == 'POST':
        import random
        word = request.form.get('mydata') # 可以用傳參 /get_df?mydata=bybit
        word2 = request.form.get('mydata2')
        print(word)
        print(word2)
        print('-----------------')
        instruments = [{'名稱': f'{word} / {word2}', '周期': random.choice(['15m', '30m', '1h', '2h']), '張數': random.randint(1, 20), '方向': random.choice([1, 0, -1])} for i in range(10)]
        return jsonify(instruments)

@app.route('/test7_get', methods=['GET','POST'])
def test7_get():
    print('test7_get.............................')
    print(request.method)
    return jsonify(['名稱', '周期', '張數', '方向'])

# get 由html傳入columns名稱，post 由ajax接收dataframe
@app.route('/test8', methods=['GET','POST'])
def test8():
    print('test8.............................')
    print(request.method)
    if request.method == 'GET':
        word = request.args.get('mydata') # 可以用傳參 /get_df?mydata=bybit
        print(word)
        print('-----------------')
        exchanges = ['OKEX', 'BYBIT']
        symbols = ['BTC', 'ETH', 'BNB', 'SOL', 'AXS']
        columns = ['名稱', '周期', '張數', '方向']
        return render_template('test8.html', exchanges=exchanges, symbols=symbols, columns=columns)
        # return 'hello'

    elif request.method == 'POST':
        import random
        word = request.form.get('mydata') # 可以用傳參 /get_df?mydata=bybit
        word2 = request.form.get('mydata2')
        print(f'輸入1: {word} 輸入2: {word2}\n-----------------')
        import pandas as pd
        # data = [
        #         ['BTCUSDT', '2h', '5',  0],
        #         ['ETHUSDT', '1h', '3',  1],
        #         ['SOLUSDT', '5m', '6',  -1],
        #         ['AXSUSDT', '30m', '7',  0],
        #         ['RVNUSDT', '15m', '21',  1],
        #         ]
        # df = pd.DataFrame(data, columns=['名稱', '周期', '張數',  '方向'])
        content = [['名稱', '周期', '張數',  '方向']] + [[f'{word} / {word2}', random.choice(['15m', '30m', '1h', '2h']), random.randint(1, 20), random.choice([1, 0, -1])] for i in range(5)]
        df = pd.DataFrame(content[1:], columns=content[0])
        instruments = [df.columns.to_list()] + [j.to_list() for i, j in df.iterrows()]
        print(instruments)
        return jsonify(instruments)

# 最終版 任意傳入dataframe 自動匹配 columns的名稱
@app.route('/test9', methods=['GET', 'POST'])
def test9():
    print('=======================')
    print(f'方法: {request.method}')
    print(f'值: {request.values.keys()}')
    print('=======================')

    if request.method == 'GET':
        word = request.args.get('mydata') # 可以用傳參 /get_df?mydata=bybit
        print(word)
        print('-----------------')
        exchanges = ['OKEX', 'BYBIT', 'BINANCE']
        symbols = ['BTC', 'ETH', 'SOL', 'AXS', 'BNB']
        columns = ['名稱', '周期', '張數',  '方向']
        return render_template('test9.html', exchanges=exchanges, symbols=symbols, columns=columns)

    elif request.method == 'POST':
        import random
        import pandas as pd
        word = request.form.get('mydata') # 可以用傳參 /get_df?mydata=bybit
        word2 = request.form.get('mydata2')
        print(f'輸入1: {word} 輸入2: {word2}\n-----------------')

        content = [['名稱', '周期', '張數',  '方向']] + [[f'{word} / {word2}', random.choice(['15m', '30m', '1h', '2h']), random.randint(1, 20), random.choice([1, 0, -1])] for i in range(5)]
        df = pd.DataFrame(content[1:], columns=content[0])
        instruments = [df.columns.to_list()] + [j.to_list() for i, j in df.iterrows()]
        print(instruments)							
        # print(df)
        # instruments = [df.columns.to_list()] + [j.to_list() for i, j in df.iterrows()]
        return jsonify(instruments)

if __name__ == "__main__":
    app.run(debug=True,threaded=True,port=5566)    
    # import requests
    # word = 'submit'
    # url = f'http://dict.youdao.com/w/{word}/'
    # html = requests.get(url)
    # print(html.text)

    # res = queryWords(word)
    # print(res)