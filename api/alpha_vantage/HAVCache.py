from util.DateUtil import DateUtil
from db.SqlExecutor import SqlExecutor


class HAVCache:
    def __init__(self):
        self.db = SqlExecutor(db_name='gpp-long-term.db')

    # check if we already have cached data for the provided date
    def has_data_for_date(self, ticker, date, no_update_if_today=False):
        found_date = self.get_last_retrieved(ticker)
        # if no found date, then it isn't in the cache at all
        if found_date is None:
            return False

        # found_date is saturday or sunday and is today, don't update cache
        if DateUtil.dates_match(date, found_date) and DateUtil.is_weekend(date) and DateUtil.is_today(date):
            return True

        # if the date is today and it isn't the weekend, we need to update our cache always
        if DateUtil.is_today(date) and not no_update_if_today:
            return False

        # if the date in the metadata is greater than the requested date
        # we already have data for this date, otherwise we need to go get it
        return found_date > date or (no_update_if_today and DateUtil.is_today(date))

    def store_result_meta_data(self, ticker, last_retrieved):
        found = self.get_last_retrieved(ticker)

        # if there's already a metadata record, just update it
        if found is not None:
            sql = 'UPDATE `HISTORIC_META_DATA` SET LAST_RETRIEVED=? WHERE TICKER=?'
            self.db.exec_insert(sql, (last_retrieved, ticker))
        else:
            sql = 'INSERT INTO `HISTORIC_META_DATA` (TICKER, LAST_RETRIEVED) VALUES (?, ?)'
            self.db.exec_insert(sql, (ticker, last_retrieved))

    def store_result_data(self, ticker, date, payload):
        sql = 'INSERT INTO `HISTORIC_DATA` (TICKER, DATE, OPEN, HIGH, LOW, CLOSE, VOLUME) ' \
              'VALUES(?, ?, ?, ?, ?, ?, ?)'

        # check to make sure we're not overwriting something
        data = self.get_daily_quote(ticker, date)
        if data is not None:
            self.db.exec_insert('DELETE FROM `HISTORIC_DATA` WHERE `TICKER`=? AND `DATE`=?', (ticker, date))

        to_send = (ticker, date)
        for item in payload:
            to_send = to_send + (item,)

        self.db.exec_insert(sql, to_send)

    # Checks whether specific date is actually in the cache
    def check_cache(self, ticker, date):
        # don't try the DB before we know if the data will be there
        if not self.has_data_for_date(ticker, date):
            return None

        result = self.get_daily_quote(ticker, date)
        if result is None:
            return None

        return {'ticker': result[0], 'date': result[1], 'open': result[2],
                'high': result[3], 'low': result[4], 'close': result[5], 'volume': result[6]}

    def get_last_retrieved(self, ticker):
        sql = 'SELECT * FROM `HISTORIC_META_DATA` WHERE TICKER=?'
        result = self.db.exec_select(sql, (ticker,)).fetchone()
        if result is None:
            return None

        found_timestamp = result[1]
        return found_timestamp

    def get_all_data(self, ticker):
        sql = 'SELECT * FROM `HISTORIC_DATA` WHERE TICKER=?'
        result = self.db.exec_select(sql, (ticker,)).fetchall()
        return result

    def get_rolling_window_quotes(self, ticker, end_date, num_desired):
        if not self.has_data_for_date(ticker, end_date, no_update_if_today=True):
            return None

        sql = 'SELECT * FROM `HISTORIC_DATA` WHERE TICKER=? AND DATE <= ? ORDER BY DATE DESC LIMIT ?'
        result = self.db.exec_select(sql, (ticker, end_date, num_desired)).fetchall()
        return result

    def get_daily_quote(self, ticker, date):
        sql = 'SELECT * FROM `HISTORIC_DATA` WHERE TICKER=? AND DATE=?'
        result = self.db.exec_select(sql, (ticker, date)).fetchone()
        return result

    def flush(self, ticker):
        sql = 'DELETE FROM `HISTORIC_DATA` WHERE TICKER=?'
        self.db.exec_insert(sql, (ticker,))
