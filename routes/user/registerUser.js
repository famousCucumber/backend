const express = require('express');
const UserSchema = require('../../model/userSchema');
const router = express.Router();

router.use('/', async function(req, res, next) {
    try {
        const { email, cityList, countyList, selectList } = req.body;
        const userSchema = new UserSchema();

        userSchema.email = email;
        userSchema.cityList = cityList.slice();
        userSchema.countyList = countyList.slice();
        userSchema.selectList = selectList.slice();

        await userSchema.save();

        res.status(200)
           .json({message: 'successfully registered'});

    } catch(err) {
        res.status(500)
           .json({message: 'failed due to internal error', err: JSON.stringify(err)});
    }
});

module.exports = router;