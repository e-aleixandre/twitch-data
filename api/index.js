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
 * Constants
 */
const maxReports = 1;

/**
 * Middleware definitions
 */
async function limitReports(ctx, next) {

    const currentReports = await Report.count({
        where: {
            errored: false,
            completed: false
        }
    });

    if (currentReports < maxReports)
    {
        return next();
    } else {
        ctx.body = {
            ok: false,
            msg: 'ER_MAX_REPORTS'
        }
    }
}

/**
 * Setup
 **/

router.post('/', limitReports, koaBody(), new_report).get('/', async function (ctx) {
    ctx.body = "Ok"
});

app.use(router.routes());

app.listen(3000);

sequelize.sync({ force: true });

/**
 * ROUTES
 */

// Create new report
async function new_report(ctx) {

    // For compatibility purposes, we get date + time, and we merge them into a suitable timestamp
    const {minDate, minTime, maxDate, maxTime} = ctx.request.body;

    const data = {
        minTimestamp: minDate + 'T' + minTime,
        maxTimestamp: maxDate + 'T' + maxTime
    };

    // Then we validate them
    const regex = /\d{4}-\d{2}-\d{2}T\d{2}:\d{2}/;

    if (!regex.test(data.minTimestamp) || !regex.test(data.maxTimestamp))
    {
        ctx.body = {
            ok: false,
            msg: 'ER_INVALID_DATE'
        }

        return;
    }

    try {

        const out = openSync('../logs/out.log', 'a');
        const err = openSync('../logs/out.log', 'a');

        const report = await Report.create({max_date: data.maxTimestamp, min_date: data.minTimestamp});

        const program = spawn('py', ['../exporter.py', data.maxTimestamp, data.minTimestamp, report.id], {
            detached: true,
            stdio: ['ignore', out, err]
        });

        program.unref();

        ctx.body = {
            ok: true,
            data: {
                id: report.id,
                pid: program.pid
            }
        }

    } catch(e) {

        let message;

        if (e.original)
        {
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
