(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-2a1a4692"],{a434:function(e,t,a){"use strict";var o=a("23e7"),r=a("23cb"),i=a("a691"),s=a("50c4"),n=a("7b0b"),l=a("65f0"),c=a("8418"),d=a("1dde"),u=d("splice"),g=Math.max,m=Math.min,p=9007199254740991,f="Maximum allowed length exceeded";o({target:"Array",proto:!0,forced:!u},{splice:function(e,t){var a,o,d,u,_,b,h=n(this),y=s(h.length),k=r(e,y),v=arguments.length;if(0===v?a=o=0:1===v?(a=0,o=y-k):(a=v-2,o=m(g(i(t),0),y-k)),y+a-o>p)throw TypeError(f);for(d=l(h,o),u=0;u<o;u++)_=k+u,_ in h&&c(d,u,h[_]);if(d.length=o,a<o){for(u=k;u<y-o;u++)_=u+o,b=u+a,_ in h?h[b]=h[_]:delete h[b];for(u=y;u>y-o+a;u--)delete h[u-1]}else if(a>o)for(u=y-o;u>k;u--)_=u+o-1,b=u+a-1,_ in h?h[b]=h[_]:delete h[b];for(u=0;u<a;u++)h[u+k]=arguments[u+2];return h.length=y-o+a,d}})},a927:function(e,t,a){"use strict";var o=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",[a("el-table",{staticStyle:{width:"100%"},attrs:{data:e.tableData,"header-cell-style":{background:"#eef1f6",color:"#606266"}},on:{"selection-change":e.handleSelectionChange}},[e.isShowSelect?a("el-table-column",{attrs:{type:"selection",width:"55"}}):e._e(),e._l(e.tableCol,(function(t,o){return["solt"==t.colType?a("el-table-column",{key:o+"only",attrs:{prop:t.field,label:t.label,width:t.width,align:t.align?t.align:"left"},scopedSlots:e._u([{key:"default",fn:function(o){return!t.isShow||t.isShow(o.row)?e._l(t.option,(function(t,r){return a("span",{key:r+"only",staticStyle:{display:"inline-block","margin-left":"5px"}},[a("el-button",{attrs:{type:"text",size:"small"},on:{click:function(e){return t.event(o.row)}}},[e._v(" "+e._s(t.label)+" ")])],1)})):void 0}}],null,!0)}):e._e(),"tag"==t.colType?a("el-table-column",{key:o+"only",attrs:{prop:t.field,label:t.label,width:t.width,align:t.align,sortable:""},scopedSlots:e._u([{key:"default",fn:function(o){return[a("el-tag",{style:[{width:t.tagRender(o.row).tagWidth?t.tagRender(o.row).tagWidth:"70px"}],attrs:{size:"medium",type:t.tagRender(o.row).tagType}},[e._v(e._s(t.tagRender(o.row).tagText))])]}}],null,!0)}):e._e(),"solt"!=t.colType&&"tag"!=t.colType&&0!=t.show?a("el-table-column",{key:o+"only",attrs:{prop:t.field,label:t.label,width:t.width,align:t.align,sortable:""}}):e._e()]}))],2),e.ispagination?a("div",{staticClass:"pagination-wrap"},[a("el-pagination",{attrs:{"current-page":e.listQuery.page,"page-sizes":[5,10,20,30,40,50,100],"page-size":e.listQuery.page_size,layout:"total, sizes, prev, pager, next, jumper",total:e.listQuery.total},on:{"size-change":e.handleSizeChange,"current-change":e.handleCurrentChange}})],1):e._e()],1)},r=[],i={name:"ELTable",props:{tableCol:{type:Array,default:function(){return[]}},tableData:{type:Array,default:function(){return[]}},ispagination:{type:Boolean,default:!0},isShowSelect:{type:Boolean,default:!1},listQuery:{type:Object,default:function(){return{page:1,page_size:10,total:0}}}},data:function(){return{}},methods:{handleSizeChange:function(e){this.$emit("sizeChange",e)},handleCurrentChange:function(e){this.$emit("currentChange",e)},handleSelectionChange:function(e){this.$emit("handleSelectionChange",e)}}},s=i,n=a("2877"),l=Object(n["a"])(s,o,r,!1,null,"b575f792",null);t["a"]=l.exports},becb:function(e,t,a){"use strict";a("f48c")},cab0:function(e,t,a){"use strict";a.r(t);var o=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",[a("div",{staticClass:"formDiv"},[a("el-form",{staticClass:"demo-form-inline",attrs:{inline:!0}},[a("el-form-item",{attrs:{label:"退料人员"}},[a("el-select",{staticStyle:{width:"100%"},attrs:{placeholder:"请选择"},model:{value:e.listQuery.back_person,callback:function(t){e.$set(e.listQuery,"back_person",t)},expression:"listQuery.back_person"}},e._l(e.PersonCodeNameList,(function(e,t){return a("el-option",{key:t+" dialog",attrs:{label:e.user_name,value:e.user_code}})})),1)],1),a("el-form-item",{staticStyle:{"margin-left":"20px !important"}},[a("el-button",{attrs:{type:"primary",size:"medium"},on:{click:e.searchBtn}},[e._v("查询")]),a("el-button",{attrs:{size:"medium"},on:{click:function(t){return e.resetForm()}}},[e._v("重置")])],1)],1)],1),a("el-card",{staticClass:"box-card mt20"},[a("div",{},[a("el-form",{staticClass:"demo-form-inline",attrs:{inline:!0}},[a("el-form-item",[a("el-button",{attrs:{type:"primary",size:"medium",plain:""},on:{click:e.addBtn}},[a("i",{staticClass:"el-icon-plus"}),e._v(" 新增")])],1)],1),a("ELTable",{attrs:{tableCol:e.tableCol,tableData:e.tableData,listQuery:e.listQuery,ispagination:e.ispagination},on:{currentChange:e.currentChange,sizeChange:e.sizeChange}})],1)]),a("el-dialog",{attrs:{title:e.dialogTitle,width:"1000px",visible:e.dialogFlag,"close-on-click-modal":!1},on:{"update:visible":function(t){e.dialogFlag=t}}},[a("el-form",{ref:"dialogFormRef",staticStyle:{padding:"0 60px 0 20px"},attrs:{model:e.dialogForm,rules:e.dialogFormRules,"label-width":"100px"}},[a("el-row",[a("p",{staticClass:"dialog-title"},[e._v("基本信息")]),a("el-row",{attrs:{gutter:20}},[a("el-col",{attrs:{span:12}},[a("el-form-item",{attrs:{label:"退料人员",prop:"back_person"}},[a("el-select",{staticStyle:{width:"100%"},attrs:{placeholder:"请选择"},model:{value:e.dialogForm.back_person,callback:function(t){e.$set(e.dialogForm,"back_person",t)},expression:"dialogForm.back_person"}},e._l(e.PersonCodeNameList,(function(e,t){return a("el-option",{key:t+" dialog",attrs:{label:e.user_name,value:e.user_code}})})),1)],1)],1),a("el-col",{attrs:{span:12}},[a("el-form-item",{attrs:{label:"退料时间",prop:"back_time"}},[a("el-date-picker",{staticStyle:{width:"100%"},attrs:{type:"datetime","value-format":"yyyy-MM-dd HH:mm:ss",format:"yyyy-MM-dd HH:mm:ss",placeholder:"选择日期"},model:{value:e.dialogForm.back_time,callback:function(t){e.$set(e.dialogForm,"back_time",t)},expression:"dialogForm.back_time"}})],1)],1)],1),a("el-form-item",{attrs:{label:"备注",prop:"description"}},[a("el-input",{attrs:{type:"textarea"},model:{value:e.dialogForm.description,callback:function(t){e.$set(e.dialogForm,"description",t)},expression:"dialogForm.description"}})],1),a("p",{staticClass:"dialog-title"},[e._v("物料明细")]),a("el-button",{attrs:{type:"primary",size:"small",plain:""},on:{click:function(t){return e.AddListRow()}}},[e._v("添加物料")]),a("el-table",{staticClass:"dialogTable",staticStyle:{width:"100%"},attrs:{data:e.dialogForm.response_datas,height:"240"}},[a("el-table-column",{attrs:{fixed:"left",label:"物料名称",align:"center"},scopedSlots:e._u([{key:"default",fn:function(t){return[a("el-form-item",{attrs:{prop:"response_datas."+t.$index+".matter_code"}},[a("el-select",{staticStyle:{width:"100%"},attrs:{placeholder:"请选择"},on:{change:function(a){return e.dialogMatterCodeChange(t.$index,t.row)}},model:{value:t.row.matter_code,callback:function(a){e.$set(t.row,"matter_code",a)},expression:"scope.row.matter_code"}},e._l(e.NoPagePersonMatterData,(function(e,t){return a("el-option",{key:t+" search",attrs:{label:e.matter_name,value:e.matter_code}})})),1)],1)]}}])}),a("el-table-column",{attrs:{label:"规格型号",align:"center"},scopedSlots:e._u([{key:"default",fn:function(t){return[a("el-form-item",{attrs:{prop:"response_datas."+t.$index+".rule"}},[a("span",[e._v(e._s(t.row.rule))])])]}}])}),a("el-table-column",{attrs:{label:"类型",align:"center"},scopedSlots:e._u([{key:"default",fn:function(t){return[a("el-form-item",{attrs:{prop:"response_datas."+t.$index+".matter_category"}},[a("span",[e._v(e._s(t.row.matter_category))])])]}}])}),a("el-table-column",{attrs:{label:"库存数量",align:"center"},scopedSlots:e._u([{key:"default",fn:function(t){return[a("el-form-item",{attrs:{prop:"response_datas."+t.$index+".matter_usage"}},[a("span",[e._v(e._s(t.row.matter_usage))])])]}}])}),a("el-table-column",{attrs:{label:"退料数量",align:"center"},scopedSlots:e._u([{key:"default",fn:function(t){return[a("el-form-item",{attrs:{prop:"response_datas."+t.$index+".matter_count",rules:[{required:!0,message:"数量不能为空",trigger:"blur"},{type:"number",message:"数量必须为数值",trigger:"blur"},{type:"number",min:0,max:t.row.matter_usage,message:"数量范围0-"+t.row.matter_usage,trigger:"blur"}]}},[a("el-input",{model:{value:t.row.matter_count,callback:function(a){e.$set(t.row,"matter_count",e._n(a))},expression:"scope.row.matter_count"}})],1)]}}])}),a("el-table-column",{attrs:{label:"操作",width:"80",align:"center"},scopedSlots:e._u([{key:"default",fn:function(t){return[a("el-form-item",[a("el-button",{attrs:{size:"small",type:"danger",plain:""},on:{click:function(a){return e.handleDelete(t.$index,t.row)}}},[e._v("删除")])],1)]}}])})],1)],1)],1),a("div",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[a("el-button",{on:{click:function(t){e.dialogFlag=!1}}},[e._v("取 消")]),a("el-button",{attrs:{type:"primary"},on:{click:e.dialogSave}},[e._v("确 定")])],1)],1)],1)},r=[],i=a("1da1"),s=a("5530"),n=(a("96cf"),a("159b"),a("a4d3"),a("e01a"),a("a434"),a("a927")),l=a("fd03"),c=a("2f62"),d={name:"MaterialReturn",components:{ELTable:n["a"]},data:function(){return{listQuery:{product_plan_code:"",back_person:"",page:1,page_size:10,total:0},listQueryBase:{product_plan_code:"",back_person:"",page:1,page_size:10,total:0},ispagination:!0,dialogTitle:"",dialogFlag:!1,dialogForm:{materials_back_code:"",back_person:"",product_plan_code:"",back_time:"",description:"",response_datas:[{matter_code:"",rule:"--",matter_category:"--",matter_usage:"--",matter_count:""}]},dialogFormBase:{materials_back_code:"",back_person:"",product_plan_code:"",back_time:"",description:"",response_datas:[{matter_code:"",rule:"--",matter_category:"--",matter_usage:"--",matter_count:""}]},dialogFormRules:{back_person:[{required:!0,message:"请选择退料人员",trigger:"change"}],back_time:[{required:!0,message:"请选择退料时间",trigger:"change"}]},tableCol:[{label:"退料人员",field:"back_person_name",align:"center"},{label:"退料时间",field:"back_time",align:"center"},{label:"备注",field:"description",align:"center"},{label:"操作",colType:"solt",align:"center",option:[{label:"修改",event:this.colEditBtn},{label:"删除",event:this.colDeleteBtn}]}],tableData:[]}},computed:Object(s["a"])({},Object(c["c"])(["PersonCodeNameList","NoPagePersonMatterData"])),methods:Object(s["a"])(Object(s["a"])({},Object(c["b"])(["getLogisticPersonCodeName","getLogisticNoPagePersonMatter"])),{},{searchBtn:function(){this.listQuery.page=1,this.getLogisticBackMatter(this.listQuery)},resetForm:function(){this.listQuery=JSON.parse(JSON.stringify(this.listQueryBase)),this.getLogisticBackMatter(this.listQuery)},currentChange:function(e){this.listQuery.page=e,this.getLogisticBackMatter(this.listQuery)},sizeChange:function(e){this.dialogMaterialListListQuery.page=1,this.dialogMaterialListListQuery.page_size=e,this.getLogisticBackMatter(this.listQuery)},getLogisticBackMatter:function(e){var t=this;return Object(i["a"])(regeneratorRuntime.mark((function a(){return regeneratorRuntime.wrap((function(a){while(1)switch(a.prev=a.next){case 0:l["a"].getLogisticBackMatter(e).then((function(e){if(console.log("生产退料列表 查询",e),0==e.code){var a=e.data.data;a.forEach((function(e){t.PersonCodeNameList.forEach((function(t){e.back_person==t.user_code&&(e.back_person_name=t.user_name)}))})),t.tableData=a,t.listQuery.total=e.data.total}else t.$message({message:e.message,type:"error"})}));case 1:case"end":return a.stop()}}),a)})))()},postLogisticBackMatter:function(e){var t=this;l["a"].postLogisticBackMatter(e).then((function(e){console.log("生产退料列表 新增",e),0==e.code?(t.dialogFlag=!1,t.getLogisticBackMatter(t.listQuery),t.$message({message:e.message,type:"success"})):t.$message({message:e.message,type:"error"})}))},AddListRow:function(){this.dialogForm.response_datas.push({matter_code:"",rule:"",matter_category:"",matter_usage:"",matter_count:""})},dialogMatterCodeChange:function(e,t){this.NoPagePersonMatterData.forEach((function(e,a){t.matter_code==e.matter_code&&(t.rule=e.rule,t.matter_category=e.matter_category,t.matter_usage=e.matter_count)}))},addBtn:function(){var e=this;this.dialogTitle="新增生产退料",this.dialogFlag=!0,this.$nextTick((function(){e.$refs.dialogFormRef.clearValidate()})),this.dialogForm=JSON.parse(JSON.stringify(this.dialogFormBase))},colEditBtn:function(e){var t=this;return Object(i["a"])(regeneratorRuntime.mark((function a(){return regeneratorRuntime.wrap((function(a){while(1)switch(a.prev=a.next){case 0:console.log(e),t.dialogTitle="修改生产退料",t.dialogFlag=!0,t.$nextTick((function(){t.$refs.dialogFormRef.clearValidate()})),e.response_datas.forEach((function(e){t.NoPagePersonMatterData.forEach((function(t){e.matter_code==t.matter_code&&(e.matter_id=t.matter_id,e.matter_name=t.matter_name,e.rule=t.rule,e.matter_category=t.matter_category,e.matter_usage=t.matter_count)}))})),console.log("rowData.response_datas",e.response_datas),t.dialogForm={materials_back_code:e.materials_back_code,back_person:e.back_person,product_plan_code:e.product_plan_code,back_time:e.back_time,description:e.description,response_datas:e.response_datas};case 7:case"end":return a.stop()}}),a)})))()},getLogisticPutBackMatter:function(e){var t=this;l["a"].getLogisticPutBackMatter(e).then((function(e){console.log("生产退料列表 修改",e),0==e.code?(t.dialogFlag=!1,t.getLogisticBackMatter(t.listQuery),t.$message({message:e.message,type:"success"})):t.$message({message:e.message,type:"error"})}))},dialogSave:function(){var e=this;console.log(this.dialogTitle),this.$refs.dialogFormRef.validate((function(t){t?"新增生产退料"==e.dialogTitle?(console.log("新增生产退料",e.dialogForm),e.postLogisticBackMatter(e.dialogForm)):"修改生产退料"==e.dialogTitle&&(console.log("修改生产退料",e.dialogForm),e.dialogForm.response_datas=JSON.stringify(e.dialogForm.response_datas),e.getLogisticPutBackMatter(e.dialogForm)):e.$message({message:"请修改正确的数据格式！",type:"warning"})}))},getLogisticDeleteBackMatter:function(e){var t=this;l["a"].getLogisticDeleteBackMatter(e).then((function(e){console.log("生产退料列表 删除",e),0==e.code?(t.getLogisticBackMatter(t.listQuery),t.$message({message:e.message,type:"success"})):t.$message({message:e.message,type:"error"})}))},handleDelete:function(e,t){var a=this;t.deal_back_code?this.$confirm("确定执行删除操作吗？","提示",{confirmButtonText:"确定",cancelButtonText:"取消",type:"warning"}).then((function(){var o={materials_back_code:t.materials_back_code,response_datas:JSON.stringify([{deal_back_code:t.deal_back_code}])};a.getLogisticDeleteBackMatter(o),a.dialogForm.response_datas.splice(e,1)})):this.dialogForm.response_datas.splice(e,1)},colDeleteBtn:function(e){var t=this;this.$confirm("确定执行删除操作吗？","提示",{confirmButtonText:"确定",cancelButtonText:"取消",type:"warning"}).then((function(){var a={materials_back_code:e.materials_back_code,response_datas:JSON.stringify([])};t.getLogisticDeleteBackMatter(a)}))}}),mounted:function(){this.getLogisticPersonCodeName(),this.getLogisticNoPagePersonMatter(),this.getLogisticBackMatter(this.listQuery)}},u=d,g=(a("becb"),a("2877")),m=Object(g["a"])(u,o,r,!1,null,"1205f7dc",null);t["default"]=m.exports},e01a:function(e,t,a){"use strict";var o=a("23e7"),r=a("83ab"),i=a("da84"),s=a("5135"),n=a("861d"),l=a("9bf2").f,c=a("e893"),d=i.Symbol;if(r&&"function"==typeof d&&(!("description"in d.prototype)||void 0!==d().description)){var u={},g=function(){var e=arguments.length<1||void 0===arguments[0]?void 0:String(arguments[0]),t=this instanceof g?new d(e):void 0===e?d():d(e);return""===e&&(u[t]=!0),t};c(g,d);var m=g.prototype=d.prototype;m.constructor=g;var p=m.toString,f="Symbol(test)"==String(d("test")),_=/^Symbol\((.*)\)[^)]+$/;l(m,"description",{configurable:!0,get:function(){var e=n(this)?this.valueOf():this,t=p.call(e);if(s(u,e))return"";var a=f?t.slice(7,-1):t.replace(_,"$1");return""===a?void 0:a}}),o({global:!0,forced:!0},{Symbol:g})}},f48c:function(e,t,a){}}]);
//# sourceMappingURL=chunk-2a1a4692.254bca0b.js.map