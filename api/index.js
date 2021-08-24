/**
 * Requirements
 **/
const Koa = require('koa');
const app = new Koa();
const router = require('@koa/router')();
const koaBody = require('koa-body');
const {spawn} = require('child_process');
const {openSync} = require('fs');
const {User, Report, sequelize} = require('./database');

require('dotenv').config({path: '../.env.local'});

/**
 * Setup
 **/

router.post('/reports', koaBody(), new_report)
      .get('/reports', download_report);

app.use(router.routes());

app.listen(3000);

sequelize.sync({force: true});

/**
 * ROUTES
 */
// Send report file
async function download_report(ctx) {

    const { filename } = ctx.query;

    // https://blog.cpming.top/p/koa-write-to-response

}

// Create new report
async function new_report(ctx) {

    // For compatibility purposes, we get date + time, and we merge them into a suitable timestamp
    const { token } = ctx.request.body;

    const report = await Report.findOne({
        where: {
            token
        }
    });

    // If the report is not found
    if (!report)
    {
        ctx.status = 404;

        ctx.body = {
            ok: false,
            msg: "ER_NOT_FOUND"
        }

        return;
    }

    // Removing the token so the endpoint is not accessible anymore
    report.token = null;
    await report.save();

    // Instantiating the child process
    try {

        const out = openSync('../logs/out.log', 'a');
        const err = openSync('../logs/out.log', 'a');

        const program = spawn('py', ['../exporter.py', report.min_date.toISOString(), report.max_date.toISOString(), report.id], {
            detached: true,
            stdio: ['ignore', out, err]
        });

        program.unref();

        ctx.body = {
            ok: true
        }

    } catch (e) {

        let message;

        if (e.original) {
            message = e.original.code;
        } else {
            // Handle other types of exceptions
            message = "ER_UNKNOWN";
        }

        ctx.body = {
            ok: false,
            message
        }

    }
}
