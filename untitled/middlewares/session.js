module.exports = function(req,res,next){
    if(!req.session.name){
        res.redirect("/login");
    }
    else{
        next();
    }
};