module.exports = {
  friendlyName: 'Create Report',

  description: 'Create a new report',

  extendedDescription: `This asks the user for a few options (for now, min and max date
  and starts a python program that creates the report. Once done, the python program
  should respond to this and send the filename, so it can be sent to the user.`,

  inputs: {
    minDate: {
      required: true,
      type: 'string',
      description: 'The datetime where the report should start'
    },
    maxDate: {
      required: true,
      type: 'string',
      description: 'The datetime where the report should end'
    }
  },

  exits: {
    success: {
      description: 'The new report was created.'
    },

    invalid: {
      responseType: 'badRequest',
      description: 'The form wasn\'t processed correctly.'
    },

    // TODO: If I decide to store filenames so they can be accessed later on,
    //  I could check here if this dates already produced a report
  },

  fn: async function ({minDate, maxDate}) {
    // Here I can process the form when it's submitted
    console.log(minDate, maxDate);

  }
}
