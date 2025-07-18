const { create } = require('md-mdast');

function parseMd(md) {
    const mdParser = create();
    const mdast = mdParser.tokenizeBlock(md);
    return mdast;
}

// Export as the main function for webpack
module.exports = parseMd;