var express = require('express');
var registerUser = require('./registerUser');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

router.post('/register/user', registerUser);

module.exports = router;
