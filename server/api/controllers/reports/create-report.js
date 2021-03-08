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
    const report = {
      minDate,
      maxDate,
      progress: 0,
      user: this.req.session.userId
    }
    // TODO: This is 100% exploitable --> sanitize dates
    const { spawn } = require('child_process');
    const { openSync } = require('fs');
    const out = openSync('../out.log', 'a');
    const err = openSync('../out.log', 'a');
    //const program = 'python3 ../exporter.py ' + minDate + ' ' + maxDate;
    const program = spawn('python3', ['../exporter.py', minDate, maxDate], {
      detached: true,
      stdio: ['ignore', out, err]
    });

    program.unref();

    report.pid = program.pid;

    const newReport = await Report.create(report);

    return exits.success(newReport);

  }


};
