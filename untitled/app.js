var express = require("express");
var app = express();
var bodyParser = require('body-parser');
var models = require("./models/index.js");
var session = require("express-session");
var session_middleware = require("./middlewares/session");
var formidable = require("express-formidable");

app.use(session({
  secret: "123swticket098"
}));
//app.use(formidable.parse());
app.use(express.static('angular'));

app.use("/",require('./routes/router.js'));
app.use("/",session_middleware);
app.use('/api', require('./routes/api.js'));
app.engine('html', require('ejs').renderFile);

app.use(bodyParser.urlencoded({extended: true }));
app.use(bodyParser.json());




//Start Server
models.sequelize.sync().then(function () {
  app.listen(3000);
})