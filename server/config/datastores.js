
module.exports.datastores = {
  default: {
    //adapter: require('sails-mysql'),
    //url: 'mysql://root:squ1ddy@localhost:3306/my_dev_db_name',
  },
  mongoDatabase: {
    adapter: require('sails-mongo'),
    url: 'mongodb://communityscraper:xgiLzQA%217%2ADJ%26AS6@communityscraperdb.duckdns.org/communityscraper'
  }
};
