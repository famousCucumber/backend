const express = require('express');
const UserSchema = require('../../model/userSchema');
const router = express.Router();

router.use('/', async function(req, res, next) {
    try {
        const userData = req.body;
        var userSchema;

        userSchema = await UserSchema.find({email: userData.email});
        if(!userSchema || !userSchema.length) {
            userSchema = new UserSchema();
        } else {
            userSchema = userSchema[0];
        }

        userSchema.email = userData.email;
        userSchema.cityList = userData.cityList.slice();
        userSchema.countyList = userData.countyList.slice();
        userSchema.selectList = userData.selectList.slice();

        await userSchema.save();

        res.status(200)
           .json({message: 'successfully registered'});

    } catch(err) {
        console.error(err);
        res.status(500)
           .json({message: 'failed due to internal error', err: JSON.stringify(err)});
    }
});

module.exports = router;