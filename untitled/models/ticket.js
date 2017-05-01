"use strict"
module.exports = function (sequelize, DataTypes) {
    var Ticket = sequelize.define("Ticket", {
        nombre: DataTypes.STRING,
        clasificacion: DataTypes.STRING,
        creador: DataTypes.STRING,
    } , {
        classMethods: {
            associate: function(models){
                Ticket.belongsTo(models.User)
            }
        }
    });
    return Ticket;
}