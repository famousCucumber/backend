const UserSchema = require('../../model/userSchema');

var buildQuery = function (in_locationList, in_selectList) {
    var locationQuery = new Array();
    var selectQuery = new Array();

    in_locationList.forEach(location => {
        locationQuery.push({ locationList: location });
    });
    in_selectList.forEach(select => {
        selectQuery.push({ selectList: select });
    });

    var query = {
        $and: [
            { $or: locationQuery },
            { $or: selectQuery },
        ],
    };
    return query;
};

var getUserEmailByKeywords = function (in_locationList, in_selectList) {
    return new Promise(async function (resolve, reject) {
        try {
            var emailList = new Set();
            var query = buildQuery(in_locationList, in_selectList);
            var userList = await UserSchema
                .find()
                .or(query)
                .exec();

            userList.forEach(user => {
                emailList.add(user.email);
            });
            resolve(emailList);
        } catch (err) {
            reject(err);
        }
    });
}

module.exports = getUserEmailByKeywords;