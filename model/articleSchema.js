var mongoose = require('mongoose');
var Schema = mongoose.Schema;

var articlePostSchema = new Schema(
    {
        date: Date,
        content: String,
        location: [String],
        keyword: [String]
    }
);

module.exports = mongoose.model('article', articlePostSchema);