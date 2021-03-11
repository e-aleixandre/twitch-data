module.exports = {


  friendlyName: 'Stop report',


  description: 'Stops the process generating the report and deletes the entry from the database',


  inputs: {
    id: {
      type: 'number',
      required: true
    }
  },

  exits: {
    success: {
      description: "The report was successfully stopped",
    },
    doesntExist: {
      description: "The report doesnt exist",
    }
  },

  fn: async function ({ id }, exits) {

    try {
      let report = await Report.destroyOne({id})

      if (report.pid !== 0)
        process.kill(report.pid)

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
