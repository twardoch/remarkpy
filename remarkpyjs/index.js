const { create } = require('md-mdast');

export function parseMd(md) {
    const mdParser = create();
    const mdast = mdParser.tokenizeBlock(md);
    return mdast;
}
//exports.hello = hello;