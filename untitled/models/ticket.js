"use strict"
module.exports = function (sequelize, DataTypes) {
    var Ticket = sequelize.define("Ticket", {
        asunto:DataTypes.STRING,
        comentario: DataTypes.STRING,
        prioridad: DataTypes.STRING,
        clasificacion: DataTypes.STRING,
        estado: DataTypes.STRING,
        creador: DataTypes.STRING
    } , {
        classMethods: {
            associate: function(models){
                Ticket.belongsTo(models.User)
            }
        }
    });
    return Ticket;
}