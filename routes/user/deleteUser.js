const express = require('express');
const UserSchema = require('../../model/userSchema');
const router = express.Router();

function validateEmail(email) {
    var re = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i;
    return re.test(email);
}

router.use('/', async function(req, res, next) {
    try {
        var targetEmail = req.query.email;

        if (!validateEmail(targetEmail)) {
            return res.status(400)
                .json({message: 'Invaild Email'});
        }

        var output = await UserSchema.deleteMany({email: targetEmail});

        if(output.n == 0) {
            console.log('User not found');
            return res.status(400)
                      .json({message: 'User not found'});
        }

        console.log('User Deleted');
        res.status(200)
           .json({message: 'successfully deleted'});

    } catch(err) {
        console.error(err);
        res.status(500)
           .json({message: 'failed due to internal error', err: JSON.stringify(err)});
    }
});

module.exports = router;