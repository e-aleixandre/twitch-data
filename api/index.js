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
    console.log("Production environment, starting http to https redirection");

    app.use(enforceHttps({
        port: 8081
    }));

    const options = {
        key: fs.readFileSync(process.env.SERVER_KEY),
        cert: fs.readFileSync(process.env.SERVER_CERT),
        // This is proven to overwrite trusted CA, only CERT_CHAIN is trusted now
        ca: fs.readFileSync(process.env.CERT_CHAIN),
        rejectUnauthorized: true,
        requestCert: true
    }
    https.createServer(options, app.callback()).listen(8081, function() {
        console.log("Listening with HTTPS on port 8081");
    });
} else {
    console.log("Development environment, starting http only");
}
