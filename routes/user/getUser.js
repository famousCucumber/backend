const UserSchema = require('../../model/userSchema');

var getUserEmailByKeywords = function (in_keywordList) {
    return new Promise(async function (resolve, reject) {
        try {
            var emailList = new Array();
            var searchDB = function() {
                return new Promise(async function(resolve, reject){
                    try{
                        for(let i = 0; i < in_keywordList.length; i++) {
                            var keyword = in_keywordList[i];
                            var userList = await UserSchema
                                .find({keywordList: keyword})
                                .exec();
                            userList.forEach(user => {
                                emailList.push(user.email);
                                console.log('in');
                                console.log(emailList);
                            });
                        }
                        resolve();
                    }catch(err) {
                        console.error(err);
                        reject();
                    }
                });
            };
            if (in_keywordList) {
                console.log('await');
                await searchDB();
                console.log('await finish');
                console.log(emailList);
                var returnList = new Set(emailList);
                resolve(returnList);
            }
        } catch (err) {
            reject(err);
        }
    });
}

module.exports = getUserEmailByKeywords;