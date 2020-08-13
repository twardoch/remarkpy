(function(f){if(typeof exports==="object"&&typeof module!=="undefined"){module.exports=f()}else if(typeof define==="function"&&define.amd){define([],f)}else{var g;if(typeof window!=="undefined"){g=window}else if(typeof global!=="undefined"){g=global}else if(typeof self!=="undefined"){g=self}else{g=this}g.util = f()}})(function(){var define,module,exports;return (function(){function r(e,n,t){function o(i,f){if(!n[i]){if(!e[i]){var c="function"==typeof require&&require;if(!f&&c)return c(i,!0);if(u)return u(i,!0);var a=new Error("Cannot find module '"+i+"'");throw a.code="MODULE_NOT_FOUND",a}var p=n[i]={exports:{}};e[i][0].call(p.exports,function(r){var n=e[i][1][r];return o(n||r)},p,p.exports,r,e,n,t)}return n[i].exports}for(var u="function"==typeof require&&require,i=0;i<t.length;i++)o(t[i]);return o}return r})()({1:[function(require,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.parseMd = parseMd;

var _require = require('md-mdast'),
    create = _require.create;

function parseMd(md) {
  var mdParser = create();
  var mdast = mdParser.tokenizeBlock(md);
  return mdast;
} //exports.hello = hello;

},{"md-mdast":4}],2:[function(require,module,exports){
(function (process){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var isTest = process.env.NODE_ENV === 'test';
// tslint:disable no-any
exports.token = function (value, type, children, overrides) {
    var tok = {
        type: type,
        len: value.length,
    };
    if (isTest) {
        tok.raw = value;
    }
    if (children) {
        tok.children = children;
    }
    if (overrides) {
        Object.assign(tok, overrides);
    }
    return tok;
};
var eat = function (subvalue, type, children, overrides) {
    var tok = exports.token(subvalue, type, children, overrides);
    return tok;
};
exports.loop = function (parser, tokenizer, value) {
    var children = [];
    var end = value.length;
    var remaining = value;
    var length = 0;
    while (length < end) {
        var tok = tokenizer.call(parser, eat, remaining);
        if (tok) {
            children.push(tok);
            length += tok.len || 0;
            remaining = remaining.substr(tok.len);
        }
        else {
            if (!children.length) {
                return;
            }
        }
    }
    return children;
};
exports.first = function (tokenizers) {
    // tslint:disable no-shadowed-variable
    return function (eat, value) {
        for (var _i = 0, tokenizers_1 = tokenizers; _i < tokenizers_1.length; _i++) {
            var tokenizer = tokenizers_1[_i];
            var tok = tokenizer.call(this, eat, value);
            if (tok) {
                return tok;
            }
        }
    };
};
var smartypants = function (text) {
    return text
        .replace(/\.{3}/g, '\u2026')
        .replace(/\(C\)/gi, '©')
        .replace(/\(R\)/gi, '®')
        .replace(/\(TM\)/gi, '™')
        .replace(/\(P\)/g, '§')
        .replace(/\+\-/g, '±')
        .replace(/---/g, '\u2014')
        .replace(/--/g, '\u2013')
        .replace(/(^|[-\u2014/(\[{"\s])'/g, '$1\u2018') // opening singles
        .replace(/'/g, '\u2019') // closing singles & apostrophes
        .replace(/(^|[-\u2014/(\[{\u2018\s])"/g, '$1\u201c') // opening doubles
        .replace(/"/g, '\u201d');
}; // closing doubles
var createParser = function (_a) {
    var inline = _a.inline, block = _a.block;
    var parser = {};
    parser.tokenizeInline = function (value) {
        var tokens = exports.loop(parser, exports.first(inline), value);
        if (!tokens) {
            return;
        }
        // MERGE ADJACENT TEXT TOKENS.
        var merged = [];
        var lastTextToken = null;
        // tslint:disable prefer-for-of
        for (var i = 0; i < tokens.length; i++) {
            var tok = tokens[i];
            if (tok.type === 'text') {
                tok.value = smartypants(tok.value);
                if (lastTextToken) {
                    lastTextToken.value += tok.value;
                    lastTextToken.len += tok.len;
                }
                else {
                    merged.push(tok);
                    lastTextToken = tok;
                }
            }
            else {
                merged.push(tok);
                lastTextToken = null;
            }
        }
        return merged;
    };
    parser.tokenizeBlock = function (value) {
        var tokens = exports.loop(parser, exports.first(block), value);
        if (!tokens) {
            return;
        }
        var children = [];
        for (var _i = 0, tokens_1 = tokens; _i < tokens_1.length; _i++) {
            var tok = tokens_1[_i];
            if (tok.type !== 'newline') {
                children.push(tok);
            }
        }
        return {
            type: 'root',
            children: children,
            len: value.length,
        };
    };
    parser.tokenizeChildBlock = function (value) {
        var children = parser.tokenizeBlock(value);
        if (!children) {
            return children;
        }
        if (children.type === 'root') {
            children = children.children;
        }
        if (!children) {
            return children;
        }
        return children;
    };
    return parser;
};
exports.default = createParser;

}).call(this,require('_process'))
},{"_process":39}],3:[function(require,module,exports){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var createRegexTokenizer = function (type, reg, childrenMatchIndex) {
    var tokenizer = function (eat, value) {
        var matches = value.match(reg);
        return matches ? eat(matches[0], type, this.tokenizeInline(matches[childrenMatchIndex])) : void 0;
    };
    return tokenizer;
};
exports.default = createRegexTokenizer;

},{}],4:[function(require,module,exports){
"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
var createParser_1 = __importDefault(require("./createParser"));
var defaults_1 = __importDefault(require("./presets/defaults"));
exports.create = function () { return createParser_1.default(defaults_1.default); };

},{"./createParser":2,"./presets/defaults":5}],5:[function(require,module,exports){
"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
var escape_1 = __importDefault(require("../tokenizer/escape"));
var icon_1 = __importDefault(require("../tokenizer/icon"));
var link_1 = __importDefault(require("../tokenizer/link"));
var text_1 = __importDefault(require("../tokenizer/text"));
var mark_1 = __importDefault(require("../tokenizer/mark"));
var inlineCode_1 = __importDefault(require("../tokenizer/inlineCode"));
var emphasis_1 = __importDefault(require("../tokenizer/emphasis"));
var strong_1 = __importDefault(require("../tokenizer/strong"));
var delete_1 = __importDefault(require("../tokenizer/delete"));
var spoiler_1 = __importDefault(require("../tokenizer/spoiler"));
var inlineMath_1 = __importDefault(require("../tokenizer/inlineMath"));
var footnoteReference_1 = __importDefault(require("../tokenizer/footnoteReference"));
var reference_1 = __importDefault(require("../tokenizer/reference"));
var inlineLink_1 = __importDefault(require("../tokenizer/inlineLink"));
var sup_1 = __importDefault(require("../tokenizer/sup"));
var sub_1 = __importDefault(require("../tokenizer/sub"));
var handle_1 = __importDefault(require("../tokenizer/handle"));
var underline_1 = __importDefault(require("../tokenizer/underline"));
var break_1 = __importDefault(require("../tokenizer/break"));
var code_1 = __importDefault(require("../tokenizer/code"));
var newline_1 = __importDefault(require("../tokenizer/newline"));
var fences_1 = __importDefault(require("../tokenizer/fences"));
var math_1 = __importDefault(require("../tokenizer/math"));
var thematicBreak_1 = __importDefault(require("../tokenizer/thematicBreak"));
var heading_1 = __importDefault(require("../tokenizer/heading"));
var blockquote_1 = __importDefault(require("../tokenizer/blockquote"));
var paragraph_1 = __importDefault(require("../tokenizer/paragraph"));
var definition_1 = __importDefault(require("../tokenizer/definition"));
var footnoteDefinition_1 = __importDefault(require("../tokenizer/footnoteDefinition"));
var list_1 = __importDefault(require("../tokenizer/list"));
var table_1 = __importDefault(require("../tokenizer/table"));
var html_1 = __importDefault(require("../tokenizer/html"));
var preset = {
    block: [
        newline_1.default,
        code_1.default,
        fences_1.default,
        math_1.default,
        thematicBreak_1.default,
        heading_1.default,
        blockquote_1.default,
        list_1.default,
        html_1.default,
        table_1.default,
        footnoteDefinition_1.default,
        definition_1.default,
        paragraph_1.default,
    ],
    inline: [
        escape_1.default,
        inlineCode_1.default(),
        strong_1.default,
        emphasis_1.default,
        spoiler_1.default,
        delete_1.default(),
        inlineMath_1.default(),
        footnoteReference_1.default,
        link_1.default(),
        reference_1.default,
        inlineLink_1.default,
        sup_1.default,
        sub_1.default,
        mark_1.default,
        handle_1.default,
        underline_1.default,
        break_1.default,
        icon_1.default(32),
        text_1.default(),
    ],
};
exports.default = preset;

},{"../tokenizer/blockquote":7,"../tokenizer/break":8,"../tokenizer/code":9,"../tokenizer/definition":10,"../tokenizer/delete":11,"../tokenizer/emphasis":12,"../tokenizer/escape":13,"../tokenizer/fences":14,"../tokenizer/footnoteDefinition":15,"../tokenizer/footnoteReference":16,"../tokenizer/handle":17,"../tokenizer/heading":18,"../tokenizer/html":19,"../tokenizer/icon":20,"../tokenizer/inlineCode":21,"../tokenizer/inlineLink":22,"../tokenizer/inlineMath":23,"../tokenizer/link":24,"../tokenizer/list":25,"../tokenizer/mark":26,"../tokenizer/math":27,"../tokenizer/newline":28,"../tokenizer/paragraph":29,"../tokenizer/reference":30,"../tokenizer/spoiler":31,"../tokenizer/strong":32,"../tokenizer/sub":33,"../tokenizer/sup":34,"../tokenizer/table":35,"../tokenizer/text":36,"../tokenizer/thematicBreak":37,"../tokenizer/underline":38}],6:[function(require,module,exports){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.replace = function (reg, map) {
    var source = reg.source;
    // tslint:disable forin
    for (var key in map) {
        source = source.replace(new RegExp(key, 'g'), map[key].source);
    }
    return new RegExp(source, reg.flags);
};
exports.label = /(?:\[[^\[\]]*\]|\\[\[\]]?|`[^`]*`|[^\[\]\\])*?/;
exports.url = /\s*(<(?:\\[<>]?|[^\s<>\\])*>|(?:\\[()]?|\([^\s\x00-\x1f()\\]*\)|[^\s\x00-\x1f()\\])*?)/;
exports.title = /"(?:\\"?|[^"\\])*"|'(?:\\'?|[^'\\])*'|\((?:\\\)?|[^)\\])*\)/;
exports.urlInline = /(https?:\/\/)(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}(\.[a-z]{2,4})?\b([-a-zA-Z0-9@:%_\+.~#?&\/\/=,\*]*)/;
exports.heading = /^ *(#{1,6}) *([^\n]+?) *(?:#+ *)?(?:\n+|$)/;
exports.lheading = /^([^\n]+)\n *(=|-){2,} *(?:\n+|$)/;
exports.blockquote = /^( *>[^\n]+(\n(?!^ *\[([^\]]+)\]: *<?([^\s>]+)>?(?: +["(]([^\n]+)[")])? *(?:\n+|$))[^\n]+)*)+/;
exports.hr = /^ {0,3}((?:- *){3,}|(?:_ *){3,}|(?:\* *){3,})(?:\n+|$)/;
exports.bull = /(?:[*+-]|\d+\.)/;
exports.def = exports.replace(/^ {0,3}\[(label)\]: *\n? *<?([^\s>]+)>?(?:(?: +\n? *| *\n *)(title))? *(?:\n+|$)/, {
    label: exports.label,
    title: exports.title,
});
exports.list = exports.replace(/^( *)(bull) [\s\S]+?(?:hr|def|\n{2,}(?! )(?!\1bull )\n*|\s*$)/, { bull: exports.bull, hr: exports.hr, def: exports.def });
exports.item = exports.replace(/^( *)(bull) [^\n]*(?:\n(?!\1bull )[^\n]*)*/gm, { bull: exports.bull });
exports.paragraph = exports.replace(/^((?:[^\n]+(\n(?!\s{0,3}bull))?)+)\n*/, { bull: exports.bull });
exports.comment = /<!--(?!-?>)[\s\S]*?-->/;
exports.tag = new RegExp('address|article|aside|base|basefont|blockquote|body|caption' +
    '|center|col|colgroup|dd|details|dialog|dir|div|dl|dt|fieldset|figcaption' +
    '|figure|footer|form|frame|frameset|h[1-6]|head|header|hr|html|iframe' +
    '|legend|li|link|main|menu|menuitem|meta|nav|noframes|ol|optgroup|option' +
    '|p|param|section|source|summary|table|tbody|td|tfoot|th|thead|title|tr' +
    '|track|ul');
exports.html = exports.replace(new RegExp('^ {0,3}(?:' + // optional indentation
    '<(script|pre|style)[\\s>][\\s\\S]*?(?:</\\1>[^\\n]*\\n+|$)' + // (1)
    '|comment[^\\n]*(\\n+|$)' + // (2)
    '|<\\?[\\s\\S]*?\\?>\\n*' + // (3)
    '|<![A-Z][\\s\\S]*?>\\n*' + // (4)
    '|<!\\[CDATA\\[[\\s\\S]*?\\]\\]>\\n*' + // (5)
    '|</?(tag)(?: +|\\n|/?>)[\\s\\S]*?(?:\\n{2,}|$)' + // (6)
    '|<(?!script|pre|style)([a-z][\\w-]*)(?:attribute)*? */?>(?=\\h*\\n)[\\s\\S]*?(?:\\n{2,}|$)' + // (7) open tag
    '|</(?!script|pre|style)[a-z][\\w-]*\\s*>(?=\\h*\\n)[\\s\\S]*?(?:\\n{2,}|$)' + // (7) closing tag
    ')'), {
    comment: exports.comment,
    tag: exports.tag,
    attribute: / +[a-zA-Z:_][\w.:-]*(?: *= *"[^"\n]*"| *= *'[^'\n]*'| *= *[^\s"'=<>`]+)?/,
});

},{}],7:[function(require,module,exports){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var regex_1 = require("../regex");
// tslint:disable only-arrow-functions, no-invalid-this
var blockquote = function (eat, value) {
    var matches = value.match(regex_1.blockquote);
    if (!matches) {
        return;
    }
    var subvalue = matches[0];
    var innerValue = subvalue.replace(/^ *> ?/gm, '');
    var children = this.tokenizeChildBlock(innerValue);
    return eat(subvalue, 'blockquote', children);
};
exports.default = blockquote;

},{"../regex":6}],8:[function(require,module,exports){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var REG1 = /^\s{2,}\n(?!\s*$)/;
var REG2 = /^ *\\n/;
var inlineBreak = function (eat, value) {
    var matches = value.match(REG1) || value.match(REG2);
    return matches ? eat(matches[0], 'break') : void 0;
};
exports.default = inlineBreak;

},{}],9:[function(require,module,exports){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var REG = /^(\s{4}[^\n]+\n*)+/;
// tslint:disable only-arrow-functions
var code = function (eat, value) {
    var matches = value.match(REG);
    if (!matches) {
        return;
    }
    var subvalue = matches[0];
    var overrides = {
        value: subvalue.replace(/^ {4}/gm, '').replace(/\n+$/, ''),
        lang: null,
    };
    return eat(subvalue, 'code', void 0, overrides);
};
exports.default = code;

},{}],10:[function(require,module,exports){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var regex_1 = require("../regex");
// tslint:disable only-arrow-functions
var definition = function (eat, value) {
    var matches = value.match(regex_1.def);
    if (!matches) {
        return void 0;
    }
    var subvalue = matches[0];
    return eat(subvalue, 'definition', void 0, {
        identifier: matches[1],
        title: matches[3] || null,
        url: matches[2],
    });
};
exports.default = definition;

},{"../regex":6}],11:[function(require,module,exports){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var REG = /^~~(?=\S)([\s\S]*?\S)~~/;
var deletedText = function () {
    // tslint:disable only-arrow-functions, no-invalid-this
    var tokenizer = function (eat, value) {
        var matches = value.match(REG);
        if (matches) {
            return eat(matches[0], 'delete', this.tokenizeInline(matches[1]));
        }
        return;
    };
    return tokenizer;
};
exports.default = deletedText;

},{}],12:[function(require,module,exports){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var REG = /^_([^\s][\s\S]*?[^\s_])_(?!_)|^_([^\s_][\s\S]*?[^\s])_(?!_)|^\*([^\s][\s\S]*?[^\s*])\*(?!\*)|^\*([^\s*][\s\S]*?[^\s])\*(?!\*)|^_([^\s_])_(?!_)|^\*([^\s*])\*(?!\*)/;
// tslint:disable only-arrow-functions, no-invalid-this
var emphasis = function (eat, value) {
    var matches = value.match(REG);
    if (matches) {
        var subvalue = matches[6] || matches[5] || matches[4] || matches[3] || matches[2] || matches[1];
        return eat(matches[0], 'emphasis', this.tokenizeInline(subvalue));
    }
    return;
};
exports.default = emphasis;

},{}],13:[function(require,module,exports){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var REG = /^\\([!"#$%&'()*+,\-./:;<=>?@\[\]\\^_`{|}~])/;
var escape = function (eat, value) {
    var matches = value.match(REG);
    return matches ? eat(matches[0], 'text', void 0, { value: matches[1] }) : void 0;
};
exports.default = escape;

},{}],14:[function(require,module,exports){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var REG = /^ *(`{3,}|~{3,})([^\s]*) *([^\n]*)\n([\s\S]*?)\s*\1 *(?:\n+|$)/;
// tslint:disable only-arrow-functions
var fences = function (eat, value) {
    var matches = value.match(REG);
    if (!matches) {
        return;
    }
    var subvalue = matches[0];
    var overrides = {
        value: matches[4] || matches[3],
        lang: matches[2] || '',
        meta: matches.length > 4 ? matches[3] : null,
    };
    return eat(subvalue, 'code', void 0, overrides);
};
exports.default = fences;

},{}],15:[function(require,module,exports){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var REG = /^\[\^([a-zA-Z0-9\-_]+)\]: *([^\n]*(\n?((  ([^\n]*)\n?)|\n(?!\n))*)?)/;
// tslint:disable only-arrow-functions, no-invalid-this
var footnoteDefinition = function (eat, value) {
    var matches = value.match(REG);
    if (!matches) {
        return void 0;
    }
    var subvalue = matches[0];
    var identifier = matches[1];
    var outdented = matches[2].replace(/^ {1,4}/gm, '');
    var children = this.tokenizeChildBlock(outdented);
    return eat(subvalue, 'footnoteDefinition', children, { identifier: identifier });
};
exports.default = footnoteDefinition;

},{}],16:[function(require,module,exports){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var REG = /^\[\^([a-zA-Z0-9\-_]{1,64})\]/;
var footnoteReference = function (eat, value) {
    var matches = value.match(REG);
    if (matches) {
        return eat(matches[0], 'footnoteReference', void 0, { value: matches[1] });
    }
    return;
};
exports.default = footnoteReference;

},{}],17:[function(require,module,exports){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var REG = /^([#~@])(([\w\-_\.\/#]{1,64})|(\{([\w\-_\.\/#=\/ ]{1,64})\}))/;
var handle = function (eat, value) {
    var matches = value.match(REG);
    if (matches) {
        var subvalue = matches[5] || matches[2];
        return eat(matches[0], 'handle', void 0, {
            value: subvalue,
            prefix: matches[1],
        });
    }
    return;
};
exports.default = handle;

},{}],18:[function(require,module,exports){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var regex_1 = require("../regex");
// tslint:disable only-arrow-functions, no-invalid-this
var heading = function (eat, value) {
    var matches = value.match(regex_1.heading);
    if (matches) {
        var subvalue = matches[2];
        return eat(matches[0], 'heading', this.tokenizeInline(subvalue), {
            depth: matches[1].length,
        });
    }
    matches = value.match(regex_1.lheading);
    if (matches) {
        var subvalue = matches[1];
        return eat(matches[0], 'heading', this.tokenizeInline(subvalue), {
            depth: matches[2] === '-' ? 1 : 2,
        });
    }
    return;
};
exports.default = heading;

},{"../regex":6}],19:[function(require,module,exports){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var regex_1 = require("../regex");
// tslint:disable-next-line only-arrow-functions
var html = function (eat, value) {
    var matches = value.match(regex_1.html);
    return matches ? eat(matches[0], 'html', void 0, { value: matches[0] }) : void 0;
};
exports.default = html;

},{"../regex":6}],20:[function(require,module,exports){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var icon = function (maxLength) {
    if (maxLength === void 0) { maxLength = 32; }
    var REG1 = new RegExp("^::([^'\\s:]{1," + maxLength + "}?)::");
    var REG2 = new RegExp("^:([^'\\s:]{1," + maxLength + "}?):");
    return function (eat, value) {
        var matches = value.match(REG1) || value.match(REG2);
        return matches ? eat(matches[0], 'icon', void 0, { emoji: matches[1] }) : void 0;
    };
};
exports.default = icon;

},{}],21:[function(require,module,exports){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var REG = /^(`+)\s*([\s\S]*?[^`])\s*\1(?!`)/;
var inlineCode = function () {
    // tslint:disable only-arrow-functions
    var tokenizer = function (eat, value) {
        var matches = value.match(REG);
        if (matches) {
            return eat(matches[0], 'inlineCode', void 0, {
                value: matches[2],
                wrap: matches[1],
            });
        }
        return;
    };
    return tokenizer;
};
exports.default = inlineCode;

},{}],22:[function(require,module,exports){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var regex_1 = require("../regex");
var REG = new RegExp('^' + regex_1.urlInline.source);
var inlineLink = function (eat, value) {
    var matches = value.match(REG);
    if (matches) {
        var subvalue = matches[0];
        return eat(subvalue, 'inlineLink', void 0, {
            value: subvalue,
        });
    }
    return;
};
exports.default = inlineLink;

},{"../regex":6}],23:[function(require,module,exports){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var REG = /^\${1,2}(?=\S)([\s\S]*?\S)\${1,2}/;
var inlineMath = function () {
    var tokenizer = function (eat, value) {
        var matches = value.match(REG);
        if (matches) {
            return eat(matches[0], 'inlineMath', void 0, { value: matches[1] });
        }
        return;
    };
    return tokenizer;
};
exports.default = inlineMath;

},{}],24:[function(require,module,exports){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var regex_1 = require("../regex");
var REG = regex_1.replace(/^!?\[(label)\]\(url(?:\s+(title))?\s*\)/, {
    label: regex_1.label,
    url: regex_1.url,
    title: regex_1.title,
});
var link = function () {
    return function (eat, value) {
        var matches = value.match(REG);
        if (matches) {
            var isImage = matches[0][0] === '!';
            var linkTitle = matches[3];
            if (linkTitle) {
                linkTitle = linkTitle.substr(1, linkTitle.length - 2);
            }
            if (isImage) {
                return eat(matches[0], 'image', void 0, {
                    url: matches[2],
                    alt: matches[1],
                    title: linkTitle,
                });
            }
            else {
                return eat(matches[0], 'link', this.tokenizeInline(matches[1]), {
                    url: matches[2],
                    title: linkTitle,
                });
            }
        }
        return;
    };
};
exports.default = link;

},{"../regex":6}],25:[function(require,module,exports){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var regex_1 = require("../regex");
var REG_BULLET = /^(\s*)([*+-]|\d\.)(\s{1,2}|\t)/;
var REG_LOOSE = /\n\n(?!\s*$)/;
var getParts = function (subvalue) {
    var parts = subvalue.match(regex_1.item);
    return parts;
};
// tslint:disable-next-line only-arrow-functions
var list = function (eat, value) {
    var matches = value.match(regex_1.list);
    if (!matches) {
        return;
    }
    var subvalue = matches[0];
    var parts = getParts(subvalue);
    // const [, ...parts] = subvalue.split(/^(?: *)(?:\-) [^\n]*(?:\n(?!\1\- )[^\n]*)*/gm);
    // const bullets = subvalue.match(REG_SPLIT);
    if (!parts) {
        return;
    }
    var length = parts.length;
    var children = [];
    var ordered = false;
    var start = null;
    var loose = false;
    for (var i = 0; i < length; i++) {
        var part = parts[i];
        var bulletMatch = part.match(REG_BULLET);
        // This should never happen.
        if (!bulletMatch) {
            return;
        }
        var sansBullet = part.substr(bulletMatch[0].length);
        // const indent = bulletMatch[1].length;
        var bulletMarker = bulletMatch[2];
        // const space = indent + bulletMarker.length;
        if (i === 0) {
            if (bulletMarker.length > 1) {
                ordered = true;
                start = parseInt(bulletMarker, 10);
            }
        }
        // Outdent
        var outdented = sansBullet.replace(/^ {1,4}/gm, '');
        // const outdented = part.replace(new RegExp('^ {1,' + space + '}', 'gm'), '')
        var checked = null;
        if (outdented[0] === '[' && outdented[2] === ']') {
            switch (outdented[1]) {
                case 'x':
                case 'X':
                    outdented = outdented.substr(3);
                    checked = true;
                    break;
                case ' ':
                    outdented = outdented.substr(3);
                    checked = false;
                    break;
            }
        }
        var partLoose = REG_LOOSE.test(sansBullet);
        if (partLoose) {
            loose = true;
        }
        children.push({
            type: 'listItem',
            loose: partLoose,
            checked: checked,
            // tslint:disable-next-line no-invalid-this
            children: this.tokenizeChildBlock(outdented),
        });
    }
    return eat(subvalue, 'list', children, {
        ordered: ordered,
        start: start,
        loose: loose,
    });
};
exports.default = list;

},{"../regex":6}],26:[function(require,module,exports){
"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
var createRegexTokenizer_1 = __importDefault(require("../createRegexTokenizer"));
var REG = /^==(?=\S)([\s\S]*?\S)==/;
var mark = createRegexTokenizer_1.default('mark', REG, 1);
exports.default = mark;

},{"../createRegexTokenizer":3}],27:[function(require,module,exports){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var REG = /^ *\$\$[ \.]*(\S+)? *\n([\s\S]*?)\s*\$\$ *(?:\n+|$)/;
// tslint:disable only-arrow-functions
var math = function (eat, value) {
    var matches = value.match(REG);
    return matches ? eat(matches[0], 'math', void 0, { value: matches[2] }) : void 0;
};
exports.default = math;

},{}],28:[function(require,module,exports){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var REG = /^\n+/;
// tslint:disable only-arrow-functions
var newline = function (eat, value) {
    var matches = value.match(REG);
    if (!matches) {
        return;
    }
    return matches ? eat(matches[0], 'newline') : void 0;
};
exports.default = newline;

},{}],29:[function(require,module,exports){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var regex_1 = require("../regex");
// tslint:disable only-arrow-functions, no-invalid-this
var paragraph = function (eat, value) {
    var matches = value.match(regex_1.paragraph);
    return matches ? eat(matches[0], 'paragraph', this.tokenizeInline(matches[1].trim())) : void 0;
};
exports.default = paragraph;

},{"../regex":6}],30:[function(require,module,exports){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var regex_1 = require("../regex");
var REG = regex_1.replace(/^!?\[(label)\]\s*(\[([^\]]*)\])?/, { label: regex_1.label });
var reference = function (eat, value) {
    var matches = value.match(REG);
    if (matches) {
        var subvalue = matches[0];
        var isImage = subvalue[0] === '!';
        var type = isImage ? 'imageReference' : 'linkReference';
        var identifier = matches[3];
        var referenceType = 'full';
        var children = void 0;
        if (!identifier) {
            identifier = matches[1];
            referenceType = matches[2] ? 'collapsed' : 'shortcut';
        }
        var overrides = {
            identifier: identifier,
            referenceType: referenceType,
        };
        if (isImage) {
            overrides.alt = matches[1] || null;
        }
        else {
            children = this.tokenizeInline(matches[1]);
        }
        return eat(subvalue, type, children, overrides);
    }
    return;
};
exports.default = reference;

},{"../regex":6}],31:[function(require,module,exports){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var REG = /^~~~([\s\S]*)~~~/;
// tslint:disable only-arrow-functions, no-invalid-this
var spoiler = function (eat, value) {
    var matches = value.match(REG);
    return matches ? eat(matches[0], 'spoiler', this.tokenizeInline(matches[1])) : void 0;
};
exports.default = spoiler;

},{}],32:[function(require,module,exports){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var REG = /^__([^\s][\s\S]*?[^\s])__(?!_)|^\*\*([^\s][\s\S]*?[^\s])\*\*(?!\*)|^__([^\s])__(?!_)|^\*\*([^\s])\*\*(?!\*)/;
// tslint:disable only-arrow-functions, no-invalid-this
var strong = function (eat, value) {
    var matches = value.match(REG);
    if (matches) {
        var subvalue = matches[4] || matches[3] || matches[2] || matches[1];
        return eat(matches[0], 'strong', this.tokenizeInline(subvalue));
    }
    return;
};
exports.default = strong;

},{}],33:[function(require,module,exports){
"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
var createRegexTokenizer_1 = __importDefault(require("../createRegexTokenizer"));
var REG = /^~(?=\S)([\s\S]*?\S)~/;
var sub = createRegexTokenizer_1.default('sub', REG, 1);
exports.default = sub;

},{"../createRegexTokenizer":3}],34:[function(require,module,exports){
"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
var createRegexTokenizer_1 = __importDefault(require("../createRegexTokenizer"));
var REG = /^\^(?=\S)([\s\S]*?\S)\^/;
var sup = createRegexTokenizer_1.default('sup', REG, 1);
exports.default = sup;

},{"../createRegexTokenizer":3}],35:[function(require,module,exports){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var REG = /^ *\|(.+)\n *\|?( *[-:]+[-| :]*)(?:\n((?: *[^>\n ].*(?:\n|$))*)\n*|$)/;
var splitCells = function (tableRow, count) {
    var cells = tableRow.replace(/([^\\])\|/g, '$1 |').split(/ +\| */);
    if (count !== void 0) {
        if (cells.length > count) {
            cells.splice(count);
        }
        else {
            while (cells.length < count) {
                cells.push('');
            }
        }
    }
    for (var i = 0; i < cells.length; i++) {
        cells[i] = cells[i].replace(/\\\|/g, '|');
    }
    return cells;
};
// tslint:disable only-arrow-functions, no-invalid-this
var table = function (eat, value) {
    var _this = this;
    var matches = value.match(REG);
    if (!matches) {
        return;
    }
    var subvalue = matches[0];
    var header = matches[1];
    var align = matches[2]
        .replace(/^ *|\| *$/g, '')
        .split(/ *\| */)
        .map(function (spec) {
        // tslint:disable-next-line no-parameter-reassignment
        spec = spec.trim();
        return spec[0] === ':'
            ? spec[spec.length - 1] === ':'
                ? 'center'
                : 'left'
            : spec[spec.length - 1] === ':'
                ? 'right'
                : null;
    });
    var rows = matches[3] ? matches[3].replace(/(?: *\| *)?\n$/, '').split('\n') : [];
    var children = [];
    var headers = splitCells(header.replace(/^ *| *\| *$/g, '')).map(function (headerText) { return ({
        type: 'tableCell',
        children: _this.tokenizeInline(headerText),
    }); });
    children.push({
        type: 'tableRow',
        children: headers,
    });
    if (rows && rows.length) {
        // tslint:disable-next-line prefer-for-of
        for (var i = 0; i < rows.length; i++) {
            var row = rows[i];
            var cells = splitCells(row.replace(/^ *\| *| *\| *$/g, ''), headers.length);
            children.push({
                type: 'tableRow',
                children: cells.map(function (cellRawValue) { return ({
                    type: 'tableCell',
                    children: _this.tokenizeInline(cellRawValue),
                }); }),
            });
        }
    }
    return eat(subvalue, 'table', children, { align: align });
};
exports.default = table;

},{}],36:[function(require,module,exports){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var regex_1 = require("../regex");
var REG = new RegExp('^[\\s\\S]+?(?=[\\<!\\[_*`:~\\|#@\\$\\^=\\+]| {2,}\\n|(' + regex_1.urlInline.source + ')|\\\\n|\\\\`|$)');
var text = function () {
    // tslint:disable only-arrow-functions
    var tokenizer = function (eat, value) {
        var matches = value.match(REG);
        if (matches) {
            var matchedValue = matches[0];
            return eat(matchedValue, 'text', void 0, { value: matchedValue });
        }
        return;
    };
    return tokenizer;
};
exports.default = text;

},{"../regex":6}],37:[function(require,module,exports){
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var regex_1 = require("../regex");
// const REG = /^ *([-*_]{3,})\s*(?:\n+|$)/;
// tslint:disable only-arrow-functions
var thematicBreak = function (eat, value) {
    var matches = value.match(regex_1.hr);
    return matches ? eat(matches[0], 'thematicBreak', void 0, { value: matches[1] }) : void 0;
};
exports.default = thematicBreak;

},{"../regex":6}],38:[function(require,module,exports){
"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
var createRegexTokenizer_1 = __importDefault(require("../createRegexTokenizer"));
var REG = /^\+\+(?=\S)([\s\S]*?\S)\+\+/;
var underline = createRegexTokenizer_1.default('underline', REG, 1);
exports.default = underline;

},{"../createRegexTokenizer":3}],39:[function(require,module,exports){
// shim for using process in browser
var process = module.exports = {};

// cached from whatever global is present so that test runners that stub it
// don't break things.  But we need to wrap it in a try catch in case it is
// wrapped in strict mode code which doesn't define any globals.  It's inside a
// function because try/catches deoptimize in certain engines.

var cachedSetTimeout;
var cachedClearTimeout;

function defaultSetTimout() {
    throw new Error('setTimeout has not been defined');
}
function defaultClearTimeout () {
    throw new Error('clearTimeout has not been defined');
}
(function () {
    try {
        if (typeof setTimeout === 'function') {
            cachedSetTimeout = setTimeout;
        } else {
            cachedSetTimeout = defaultSetTimout;
        }
    } catch (e) {
        cachedSetTimeout = defaultSetTimout;
    }
    try {
        if (typeof clearTimeout === 'function') {
            cachedClearTimeout = clearTimeout;
        } else {
            cachedClearTimeout = defaultClearTimeout;
        }
    } catch (e) {
        cachedClearTimeout = defaultClearTimeout;
    }
} ())
function runTimeout(fun) {
    if (cachedSetTimeout === setTimeout) {
        //normal enviroments in sane situations
        return setTimeout(fun, 0);
    }
    // if setTimeout wasn't available but was latter defined
    if ((cachedSetTimeout === defaultSetTimout || !cachedSetTimeout) && setTimeout) {
        cachedSetTimeout = setTimeout;
        return setTimeout(fun, 0);
    }
    try {
        // when when somebody has screwed with setTimeout but no I.E. maddness
        return cachedSetTimeout(fun, 0);
    } catch(e){
        try {
            // When we are in I.E. but the script has been evaled so I.E. doesn't trust the global object when called normally
            return cachedSetTimeout.call(null, fun, 0);
        } catch(e){
            // same as above but when it's a version of I.E. that must have the global object for 'this', hopfully our context correct otherwise it will throw a global error
            return cachedSetTimeout.call(this, fun, 0);
        }
    }


}
function runClearTimeout(marker) {
    if (cachedClearTimeout === clearTimeout) {
        //normal enviroments in sane situations
        return clearTimeout(marker);
    }
    // if clearTimeout wasn't available but was latter defined
    if ((cachedClearTimeout === defaultClearTimeout || !cachedClearTimeout) && clearTimeout) {
        cachedClearTimeout = clearTimeout;
        return clearTimeout(marker);
    }
    try {
        // when when somebody has screwed with setTimeout but no I.E. maddness
        return cachedClearTimeout(marker);
    } catch (e){
        try {
            // When we are in I.E. but the script has been evaled so I.E. doesn't  trust the global object when called normally
            return cachedClearTimeout.call(null, marker);
        } catch (e){
            // same as above but when it's a version of I.E. that must have the global object for 'this', hopfully our context correct otherwise it will throw a global error.
            // Some versions of I.E. have different rules for clearTimeout vs setTimeout
            return cachedClearTimeout.call(this, marker);
        }
    }



}
var queue = [];
var draining = false;
var currentQueue;
var queueIndex = -1;

function cleanUpNextTick() {
    if (!draining || !currentQueue) {
        return;
    }
    draining = false;
    if (currentQueue.length) {
        queue = currentQueue.concat(queue);
    } else {
        queueIndex = -1;
    }
    if (queue.length) {
        drainQueue();
    }
}

function drainQueue() {
    if (draining) {
        return;
    }
    var timeout = runTimeout(cleanUpNextTick);
    draining = true;

    var len = queue.length;
    while(len) {
        currentQueue = queue;
        queue = [];
        while (++queueIndex < len) {
            if (currentQueue) {
                currentQueue[queueIndex].run();
            }
        }
        queueIndex = -1;
        len = queue.length;
    }
    currentQueue = null;
    draining = false;
    runClearTimeout(timeout);
}

process.nextTick = function (fun) {
    var args = new Array(arguments.length - 1);
    if (arguments.length > 1) {
        for (var i = 1; i < arguments.length; i++) {
            args[i - 1] = arguments[i];
        }
    }
    queue.push(new Item(fun, args));
    if (queue.length === 1 && !draining) {
        runTimeout(drainQueue);
    }
};

// v8 likes predictible objects
function Item(fun, array) {
    this.fun = fun;
    this.array = array;
}
Item.prototype.run = function () {
    this.fun.apply(null, this.array);
};
process.title = 'browser';
process.browser = true;
process.env = {};
process.argv = [];
process.version = ''; // empty string to avoid regexp issues
process.versions = {};

function noop() {}

process.on = noop;
process.addListener = noop;
process.once = noop;
process.off = noop;
process.removeListener = noop;
process.removeAllListeners = noop;
process.emit = noop;
process.prependListener = noop;
process.prependOnceListener = noop;

process.listeners = function (name) { return [] }

process.binding = function (name) {
    throw new Error('process.binding is not supported');
};

process.cwd = function () { return '/' };
process.chdir = function (dir) {
    throw new Error('process.chdir is not supported');
};
process.umask = function() { return 0; };

},{}]},{},[1])(1)
});
