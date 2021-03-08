/**
 * Report.js
 *
 * CommunityScraper reports
 */

module.exports = {
  attributes: {
    fileName: {
      type: 'string',
      example: 'c4aa317fb1490c04365f2994e15f6d731e9b26988314dc4012339d40'
    },
    minDate: {
      type: 'string',
      required: true
    },
    maxDate: {
      type: 'string',
      required: true
    },
    progress: {
      type: 'number',
      columnType: 'FLOAT',
      required: true,
      example: '78.4'
    },
    completed: {
      type: 'boolean',
      defaultsTo: false
    },
    pid: {
      type: 'number',
      required: true,
      example: 4875
    },
    //  ╔═╗╔═╗╔═╗╔═╗╔═╗╦╔═╗╔╦╗╦╔═╗╔╗╔╔═╗
    //  ╠═╣╚═╗╚═╗║ ║║  ║╠═╣ ║ ║║ ║║║║╚═╗
    //  ╩ ╩╚═╝╚═╝╚═╝╚═╝╩╩ ╩ ╩ ╩╚═╝╝╚╝╚═╝
    user: {
      model: 'user'
    }
  }
}
