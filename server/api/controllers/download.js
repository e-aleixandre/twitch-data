module.exports = {


  friendlyName: 'Download a report',


  description: 'Sends the file to the user\'s browser',


  exits: {

    success: {
      description: 'The file has been sent for download.',
    },
    noFilename: {
      description: 'No filename',
      responseType: 'redirect'
    }

  },


  fn: async function (exits) {
    var file = await this.req.params.filename;
    if(!file) { throw 'error'}
    file = file + ".xlsx";
    this.res.attachment(file);
    var downloading = await sails.startDownload("/downloads/" + file);
    return exits.success(downloading);
  }


};
