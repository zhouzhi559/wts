(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-c3c707ae"],{"0cb2":function(e,t,a){var r=a("7b0b"),n=Math.floor,i="".replace,o=/\$([$&'`]|\d{1,2}|<[^>]*>)/g,s=/\$([$&'`]|\d{1,2})/g;e.exports=function(e,t,a,l,c,u){var d=a+e.length,f=l.length,g=s;return void 0!==c&&(c=r(c),g=o),i.call(u,g,(function(r,i){var o;switch(i.charAt(0)){case"$":return"$";case"&":return e;case"`":return t.slice(0,a);case"'":return t.slice(d);case"<":o=c[i.slice(1,-1)];break;default:var s=+i;if(0===s)return r;if(s>f){var u=n(s/10);return 0===u?r:u<=f?void 0===l[u-1]?i.charAt(1):l[u-1]+i.charAt(1):r}o=l[s-1]}return void 0===o?"":o}))}},1148:function(e,t,a){"use strict";var r=a("a691"),n=a("1d80");e.exports=function(e){var t=String(n(this)),a="",i=r(e);if(i<0||i==1/0)throw RangeError("Wrong number of repetitions");for(;i>0;(i>>>=1)&&(t+=t))1&i&&(a+=t);return a}},"14c3":function(e,t,a){var r=a("c6b6"),n=a("9263");e.exports=function(e,t){var a=e.exec;if("function"===typeof a){var i=a.call(e,t);if("object"!==typeof i)throw TypeError("RegExp exec method returned something other than an Object or null");return i}if("RegExp"!==r(e))throw TypeError("RegExp#exec called on incompatible receiver");return n.call(e,t)}},"207e":function(e,t,a){"use strict";a.d(t,"a",(function(){return r}));a("5319"),a("ac1f"),a("4d63"),a("25f0");function r(e,t){var a=new Date(e),r={"M+":a.getMonth()+1,"d+":a.getDate(),"h+":a.getHours(),"m+":a.getMinutes(),"s+":a.getSeconds(),"w+":a.getDay(),"q+":Math.floor((a.getMonth()+3)/3),S:a.getMilliseconds()};for(var n in/(y+)/.test(t)&&(t=t.replace(RegExp.$1,(a.getFullYear()+"").substr(4-RegExp.$1.length))),r)"w+"===n?0===r[n]?t=t.replace("w","周日"):1===r[n]?t=t.replace("w","周一"):2===r[n]?t=t.replace("w","周二"):3===r[n]?t=t.replace("w","周三"):4===r[n]?t=t.replace("w","周四"):5===r[n]?t=t.replace("w","周五"):6===r[n]&&(t=t.replace("w","周六")):new RegExp("("+n+")").test(t)&&(t=t.replace(RegExp.$1,1==RegExp.$1.length?r[n]:("00"+r[n]).substr((""+r[n]).length)));return t}},"25f0":function(e,t,a){"use strict";var r=a("6eeb"),n=a("825a"),i=a("d039"),o=a("ad6d"),s="toString",l=RegExp.prototype,c=l[s],u=i((function(){return"/a/b"!=c.call({source:"a",flags:"b"})})),d=c.name!=s;(u||d)&&r(RegExp.prototype,s,(function(){var e=n(this),t=String(e.source),a=e.flags,r=String(void 0===a&&e instanceof RegExp&&!("flags"in l)?o.call(e):a);return"/"+t+"/"+r}),{unsafe:!0})},"2f82":function(e,t,a){},"2fb8":function(e,t,a){"use strict";a("fd09")},"408a":function(e,t,a){var r=a("c6b6");e.exports=function(e){if("number"!=typeof e&&"Number"!=r(e))throw TypeError("Incorrect invocation");return+e}},"44e7":function(e,t,a){var r=a("861d"),n=a("c6b6"),i=a("b622"),o=i("match");e.exports=function(e){var t;return r(e)&&(void 0!==(t=e[o])?!!t:"RegExp"==n(e))}},"4d63":function(e,t,a){var r=a("83ab"),n=a("da84"),i=a("94ca"),o=a("7156"),s=a("9bf2").f,l=a("241c").f,c=a("44e7"),u=a("ad6d"),d=a("9f7f"),f=a("6eeb"),g=a("d039"),p=a("69f3").set,h=a("2626"),m=a("b622"),_=m("match"),v=n.RegExp,y=v.prototype,b=/a/g,w=/a/g,x=new v(b)!==b,C=d.UNSUPPORTED_Y,S=r&&i("RegExp",!x||C||g((function(){return w[_]=!1,v(b)!=b||v(w)==w||"/a/i"!=v(b,"i")})));if(S){var P=function(e,t){var a,r=this instanceof P,n=c(e),i=void 0===t;if(!r&&n&&e.constructor===P&&i)return e;x?n&&!i&&(e=e.source):e instanceof P&&(i&&(t=u.call(e)),e=e.source),C&&(a=!!t&&t.indexOf("y")>-1,a&&(t=t.replace(/y/g,"")));var s=o(x?new v(e,t):v(e,t),r?this:y,P);return C&&a&&p(s,{sticky:a}),s},k=function(e){e in P||s(P,e,{configurable:!0,get:function(){return v[e]},set:function(t){v[e]=t}})},E=l(v),L=0;while(E.length>L)k(E[L++]);y.constructor=P,P.prototype=y,f(n,"RegExp",P)}h("RegExp")},5319:function(e,t,a){"use strict";var r=a("d784"),n=a("825a"),i=a("50c4"),o=a("a691"),s=a("1d80"),l=a("8aa5"),c=a("0cb2"),u=a("14c3"),d=Math.max,f=Math.min,g=function(e){return void 0===e?e:String(e)};r("replace",2,(function(e,t,a,r){var p=r.REGEXP_REPLACE_SUBSTITUTES_UNDEFINED_CAPTURE,h=r.REPLACE_KEEPS_$0,m=p?"$":"$0";return[function(a,r){var n=s(this),i=void 0==a?void 0:a[e];return void 0!==i?i.call(a,n,r):t.call(String(n),a,r)},function(e,r){if(!p&&h||"string"===typeof r&&-1===r.indexOf(m)){var s=a(t,e,this,r);if(s.done)return s.value}var _=n(e),v=String(this),y="function"===typeof r;y||(r=String(r));var b=_.global;if(b){var w=_.unicode;_.lastIndex=0}var x=[];while(1){var C=u(_,v);if(null===C)break;if(x.push(C),!b)break;var S=String(C[0]);""===S&&(_.lastIndex=l(v,i(_.lastIndex),w))}for(var P="",k=0,E=0;E<x.length;E++){C=x[E];for(var L=String(C[0]),N=d(f(o(C.index),v.length),0),R=[],$=1;$<C.length;$++)R.push(g(C[$]));var T=C.groups;if(y){var Q=[L].concat(R,N,v);void 0!==T&&Q.push(T);var O=String(r.apply(void 0,Q))}else O=c(L,v,N,R,T,r);N>=k&&(P+=v.slice(k,N)+O,k=N+L.length)}return P+v.slice(k)}]}))},5849:function(e,t,a){"use strict";a("2f82")},7156:function(e,t,a){var r=a("861d"),n=a("d2bb");e.exports=function(e,t,a){var i,o;return n&&"function"==typeof(i=t.constructor)&&i!==a&&r(o=i.prototype)&&o!==a.prototype&&n(e,o),e}},"8aa5":function(e,t,a){"use strict";var r=a("6547").charAt;e.exports=function(e,t,a){return t+(a?r(e,t).length:1)}},9263:function(e,t,a){"use strict";var r=a("ad6d"),n=a("9f7f"),i=a("5692"),o=RegExp.prototype.exec,s=i("native-string-replace",String.prototype.replace),l=o,c=function(){var e=/a/,t=/b*/g;return o.call(e,"a"),o.call(t,"a"),0!==e.lastIndex||0!==t.lastIndex}(),u=n.UNSUPPORTED_Y||n.BROKEN_CARET,d=void 0!==/()??/.exec("")[1],f=c||d||u;f&&(l=function(e){var t,a,n,i,l=this,f=u&&l.sticky,g=r.call(l),p=l.source,h=0,m=e;return f&&(g=g.replace("y",""),-1===g.indexOf("g")&&(g+="g"),m=String(e).slice(l.lastIndex),l.lastIndex>0&&(!l.multiline||l.multiline&&"\n"!==e[l.lastIndex-1])&&(p="(?: "+p+")",m=" "+m,h++),a=new RegExp("^(?:"+p+")",g)),d&&(a=new RegExp("^"+p+"$(?!\\s)",g)),c&&(t=l.lastIndex),n=o.call(f?a:l,m),f?n?(n.input=n.input.slice(h),n[0]=n[0].slice(h),n.index=l.lastIndex,l.lastIndex+=n[0].length):l.lastIndex=0:c&&n&&(l.lastIndex=l.global?n.index+n[0].length:t),d&&n&&n.length>1&&s.call(n[0],a,(function(){for(i=1;i<arguments.length-2;i++)void 0===arguments[i]&&(n[i]=void 0)})),n}),e.exports=l},"9f7f":function(e,t,a){"use strict";var r=a("d039");function n(e,t){return RegExp(e,t)}t.UNSUPPORTED_Y=r((function(){var e=n("a","y");return e.lastIndex=2,null!=e.exec("abcd")})),t.BROKEN_CARET=r((function(){var e=n("^r","gy");return e.lastIndex=2,null!=e.exec("str")}))},a927:function(e,t,a){"use strict";var r=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",[a("el-table",{staticStyle:{width:"100%"},attrs:{data:e.tableData,"header-cell-style":{background:"#eef1f6",color:"#606266"}},on:{"selection-change":e.handleSelectionChange}},[e.isShowSelect?a("el-table-column",{attrs:{type:"selection",width:"55"}}):e._e(),e._l(e.tableCol,(function(t,r){return["solt"==t.colType?a("el-table-column",{key:r+"only",attrs:{prop:t.field,label:t.label,width:t.width,align:t.align?t.align:"left"},scopedSlots:e._u([{key:"default",fn:function(r){return!t.isShow||t.isShow(r.row)?e._l(t.option,(function(t,n){return a("span",{key:n+"only",staticStyle:{display:"inline-block","margin-left":"5px"}},[a("el-button",{attrs:{type:"text",size:"small"},on:{click:function(e){return t.event(r.row)}}},[e._v(" "+e._s(t.label)+" ")])],1)})):void 0}}],null,!0)}):e._e(),"tag"==t.colType?a("el-table-column",{key:r+"only",attrs:{prop:t.field,label:t.label,width:t.width,align:t.align,sortable:""},scopedSlots:e._u([{key:"default",fn:function(r){return[a("el-tag",{style:[{width:t.tagRender(r.row).tagWidth?t.tagRender(r.row).tagWidth:"70px"}],attrs:{size:"medium",type:t.tagRender(r.row).tagType}},[e._v(e._s(t.tagRender(r.row).tagText))])]}}],null,!0)}):e._e(),"solt"!=t.colType&&"tag"!=t.colType&&0!=t.show?a("el-table-column",{key:r+"only",attrs:{prop:t.field,label:t.label,width:t.width,align:t.align,sortable:""}}):e._e()]}))],2),e.ispagination?a("div",{staticClass:"pagination-wrap"},[a("el-pagination",{attrs:{"current-page":e.listQuery.page,"page-sizes":[5,10,20,30,40,50,100],"page-size":e.listQuery.page_size,layout:"total, sizes, prev, pager, next, jumper",total:e.listQuery.total},on:{"size-change":e.handleSizeChange,"current-change":e.handleCurrentChange}})],1):e._e()],1)},n=[],i={name:"ELTable",props:{tableCol:{type:Array,default:function(){return[]}},tableData:{type:Array,default:function(){return[]}},ispagination:{type:Boolean,default:!0},isShowSelect:{type:Boolean,default:!1},listQuery:{type:Object,default:function(){return{page:1,page_size:10,total:0}}}},data:function(){return{}},methods:{handleSizeChange:function(e){this.$emit("sizeChange",e)},handleCurrentChange:function(e){this.$emit("currentChange",e)},handleSelectionChange:function(e){this.$emit("handleSelectionChange",e)}}},o=i,s=a("2877"),l=Object(s["a"])(o,r,n,!1,null,"b575f792",null);t["a"]=l.exports},ac1f:function(e,t,a){"use strict";var r=a("23e7"),n=a("9263");r({target:"RegExp",proto:!0,forced:/./.exec!==n},{exec:n})},ad6d:function(e,t,a){"use strict";var r=a("825a");e.exports=function(){var e=r(this),t="";return e.global&&(t+="g"),e.ignoreCase&&(t+="i"),e.multiline&&(t+="m"),e.dotAll&&(t+="s"),e.unicode&&(t+="u"),e.sticky&&(t+="y"),t}},b680:function(e,t,a){"use strict";var r=a("23e7"),n=a("a691"),i=a("408a"),o=a("1148"),s=a("d039"),l=1..toFixed,c=Math.floor,u=function(e,t,a){return 0===t?a:t%2===1?u(e,t-1,a*e):u(e*e,t/2,a)},d=function(e){var t=0,a=e;while(a>=4096)t+=12,a/=4096;while(a>=2)t+=1,a/=2;return t},f=function(e,t,a){var r=-1,n=a;while(++r<6)n+=t*e[r],e[r]=n%1e7,n=c(n/1e7)},g=function(e,t){var a=6,r=0;while(--a>=0)r+=e[a],e[a]=c(r/t),r=r%t*1e7},p=function(e){var t=6,a="";while(--t>=0)if(""!==a||0===t||0!==e[t]){var r=String(e[t]);a=""===a?r:a+o.call("0",7-r.length)+r}return a},h=l&&("0.000"!==8e-5.toFixed(3)||"1"!==.9.toFixed(0)||"1.25"!==1.255.toFixed(2)||"1000000000000000128"!==(0xde0b6b3a7640080).toFixed(0))||!s((function(){l.call({})}));r({target:"Number",proto:!0,forced:h},{toFixed:function(e){var t,a,r,s,l=i(this),c=n(e),h=[0,0,0,0,0,0],m="",_="0";if(c<0||c>20)throw RangeError("Incorrect fraction digits");if(l!=l)return"NaN";if(l<=-1e21||l>=1e21)return String(l);if(l<0&&(m="-",l=-l),l>1e-21)if(t=d(l*u(2,69,1))-69,a=t<0?l*u(2,-t,1):l/u(2,t,1),a*=4503599627370496,t=52-t,t>0){f(h,0,a),r=c;while(r>=7)f(h,1e7,0),r-=7;f(h,u(10,r,1),0),r=t-1;while(r>=23)g(h,1<<23),r-=23;g(h,1<<r),f(h,1,1),g(h,2),_=p(h)}else f(h,0,a),f(h,1<<-t,0),_=p(h)+o.call("0",c);return c>0?(s=_.length,_=m+(s<=c?"0."+o.call("0",c-s)+_:_.slice(0,s-c)+"."+_.slice(s-c))):_=m+_,_}})},bf51:function(e,t,a){"use strict";a.r(t);var r=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",[a("el-card",[a("div",{staticClass:"clearfix",attrs:{slot:"header"},slot:"header"},[a("CommonMissStationHeader")],1),a("el-row",{attrs:{gutter:20}},[a("el-col",{attrs:{span:14}},[a("div",[a("span",[e._v("应加工物料数量 : "+e._s(e.form.response_datas.length))]),a("span",{staticClass:"ml20"},[e._v(" 已加工物料数量 : "+e._s(e.form.matter_arr.length)+"/ "+e._s(e.form.response_datas.length))]),e.QualifiedFlag?a("span",{staticClass:"ml20"},[e._v(" 产品编码 : "+e._s(e.form.finished_product_code))]):e._e()]),a("el-form",{ref:"formRef",staticStyle:{padding:"0 60px 0 20px",width:"90%",margin:"20px 0 40px"},attrs:{model:e.form,rules:e.formRules,"label-width":"none"}},[a("el-form-item",{directives:[{name:"show",rawName:"v-show",value:!e.QualifiedFlag,expression:"!QualifiedFlag"}],attrs:{prop:"finished_product_code",label:"产品编码",rules:[{required:!0,message:"产品编码不能为空"}]}},[a("el-input",{ref:"firstInput",attrs:{clearable:""},on:{input:e.inputChange},model:{value:e.form.finished_product_code,callback:function(t){e.$set(e.form,"finished_product_code",t)},expression:"form.finished_product_code"}})],1),e._l(e.form.response_datas,(function(t,r){return a("div",{key:r+" onlyItem"},[a("el-form-item",{directives:[{name:"show",rawName:"v-show",value:e.form.matter_arr.length==r&&e.QualifiedFlag,expression:"form.matter_arr.length == index && QualifiedFlag"}],attrs:{prop:"response_datas."+r+".matter_id",label:t.matter_name+"编码"+(r+1)+":","label-width":"none"}},[a("el-input",{ref:"matterInput"+r,refInFor:!0,on:{input:function(a){e.nextFocus("matterInput"+(r+1),r,t.matter_code,a)}},model:{value:t.matter_id,callback:function(a){e.$set(t,"matter_id",a)},expression:"item.matter_id"}})],1)],1)})),a("el-form-item",{directives:[{name:"show",rawName:"v-show",value:e.test_resultFlag,expression:"test_resultFlag"}],attrs:{label:"检验结果",prop:"test_result"}},[a("el-select",{staticStyle:{width:"100%"},attrs:{placeholder:"请选择"},model:{value:e.form.test_result,callback:function(t){e.$set(e.form,"test_result",t)},expression:"form.test_result"}},[a("el-option",{attrs:{label:"合格",value:"合格"}}),a("el-option",{attrs:{label:"不合格",value:"不合格"}})],1)],1),"不合格"==e.form.test_result?a("el-form-item",{attrs:{label:"不合格原因",prop:"description"}},[a("el-select",{staticStyle:{width:"100%"},attrs:{placeholder:"请选择"},model:{value:e.form.description,callback:function(t){e.$set(e.form,"description",t)},expression:"form.description"}},e._l(e.UnqualifiedResultCodeNameList,(function(e,t){return a("el-option",{key:t+" dialog",attrs:{label:e.unqualified_result_code+"_"+e.unqualified_result_name,value:e.unqualified_result_code}})})),1)],1):e._e()],2),a("div",[a("el-button",{on:{click:e.resetForm}},[e._v("重 置")]),a("el-button",{staticStyle:{"margin-left":"60px"},attrs:{type:"primary"},on:{click:e.dialogSave}},[e._v("确 定")])],1)],1),a("el-col",{attrs:{span:10}},[a("div",{ref:"PieChart",staticClass:"chart chartClass"})])],1)],1),a("div",{staticClass:"formDiv mt20"},[a("el-form",{staticClass:"demo-form-inline",attrs:{inline:!0}},[a("el-form-item",{attrs:{label:"时间"}},[a("el-date-picker",{attrs:{type:"daterange","range-separator":"至","start-placeholder":"开始日期","end-placeholder":"结束日期","value-format":"yyyy-MM-dd",format:"yyyy-MM-dd"},on:{change:e.daterange_change},model:{value:e.listQuery.daterangeArr,callback:function(t){e.$set(e.listQuery,"daterangeArr",t)},expression:"listQuery.daterangeArr"}})],1),a("el-form-item",{staticStyle:{"margin-left":"20px !important"}},[a("el-button",{attrs:{type:"primary",size:"medium"},on:{click:e.searchBtn}},[e._v("查 询")]),a("el-button",{attrs:{size:"medium"},on:{click:function(t){return e.resetTable()}}},[e._v("重 置")])],1)],1)],1),a("el-card",{staticClass:"box-card mt20"},[a("div",{staticClass:"clearfix",attrs:{slot:"header"},slot:"header"},[a("span",[e._v("过站信息")])]),a("div",{},[a("ELTable",{attrs:{tableCol:e.tableCol,tableData:e.tableData,listQuery:e.listQuery,ispagination:!0},on:{currentChange:e.currentChange,sizeChange:e.sizeChange}})],1)])],1)},n=[],i=a("ade3"),o=a("1da1"),s=a("5530"),l=(a("96cf"),a("159b"),a("b0c0"),a("b680"),a("fd03")),c=a("2f62"),u=a("e3d2"),d=a("a927"),f=a("207e"),g=a("313e"),p={name:"MissStation",components:{CommonMissStationHeader:u["a"],ELTable:d["a"]},created:function(){window.addEventListener("keydown",this.handleKeyDown,!0)},data:function(){return{myChart:null,seriesData:[],titleTotal:0,timeout:"",Package_Qty:"",Shipping_SN_length:"",Product_length:"",QualifiedFlag:!1,test_resultFlag:!1,form:{product_plan_code:"",finished_product_code:"",matter_arr:[],response_datas:[],test_result:"合格",description:""},formBase:{product_plan_code:"",finished_product_code:"",matter_arr:[],response_datas:[],test_result:"合格",description:""},formRules:{test_result:[{required:!0,message:"请选择检验结果",trigger:"change"}]},response_datasRules:{matter_id:[{required:!0,message:"数量不能为空",trigger:"blur"}]},listQuery:{daterangeArr:[Object(f["a"])(new Date,"yyyy-MM-dd 00:00:00"),Object(f["a"])(new Date,"yyyy-MM-dd 23:59:59")],start_time:Object(f["a"])(new Date,"yyyy-MM-dd 00:00:00"),end_time:Object(f["a"])(new Date,"yyyy-MM-dd 23:59:59"),user_code:"",work_code:"",test_result:"",product_plan_code:this.ProductionPlanCode,product_code:"",page:1,page_size:10,total:0},listQueryBase:{daterangeArr:[Object(f["a"])(new Date,"yyyy-MM-dd 00:00:00"),Object(f["a"])(new Date,"yyyy-MM-dd 23:59:59")],start_time:Object(f["a"])(new Date,"yyyy-MM-dd 00:00:00"),end_time:Object(f["a"])(new Date,"yyyy-MM-dd 23:59:59"),matter_code:"",user_code:"",work_code:"",test_result:"",product_plan_code:this.ProductionPlanCode,product_code:"",page:1,page_size:10,total:0},ispagination:!0,tableCol:[{label:"生产计划",field:"product_plan_name",align:"center"},{label:"产品名称",field:"product_name",align:"center"},{label:"产品编码",field:"finished_product_code",align:"center"},{label:"工站名称",field:"work_name",align:"center"},{label:"操作人员",field:"user_name",width:"200px",align:"center"},{label:"检验结果",width:"200px",field:"test_result",align:"center",colType:"tag",tagRender:function(e){"PASS"==e.test_result?e.test_result="合格":"FAIL"==e.test_result&&(e.test_result="不合格");var t={tagType:"",tagText:e.test_result};return"合格"==e.test_result?t.tagType="":t.tagType="warning",t}},{label:"时间",field:"out_time",align:"center"}],tableData:[]}},computed:Object(s["a"])({},Object(c["c"])(["ProductionPlanCode","ProductPlanCodeNameList","MatterCodeNameList","BomMatterCodeNameList","PersonCodeNameList","CurrentUserInfo","WorkCodeNameList","UnqualifiedResultCodeNameList"])),methods:Object(s["a"])(Object(s["a"])({},Object(c["b"])(["getLogisticProductPlanDeal","getLogisticProductPlanCodeName","getLogisticMatterNameCode","getLogisticBomMatterCodeName","getLogisticPersonCodeName","getLogisticWorkCodeName","getLogisticNopageWorkUnqualifiedResultName"])),{},{daterange_change:function(){this.listQuery.daterangeArr.length>0&&(this.listQuery.start_time=this.listQuery.daterangeArr[0]+" 00:00:00",this.listQuery.end_time=this.listQuery.daterangeArr[1]+" 23:59:59")},searchBtn:function(){this.listQuery.page=1,this.getLogisticTransitProductQualifiedSearch(this.listQuery)},resetTable:function(){this.listQuery=JSON.parse(JSON.stringify(this.listQueryBase)),this.getLogisticTransitProductQualifiedSearch(this.listQuery)},getLogisticOperationSystem:function(){var e=this;l["a"].getLogisticOperationSystem({page:1,page_size:10}).then((function(t){console.log("打印参数列表 查询",t),0==t.code?(e.Package_Qty=t.data.data[0].Package_Qty,e.Shipping_SN_length=t.data.data[0].Shipping_SN_length,e.Product_length=t.data.data[0].Product_length):e.$message({message:t.message,type:"error"})}))},inputChange:function(e){var t=this,a=e;this.timeout&&clearTimeout(this.timeout),this.timeout=setTimeout((function(){if(t.form.finished_product_code.length!=t.Product_length)return t.$message.warning("产品编码长度为"+t.Product_length+"个字节。"),!1;if(0==t.form.finished_product_code.length)return!1;if(t.form.finished_product_code==a&&t.form.finished_product_code){var e={finished_product_code:t.form.finished_product_code};l["a"].getLogisticQualifiedMatterCode(e).then((function(e){console.log("寻找此工站的上一站的物料是否合格接口： 查询",e),0==e.code?(t.QualifiedFlag=!0,t.$nextTick((function(){t.$refs.matterInput0[0].focus()}))):t.$message({message:e.message,type:"error"})}))}}),500)},nextFocus:function(e,t,a){var r=this;this.timeout&&clearTimeout(this.timeout),this.timeout=setTimeout((function(){return""==r.form.response_datas[t].matter_id?(r.$message.warning("物料编码不能为空"),!1):r.form.response_datas[t].matter_id.indexOf(r.form.response_datas[t].rule)<0?(r.$message.warning("物料编码需要包含"+r.form.response_datas[t].rule),!1):r.form.response_datas[t].matter_id.length!=r.form.response_datas[t].code_length?(r.$message.warning("物料编码长度为"+r.form.response_datas[t].code_length+"个字节。"),!1):(r.form.matter_arr.push(r.form.response_datas[t].matter_id),void(t<r.form.response_datas.length-1?r.$nextTick((function(){r.$refs[e][0].focus()})):r.test_resultFlag=!0))}),500)},getLogisticWorkStationGetData:function(){var e=this;return Object(o["a"])(regeneratorRuntime.mark((function t(){return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:return t.next=2,e.getLogisticBomMatterCodeName();case 2:l["a"].getLogisticWorkStationGetData().then((function(t){if(console.log("通过工站获取BOM产品物料： 查询",t),console.log("产品　物料code和名称接口 查询 BomMatterCodeNameList",e.BomMatterCodeNameList),0==t.code){var a=t.data[0].response_datas,r=[];a.forEach((function(t,a){e.BomMatterCodeNameList.forEach((function(e){t.matter_code==e.matter_code&&(t.matter_name=e.matter_name,t.rule=e.rule,t.code_length=e.code_length)}))}));for(var n=0;n<a.length;n++)for(var i=0;i<a[n].install_number;i++)r.push({matter_name:a[n].matter_name,matter_code:a[n].matter_code,matter_id:a[n].matter_id,rule:a[n].rule,code_length:a[n].code_length});e.form.response_datas=r}else e.$message({message:t.message,type:"error"})}));case 3:case"end":return t.stop()}}),t)})))()},postLogisticProductTransitInfo:function(e){var t=this;l["a"].postLogisticProductTransitInfo(e).then((function(e){console.log("产品过站 新增",e),0==e.code?(t.resetForm(),t.getLogisticTransitProductQualifiedSearch(t.listQuery),t.$message({message:e.message,type:"success"})):t.$message({message:e.message,type:"error"})}))},resetForm:function(){var e=this;this.form=JSON.parse(JSON.stringify(this.formBase)),this.getLogisticWorkStationGetData(),this.QualifiedFlag=!1,this.test_resultFlag=!1,this.form.test_result,this.$nextTick((function(){e.$refs.formRef.clearValidate(),e.$refs.firstInput.focus()}))},dialogSave:function(){var e=this;return!!this.test_resultFlag&&(this.ProductionPlanCode?this.form.finished_product_code.length!=this.Product_length?(this.$message.warning("产品编码长度为"+this.Product_length+"个字节。"),!1):this.form.matter_arr.length<this.form.response_datas.length?(this.$message.warning("存在未加工物料！"),!1):void this.$refs.formRef.validate((function(t){if(t){console.log("产品过站",e.form),e.form.product_plan_code=e.ProductionPlanCode;var a=JSON.parse(JSON.stringify(e.form));e.QualifiedFlag?("合格"==a.test_result?a.test_result="PASS":"不合格"==a.test_result&&(a.test_result="FAIL"),e.postLogisticProductTransitInfo(a)):e.$message({message:"该产品上一工站不合格",type:"error"})}else e.$message({message:"请修改正确的数据格式！",type:"warning"})})):(this.$message.warning("没有进行中的生产计划！"),!1))},handleKeyDown:function(e){var t=null;t=void 0===window.event?e.keyCode:window.event.keyCode,13===t&&this.dialogSave()},getLogisticTransitProductQualifiedSearch:function(e){var t=this;e.product_plan_code=this.ProductionPlanCode,l["a"].getLogisticTransitProductQualifiedSearch(e).then((function(e){if(console.log("过站查询 查询",e),0==e.code){var a=e.data.data;t.seriesData=[{value:e.data.pass_num,name:"合格"},{value:e.data.fail_num,name:"不合格"}],t.titleTotal=e.data.pass_num+e.data.fail_num,t.chartInit(),a.forEach((function(e){t.ProductPlanCodeNameList.forEach((function(t){e.product_plan_code==t.product_plan_code&&(e.product_plan_name=t.product_plan_name)})),t.PersonCodeNameList.forEach((function(t){e.user_code==t.user_code&&(e.user_name=t.user_name)})),t.MatterCodeNameList.forEach((function(t){e.matter_code==t.matter_code&&(e.matter_name=t.matter_name)})),t.WorkCodeNameList.forEach((function(t){e.work_code==t.work_code&&(e.work_name=t.work_name)}))})),t.tableData=a,t.listQuery.total=e.data.total}else t.$message({message:e.message,type:"error"})}))},currentChange:function(e){this.listQuery.page=e,this.getLogisticTransitProductQualifiedSearch(this.listQuery)},sizeChange:function(e){this.listQuery.page=1,this.listQuery.page_size=e,this.getLogisticTransitProductQualifiedSearch(this.listQuery)},chartInit:function(){var e=this,t=this;null!=this.myChart&&""!=this.myChart&&void 0!=this.myChart&&this.myChart.dispose(),this.myChart=g["a"](this.$refs.PieChart);var a,r={};for(var n in this.noneFlag=!1,this.seriesData)this.seriesData[n].value>0&&(this.noneFlag=!0);this.noneFlag?r={title:{text:"总计:"+this.titleTotal,top:"5%",right:"8%",textStyle:{fontSize:"16"}},color:["#5470c6","#FAC858"],tooltip:{trigger:"item",formatter:function(t){return t.name+":  "+t.value+" "+(t.value/e.titleTotal*100).toFixed(2)+"%"}},legend:{type:"scroll",orient:"vertical",top:"center",right:"3%",textStyle:{padding:5}},series:[(a={type:"pie",radius:["45%","75%"],center:["50%","50%"],avoidLabelOverlap:!1,label:{show:!1,position:"center"},emphasis:{label:{show:!0}}},Object(i["a"])(a,"label",{formatter:" {b|{b}：}{c}  {per|{d}%}  ",borderRadius:4,rich:{per:{borderRadius:4}}}),Object(i["a"])(a,"labelLine",{}),Object(i["a"])(a,"data",this.seriesData),a)]}:r={title:{text:"无数据",top:"center",left:"center"},series:[]};this.myChart.setOption(r),this.myChart.on("click",(function(e){t.$emit("pieChartClick",e)})),window.addEventListener("resize",(function(){t.myChart.resize()}))}}),mounted:function(){var e=this;this.getLogisticOperationSystem(),this.getLogisticProductPlanDeal(),this.getLogisticWorkStationGetData(),this.getLogisticProductPlanCodeName(),this.getLogisticPersonCodeName(),this.getLogisticMatterNameCode(),this.getLogisticWorkCodeName(),this.getLogisticNopageWorkUnqualifiedResultName({work_id:this.CurrentUserInfo.work_id}),this.getLogisticTransitProductQualifiedSearch(this.listQuery),this.$nextTick((function(){e.$refs.firstInput.focus()}))}},h=p,m=(a("2fb8"),a("2877")),_=Object(m["a"])(h,r,n,!1,null,"a68b19cc",null);t["default"]=_.exports},d784:function(e,t,a){"use strict";a("ac1f");var r=a("6eeb"),n=a("d039"),i=a("b622"),o=a("9263"),s=a("9112"),l=i("species"),c=!n((function(){var e=/./;return e.exec=function(){var e=[];return e.groups={a:"7"},e},"7"!=="".replace(e,"$<a>")})),u=function(){return"$0"==="a".replace(/./,"$0")}(),d=i("replace"),f=function(){return!!/./[d]&&""===/./[d]("a","$0")}(),g=!n((function(){var e=/(?:)/,t=e.exec;e.exec=function(){return t.apply(this,arguments)};var a="ab".split(e);return 2!==a.length||"a"!==a[0]||"b"!==a[1]}));e.exports=function(e,t,a,d){var p=i(e),h=!n((function(){var t={};return t[p]=function(){return 7},7!=""[e](t)})),m=h&&!n((function(){var t=!1,a=/a/;return"split"===e&&(a={},a.constructor={},a.constructor[l]=function(){return a},a.flags="",a[p]=/./[p]),a.exec=function(){return t=!0,null},a[p](""),!t}));if(!h||!m||"replace"===e&&(!c||!u||f)||"split"===e&&!g){var _=/./[p],v=a(p,""[e],(function(e,t,a,r,n){return t.exec===o?h&&!n?{done:!0,value:_.call(t,a,r)}:{done:!0,value:e.call(a,t,r)}:{done:!1}}),{REPLACE_KEEPS_$0:u,REGEXP_REPLACE_SUBSTITUTES_UNDEFINED_CAPTURE:f}),y=v[0],b=v[1];r(String.prototype,e,y),r(RegExp.prototype,p,2==t?function(e,t){return b.call(e,this,t)}:function(e){return b.call(e,this)})}d&&s(RegExp.prototype[p],"sham",!0)}},e3d2:function(e,t,a){"use strict";var r=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",[a("span",{staticClass:"boxDivSpanFontSize"},[e._v(" 生产计划 : ")]),a("span",{},[e._v(e._s(e.ProductionPlanName))]),a("span",{staticClass:"ml20 boxDivSpanFontSize"},[e._v(" 工站编码 : ")]),a("span",{},[e._v(e._s(e.CurrentUserInfo.work_id))]),a("span",{staticClass:"ml20 boxDivSpanFontSize"},[e._v("工站名称 : ")]),a("span",[e._v(e._s(e.workStationName))]),a("span",{staticClass:"ml20 boxDivSpanFontSize"},[e._v("工站类型 : ")]),a("span",[e._v(e._s(e.CurrentUserInfo.work_type))])])},n=[],i=a("1da1"),o=a("5530"),s=(a("96cf"),a("159b"),a("fd03")),l=a("2f62"),c={computed:Object(o["a"])({},Object(l["c"])(["WorkCodeNameList","ProductionPlanCode","CurrentUserInfo"])),created:function(){},data:function(){return{workStationName:"",ProductionPlanName:""}},methods:Object(o["a"])(Object(o["a"])({},Object(l["b"])(["getLogisticWorkCodeName","getLogisticProductPlanDeal"])),{},{getMissStationHeaderWorkName:function(){var e=this;return Object(i["a"])(regeneratorRuntime.mark((function t(){return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:return t.next=2,e.getLogisticWorkCodeName();case 2:e.WorkCodeNameList.forEach((function(t){e.CurrentUserInfo.work_id==t.work_id&&(e.workStationName=t.work_name)}));case 3:case"end":return t.stop()}}),t)})))()}}),mounted:function(){var e=this;s["a"].getLogisticProductPlanDeal({prodect_code:"",plan_name:"",plan_status:"进行中",page:1,page_size:10,total:0}).then((function(t){0==t.code&&(console.log(111,t),console.log(111,t.data.data[0]),e.ProductionPlanName=t.data.data[0].plan_name)})),this.getMissStationHeaderWorkName()}},u=c,d=(a("5849"),a("2877")),f=Object(d["a"])(u,r,n,!1,null,"602c22a7",null);t["a"]=f.exports},fd09:function(e,t,a){}}]);
//# sourceMappingURL=chunk-c3c707ae.6d70f029.js.map