var express = require('express');
var registerUser = require('./user/registerUser');
var deleteUser = require('./user/deleteUser');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

router.get('/user/delete', deleteUser);
router.post('/user/register', registerUser);

module.exports = router;
