module.exports = {


  friendlyName: 'View report created',


  description: 'Display "Report created" page.',


  exits: {

    success: {
      viewTemplatePath: 'pages/reports/report-created'
    }

  },


  fn: async function () {

    // Respond with view.
    return {};

  }


};
