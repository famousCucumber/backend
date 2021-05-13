const fs = require('fs');
const path = require('path');

presolve = (x) => path.resolve(__dirname, x);

module.exports = {
    welcome: fs.readFileSync(presolve('000-welcome.html'), 'utf8')
};
