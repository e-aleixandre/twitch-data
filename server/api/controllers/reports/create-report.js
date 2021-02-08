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

  fn: async function ({minDate, maxDate}, exits) {

    var execSync = require('child_process').execSync, output;
    var program = 'python ../exporter.py ' + minDate + ' ' + maxDate;
    output = execSync(program, { encoding: 'utf-8' });

    var json = JSON.parse(output);
    return exits.success(json);

  }


};
