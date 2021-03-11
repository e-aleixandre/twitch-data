module.exports = {


  friendlyName: 'Available reports',


  description: 'Checks if there are available reports or already too many processes running.',

  fn: async function () {
    const running = await Report.count({errored: false, completed: false})

    return running < sails.config.scraper.maxConcurrentReports
  }


};

