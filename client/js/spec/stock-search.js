(function(window) {
    'use strict';

    const createElement = (elType, innerText) => {
        const el = window.document.createElement(elType);
        el.innerText = innerText ? innerText : '';
        return el;
    };

    const constructTable = tickerMeta => {
        const table = createElement('table');
        table.setAttribute('id', 'ticker-table');
        const thead = createElement('thead');
        let row = createElement('tr');
        row.appendChild(createElement('th', 'Ticker'));
        row.appendChild(createElement('th', tickerMeta.ticker));
        thead.appendChild(row);
        table.appendChild(thead);

        const tbody = createElement('tbody');
        Object.keys(tickerMeta).forEach(metaKey => {
            if (metaKey === 'ticker')
                return;

            row = createElement('tr');
            row.appendChild(createElement('td', metaKey));
            row.appendChild(createElement('td', tickerMeta[metaKey]));
            tbody.appendChild(row);
        });

        table.appendChild(tbody);
        return table;
    };

    let currentTicker = null;
    window.addEventListener('load', () => {
        const tableTarget = window.document.querySelector('#stock-target');
        const refreshButton = window.document.querySelector('#refresh-meta-btn');
        const buildTickerTable = () => {
            currentTicker = null;
            const ticker = window.document.querySelector('#stock-ticker').value;
            request('/stock-search/ticker?t=' + ticker, {} , data => {
                Array.from(tableTarget.children).forEach(el => tableTarget.removeChild(el));
                refreshButton.classList.add('hidden');
                if (!data) {
                    tableTarget.appendChild(createElement('b', 'No results found'));
                    return;
                }

                const table = constructTable(data);
                tableTarget.appendChild(table);
                refreshButton.classList.remove('hidden');
                currentTicker = ticker.toUpperCase();
            }, e => {
                console.error(e);
            }, request.METHODS.GET);
        };

        window.document.querySelector('#search-btn').addEventListener('click', buildTickerTable);

        window.document.querySelector('#stock-ticker').addEventListener('keyup', e => {
            const k = e.key.toLowerCase();
            if (k === 'enter' || k === 'return')
                buildTickerTable();
        });

        refreshButton.addEventListener('click', () => {
            if (!currentTicker)
                return;

            refreshButton.setAttribute('disabled', 'true');
            request('/stock-search/ticker?t=' + currentTicker, {} , data => {
                Array.from(tableTarget.children).forEach(el => tableTarget.removeChild(el));
                if (!data) {
                    tableTarget.appendChild(createElement('b', 'No results found'));
                    return;
                }

                const table = constructTable(data);
                tableTarget.appendChild(table);
                refreshButton.removeAttribute('disabled');
            }, e => {
                console.error(e);
            }, request.METHODS.PUT);
        });
    });
})(window);