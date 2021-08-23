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
                type: DataTypes.STRING,
                unique: true
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
                defaultValue: 0.0
            },
            completed: {
                type: DataTypes.BOOLEAN,
                defaultValue: false
            },
            errored: {
                type: DataTypes.BOOLEAN,
                defaultValue: false
            },
            pid: {
                type: DataTypes.INTEGER,
                defaultValue: 0
            }
        },
        {
            createdAt: 'created_at',
            updatedAt: 'updated_at',
            uniqueKeys: {
                dates_unique: {
                    fields: ['min_date', 'max_date']
                }
            }
        })
}
