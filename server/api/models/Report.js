/**
 * Report.js
 *
 * CommunityScraper reports
 */

module.exports = {
  tableName: 'reports',
  attributes: {
    fileName: {
      type: 'string',
      example: 'c4aa317fb1490c04365f2994e15f6d731e9b26988314dc4012339d40'
    },
    minDate: {
      type: 'ref',
      columnType: 'timestamp',
      required: true
    },
    maxDate: {
      type: 'ref',
      columnType: 'timestamp',
      required: true
    },
    progress: {
      type: 'number',
      columnType: 'decimal',
      defaultsTo: 0.0,
      example: '78.4'
    },
    completed: {
      type: 'boolean',
      defaultsTo: false
    },
    errored: {
      type: 'boolean',
      defaultsTo: false
    },
    pid: {
      type: 'number',
      defaultsTo: 0
    },
    //  ╔═╗╔═╗╔═╗╔═╗╔═╗╦╔═╗╔╦╗╦╔═╗╔╗╔╔═╗
    //  ╠═╣╚═╗╚═╗║ ║║  ║╠═╣ ║ ║║ ║║║║╚═╗
    //  ╩ ╩╚═╝╚═╝╚═╝╚═╝╩╩ ╩ ╩ ╩╚═╝╝╚╝╚═╝
    user: {
      model: 'user'
    }
  }
}
