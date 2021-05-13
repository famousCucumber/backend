var cron = require('node-cron');
const { PythonShell } = require('python-shell');
const ArticleSchema = require('../../model/articleSchema');

cron.schedule('*/1 * * * *', function () {
    ArticleSchema.findOne()
        .sort('-ordr')
        .exec((err, article) => {
            if(!article) {
                articleJson = {
                    'ordr': 105251,
                    'date': '2021/05/13 15:29:51',
                    'content': '[진주시청]12일 15시이후 확진자 3명(자가격리중2명, 타지역접촉자1명), 13일 15시기준 2명 발생(자가격리중1명, 접촉자1명), 시홈페이지 참고바랍니다.\r\n\r\n-송출지역-\r\n경상남도 진주시', 
                    'keyword': ['코로나'],
                    'location': ['경상남도 진주시']
                };

                let firstArticle = new ArticleSchema({
                    ordr: articleJson.ordr,
                    date: articleJson.date,
                    content: articleJson.content,
                    location: articleJson.location,
                    keyword: articleJson.keyword
                })
                firstArticle.save();
                return;
            }

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

module.exports = this;