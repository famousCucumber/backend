var cron = require('node-cron');
const { PythonShell } = require('python-shell');
const ArticleSchema = require('../../model/articleSchema');

cron.schedule('*/1 * * * *', function () {
    ArticleSchema.findOne()
        .sort('-ordr')
        .exec((err, article) => {
            let lastOrdr = article.ordr;
        
            let options = {
                scriptPath: path.join(__dirname, "../../tools/"),
                args: [lastOrdr]
            };

            // Run Python
            PythonShell.run("crawler.py", options, function (err, data) {
                let json = JSON.parse(data);
                for(let articleJson of json) {
                    let article = new ArticleSchema({
                        ordr: articleJson.ordr,
                        date: articleJson.date,
                        content: articleJson.content,
                        location: articleJson.location,
                        keyword: articleJson.keyword
                    })

                    article.save((err) => {
                        console.log(err);
                    })
                }
            });
        })
});