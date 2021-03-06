var cron = require('node-cron');
const { PythonShell } = require('python-shell');
var path = require('path');
const ArticleSchema = require('../../model/articleSchema');
var { sendMail } = require("../../tools/sendEmail");
var getUserEmailByKeywords = require("../user/getUser");
const templates = require('../../tools/templates');


cron.schedule('*/1 * * * *', function () {
    try {
        ArticleSchema.findOne()
            .sort('-ordr')
            .exec((err, article) => {
                if (!article) {
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
                    let json = JSON.parse(data[0].toString('utf-8'));    //let json = JSON.parse(data);
                    for (let articleJson of json) {
                        // Send mail
                        getUserEmailByKeywords(articleJson.location, articleJson.keyword).then(emailList => {
                            let keywords = '#' + articleJson.keyword.join(' #');
                            for (let email of emailList) {
                                let html = templates.notification.render({
                                    keywords: keywords,
                                    content: articleJson.content,
                                    deleteURL: "https://famouscucumber-ojebi.run.goorm.io/user/delete?email=" + email
                                });
                                sendMail(email, `[난보바] ${articleJson.keyword[0]} 재난 문자`, html);
                            }
                        }).catch((err) => {
                            console.log(err)
                        });

                        // Save
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
    }
    catch (err) {
        console.log("Scheduler Error: " + err)
        return;
    }
});

module.exports = this;
