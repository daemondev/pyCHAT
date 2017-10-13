/* axios v0.8.0 | (c) 2015 by Matt Zabriskie */
!function(e,t){"object"==typeof exports&&"object"==typeof module?module.exports=t():"function"==typeof define&&define.amd?define([],t):"object"==typeof exports?exports.axios=t():e.axios=t()}(this,function(){return function(e){function t(n){if(r[n])return r[n].exports;var o=r[n]={exports:{},id:n,loaded:!1};return e[n].call(o.exports,o,o.exports,t),o.loaded=!0,o.exports}var r={};return t.m=e,t.c=r,t.p="",t(0)}([function(e,t,r){e.exports=r(1)},function(e,t,r){"use strict";function n(e){this.defaultConfig=i.merge({headers:{},timeout:o.timeout,transformRequest:o.transformRequest,transformResponse:o.transformResponse},e),this.interceptors={request:new u,response:new u}}var o=r(2),i=r(3),s=r(4),u=r(12),a=r(13),c=r(14),f=r(15);n.prototype.request=function(e){"string"==typeof e&&(e=i.merge({url:arguments[0]},arguments[1])),e=i.merge(this.defaultConfig,{method:"get"},e),e.baseURL&&!a(e.url)&&(e.url=c(e.baseURL,e.url)),e.withCredentials=e.withCredentials||o.withCredentials;var t=[s,void 0],r=Promise.resolve(e);for(this.interceptors.request.forEach(function(e){t.unshift(e.fulfilled,e.rejected)}),this.interceptors.response.forEach(function(e){t.push(e.fulfilled,e.rejected)});t.length;)r=r.then(t.shift(),t.shift());return r};var p=new n,l=e.exports=f(n.prototype.request,p);l.create=function(e){return new n(e)},l.defaults=o,l.all=function(e){return Promise.all(e)},l.spread=r(16),l.interceptors=p.interceptors,i.forEach(["delete","get","head"],function(e){n.prototype[e]=function(t,r){return this.request(i.merge(r||{},{method:e,url:t}))},l[e]=f(n.prototype[e],p)}),i.forEach(["post","put","patch"],function(e){n.prototype[e]=function(t,r,n){return this.request(i.merge(n||{},{method:e,url:t,data:r}))},l[e]=f(n.prototype[e],p)})},function(e,t,r){"use strict";var n=r(3),o=/^\)\]\}',?\n/,i={"Content-Type":"application/x-www-form-urlencoded"};e.exports={transformRequest:[function(e,t){return n.isFormData(e)?e:n.isArrayBuffer(e)?e:n.isArrayBufferView(e)?e.buffer:!n.isObject(e)||n.isFile(e)||n.isBlob(e)?e:(n.isUndefined(t)||(n.forEach(t,function(e,r){"content-type"===r.toLowerCase()&&(t["Content-Type"]=e)}),n.isUndefined(t["Content-Type"])&&(t["Content-Type"]="application/json;charset=utf-8")),JSON.stringify(e))}],transformResponse:[function(e){if("string"==typeof e){e=e.replace(o,"");try{e=JSON.parse(e)}catch(t){}}return e}],headers:{common:{Accept:"application/json, text/plain, */*"},patch:n.merge(i),post:n.merge(i),put:n.merge(i)},timeout:0,xsrfCookieName:"XSRF-TOKEN",xsrfHeaderName:"X-XSRF-TOKEN"}},function(e,t){"use strict";function r(e){return"[object Array]"===g.call(e)}function n(e){return"[object ArrayBuffer]"===g.call(e)}function o(e){return"[object FormData]"===g.call(e)}function i(e){var t;return t="undefined"!=typeof ArrayBuffer&&ArrayBuffer.isView?ArrayBuffer.isView(e):e&&e.buffer&&e.buffer instanceof ArrayBuffer}function s(e){return"string"==typeof e}function u(e){return"number"==typeof e}function a(e){return"undefined"==typeof e}function c(e){return null!==e&&"object"==typeof e}function f(e){return"[object Date]"===g.call(e)}function p(e){return"[object File]"===g.call(e)}function l(e){return"[object Blob]"===g.call(e)}function d(e){return e.replace(/^\s*/,"").replace(/\s*$/,"")}function h(){return"undefined"!=typeof window&&"undefined"!=typeof document&&"function"==typeof document.createElement}function m(e,t){if(null!==e&&"undefined"!=typeof e)if("object"==typeof e||r(e)||(e=[e]),r(e))for(var n=0,o=e.length;o>n;n++)t.call(null,e[n],n,e);else for(var i in e)e.hasOwnProperty(i)&&t.call(null,e[i],i,e)}function y(){function e(e,r){t[r]=e}for(var t={},r=0,n=arguments.length;n>r;r++)m(arguments[r],e);return t}var g=Object.prototype.toString;e.exports={isArray:r,isArrayBuffer:n,isFormData:o,isArrayBufferView:i,isString:s,isNumber:u,isObject:c,isUndefined:a,isDate:f,isFile:p,isBlob:l,isStandardBrowserEnv:h,forEach:m,merge:y,trim:d}},function(e,t,r){"use strict";e.exports=function(e){return new Promise(function(t,n){try{"undefined"!=typeof XMLHttpRequest||"undefined"!=typeof ActiveXObject?r(5)(t,n,e):"undefined"!=typeof process&&r(5)(t,n,e)}catch(o){n(o)}})}},function(e,t,r){"use strict";var n=r(2),o=r(3),i=r(6),s=r(7),u=r(8),a=r(9),c=window.btoa||r(10);e.exports=function(e,t,f){var p=u(f.data,f.headers,f.transformRequest),l=o.merge(n.headers.common,n.headers[f.method]||{},f.headers||{});o.isFormData(p)&&delete l["Content-Type"];var d=XMLHttpRequest||ActiveXObject,h="onreadystatechange",m=!1;if(!a(f.url)&&window.XDomainRequest&&(d=window.XDomainRequest,h="onload",m=!0),f.auth){var y=f.auth.username||"",g=f.auth.password||"";l.Authorization="Basic "+c(y+":"+g)}var w=new d("Microsoft.XMLHTTP");if(w.open(f.method.toUpperCase(),i(f.url,f.params,f.paramsSerializer),!0),w.timeout=f.timeout,w[h]=function(){if(w&&(4===w.readyState||m)){var r=m?null:s(w.getAllResponseHeaders()),n=-1!==["text",""].indexOf(f.responseType||"")?w.responseText:w.response,o={data:u(n,r,f.transformResponse),status:w.status,statusText:w.statusText,headers:r,config:f};(w.status>=200&&w.status<300||m&&w.responseText?e:t)(o),w=null}},o.isStandardBrowserEnv()){var v=r(11),x=f.withCredentials||a(f.url)?v.read(f.xsrfCookieName||n.xsrfCookieName):void 0;x&&(l[f.xsrfHeaderName||n.xsrfHeaderName]=x)}if(m||o.forEach(l,function(e,t){p||"content-type"!==t.toLowerCase()?w.setRequestHeader(t,e):delete l[t]}),f.withCredentials&&(w.withCredentials=!0),f.responseType)try{w.responseType=f.responseType}catch(b){if("json"!==w.responseType)throw b}o.isArrayBuffer(p)&&(p=new DataView(p)),w.send(p)}},function(e,t,r){"use strict";function n(e){return encodeURIComponent(e).replace(/%40/gi,"@").replace(/%3A/gi,":").replace(/%24/g,"$").replace(/%2C/gi,",").replace(/%20/g,"+").replace(/%5B/gi,"[").replace(/%5D/gi,"]")}var o=r(3);e.exports=function(e,t,r){if(!t)return e;var i;if(r)i=r(t);else{var s=[];o.forEach(t,function(e,t){null!==e&&"undefined"!=typeof e&&(o.isArray(e)&&(t+="[]"),o.isArray(e)||(e=[e]),o.forEach(e,function(e){o.isDate(e)?e=e.toISOString():o.isObject(e)&&(e=JSON.stringify(e)),s.push(n(t)+"="+n(e))}))}),i=s.join("&")}return i&&(e+=(-1===e.indexOf("?")?"?":"&")+i),e}},function(e,t,r){"use strict";var n=r(3);e.exports=function(e){var t,r,o,i={};return e?(n.forEach(e.split("\n"),function(e){o=e.indexOf(":"),t=n.trim(e.substr(0,o)).toLowerCase(),r=n.trim(e.substr(o+1)),t&&(i[t]=i[t]?i[t]+", "+r:r)}),i):i}},function(e,t,r){"use strict";var n=r(3);e.exports=function(e,t,r){return n.forEach(r,function(r){e=r(e,t)}),e}},function(e,t,r){"use strict";var n=r(3);e.exports=n.isStandardBrowserEnv()?function(){function e(e){var t=e;return r&&(o.setAttribute("href",t),t=o.href),o.setAttribute("href",t),{href:o.href,protocol:o.protocol?o.protocol.replace(/:$/,""):"",host:o.host,search:o.search?o.search.replace(/^\?/,""):"",hash:o.hash?o.hash.replace(/^#/,""):"",hostname:o.hostname,port:o.port,pathname:"/"===o.pathname.charAt(0)?o.pathname:"/"+o.pathname}}var t,r=/(msie|trident)/i.test(navigator.userAgent),o=document.createElement("a");return t=e(window.location.href),function(r){var o=n.isString(r)?e(r):r;return o.protocol===t.protocol&&o.host===t.host}}():function(){return function(){return!0}}()},function(e,t){"use strict";function r(e){this.message=e}function n(e){for(var t,n,i=String(e),s="",u=0,a=o;i.charAt(0|u)||(a="=",u%1);s+=a.charAt(63&t>>8-u%1*8)){if(n=i.charCodeAt(u+=.75),n>255)throw new r("INVALID_CHARACTER_ERR: DOM Exception 5");t=t<<8|n}return s}var o="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";r.prototype=new Error,r.prototype.code=5,r.prototype.name="InvalidCharacterError",e.exports=n},function(e,t,r){"use strict";var n=r(3);e.exports=n.isStandardBrowserEnv()?function(){return{write:function(e,t,r,o,i,s){var u=[];u.push(e+"="+encodeURIComponent(t)),n.isNumber(r)&&u.push("expires="+new Date(r).toGMTString()),n.isString(o)&&u.push("path="+o),n.isString(i)&&u.push("domain="+i),s===!0&&u.push("secure"),document.cookie=u.join("; ")},read:function(e){var t=document.cookie.match(new RegExp("(^|;\\s*)("+e+")=([^;]*)"));return t?decodeURIComponent(t[3]):null},remove:function(e){this.write(e,"",Date.now()-864e5)}}}():function(){return{write:function(){},read:function(){return null},remove:function(){}}}()},function(e,t,r){"use strict";function n(){this.handlers=[]}var o=r(3);n.prototype.use=function(e,t){return this.handlers.push({fulfilled:e,rejected:t}),this.handlers.length-1},n.prototype.eject=function(e){this.handlers[e]&&(this.handlers[e]=null)},n.prototype.forEach=function(e){o.forEach(this.handlers,function(t){null!==t&&e(t)})},e.exports=n},function(e,t){"use strict";e.exports=function(e){return/^([a-z][a-z\d\+\-\.]*:)?\/\//i.test(e)}},function(e,t){"use strict";e.exports=function(e,t){return e.replace(/\/+$/,"")+"/"+t.replace(/^\/+/,"")}},function(e,t){"use strict";e.exports=function(e,t){return function(){for(var r=new Array(arguments.length),n=0;n<r.length;n++)r[n]=arguments[n];return e.apply(t,r)}}},function(e,t){"use strict";e.exports=function(e){return function(t){return e.apply(null,t)}}}])});
//# sourceMappingURL=axios.min.map
