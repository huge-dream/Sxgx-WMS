(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([[20],{"9c54":function(t,e,o){"use strict";o.r(e);var a=function(){var t=this,e=t._self._c;return e("div",[e("transition",{attrs:{appear:"","enter-active-class":"animated fadeIn"}},[e("q-table",{staticClass:"my-sticky-header-column-table shadow-24",attrs:{data:t.table_list,"row-key":"id",separator:t.separator,loading:t.loading,filter:t.filter,columns:t.columns,"hide-bottom":"",pagination:t.pagination,"no-data-label":"No data","no-results-label":"No data you want","table-style":{height:t.height},flat:"",bordered:""},on:{"update:pagination":function(e){t.pagination=e}},scopedSlots:t._u([{key:"top",fn:function(){return[e("q-btn-group",{attrs:{push:""}},[e("q-btn",{attrs:{label:t.$t("new"),icon:"add"},on:{click:function(e){t.newForm=!0}}},[e("q-tooltip",{attrs:{"content-class":"bg-amber text-black shadow-4",offset:[10,10],"content-style":"font-size: 12px"}},[t._v("\n             "+t._s(t.$t("newtip"))+"\n           ")])],1),e("q-btn",{attrs:{label:t.$t("refresh"),icon:"refresh"},on:{click:function(e){return t.reFresh()}}},[e("q-tooltip",{attrs:{"content-class":"bg-amber text-black shadow-4",offset:[10,10],"content-style":"font-size: 12px"}},[t._v("\n             "+t._s(t.$t("refreshtip"))+"\n           ")])],1)],1),e("q-space"),e("q-input",{attrs:{outlined:"",rounded:"",dense:"",debounce:"300",color:"primary",placeholder:t.$t("search")},on:{blur:function(e){return t.getSearchList()},keyup:function(e){return!e.type.indexOf("key")&&t._k(e.keyCode,"enter",13,e.key,"Enter")?null:t.getSearchList()}},scopedSlots:t._u([{key:"append",fn:function(){return[e("q-icon",{attrs:{name:"search"},on:{click:function(e){return t.getSearchList()}}})]},proxy:!0}]),model:{value:t.filter,callback:function(e){t.filter=e},expression:"filter"}})]},proxy:!0},{key:"body",fn:function(o){return[e("q-tr",{attrs:{props:o}},[o.row.id===t.editid?[e("q-td",{key:"goods_color",attrs:{props:o}},[e("q-input",{attrs:{dense:"",outlined:"",square:"",label:t.$t("goods.view_goodslist.goods_color"),autofocus:"",rules:[e=>e&&e.length>0||t.error1]},model:{value:t.editFormData.goods_color,callback:function(e){t.$set(t.editFormData,"goods_color",e)},expression:"editFormData.goods_color"}})],1)]:o.row.id!==t.editid?[e("q-td",{key:"goods_color",attrs:{props:o}},[t._v("\n             "+t._s(o.row.goods_color)+"\n           ")])]:t._e(),e("q-td",{key:"creater",attrs:{props:o}},[t._v("\n           "+t._s(o.row.creater)+"\n         ")]),e("q-td",{key:"create_time",attrs:{props:o}},[t._v("\n           "+t._s(o.row.create_time)+"\n         ")]),e("q-td",{key:"update_time",attrs:{props:o}},[t._v("\n           "+t._s(o.row.update_time)+"\n         ")]),t.editMode?t.editMode?[o.row.id===t.editid?[e("q-td",{key:"action",staticStyle:{width:"100px"},attrs:{props:o}},[e("q-btn",{attrs:{round:"",flat:"",push:"",color:"secondary",icon:"check"},on:{click:function(e){return t.editDataSubmit()}}},[e("q-tooltip",{attrs:{"content-class":"bg-amber text-black shadow-4",offset:[10,10],"content-style":"font-size: 12px"}},[t._v("\n                 "+t._s(t.$t("confirmedit"))+"\n              ")])],1),e("q-btn",{attrs:{round:"",flat:"",push:"",color:"red",icon:"close"},on:{click:function(e){return t.editDataCancel()}}},[e("q-tooltip",{attrs:{"content-class":"bg-amber text-black shadow-4",offset:[10,10],"content-style":"font-size: 12px"}},[t._v("\n                 "+t._s(t.$t("canceledit"))+"\n              ")])],1)],1)]:o.row.id!==t.editid?void 0:t._e()]:t._e():[e("q-td",{key:"action",staticStyle:{width:"100px"},attrs:{props:o}},[e("q-btn",{attrs:{round:"",flat:"",push:"",color:"purple",icon:"edit"},on:{click:function(e){return t.editData(o.row)}}},[e("q-tooltip",{attrs:{"content-class":"bg-amber text-black shadow-4",offset:[10,10],"content-style":"font-size: 12px"}},[t._v("\n                 "+t._s(t.$t("edit"))+"\n              ")])],1),e("q-btn",{attrs:{round:"",flat:"",push:"",color:"dark",icon:"delete"},on:{click:function(e){return t.deleteData(o.row.id)}}},[e("q-tooltip",{attrs:{"content-class":"bg-amber text-black shadow-4",offset:[10,10],"content-style":"font-size: 12px"}},[t._v("\n                 "+t._s(t.$t("delete"))+"\n              ")])],1)],1)]],2)]}}])})],1),[e("div",{staticClass:"q-pa-md flex flex-center"},[e("q-btn",{directives:[{name:"show",rawName:"v-show",value:t.pathname_previous,expression:"pathname_previous"}],attrs:{flat:"",push:"",color:"purple",label:t.$t("previous"),icon:"navigate_before"},on:{click:function(e){return t.getListPrevious()}}},[e("q-tooltip",{attrs:{"content-class":"bg-amber text-black shadow-4",offset:[10,10],"content-style":"font-size: 12px"}},[t._v("\n          "+t._s(t.$t("previous"))+"\n        ")])],1),e("q-btn",{directives:[{name:"show",rawName:"v-show",value:t.pathname_next,expression:"pathname_next"}],attrs:{flat:"",push:"",color:"purple",label:t.$t("next"),"icon-right":"navigate_next"},on:{click:function(e){return t.getListNext()}}},[e("q-tooltip",{attrs:{"content-class":"bg-amber text-black shadow-4",offset:[10,10],"content-style":"font-size: 12px"}},[t._v("\n          "+t._s(t.$t("next"))+"\n        ")])],1),e("q-btn",{directives:[{name:"show",rawName:"v-show",value:!t.pathname_previous&&!t.pathname_next,expression:"!pathname_previous && !pathname_next"}],attrs:{flat:"",push:"",color:"dark",label:t.$t("no_data")}})],1)],e("q-dialog",{model:{value:t.newForm,callback:function(e){t.newForm=e},expression:"newForm"}},[e("q-card",{staticClass:"shadow-24"},[e("q-bar",{staticClass:"bg-light-blue-10 text-white rounded-borders",staticStyle:{height:"50px"}},[e("div",[t._v(t._s(t.$t("newtip")))]),e("q-space"),e("q-btn",{directives:[{name:"close-popup",rawName:"v-close-popup"}],attrs:{dense:"",flat:"",icon:"close"}},[e("q-tooltip",{attrs:{"content-class":"bg-amber text-black shadow-4"}},[t._v(t._s(t.$t("index.close")))])],1)],1),e("q-card-section",{staticClass:"scroll",staticStyle:{"max-height":"325px",width:"400px"}},[e("q-input",{attrs:{dense:"",outlined:"",square:"",label:t.$t("goods.view_goodslist.goods_color"),autofocus:"",rules:[e=>e&&e.length>0||t.error1]},on:{keyup:function(e){return!e.type.indexOf("key")&&t._k(e.keyCode,"enter",13,e.key,"Enter")?null:t.newDataSubmit()}},model:{value:t.newFormData.goods_color,callback:function(e){t.$set(t.newFormData,"goods_color",e)},expression:"newFormData.goods_color"}})],1),e("div",{staticStyle:{float:"right",padding:"15px 15px 15px 0"}},[e("q-btn",{staticStyle:{"margin-right":"25px"},attrs:{color:"white","text-color":"black"},on:{click:function(e){return t.newDataCancel()}}},[t._v(t._s(t.$t("cancel")))]),e("q-btn",{attrs:{color:"primary"},on:{click:function(e){return t.newDataSubmit()}}},[t._v(t._s(t.$t("submit")))])],1)],1)],1),e("q-dialog",{model:{value:t.deleteForm,callback:function(e){t.deleteForm=e},expression:"deleteForm"}},[e("q-card",{staticClass:"shadow-24"},[e("q-bar",{staticClass:"bg-light-blue-10 text-white rounded-borders",staticStyle:{height:"50px"}},[e("div",[t._v(t._s(t.$t("delete")))]),e("q-space"),e("q-btn",{directives:[{name:"close-popup",rawName:"v-close-popup"}],attrs:{dense:"",flat:"",icon:"close"}},[e("q-tooltip",[t._v(t._s(t.$t("index.close")))])],1)],1),e("q-card-section",{staticClass:"scroll",staticStyle:{"max-height":"325px",width:"400px"}},[t._v("\n       "+t._s(t.$t("deletetip"))+"\n     ")]),e("div",{staticStyle:{float:"right",padding:"15px 15px 15px 0"}},[e("q-btn",{staticStyle:{"margin-right":"25px"},attrs:{color:"white","text-color":"black"},on:{click:function(e){return t.deleteDataCancel()}}},[t._v(t._s(t.$t("cancel")))]),e("q-btn",{attrs:{color:"primary"},on:{click:function(e){return t.deleteDataSubmit()}}},[t._v(t._s(t.$t("submit")))])],1)],1)],1)],2)},n=[],r=o("3004"),s={name:"Pagegoodscolor",data(){return{openid:"",login_name:"",authin:"0",pathname:"goodscolor/",pathname_previous:"",pathname_next:"",separator:"cell",loading:!1,height:"",table_list:[],columns:[{name:"goods_color",required:!0,label:this.$t("goods.view_color.goods_color"),align:"left",field:"goods_color"},{name:"creater",label:this.$t("creater"),field:"creater",align:"center"},{name:"create_time",label:this.$t("createtime"),field:"create_time",align:"center"},{name:"update_time",label:this.$t("updatetime"),field:"update_time",align:"center"},{name:"action",label:this.$t("action"),align:"right"}],filter:"",pagination:{page:1,rowsPerPage:"30"},newForm:!1,newFormData:{goods_color:"",creater:""},editid:0,editFormData:{},editMode:!1,deleteForm:!1,deleteid:0,error1:this.$t("goods.view_color.error1")}},methods:{getList(){var t=this;t.$q.localStorage.has("auth")&&Object(r["e"])(t.pathname,{}).then((e=>{t.table_list=e.results,t.pathname_previous=e.previous,t.pathname_next=e.next})).catch((e=>{t.$q.notify({message:e.detail,icon:"close",color:"negative"})}))},getSearchList(){var t=this;t.$q.localStorage.has("auth")&&Object(r["e"])(t.pathname+"?goods_color__icontains="+t.filter,{}).then((e=>{t.table_list=e.results,t.pathname_previous=e.previous,t.pathname_next=e.next})).catch((e=>{t.$q.notify({message:e.detail,icon:"close",color:"negative"})}))},getListPrevious(){var t=this;t.$q.localStorage.has("auth")&&Object(r["e"])(t.pathname_previous,{}).then((e=>{t.table_list=e.results,t.pathname_previous=e.previous,t.pathname_next=e.next})).catch((e=>{t.$q.notify({message:e.detail,icon:"close",color:"negative"})}))},getListNext(){var t=this;t.$q.localStorage.has("auth")&&Object(r["e"])(t.pathname_next,{}).then((e=>{t.table_list=e.results,t.pathname_previous=e.previous,t.pathname_next=e.next})).catch((e=>{t.$q.notify({message:e.detail,icon:"close",color:"negative"})}))},reFresh(){var t=this;t.getList()},newDataSubmit(){var t=this,e=[];t.table_list.forEach((t=>{e.push(t.goods_color)})),-1===e.indexOf(t.newFormData.goods_color)&&0!==t.newFormData.goods_color.length?(t.newFormData.creater=t.login_name,Object(r["h"])(t.pathname,t.newFormData).then((e=>{t.getList(),t.newDataCancel(),t.$q.notify({message:"Success Create",icon:"check",color:"green"})})).catch((e=>{t.$q.notify({message:e.detail,icon:"close",color:"negative"})}))):-1!==e.indexOf(t.newFormData.goods_color)?t.$q.notify({message:t.$t("notice.goodserror.goods_colorerror"),icon:"close",color:"negative"}):0===t.newFormData.goods_color.length&&t.$q.notify({message:t.$t("goods.view_color.error1"),icon:"close",color:"negative"}),e=[]},newDataCancel(){var t=this;t.newForm=!1,t.newFormData={goods_color:"",creater:""}},editData(t){var e=this;e.editMode=!0,e.editid=t.id,e.editFormData={goods_color:t.goods_color,creater:e.login_name}},editDataSubmit(){var t=this;Object(r["i"])(t.pathname+t.editid+"/",t.editFormData).then((e=>{t.editDataCancel(),t.getList(),t.$q.notify({message:"Success Edit Data",icon:"check",color:"green"})})).catch((e=>{t.$q.notify({message:e.detail,icon:"close",color:"negative"})}))},editDataCancel(){var t=this;t.editMode=!1,t.editid=0,t.editFormData={goods_color:"",creater:""}},deleteData(t){var e=this;e.deleteForm=!0,e.deleteid=t},deleteDataSubmit(){var t=this;Object(r["d"])(t.pathname+t.deleteid+"/").then((e=>{t.deleteDataCancel(),t.getList(),t.$q.notify({message:"Success Edit Data",icon:"check",color:"green"})})).catch((e=>{t.$q.notify({message:e.detail,icon:"close",color:"negative"})}))},deleteDataCancel(){var t=this;t.deleteForm=!1,t.deleteid=0}},created(){var t=this;t.$q.localStorage.has("openid")?t.openid=t.$q.localStorage.getItem("openid"):(t.openid="",t.$q.localStorage.set("openid","")),t.$q.localStorage.has("login_name")?t.login_name=t.$q.localStorage.getItem("login_name"):(t.login_name="",t.$q.localStorage.set("login_name","")),t.$q.localStorage.has("auth")?(t.authin="1",t.getList()):t.authin="0"},mounted(){var t=this;t.$q.platform.is.electron?t.height=String(t.$q.screen.height-290)+"px":t.height=t.$q.screen.height-290+"px"},updated(){},destroyed(){}},i=s,l=o("2877"),c=o("ec92"),d=o("eaac"),p=o("e7a9"),u=o("9c40"),h=o("05c0"),g=o("2c91"),m=o("27f9"),_=o("0016"),f=o("bd08"),b=o("db86"),v=o("24e8"),w=o("f09f"),q=o("d847"),x=o("a370"),y=o("7f67"),$=o("eebe"),k=o.n($),D=Object(l["a"])(i,a,n,!1,null,null,null);"function"===typeof c["default"]&&Object(c["default"])(D);e["default"]=D.exports;k()(D,"components",{QTable:d["a"],QBtnGroup:p["a"],QBtn:u["a"],QTooltip:h["a"],QSpace:g["a"],QInput:m["a"],QIcon:_["a"],QTr:f["a"],QTd:b["a"],QDialog:v["a"],QCard:w["a"],QBar:q["a"],QCardSection:x["a"]}),k()(D,"directives",{ClosePopup:y["a"]})},c067:function(t,e){},ec92:function(t,e,o){"use strict";var a=o("c067"),n=o.n(a);e["default"]=n.a}}]);