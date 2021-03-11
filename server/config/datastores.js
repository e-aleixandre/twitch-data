
module.exports.datastores = {
  default: {
    adapter: require('sails-postgresql'),
    url: 'postgresql://csfrontend:99hxN2Whum%5E1WYQg@communityscraperdb.duckdns.org/csfrontend',
  },
  mongoDatabase: {
    adapter: require('sails-mongo'),
    url: 'mongodb://communityscraper:xgiLzQA%217%2ADJ%26AS6@communityscraperdb.duckdns.org/communityscraper'
  }
};
