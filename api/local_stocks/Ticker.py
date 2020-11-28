from db.SqlExecutor import SqlExecutor


class Ticker:
    STOCK = 'STOCK'
    FUND = 'FUND'

    @staticmethod
    def get_ticker(ticker):
        executor = SqlExecutor()
        result = executor.exec_select('SELECT * FROM COMPANY WHERE TICKER=?', (ticker,))
        return result.fetchone()

    @staticmethod
    def get_stock(ticker):
        return Ticker.get_ticker_with_class(ticker, Ticker.STOCK)

    @staticmethod
    def get_etf(ticker):
        return Ticker.get_ticker_with_class(ticker, Ticker.FUND)

    @staticmethod
    def get_ticker_with_class(ticker, fd_class):
        executor = SqlExecutor()
        result = executor.exec_select('SELECT * FROM COMPANY WHERE TICKER=? AND CLASS=?', (ticker, fd_class))
        return result.fetchone()

    @staticmethod
    def get_n_stocks(n=5):
        executor = SqlExecutor()
        result = executor.exec_select('SELECT * FROM COMPANY WHERE CLASS=? AND NAME IS NOT NULL LIMIT ?', (Ticker.STOCK, n))
        return result.fetchall()

    @staticmethod
    def insert_new_ticker(ticker, fd_class):
        if fd_class is not Ticker.STOCK and fd_class is not Ticker.FUND:
            raise TypeError('fd_class must be one of STOCK or FUND')

        executor = SqlExecutor()
        executor.exec_insert('INSERT INTO COMPANY (TICKER, CLASS) VALUES (?, ?)', (ticker, fd_class))
        executor.close()

    @staticmethod
    def delete_ticker(ticker):
        """
        Deletes teh provided ticker if it exists in the database. This action cannot be undone.
        :param ticker:
        :return:
        """
        found_t = Ticker.get_ticker(ticker)
        if found_t is None:
            return

        executor = SqlExecutor()
        executor.exec_insert('DELETE FROM Company WHERE TICKER=?', (ticker,))
        executor.close()
