"use strict";
module.exports = function (sequelize, DataTypes) {
    var User = sequelize.define("User", {
        username: DataTypes.STRING,
        password: DataTypes.STRING,
        permiso: DataTypes.STRING,
    } , {
        classMethods: {
            associate: function(models){
                User.hasMany(models.Ticket)
            }
        }
    });
    return User;
}