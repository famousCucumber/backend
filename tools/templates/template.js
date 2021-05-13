const nunjucks = require('nunjucks');

class Template {
    content;

    constructor(content) {
        this.content = content;
    }

    render(entries) {
        nunjucks.configure('views', { autoescape: true });
        return nunjucks.renderString(this.content, entries);
    }
}


module.exports = Template;
