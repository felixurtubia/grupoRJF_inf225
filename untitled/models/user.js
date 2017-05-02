"use strict";
module.exports = function (sequelize, DataTypes) {
    var User = sequelize.define("User", {
        nombre: DataTypes.STRING,
        apellido: DataTypes.STRING,
        email: DataTypes.STRING,
        password: DataTypes.STRING,
        permiso: DataTypes.STRING
    });
    return User;
}