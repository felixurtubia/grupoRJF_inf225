var express = require('express');
var router= express.Router();
var path = require("path");
var bodyParser = require('body-parser');
var app=express();
var models  = require('../models/index.js');
var fs = require("fs");




app.use(bodyParser.urlencoded({extended: true }));
app.use(bodyParser.json());
//logout
router.get("/logout",function (req,res) {
    if(req.session.name){
        req.session.destroy();
    }
    res.redirect("/")
});

//------------- CRUD usuario
//Obtener todos los usuarios, ANGULAR
router.get("/usuarios", function (req,res) {
    if (req.session.permiso == "ADMIN") {
        models.User.findAll().then(function (user) {
            res.json(user);
        })
    }
    else {
        res.redirect("/");
    }
});
//Crear usuario
router.post("/usuarios", function (req,res) {
    models.User.create({
        nombre: req.body.nombre,
        apellido: req.body.apellido,
        email:req.body.email,
        password: req.body.password,
        permiso: req.body.permiso
    }).then(function (result) {
        res.redirect("/");
    });
});


//Editar y eliminar users,redirect
router.post('/usuarios/:id',function(req,res) {
    if (req.body.method == "PUT") {
        models.User.find({where: {id: req.params.id}}).then(function (user) {
            if (req.body.username) {
                if (req.body.email) {
                    user.updateAttributes({
                        username: req.body.username,
                        email: req.body.email

                    }).then(function (result) {
                        res.redirect("/");
                    })
                }
                else {
                    user.updateAttributes({
                        username: req.body.username
                    }).then(function (result) {

                        res.redirect("/");
                    })
                }

            }
            else if(req.body.email){
                user.updateAttributes({
                    email: req.body.email
                }).then(function (result){
                    res.redirect("/");
                })
            }
        })
    }
    else if (req.body.text == "DELETE") {
        models.User.destroy({where: {id: req.params.id}}).then(function (user) {
            models.User.findAll().then(function (user) {
                res.json(user);
            })
        })
    }
});

//Crear Ticket
router.post("/tickets", function (req,res) {
    models.Ticket.create({
        asunto: req.body.asunto,
        comentario: req.body.comentario,
        prioridad:req.body.prioridad,
        clasificacion: req.body.clasificacion,
        estado: "no validado",
        creador: req.session.name,
        UserId: req.session.UserId
    }).then(function (result) {
        res.redirect("/");
    });
});

//Obtener tickets
router.get("/tickets", function (req,res) {
    if (req.session.name != null) {
        models.Ticket.findAll().then(function (tickets) {
            res.json(tickets);
        })
    }
    else {
        res.redirect("/");
    }
});

module.exports = router;
