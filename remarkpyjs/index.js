var unified = require('unified')
var markdown = require('remark-parse')
var remark2rehype = require('remark-rehype')
var html = require('rehype-stringify')

const { create } = require('md-mdast');

const parser = create();

var processor = unified()
    .use(markdown, { commonmark: true })
    .use(remark2rehype)
    .use(html)


function parseHTML(html) {
    const hast = processor.parse(html);
    if (hast.type === 'root' && hast.children.length > 0) {
        return hast.children[0];
    }
    return hast;
}

function parseMD(md) {
    const mdast = parser.tokenizeBlock(md);
    return mdast;
}

module.exports = [parseHTML, parseMD];

module.exports = {
    optimization: {
        minimize: false
    },
    parseMD: parseMD,
    parseHTML: parseHTML
}