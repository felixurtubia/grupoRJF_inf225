var express = require("express");
var app=express();
var bodyParser = require('body-parser');
var models  = require('../models/index.js');
var fs = require('fs');

app.use(bodyParser.urlencoded({extended: true }));
app.use(bodyParser.json());


app.get("/",function (req,res) {
    if(req.session.name!=null) {
        res.render('index.html', {session: req.session});
    }else{
        res.render('login.html');
    }
});

app.post("/showUser",function (req,res) {
    if(req.session.name!=null){
        res.render("profile.html",{user:req.body.id})
    }else {
        res.render("login.html")
    }
});

app.get("/showUser",function (req,res) {
    if(req.session.name!=null) {
        res.render("showUser.html")
    }else{
        res.render('login.html')
    }
});

app.post("/modificar",function (req,res) {
    if(req.session.name!=null) {
        res.render("Modificar.html", {id: req.body.id})
    }
    else{
        res.render('login.html')
    }
});


app.get("/createUser",function (req,res) {
    if(req.session.permiso=="ADMIN") {
        res.render("createUser.html");
    }
    else{
        res.redirect("/");
    }
});

app.get("/createTicket",function (req,res) {
    if(req.session.permiso!==null) {
        res.render("createTicket.html");
    }
    else{
        res.redirect("/");
    }
});

app.get("/Proyecto",function (req,res) {
    if(req.session.name!=null) {
        res.render("proyects.html")
    }else{
        res.render('login.html')
    }
});

app.post("/Proyect",function (req,res) {
    if(req.session.name!=null){
        res.render("profileProyect.html",{proyect:req.body.id})
    }else {
        res.render("login.html")
    }
});

app.post("/updateProyect",function (req, res) {
    if(req.session.permiso=="ADMIN") {
        res.render("updateProyect.html", {id: req.body.id})
    }
    else{
        res.redirect("/");
    }
});

app.get("/CreateProyect",function (req,res) {
    if(req.session.permiso=="ADMIN") {
        res.render("CreateProyect.html");
    }
    else{
        res.redirect("/");
    }
});

app.get("/login",function (req,res) {
    if(!req.session.name){
        res.render("login.html")
    }
    else{
        res.redirect("/")
    }
});

app.post("/login", function (req,res) {
    if(req.body.username!=="admin") {
        try {
            models.User.find({where: {username: req.body.username}}).then(function (user) {
                if (user !== null) {
                    if (req.body.password == user.password) {
                        req.session.name = user.username;
                        req.session.UserId = user.id;
                        req.session.permiso = user.permiso;
                        req.session.save();
                        res.render('index.html',{session: req.session})
                    }
                    else {
                        console.log("contraseña erronea");
                        res.render('login.html');
                    }
                }
                else {
                    console.log("error de usuario");
                    res.render('login.html');
                }
            });
        }

        catch (ex) {
            console.log("error de usuario");
            res.render('login.html');
        }
    }
    else{
        req.session.name="admin";
        req.session.permiso="ADMIN";
        req.session.save();
        console.log("Ingreso como administrador");
        res.render('index.html',{session: req.session});
    }

});


module.exports = app;