module.exports = {


  friendlyName: 'View create report',


  description: 'Display "Create report" page.',


  exits: {
    success: {
      responseType: 'view',
      viewTemplatePath: 'pages/reports/create-report'
    }


  },


  fn: async function (exits) {

    // Respond with view.
    return {
      "ok": false,
      "fileName": ""
    }


  }


};
