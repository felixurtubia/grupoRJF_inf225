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

//los usa userController--> agregar al reves para usar en profileController
router.get("/usersProyect/:id", function (req,res) {
    models.UserProyect.findAll({where:{UserId: req.params.id}}).then(function (result) {
        res.json(result);
    });
});
router.get("/proyectUsers/:id", function (req,res) {
    models.UserProyect.findAll({where:{ProyectId: req.params.id}}).then(function (result) {
        res.json(result);
    });
});

router.get("/userProyect",function (req,res) {
    models.UserProyect.findAll().then(function (datos) {
        res.json(datos)
    })
});

router.post('/userProyect/:id',function(req,res) {
    if (req.body.text == "DELETE") {
        models.UserProyect.destroy({where: {id: req.params.id}}).then(function (userProyect) {
            return models.UserProyect.findAll().then(function (userProyect) {
                res.json(userProyect);
            })
        })
    }
    else if(req.body.text=="Create"){
        models.UserProyect.create({
            UserId: req.params.id,
            ProyectId: req.body.proyectId
        }).then(function (result) {
            models.UserProyect.findAll({}).then(function (userProyect) {
                res.json(userProyect);
            })
        });
    }

});

router.post('/proyectUsers/:id',function(req,res) {
    if(req.body.text=="Create"){
        models.UserProyect.create({
            UserId: req.body.userId,
            ProyectId: req.params.id
        }).then(function (result) {
            models.UserProyect.findAll().then(function (userProyect) {
                res.json(userProyect);
            })
        });
    }
});

//obtener datos tabla rol
router.get("/Rol",function (req,res) {
    models.Rol.findAll().then(function (datos) {
        res.json(datos)
    })
});

router.get("/Rol/:id",function (req,res) {
    models.Rol.findAll({where:{UserId: req.params.id}}).then(function (datos) {
        res.json(datos)
    })
});


//??????
router.post("/baseDatosLlamar",function (req,res) {
    models.Dato.findAll({
        where: {
            estado:  "no"
            ,
            ProyectId: req.body.id
        }
    }).then(function (dato) {
        res.json(dato)
    })

});
router.post('/baseDatosLlamar/:id',function(req,res) {
    models.Dato.find({where: {ProyectId: req.body.id, Id: req.params.id}}).then(function (dato) {
        dato.updateAttributes({
            estado: req.body.text
        });
        res.json(dato);
    });
});
// Ver tabla
//ver datos de tabla
router.post("/baseDatos",function (req,res) {
    if(req.session.permiso == "ADMIN") {
        models.Dato.findAll({where: {ProyectId: req.body.idProyect}}).then(function (dato){
            res.render('tabla.html',{datos: dato});
        })
    }
    else {
        res.redirect("/");
    }
});
//lo esta usando el userController, quita eso y cambialo por el de abajo
router.get("/Proyect",function (req,res) {
    models.Proyect.findAll().then(function (proyect) {
        res.json(proyect);
    })
});

//CRUD proyecto

//obtener proyectos
router.get("/Proyect/:id",function (req,res) {
    models.Proyect.findAll({where:{id:req.params.id}}).then(function (proyect) {
        res.json(proyect)
    })
})

//Crear proyecto
router.post("/Proyect",function (req,res) {
    if(req.body.url.slice(0,7)=="http://" || req.body.url.slice(0,8)=="https://") {
        models.Proyect.create({
            nombre: req.body.nombre,
            URL: req.body.url
        });
    }else{
        models.Proyect.create({
            nombre: req.body.nombre,
            URL: "http://"+req.body.url
        });
    }
    res.redirect("/");
});

//editar, borrar proyecto, redirecciona
router.post('/Proyect/:id',function(req,res) {
    if (req.body.method == "PUT") {
        models.Proyect.find({where: {id: req.params.id}}).then(function (proyect) {
            proyect.updateAttributes({
                nombre: req.body.nombre
            }).then(function (result) {
                res.redirect("/");
            })
        })
    }
    else if (req.body.text == "DELETE") {
        models.Proyect.destroy({where: {id: req.params.id}}).then(function (proyect) {
            return models.Proyect.findAll().then(function (proyect) {
                res.json(proyect);
            })
        })
    }
});

//CRUD usuario
//Obtener todos los usuarios, angular
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
        username: req.body.username,
        password: req.body.password,
        permiso: req.body.permiso,
    }).then(function (result) {
        res.redirect("/");
    });
});

//obtener datos, angular
router.get('/profile/:id',function(req,res) {
    models.User.findAll({
        where: {
            id: req.params.id
        }
    }).then(function (user) {
        res.json(user);
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

router.get("/download/:name",function (req,res) {
    res.download('../Proyecto/public/download/'+req.params.name)
});


router.get("/Download", function (req,res) {
    var p = "./public/download";
    var archivo = []
    fs.readdir(p, function (err, files) {
        console.log(files)
        if (err) {
            throw err;
        }
        files.forEach(function (file) {
            archivo.push(file);
        });
        res.render("TablaDescarga.html",{archivo:archivo})
    });

});

//Cargar datos---> agregar extensiones posibles y mejorar la pagina de subida
router.post("/CargarArchivo", function (req,res) {
    fs.readFile(req.body.archivo.path,'utf8',function read(err,allText) {
        if (err){
            throw err;
        }
        var allTextLines = allText.split(/\r\n|\n/);
        var headers = allTextLines[0].split(',');
        var lines = [];
        for (var i=1; i<allTextLines.length; i++) {
            var data = allTextLines[i].split(',');
            if (data.length == headers.length) {
                var tarr = [];
                for (var j=0; j<headers.length; j++) {
                    tarr.push(data[j]);
                }
                lines.push(tarr);
            }
        }
        for(var j=0;j<lines.length;j++){
            models.Dato.create({
                nombre: lines[j][0],
                apellido: lines[j][1],
                numero: lines[j][2],
                estado: lines[j][3],
                ProyectId: req.body.id
            })
        }
        console.log(req.body.archivo.path);
        res.render("MostrarDatos.html", {datos: lines} );
    })
});



module.exports = router;
