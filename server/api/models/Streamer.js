/**
 * Streamer.js
 *
 * Streamers to fetch data from
 */
module.exports = {
  datastore: 'mongoDatabase',
  tableName: 'streamers',
  attributes: {
    id: {
      type: 'string',
      columnName: '_id'
    },
    userLogin: {
      columnName: 'user_login',
      type: 'string',
      required: true,
      unique: true,
      example: 'nombre_random'
    }
  }
};
