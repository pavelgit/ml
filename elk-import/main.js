const fs = require('fs-extra');
const elasticsearch = require('elasticsearch');
const moment = require('moment');
const client = new elasticsearch.Client({
    host: 'HOST:PORT'
});

const ISO_8601_DATE_TIME = 'YYYY-MM-DDTHH:mm:ss';

const loadPage = async (startDate, endDate) => {
    const resp = await client.search({
        body: {
          "size": 10000,
          "query": {
            "bool": {
              "must": [
                {
                  "match": {
                    "message": "mmTipperPrices"
                  }
                },
                {
                  "range": {
                    "@timestamp": {
                      "gte": startDate.format(ISO_8601_DATE_TIME),
                      "lt": endDate.format(ISO_8601_DATE_TIME)
                    }
                  }
                }
              ]
            }
          }
        }
    });
    const hits = resp.hits.hits;
    const mappedHits = hits.map(hit => ({
        timestamp: hit._source['@timestamp'],
        calculationInput: hit._source.calculationInput,
        prices: hit._source.prices
    }));
    return {
        hits: mappedHits,
        total: resp.hits.total
    }
};

const loadAllPages = async () => {
    console.log('Ping...');
    await client.ping();
    console.log('Ping successful');
    const fd = await fs.open('output.json', 'w');
    await fs.write(fd, '[');
    try {
        let counter = 0;
        const startDate = moment('2018-02-05 00:00:00');
        const minutesDelta = 10;
        for (; ;) {
            if (startDate.isAfter(moment())) {
              break;
            }
            const endDate = startDate.clone().add(minutesDelta, 'minute');
            const { hits } = await loadPage(startDate, endDate);
            if (hits.length > 0) {
              const hitsJson = JSON.stringify(hits, null, 4);
              const hitsItemsJson = hitsJson.substring(1, hitsJson.length - 1);
              await fs.write(fd, hitsItemsJson);
              await fs.write(fd, ',');
              counter += hits.length;
            }
            console.log('Progress', counter, startDate.format(ISO_8601_DATE_TIME));
            startDate.add(minutesDelta, 'minute');
        }
    } finally {
        await fs.write(fd, ']');
        await fs.close(fd);
    }
};

loadAllPages();