var mongoose = require('mongoose');
var Schema = mongoose.Schema;

var userPostSchema = new Schema(
    {
        email: String,
        cityList: Array,
        countyList: Array,
        selectList: Array,
        created: {
            type: Date,
            default: Date.now,
        },
    }
);

module.exports = mongoose.model('user', userPostSchema);