const {Sequelize, DataTypes} = require('sequelize');
require('dotenv').config({path: '../.env.local'});

/**
 * Initialize DB
 */
const sequelize = new Sequelize(process.env.FRONTENDDB_NAME, process.env.FRONTENDDB_USER, process.env.FRONTENDDB_PASS, {
    host: process.env.FRONTENDDB_HOST,
    dialect: 'mariadb'
});

/**
 * Exports and model definitions
 */
module.exports = {
    sequelize,
    User: sequelize.define('User', {
            name: {
                type: DataTypes.STRING,
                allowNull: false
            }
        },
        {
            createdAt: 'created_at',
            updatedAt: 'updated_at'
        }),
    Report: sequelize.define('Report', {
            filename: {
                type: DataTypes.STRING
            },
            min_date: {
                type: DataTypes.DATE,
                allowNull: false
            },
            max_date: {
                type: DataTypes.DATE,
                allowNull: false
            },
            progress: {
                type: DataTypes.FLOAT,
                default: 0.0
            },
            completed: {
                type: DataTypes.BOOLEAN,
                default: false
            },
            errored: {
                type: DataTypes.BOOLEAN,
                default: false
            },
            pid: {
                type: DataTypes.INTEGER,
                default: 0
            }
        },
        {
            createdAt: 'created_at',
            updatedAt: 'updated_at'
        })
}
