module.exports = {


  friendlyName: 'Delete report',


  description: 'Deletes a report from the DB and the filesystem',


  inputs: {
    id: {
      type: 'number',
      required: true
    }
  },

  exits: {
    success: {
      description: "The report was successfully deleted",
    },
    doesntExist: {
      description: "The report doesnt exist",
    }
  },

  fn: async function ({ id }, exits) {

    const { unlinkSync } = require('fs');

    try {
      let report = await Report.destroyOne({id})
      unlinkSync(`.tmp/public/reports/${report.fileName}`);

      return exits.success({
        ok: true,
        report
      });
    } catch (e) {
      return exits.success({
        ok: false
      });
    }
  }


};
