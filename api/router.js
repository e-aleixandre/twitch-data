const koaBody = require('koa-body');
const {Report} = require("./database");
const fsPromises = require("fs").promises;
const findProcess = require("find-process");
const {spawn} = require("child_process");
const send = require("koa-send");
const router = require('@koa/router')();

module.exports = function (path) {
    /**
     * Middleware
     */

    const reportFromIdAndToken = async (ctx, next) => {
        const {id} = ctx.params;
        const {token} = ctx.request.body;

        const report = await Report.findOne(
            {
                where: {
                    id,
                    token
                }
            }
        );

        if (report) {
            ctx.state.report = report;
            await next();
        } else
            ctx.throw(404);
    }

    const clearToken = async (ctx, next) => {
        const {report} = ctx.state;

        await report.update({
            token: null
        });

        await next();
    }

    const reportFromToken = async (ctx, next) => {
        const {token} = ctx.request.body;

        const report = await Report.findOne({
            where: {
                token
            }
        });

        if (report) {
            ctx.state.report = report;
            await next();
        } else
            ctx.throw(404);
    }

    const needsFilename = async (ctx, next) => {
        const {filename} = ctx.query;

        // TODO: Verify filename for attacks? The PHP backend is the only IP that can fetch this
        //  Sequelize most probably uses prepared statements, and if the filename exists then it's safe
        const report = await Report.count({
            where: {
                filename
            }
        });

        if (report) {
            ctx.state.filename = filename;
            await next();
        } else
            ctx.throw(404);

    }

    /**
     * This function actually checks if its errored OR stopped. At both errored is == 1
     * // TODO: Change name to better describe it then?
     * @param ctx
     * @param next
     * @returns {Promise<void>}
     */
    const isErrored = async (ctx, next) => {
        if (ctx.state.report.errored)
            await next();
        else
            ctx.throw(400);
    }

    const deleteReport = async ctx => {
        const {report} = ctx.state;

        // The report exists
        console.log(`Deleting report ${report.id} with filename ${report.filename}`);

        const filepath = `../temp/${report.filename}`;

        fsPromises.rm(filepath).then(() => {
            console.log("File deleted");
        }).catch(() => {
            console.error("Exception deleting the file");
        });

        await report.destroy();

        ctx.body = {
            ok: true
        }
    }

    // Stop report
    const stopReport = async ctx => {

        const {report} = ctx.state;

        const [proc] = await findProcess("pid", report.pid);

        // If it does exist
        if (proc && proc.name === process.env.PYTHON_EXEC) {
            // Kill it
            process.kill(proc.pid);
            // Set stopped
            await report.update({
                errored: true,
                completed: true
            });
        } else {
            // If it doesn't exist but it was showing as running, set it as errored
            await report.update({
                errored: true
            });
        }

        ctx.body = {
            ok: true
        }
    }

    // Send report file
    const downloadReport = async ctx => {
        const {filename} = ctx.state;

        await send(ctx, filename, {
            root: path.join(__dirname, '../', process.env.EXPORTS)
        });
    }

    // Create new report
    const newReport = async ctx => {

        const {report} = ctx.state;

        // Instantiating the child process
        const out = await fsPromises.open('../logs/out.log', 'a');
        const err = await fsPromises.open('../logs/out.log', 'a');

        const program = spawn(process.env.PYTHON_EXEC, ['../exporter.py', report.min_date.toISOString(), report.max_date.toISOString(), report.id], {
            detached: true,
            stdio: ['ignore', out, err]
        });

        program.unref();

        ctx.body = {
            ok: true
        }
    }

    /**
     * Function for CERTBOT to generate an SSL Certificate
     * @param ctx
     * @returns {Promise<void>}
     */
    const acme_challenge = async ctx => {
        const {file} = ctx.params;

        if (!file)
            ctx.throw(404);

        await send(ctx, file, {
            root: path.join(__dirname, '/.well-known/acme-challenge/')
        });
    }

    /**
     * Restarts an errored report
     *
     * @param ctx
     * @returns {Promise<void>}
     */
    const restartReport = async ctx => {
        const {report} = ctx.state;

        await report.update({
            completed: 0,
            errored: 0
        });

        await newReport(ctx);
    }


    /**
     * Applying routes
     */
    router.post('/reports', koaBody(), reportFromToken, clearToken, newReport)
        .get('/reports', needsFilename, downloadReport)
        .post('/reports/:id/stop', koaBody(), reportFromIdAndToken, clearToken, stopReport)
        .post('/reports/:id/destroy', koaBody(), reportFromIdAndToken, clearToken, deleteReport)
        .get('/.well-known/acme-challenge/:file', acme_challenge)
        .post('/reports/:id/restart', koaBody(), reportFromIdAndToken, clearToken, isErrored, restartReport);

    return router;
}
