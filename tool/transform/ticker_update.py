from db.SqlExecutor import SqlExecutor

# TRANSCRIBE_FILE = '../../data/tickers/compiled/all_tickers.txt'
TRANSCRIBE_FILE = '../../data/tickers/raw/etfs/etfs.txt'

INSERT_SQL = "INSERT INTO `COMPANY` (TICKER) VALUES (?);"
executor = SqlExecutor(debug=True)
with open(TRANSCRIBE_FILE) as all_tickers:
    for ticker_text in all_tickers:
        ticker = ticker_text.strip()
        result = executor.exec_select("SELECT COUNT(*) AS ROW_COUNT FROM `COMPANY` WHERE `TICKER`=?", (ticker,))
        if result.fetchone()[0] == 1:
            print("Already found record for ticker %s, continuing..." % (ticker,))
            continue

        print(ticker)
        executor.exec_insert(INSERT_SQL, (ticker,))

rows = executor.exec_select('SELECT COUNT(*) AS rowcount FROM COMPANY;')
for row in rows:
    print(row[0])

