const express = require('express');
const UserSchema = require('../../model/userSchema');
const router = express.Router();

function validateEmail(email) {
    var re = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;
    return re.test(email);
}

router.use('/', async function(req, res, next) {
    try {
        const userData = req.body;
        var userSchema;
        var responseJSON = {};
        
        if (!validateEmail(userData.email)) {
            return res.status(400)
                .json({message: 'Invaild Email'});
        }

        userSchema = await UserSchema.find({email: userData.email});
        if(!userSchema || !userSchema.length) {
            userSchema = new UserSchema();
            responseJSON.message = 'Successfully registered new user';
        } else {
            userSchema = userSchema[0];
            responseJSON.message = 'Successfully modified user information';
        }

        userSchema.email = userData.email;
        userSchema.locationList = userData.locationList.slice();
        userSchema.selectList = userData.selectList.slice();

        await userSchema.save();

        res.status(200)
           .json(responseJSON);
        
    } catch(err) {
        console.error(err);
        res.status(500)
           .json({message: 'failed due to internal error', err: JSON.stringify(err)});
    }
});

module.exports = router;