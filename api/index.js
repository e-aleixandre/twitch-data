/**
 * Requirements
 **/
const Koa = require('koa');
const app = new Koa();
const fs = require('fs');
const http = require('http');
const https = require('https');
const { default: enforceHttps } = require('koa-sslify');
const path = require('path');
const router = require('./router')(path);
//const router = require('@koa/router')();
require('dotenv').config({path: '../.env.local'});

/**
 * Setup
 **/

app.use(router.routes());

if (process.env.ENVIRONMENT === 'production')
{
    app.use(enforceHttps({
        port: 8081
    }));

    const options = {
        key: fs.readFileSync(path.join(__dirname, process.env.CERTS_FOLDER, '/privkey.pem')),
        cert: fs.readFileSync(path.join(__dirname, process.env.CERTS_FOLDER, '/fullchain.pem'))
    }
    https.createServer(options, app.callback()).listen(8081, function() {
        console.log("Listening with HTTPS on port 8081");
    });
}

https.createServer(app.callback()).listen(8080, function() {
    console.log("Listening with HTTP on port 8080");
});
