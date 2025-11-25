import pytest
from datetime import datetime

import backtrader as bt


def test_yfinance_data_download(monkeypatch):
    yf = pytest.importorskip('yfinance', reason='yfinance extra not installed')
    pd = pytest.importorskip('pandas', reason='pandas required for yfinance')
    from backtrader.feeds.yahoo import YahooFinanceData

    # Build a timezone-aware DataFrame to exercise tz stripping in start_yfinance
    index = pd.DatetimeIndex([pd.Timestamp('2024-01-02T00:00:00Z')])
    df = pd.DataFrame(
        {
            'Open': [1.0],
            'High': [2.0],
            'Low': [0.5],
            'Close': [1.5],
            'Adj Close': [1.4],
            'Volume': [10],
        },
        index=index,
    )
    df.index.name = 'Date'

    def fake_download(ticker, start=None, end=None, interval=None, **kwargs):
        assert ticker == 'AAPL'
        assert interval == '1d'
        return df

    monkeypatch.setattr(yf, 'download', fake_download)

    data = YahooFinanceData(
        dataname='AAPL',
        fromdate=datetime(2024, 1, 2),
        todate=datetime(2024, 1, 3),
        timeframe=bt.TimeFrame.Days,
    )

    captured = []

    class Recorder(bt.Strategy):
        def next(self):
            captured.append(
                (
                    self.data.datetime.datetime(0),
                    self.data.open[0],
                    self.data.high[0],
                    self.data.low[0],
                    self.data.close[0],
                    self.data.volume[0],
                    self.data.adjclose[0],
                )
            )

    cerebro = bt.Cerebro(stdstats=False, runonce=True, preload=True, exactbars=1)
    cerebro.adddata(data)
    cerebro.addstrategy(Recorder)
    cerebro.run()

    assert len(captured) == 1
    dt, o, h, l, c, v, adj = captured[0]
    assert dt.date() == datetime(2024, 1, 2).date()
    adjfactor = 1.5 / 1.4  # values will be adjusted because adjclose=True
    decimals = 2
    assert o == pytest.approx(round(1.0 / adjfactor, decimals))
    assert h == pytest.approx(round(2.0 / adjfactor, decimals))
    assert l == pytest.approx(round(0.5 / adjfactor, decimals))
    assert c == pytest.approx(1.4)
    assert v == pytest.approx(round(10 * adjfactor, 0))
    assert adj == pytest.approx(1.4)
