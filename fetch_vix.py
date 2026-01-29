import yfinance as yf
import json
import os

def get_vix_data():
    try:
        # 使用 yfinance 抓取 VIX 指數 (^VIX)
        vix = yf.Ticker("^VIX")
        
        # 抓取最近 5 天的資料
        hist = vix.history(period="5d")
        
        # 確保資料足夠
        if len(hist) < 3:
            print("資料不足")
            return None

        # 取出「收盤價」並只留最後 3 筆
        closes = hist['Close'].tail(3).values.tolist()
        
        # 計算 3 日平均
        avg_price = sum(closes) / len(closes)
        current_price = closes[-1]

        # 整理要輸出的資料
        data = {
            "status": "success",
            "current": round(current_price, 2),
            "avg3": round(avg_price, 2),
            "history": [round(x, 2) for x in closes],
            "last_update": str(hist.index[-1].date())
        }
        return data

    except Exception as e:
        print(f"錯誤: {e}")
        return {"status": "error"}

if __name__ == "__main__":
    data = get_vix_data()
    
    # 將資料存成 vix.json 檔案
    with open("vix.json", "w") as f:
        json.dump(data, f)
    print("VIX 資料已更新")
