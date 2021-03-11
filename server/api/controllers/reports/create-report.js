module.exports = {


  friendlyName: 'Create report',


  description: '',


  inputs: {
    minDate: {required: true, type: 'string'},
    maxDate: {required: true, type: 'string'}
  },

  exits: {
    success: {
      description: "The report was successfully generated",
    },
    incorrectInput: {
      description: "Starting date is higher than ending date",
      response: "redirect",

    },
    reportsLimit: {
      description: "Too many concurrent reports",
      statusCode: 200,
    }
  },

  fn: async function ({ minDate, maxDate }, exits) {

    const availableReports = await sails.helpers.availableReports();
    if (!availableReports) {
      return exits.success({
        ok: false,
        message: "Hay demasiados informes generándose a la vez. Espera a que acabe alguno."
      });
    }

    const regex = /\d{4}-\d{2}-\d{2}T\d{2}:\d{2}/;

    if (!regex.test(minDate) || !regex.test(maxDate))
    {
      // Las fechas no están bien introducidas (podría ser un intento de ataque)
      return exits.incorrectInput({
        ok: false,
        message: "Las fechas introducidas no son correctas."
      });
    }

    const report = {
      minDate,
      maxDate,
      user: this.req.session.userId
    }

    const newReport = await Report.create(report).fetch();

    const { spawn } = require('child_process');
    const { openSync } = require('fs');
    const out = openSync('../out.log', 'a');
    const err = openSync('../out.log', 'a');

    const program = spawn('python3', ['../exporter.py', minDate, maxDate, newReport.id], {
      detached: true,
      stdio: ['ignore', out, err]
    });

    program.unref();



    return exits.success({
      ok: true,
      report: newReport
    });

  }


};
