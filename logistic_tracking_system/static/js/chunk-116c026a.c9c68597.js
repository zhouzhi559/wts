(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-116c026a"],{5711:function(t,e,s){},7395:function(t,e,s){"use strict";s("5711")},"835c":function(t,e,s){"use strict";s.r(e);var o=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("FinishedProductStorageDispatch",{attrs:{formStatus:"入库",cardTitle:"入库"}})},a=[],i=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",[s("el-card",[s("div",{staticClass:"clearfix",attrs:{slot:"header"},slot:"header"},[s("span",[t._v("成品"+t._s(t.cardTitle))])]),s("el-form",{ref:"formRef",staticStyle:{padding:"0 60px 0 20px",width:"700px",margin:"60px 0"},attrs:{model:t.form,rules:t.formRules,"label-width":"none"}},t._l(t.form.response_datas,(function(e,o){return s("div",{key:o+" onlyItem"},[s("el-form-item",{attrs:{prop:"response_datas."+o+".pack_id",rules:[],label:"包装编码"}},[s("el-input",{ref:"finishedProductCode"+o,refInFor:!0,on:{input:function(s){t.nextFocus("finishedProductCode"+(o+1),o,e.pack_id)}},model:{value:e.pack_id,callback:function(s){t.$set(e,"pack_id",s)},expression:"item.pack_id"}})],1)],1)})),0),s("div",[s("el-button",{on:{click:t.resetForm}},[t._v("重 置")])],1)],1)],1)},n=[],r=s("5530"),c=s("fd03"),u=s("2f62"),l={name:"MissStation",computed:Object(r["a"])({},Object(u["c"])(["ProductionPlanCode"])),props:{formStatus:{type:String,default:""},cardTitle:{type:String,default:""}},data:function(){return{timeout:"",Shipping_SN_length:"",form:{product_plan_code:"",status:"",response_datas:[{pack_id:""}]},formBase:{product_plan_code:"",status:"",response_datas:[{pack_id:""}]},formRules:{}}},methods:Object(r["a"])(Object(r["a"])({},Object(u["b"])(["getLogisticProductPlanDeal"])),{},{nextFocus:function(t,e,s){var o=this;this.timeout&&clearTimeout(this.timeout),this.timeout=setTimeout((function(){if(o.form.response_datas[0].length!=o.Shipping_SN_length)return o.$message.warning("包装编码长度为"+o.Shipping_SN_length+"个字节。"),!1;o.dialogSave()}),500)},getLogisticOperationSystem:function(){var t=this;c["a"].getLogisticOperationSystem({page:1,page_size:10}).then((function(e){console.log("打印参数列表 查询",e),0==e.code?(t.Package_Qty=e.data.data[0].Package_Qty,t.Shipping_SN_length=e.data.data[0].Shipping_SN_length,t.Product_length=e.data.data[0].Product_length,console.log("this.Package_Qty ",t.Package_Qty)):t.$message({message:e.message,type:"error"})}))},getLogisticstockInStockOut:function(t){var e=this;c["a"].getLogisticstockInStockOut(t).then((function(t){console.log("产品过站 新增",t),0==t.code?(e.form=JSON.parse(JSON.stringify(e.formBase)),e.$message({message:t.message,type:"success"})):e.$message({message:t.message,type:"error"})}))},resetForm:function(){this.form=JSON.parse(JSON.stringify(this.formBase))},dialogSave:function(){var t=this;if(console.log("this.form",this.form),!this.ProductionPlanCode)return this.$message.warning("没有进行中的生产计划！"),!1;this.$refs.formRef.validate((function(e){if(e){console.log("产品过站",t.form);var s=JSON.parse(JSON.stringify(t.form));s.status=t.formStatus,s.product_plan_code=t.ProductionPlanCode,s.response_datas=JSON.stringify(t.form.response_datas),console.log("paramsparams",s),t.getLogisticstockInStockOut(s)}else t.$message({message:"请修改正确的数据格式！",type:"warning"})}))}}),mounted:function(){var t=this;this.getLogisticOperationSystem(),this.getLogisticProductPlanDeal(),this.$nextTick((function(){t.$refs.firstInput.focus()}))}},d=l,f=(s("7395"),s("2877")),p=Object(f["a"])(d,i,n,!1,null,"5eaf98c7",null),g=p.exports,m={name:"UserLogin",data:function(){return{}},components:{FinishedProductStorageDispatch:g}},h=m,_=Object(f["a"])(h,o,a,!1,null,null,null);e["default"]=_.exports}}]);
//# sourceMappingURL=chunk-116c026a.c9c68597.js.map