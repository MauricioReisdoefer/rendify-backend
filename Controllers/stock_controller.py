from flask import Blueprint, request, jsonify
from Models.stock_model import StockModel
from Extras import db
from twelvedata import TDClient
from Controllers.stock_history_controller import add_or_update_stock_history
import datetime

td = TDClient(apikey="d84cec2223444503b9878a61089236ca")

def get_or_create_stock(symbol):
    try:
        existing_stock = StockModel.query.filter_by(symbol=symbol.upper()).first()
        response = td.price(symbol=symbol.upper()).as_json()
        if 'price' not in response:
            return jsonify({'Message': 'Invalid Symbol or Search Error', "Status":400, "Result":"Error"})

        current_price = float(response['price'])
        new_stock = None
        if existing_stock:
            existing_stock.price = current_price
            add_or_update_stock_history(existing_stock.id, data=datetime.date.today())
        else:
            new_stock = StockModel(symbol=symbol.upper(), price=current_price)
            add_or_update_stock_history(new_stock.id, data=datetime.date.today())
            db.db.session.add(new_stock)
        db.db.session.commit()
        return jsonify({"Result":{
            'symbol': symbol.upper(),
            'price': current_price,
        }, "Message":"Found Price", "Status":200})

    except Exception as e:
        return jsonify({'Result': str(e), "Message":"Error", "Status":500})
    
def get_all_stocks(symbols):
    try:
        symbols_response = td.symbol_search(symbol=symbols).as_json()
        symbols_response = symbols_response[:5]

        if not isinstance(symbols_response, list):
            return jsonify({"Message": "Erro ao buscar símbolos", "Status": 500, "Result": symbols_response})

        success = []
        failed = []
        processed = set()  

        for item in symbols_response:
            symbol = item.get("symbol")
            if not symbol or symbol in processed:
                continue

            processed.add(symbol) 

            try:
                price_response = td.price(symbol=symbol).as_json()
                if "price" not in price_response:
                    failed.append({"symbol": symbol, "error": "Sem preço"})
                    continue

                current_price = float(price_response["price"])
                stock = StockModel.query.filter_by(symbol=symbol).first()

                if stock:
                    stock.price = current_price
                else:
                    new_stock = StockModel(symbol=symbol, price=current_price)
                    db.db.session.add(new_stock)
                    db.db.session.flush()

                success.append({"symbol": symbol, "price": current_price})
            except Exception as e:
                failed.append({"symbol": symbol, "error": str(e)})
                continue

        db.db.session.commit()

        return jsonify({
            "Message": "Finalizado",
            "Status": 200,
            "Success": success,
            "Failed": failed
        })

    except Exception as e:
        return jsonify({"Message": "Erro geral", "Status": 500, "Result": str(e)})
