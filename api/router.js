const koaBody = require('koa-body');

const {Report} = require("./database");
const fs = require("fs");
const findProcess = require("find-process");
const mime = require("mime-types");
const {openSync} = require("fs");
const {spawn} = require("child_process");
const send = require("koa-send");
const router = require('@koa/router')();


module.exports = function(path) {
    /**
     * ROUTES
     */
// Delete report (file)
    async function delete_report(ctx) {
        const {id} = ctx.params;
        const {token} = ctx.request.body;

        let report;

        if (id && token) {
            report = await Report.findOne({
                where: {
                    id,
                    token
                },
                attributes: [
                    'id',
                    'filename'
                ]
            });
        }

        if (!report)
            ctx.throw(404);

        const path = `../temp/${report.filename}`;

        try {
            if (fs.existsSync(path)) {
                fs.rmSync(path);
            }
        } catch (e) {
            ctx.throw(500);
        }

        // File is removed, remove report from DB
        await report.destroy();

        ctx.body = {
            ok: true
        }
    }

// Stop report
    async function stop_report(ctx) {

        const {id} = ctx.params;
        const {token} = ctx.request.body;

        let report;

        // If url and data params exist, find the report with those properties
        if (id && token) {
            report = await Report.findOne({
                where: {
                    id,
                    token
                }
            });
        }

        // If no report, throw 404
        if (!report)
            ctx.throw(404);

        // If exists, remove the token so it can't be used again
        // And set it as stopped (errored && completed)
        await report.update({
            token: null,
            errored: true,
            completed: true
        });

        findProcess("pid", report.pid).then(results => {

            const proc = results[0];

            if (proc && proc.name === process.env.PYTHON_EXEC) {
                process.kill(proc.pid);
            }
        });

        ctx.body = {
            ok: true
        }
    }

// Send report file
    async function download_report(ctx) {

        const { filename } = ctx.query;

        // TODO: Verify filename for attacks? The PHP backend is the only IP that can fetch this
        //  Sequelize most probably uses prepared statements, and if the filename exists then it's safe
        let report;

        if (filename)
            report = await Report.count({
                where: {
                    filename
                }
            });

        if (!report) {
            ctx.throw(404);
        }

        await send(ctx, filename, {
            root: path.join(__dirname, process.env.EXPORTS)
        });
    }

// Create new report
    async function new_report(ctx) {

        // For compatibility purposes, we get date + time, and we merge them into a suitable timestamp
        const {token} = ctx.request.body;

        const report = await Report.findOne({
            where: {
                token
            }
        });

        // If the report is not found
        if (!report) {
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

            const program = spawn(process.env.PYTHON_EXEC, ['../exporter.py', report.min_date.toISOString(), report.max_date.toISOString(), report.id], {
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

    /**
     * Function for CERTBOT to generate an SSL Certificate
     * @param ctx
     * @returns {Promise<void>}
     */
    async function acme_challenge(ctx) {
        const { file } = ctx.params;

        if (!file)
            ctx.throw(404);

        await send(ctx, file, {
            root: path.join(__dirname,'/.well-known/acme-challenge/')
        });
    }

    /**
     * Applying routes
     */
    router.post('/reports', koaBody(), new_report)
        .get('/reports', download_report)
        .post('/reports/:id/stop', koaBody(), stop_report)
        .post('/reports/:id/destroy', koaBody(), delete_report)
        .get('/.well-known/acme-challenge/:file', acme_challenge);

    return router;
}
