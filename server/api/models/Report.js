/**
 * Report.js
 *
 * CommunityScraper reports
 */

module.exports = {
  attributes: {
    fileName: {
      type: 'string',
      required: true,
      unique: true,
      example: 'c4aa317fb1490c04365f2994e15f6d731e9b26988314dc4012339d40'
    },
    process: {
      type: 'number',
      columnType: 'FLOAT',
      required: true,
      example: '78.4'
    },
    //  ╔═╗╔═╗╔═╗╔═╗╔═╗╦╔═╗╔╦╗╦╔═╗╔╗╔╔═╗
    //  ╠═╣╚═╗╚═╗║ ║║  ║╠═╣ ║ ║║ ║║║║╚═╗
    //  ╩ ╩╚═╝╚═╝╚═╝╚═╝╩╩ ╩ ╩ ╩╚═╝╝╚╝╚═╝
    user: {
      model: 'user'
    }
  }

}
