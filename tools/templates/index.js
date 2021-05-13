const fs = require('fs');
const path = require('path');
const Template = require('./template');

presolve = (x) => path.resolve(__dirname, x);

module.exports = {
    welcome: new Template(fs.readFileSync(presolve('000-welcome.html'), 'utf8')),
    notification: new Template(fs.readFileSync(presolve('001-notification.html'), 'utf8')),
};

/* HOW TO RENDER TEMPLATE
const templates = require('./tools/templates');

const html = templates.notification.render({
    keywords: "#서울 #강북구 #지진"
});
*/
