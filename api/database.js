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
            },
            email: {
                type: DataTypes.STRING,
                allowNull: false,
                unique: true
            },
            email_verified_at: {
                type: DataTypes.DATE
            },
            password: {
                type: DataTypes.STRING
            },
            remember_token: {
                type: DataTypes.STRING(100)
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
            token: {
                type: DataTypes.STRING
            },
            pid: {
                type: DataTypes.INTEGER,
                defaultValue: 0
            }
        },
        {
            createdAt: 'created_at',
            updatedAt: 'updated_at',
            indexes: [
                {
                    name: 'pending_index',
                    fields: ['errored', 'completed']
                },
                {
                    name: 'token_index',
                    fields: ['token']
                }
            ]
        })
}
