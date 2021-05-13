var mongoose = require('mongoose')

var init = function() {
    const config = {
        protocol: "mongodb+srv",
        userName: "hellobye9290",
        userPW: "tmteatn319",
        path: "cluster0.x9izi.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",
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