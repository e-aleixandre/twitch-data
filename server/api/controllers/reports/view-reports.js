module.exports = {


  friendlyName: 'View reports',


  description: 'Display "Reports" page.',


  exits: {

    success: {
      responseType: 'view',
      viewTemplatePath: 'pages/reports/reports'
    }

  },


  fn: async function () {

    let reports = await Report.find();
    // Respond with view.
    return {reports};

  }


};
