var mongoose = require('mongoose')

var init = function() {
    const config = {
        protocol: "mongodb",
        userName: process.env.DB_USERNAME,
        userPW: process.env.DB_PW,
        path: process.env.DB_PATH,
        getfullURL: function() {
            return`${this.protocol}://${this.userName}:${this.userPW}@${this.path}`;
        },
    }

    var dbConnectURL = config.getfullURL();
    var dbConnectOption = {
        useUnifiedTopology: true,
        useNewUrlParser: true
    };
    var db = mongoose.connection;

    db.on('error', console.error);
    db.once('open', () => console.log('Connected to MongoDB'));
    mongoose.connect(dbConnectURL, dbConnectOption);
    return db;
}

module.exports = init;