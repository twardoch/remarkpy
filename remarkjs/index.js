var unified = require('unified')
var createStream = require('unified-stream')
var markdown = require('remark-parse')
var remark2rehype = require('remark-rehype')
var html = require('rehype-stringify')

var processor = unified()
    .use(markdown, { commonmark: true })
    .use(remark2rehype)
    .use(html)

process.stdin.pipe(createStream(processor)).pipe(process.stdout)