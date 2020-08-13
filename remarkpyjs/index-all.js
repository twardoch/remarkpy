/*
const unified = require('unified')
const markdown = require('remark-parse')
const remark2rehype = require('remark-rehype')
const html = require('rehype-stringify')

const processor = unified()
    .use(markdown, { commonmark: true })
    .use(remark2rehype)
    .use(html)

function parseHtml(html) {
    console.log(this);
    const hast = processor.parse(html);
    if (hast.type === 'root' && hast.children.length > 0) {
        return hast.children[0];
    }
    return hast;
}

*/
const mdast = require('md-mdast');

function parseMd(md) {
    const mdParser = mdast();
    const mdast = mdParser.tokenizeBlock(md);
    return mdast;
}

//console.log(parseHtml('<h1>Html Heading</h1>'));


//exports.parseMd = parseMd;
//exports.parseHtml = parseHtml;
//module.exports.hello = hello;