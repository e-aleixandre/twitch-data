parasails.registerPage('reports', {
  //  ╦╔╗╔╦╔╦╗╦╔═╗╦    ╔═╗╔╦╗╔═╗╔╦╗╔═╗
  //  ║║║║║ ║ ║╠═╣║    ╚═╗ ║ ╠═╣ ║ ║╣
  //  ╩╝╚╝╩ ╩ ╩╩ ╩╩═╝  ╚═╝ ╩ ╩ ╩ ╩ ╚═╝
  data: {
    reports: []
  },

  //  ╦  ╦╔═╗╔═╗╔═╗╦ ╦╔═╗╦  ╔═╗
  //  ║  ║╠╣ ║╣ ║  ╚╦╝║  ║  ║╣
  //  ╩═╝╩╚  ╚═╝╚═╝ ╩ ╚═╝╩═╝╚═╝
  beforeMount:  function() {
    const format = "DD-MM-YY, HH:MM";
    this.reports = this.reports.map(report => {
      if (report.completed)
      {
        report.filePath = `/reports/${report.fileName}`;
      }

      report.minDate = moment(report.minDate).format(format);
      report.maxDate = moment(report.maxDate).format(format);
      return report;
    });
  },
  mounted: function() {
    //...
  },

  //  ╦╔╗╔╔╦╗╔═╗╦═╗╔═╗╔═╗╔╦╗╦╔═╗╔╗╔╔═╗
  //  ║║║║ ║ ║╣ ╠╦╝╠═╣║   ║ ║║ ║║║║╚═╗
  //  ╩╝╚╝ ╩ ╚═╝╩╚═╩ ╩╚═╝ ╩ ╩╚═╝╝╚╝╚═╝
  methods: {
    stopReport: async function(id) {
      const _csrf = SAILS_LOCALS._csrf;
      let response = await $.post("/api/v1/reports/stop-report", {id, _csrf})
      if (response.ok) {
        this.reports = this.reports.filter(report => report.id !== id);
      } else {
        alert("Error al parar el informe. Puede que se haya parado o puede que no, puede que el informe aún siga en la lista.");
      }
    },
    downloadReport: function(filePath) {
      this.goto(filePath)
    },
    deleteReport: async function(id) {
      const _csrf = SAILS_LOCALS._csrf;
      let response = await $.post("/api/v1/reports/delete-report", {id, _csrf});
      if (response.ok) {
        this.reports = this.reports.filter(report => report.id !== id);
      } else {
        alert("Error al borrar el informe. Puede que no se haya borrado el archivo, o puede que el informe siga en la lista.");
      }
    }
  }
});
