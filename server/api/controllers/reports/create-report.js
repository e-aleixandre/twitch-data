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

    }
  },

  fn: async function ({ minDate, maxDate }, exits) {
    const regex = /\d{2}\/\d{2}\/\d{4}T\d{2}:\d{2}/;

    if (!regex.test(minDate) || !regex.test(maxDate))
    {
      // Las fechas no están bien introducidas (podría ser un intento de ataque)
      return exits.incorrectInput();
    }

    const report = {
      minDate,
      maxDate,
      progress: 0,
      user: this.req.session.userId
    }
    /*
    // TODO: This is 100% exploitable --> sanitize dates
    const { spawn } = require('child_process');
    const { openSync } = require('fs');
    const out = openSync('../out.log', 'a');
    const err = openSync('../out.log', 'a');

    const program = spawn('python3', ['../exporter.py', minDate, maxDate], {
      detached: true,
      stdio: ['ignore', out, err]
    });

    program.unref();

    report.pid = program.pid;

    const newReport = await Report.create(report);
    */
    const newReport = {
      minDate,
      maxDate,
      progress: 0,
      user: this.req.session.userId,
      pid: 2004,
      ok: true
    }
    return exits.success(newReport);

  }


};
