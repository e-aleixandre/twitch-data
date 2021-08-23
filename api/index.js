/**
 * Requirements
 **/
const Koa = require('koa');
const app = new Koa();
const router = require('@koa/router')();
const koaBody = require('koa-body');
const {spawn} = require('child_process');
const {openSync} = require('fs');
const {User, Report, sequelize} = require('./models');

require('dotenv').config({path: '../.env.local'});

/**
 * Setup
 **/

router.post('/', koaBody(), new_report).get('/', async function (ctx) {
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

    const {minDate, maxDate} = ctx.request.body;

    try {
        const out = openSync('../logs/out.log', 'a');
        const err = openSync('../logs/out.log', 'a');

        const report = await Report.create({max_date: maxDate, min_date: minDate});

        const program = spawn('py', ['../exporter.py', minDate, maxDate, report.id], {
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
        ctx.body = {
            ok: false
        }
    }
}

