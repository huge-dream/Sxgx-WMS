(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([[56],{"46b2":function(e,t,a){"use strict";a.r(t);var l=function(){var e=this,t=e._self._c;return t("div",{staticClass:"shadow-24 q-pa-md",style:{height:e.height,background:"white",borderRadius:"4px"}},[t("q-btn-group",{attrs:{push:""}},[t("q-btn",{attrs:{label:e.$t("upload_center.downloadgoodstemplate"),icon:"cloud_download"},on:{click:function(t){return e.downloadgoodstemplate()}}},[t("q-tooltip",{attrs:{"content-class":"bg-amber text-black shadow-4",offset:[10,10],"content-style":"font-size: 12px"}},[e._v(e._s(e.$t("upload_center.downloadgoodstemplate")))])],1),t("q-btn",{attrs:{label:e.$t("upload_center.downloadcustomertemplate"),icon:"cloud_download"},on:{click:function(t){return e.downloadcustomertemplate()}}},[t("q-tooltip",{attrs:{"content-class":"bg-amber text-black shadow-4",offset:[10,10],"content-style":"font-size: 12px"}},[e._v(e._s(e.$t("upload_center.downloadcustomertemplate")))])],1),t("q-btn",{attrs:{label:e.$t("upload_center.downloadsuppliertemplate"),icon:"cloud_download"},on:{click:function(t){return e.downloadsuppliertemplate()}}},[t("q-tooltip",{attrs:{"content-class":"bg-amber text-black shadow-4",offset:[10,10],"content-style":"font-size: 12px"}},[e._v(e._s(e.$t("upload_center.downloadsuppliertemplate")))])],1)],1),t("div",{staticStyle:{display:"flex"}},[t("div",{staticClass:"q-pt-md q-gutter-md row items-start"},[t("q-uploader",{staticStyle:{width:"300px",height:"200px"},attrs:{url:e.goodslistfile_pathname,method:"post",headers:[{name:"token",value:e.token},{name:"language",value:e.lang},{name:"operator",value:e.login_id}],"field-name":e=>"file",label:e.$t("upload_center.uploadgoodslistfile"),accept:".xlsx,csv,xls/*"},on:{rejected:e.onRejected,added:e.getfileinfo}})],1),t("div",{staticClass:"q-pa-md q-gutter-md row items-start"},[t("q-uploader",{staticStyle:{width:"300px",height:"200px"},attrs:{url:e.customerfile_pathname,method:"post",headers:[{name:"token",value:e.token},{name:"language",value:e.lang},{name:"operator",value:e.login_id}],"field-name":e=>"file",label:e.$t("upload_center.uploadcustomerfile"),accept:".xlsx,csv,xls/*"},on:{rejected:e.onRejected,added:e.getfileinfo}})],1),t("div",{staticClass:"q-pt-md q-gutter-md row items-start"},[t("q-uploader",{staticStyle:{width:"300px",height:"200px"},attrs:{url:e.supplierfile_pathname,method:"post",headers:[{name:"token",value:e.token},{name:"language",value:e.lang},{name:"operator",value:e.login_id}],"field-name":e=>"file",label:e.$t("upload_center.uploadsupplierfile"),accept:".xlsx,csv,xls/*"},on:{rejected:e.onRejected,added:e.getfileinfo}})],1)])],1)},o=[],n=a("3004"),i=a("18d6"),s=a("b06b"),d={name:"Pagecapital",data(){return{height:"",token:i["a"].getItem("openid"),lang:i["a"].getItem("lang"),login_id:i["a"].getItem("login_id"),capitalfile_pathname:n["b"]+"uploadfile/capitalfile/",customerfile_pathname:n["b"]+"uploadfile/customerfile/",freightfile_pathname:n["b"]+"uploadfile/freightfile/",goodslistfile_pathname:n["b"]+"uploadfile/goodslistfile/",supplierfile_pathname:n["b"]+"uploadfile/supplierfile/"}},methods:{checkFileType(e){return e.filter((e=>".xlsx, xls,csv/*"===e.type))},onRejected(e){this.$q.notify({type:"negative",message:`${e.length} file(s) did not pass validation constraints`})},getfileinfo(e){console.log(e)},downloadgoodstemplate(){var e=this;i["a"].has("auth")?i["a"].has("lang")&&"zh-hans"===i["a"].getItem("lang")?Object(s["a"])(n["b"]+"media/upload_example/goodslist_cn.xlsx"):Object(s["a"])(n["b"]+"media/upload_example/goodslist_en.xlsx"):e.$q.notify({message:e.$t("notice.loginerror"),color:"negative",icon:"warning"})},downloadcustomertemplate(){var e=this;i["a"].has("auth")?i["a"].has("lang")&&"zh-hans"===i["a"].getItem("lang")?Object(s["a"])(n["b"]+"media/upload_example/customer_cn.xlsx"):Object(s["a"])(n["b"]+"media/upload_example/customer_en.xlsx"):e.$q.notify({message:e.$t("notice.loginerror"),color:"negative",icon:"warning"})},downloadsuppliertemplate(){var e=this;i["a"].has("auth")?i["a"].has("lang")&&"zh-hans"===i["a"].getItem("lang")?Object(s["a"])(n["b"]+"media/upload_example/supplier_cn.xlsx"):Object(s["a"])(n["b"]+"media/upload_example/supplier_en.xlsx"):e.$q.notify({message:e.$t("notice.loginerror"),color:"negative",icon:"warning"})},setHeight(){this.$nextTick((()=>{this.$q.platform.is.electron?this.height=String(this.$q.screen.height-185)+"px":this.height=this.$q.screen.height-185+"px"}))}},mounted(){this.setHeight(),window.addEventListener("resize",this.setHeight)},beforeDestroy(){window.removeEventListener("resize",this.setHeight)},destroyed(){}},r=d,p=a("42e1"),c=a("a83f"),u=a("e7a9"),m=a("9c40"),g=a("05c0"),h=a("ee89"),f=a("eebe"),x=a.n(f),b=Object(p["a"])(r,l,o,!1,null,null,null);"function"===typeof c["default"]&&Object(c["default"])(b);t["default"]=b.exports;x()(b,"components",{QBtnGroup:u["a"],QBtn:m["a"],QTooltip:g["a"],QUploader:h["a"]})},a3ea:function(e,t){},a83f:function(e,t,a){"use strict";var l=a("a3ea"),o=a.n(l);t["default"]=o.a}}]);