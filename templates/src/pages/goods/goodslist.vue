<template>
  <div>
    <transition appear enter-active-class="animated fadeIn">
      <q-table
        class="my-sticky-header-column-table shadow-24"
        :data="table_list"
        row-key="id"
        :separator="separator"
        :loading="loading"
        :filter="filter"
        :columns="columns"
        hide-bottom
        :pagination.sync="pagination"
        no-data-label="No data"
        no-results-label="No data you want"
        :table-style="{ height: height }"
        flat
        bordered
      >
        <template v-slot:top>
          <q-btn-group push>
            <q-btn :label="$t('new')" icon="add" @click="newForm = true">
              <q-tooltip content-class="bg-amber text-black shadow-4" :offset="[10, 10]" content-style="font-size: 12px">{{ $t('newtip') }}</q-tooltip>
            </q-btn>
            <q-btn :label="$t('refresh')" icon="refresh" @click="reFresh()">
              <q-tooltip content-class="bg-amber text-black shadow-4" :offset="[10, 10]" content-style="font-size: 12px">{{ $t('refreshtip') }}</q-tooltip>
            </q-btn>
          </q-btn-group>
          <q-space />
          <q-input outlined rounded dense debounce="300" color="primary" v-model="filter" :placeholder="$t('search')" @blur="getSearchList()" @keyup.enter="getSearchList()">
            <template v-slot:append>
              <q-icon name="search" @click="getSearchList()" />
            </template>
          </q-input>
        </template>
        <template v-slot:body="props">
          <q-tr :props="props">
            <template v-if="props.row.id === editid">
              <q-td key="goods_code" :props="props">
                <q-input
                  dense
                  outlined
                  square
                  v-model="editFormData.goods_code"
                  :label="$t('goods.view_goodslist.goods_code')"
                  autofocus
                  :rules="[val => (val && val.length > 0) || error1]"
                />
              </q-td>
            </template>
            <template v-else-if="props.row.id !== editid">
              <q-td key="goods_code" :props="props">{{ props.row.goods_code }}</q-td>
            </template>
            <template v-if="props.row.id === editid">
              <q-td key="goods_unit" :props="props">
                <q-input
                  dense
                  outlined
                  square
                  v-model="editFormData.goods_unit"
                  :label="'单位'"
                  autofocus
                  :rules="[val => (val && val.length > 0) || '单位不能为空']"
                />
              </q-td>
            </template>
            <template v-else-if="props.row.id !== editid">
              <q-td key="goods_unit" :props="props">{{ props.row.goods_unit }}</q-td>
            </template>
            <template v-if="props.row.id === editid">
              <q-td key="goods_desc" :props="props">
                <q-input
                  dense
                  outlined
                  square
                  v-model="editFormData.goods_desc"
                  :label="$t('goods.view_goodslist.goods_desc')"
                  :rules="[val => (val && val.length > 0) || error2]"
                />
              </q-td>
            </template>
            <template v-else-if="props.row.id !== editid">
              <q-td key="goods_desc" :props="props">{{ props.row.goods_desc }}</q-td>
            </template>
            <template v-if="props.row.id === editid">
              <q-td key="light_guidance" :props="props">
              <q-toggle
                v-model="editFormData.light_guidance"
              />
              </q-td>
            </template>
            <template v-else-if="props.row.id !== editid">
              <q-td key="light_guidance" :props="props">{{ props.row.light_guidance?'是':'否' }}</q-td>
            </template>
            <q-td key="creater" :props="props">{{ props.row.creater }}</q-td>
            <q-td key="create_time" :props="props">{{ props.row.create_time }}</q-td>
            <q-td key="update_time" :props="props">{{ props.row.update_time }}</q-td>
            <template v-if="!editMode">
              <q-td key="action" :props="props" style="width: 100px">
                <q-btn
                  v-show="
                    $q.localStorage.getItem('staff_type') !== 'Supplier' &&
                      $q.localStorage.getItem('staff_type') !== 'Customer' &&
                      $q.localStorage.getItem('staff_type') !== 'Outbound' &&
                      $q.localStorage.getItem('staff_type') !== 'StockControl'
                  "
                  round
                  flat
                  push
                  color="info"
                  icon="print"
                  @click="viewData(props.row)"
                >
                  <q-tooltip content-class="bg-amber text-black shadow-4" :offset="[10, 10]" content-style="font-size: 12px">
                    {{ $t('goods.view_goodslist.print_goods_label') }}
                  </q-tooltip>
                </q-btn>
                <q-btn round flat push color="purple" icon="edit" @click="editData(props.row)">
                  <q-tooltip content-class="bg-amber text-black shadow-4" :offset="[10, 10]" content-style="font-size: 12px">{{ $t('edit') }}</q-tooltip>
                </q-btn>
                <q-btn round flat push color="dark" icon="delete" @click="deleteData(props.row.id)">
                  <q-tooltip content-class="bg-amber text-black shadow-4" :offset="[10, 10]" content-style="font-size: 12px">{{ $t('delete') }}</q-tooltip>
                </q-btn>
              </q-td>
            </template>
            <template v-else-if="editMode">
              <template v-if="props.row.id === editid">
                <q-td key="action" :props="props" style="width: 100px">
                  <q-btn round flat push color="secondary" icon="check" @click="editDataSubmit()">
                    <q-tooltip content-class="bg-amber text-black shadow-4" :offset="[10, 10]" content-style="font-size: 12px">{{ $t('confirmedit') }}</q-tooltip>
                  </q-btn>
                  <q-btn round flat push color="red" icon="close" @click="editDataCancel()">
                    <q-tooltip content-class="bg-amber text-black shadow-4" :offset="[10, 10]" content-style="font-size: 12px">{{ $t('canceledit') }}</q-tooltip>
                  </q-btn>
                </q-td>
              </template>
              <template v-else-if="props.row.id !== editid"></template>
            </template>
          </q-tr>
        </template>
      </q-table>
    </transition>
    <template>
      <div class="q-pa-lg flex flex-center">
        <q-btn v-show="pathname_previous" flat push color="purple" :label="$t('previous')" icon="navigate_before" @click="getListPrevious()">
          <q-tooltip content-class="bg-amber text-black shadow-4" :offset="[10, 10]" content-style="font-size: 12px">{{ $t('previous') }}</q-tooltip>
        </q-btn>
        <q-btn v-show="pathname_next" flat push color="purple" :label="$t('next')" icon-right="navigate_next" @click="getListNext()">
          <q-tooltip content-class="vbg-amber text-black shadow-4" :offset="[10, 10]" content-style="font-size: 12px">{{ $t('next') }}</q-tooltip>
        </q-btn>
        <q-btn v-show="!pathname_previous && !pathname_next" flat push color="dark" :label="$t('no_data')"></q-btn>
      </div>
    </template>
    <q-dialog v-model="newForm">
      <q-card class="shadow-24">
        <q-bar class="bg-light-blue-10 text-white rounded-borders" style="height: 50px">
          <div>{{ $t('newtip') }}</div>
          <q-space />
          <q-btn dense flat icon="close" v-close-popup>
            <q-tooltip content-class="bg-amber text-black shadow-4">{{ $t('index.close') }}</q-tooltip>
          </q-btn>
        </q-bar>
        <q-card-section style="max-height: 325px; width: 400px" class="scroll">
          <q-input
            dense
            outlined
            square
            v-model="newFormData.goods_code"
            :label="$t('goods.view_goodslist.goods_code')"
            autofocus
            :rules="[val => (val && val.length > 0) || error1]"
            @keyup.enter="newDataSubmit()"
          />
          <q-input
            dense
            outlined
            square
            v-model="newFormData.goods_desc"
            :label="$t('goods.view_goodslist.goods_desc')"
            :rules="[val => (val && val.length > 0) || error2]"
            @keyup.enter="newDataSubmit()"
          />
          <q-toggle
            left-label
            :label="$t('goods.view_goodslist.light_guidance')"
              v-model="newFormData.light_guidance"
          />
        </q-card-section>
        <div style="float: right; padding: 15px 15px 15px 0">
          <q-btn color="white" text-color="black" style="margin-right: 25px" @click="newDataCancel()">{{ $t('cancel') }}</q-btn>
          <q-btn color="primary" @click="newDataSubmit()">{{ $t('submit') }}</q-btn>
        </div>
      </q-card>
    </q-dialog>
    <q-dialog v-model="deleteForm">
      <q-card class="shadow-24">
        <q-bar class="bg-light-blue-10 text-white rounded-borders" style="height: 50px">
          <div>{{ $t('delete') }}</div>
          <q-space />
          <q-btn dense flat icon="close" v-close-popup>
            <q-tooltip>{{ $t('index.close') }}</q-tooltip>
          </q-btn>
        </q-bar>
        <q-card-section style="max-height: 325px; width: 400px" class="scroll">{{ $t('deletetip') }}</q-card-section>
        <div style="float: right; padding: 15px 15px 15px 0">
          <q-btn color="white" text-color="black" style="margin-right: 25px" @click="deleteDataCancel()">{{ $t('cancel') }}</q-btn>
          <q-btn color="primary" @click="deleteDataSubmit()">{{ $t('submit') }}</q-btn>
        </div>
      </q-card>
    </q-dialog>
    <q-dialog v-model="viewForm">
      <div class="row" id="printMe" style="width: 500px;height:110px;background-color: white">
        <div style="margin-top: 5px;">
          <q-card-section>
            <div class="row" style="height: 30px;width: 200px;">
<!--              <div class="col-3"><img src="statics/goods/logo.png" style="width: 30px;height: 30px;margin-top: -10px;margin-left: 5px" /></div>-->
              <div class="col-12" style="height: 40px;float: contour;margin-top: -10px;margin-right: 10px">
                <p style="font-size: 16px;font-weight: 500">
                  {{ $t('goods.view_goodslist.goods_code') + ': ' + goods_code }}
                  <br>
                  {{ $t('goods.view_goodslist.goods_name') + ': ' }} {{ goods_desc }}
                </p>
              </div>
            </div>
            <hr>
              <canvas id="barCode" style="width: 100%;"/>
          </q-card-section>
        </div>
        <div style="margin-top: 5px;">
          <q-card-section>
            <div class="row" style="height: 30px;width: 200px;">
<!--              <div class="col-3"><img src="statics/goods/logo.png" style="width: 30px;height: 30px;margin-top: -10px;margin-left: 5px" /></div>-->
              <div class="col-12" style="height: 40px;float: contour;margin-top: -10px">
                <p style="font-size: 16px;font-weight: 500">
                  {{ $t('goods.view_goodslist.goods_code') + ': ' + goods_code }}
                  <br>
                  {{ $t('goods.view_goodslist.goods_name') + ': ' }} {{ goods_desc }}
                </p>
              </div>
            </div>
            <hr />
            <canvas id="barCode" style="width: 100%;"/>
          </q-card-section>
        </div>
      </div>
      <div style="float: right; padding: 15px 15px 15px 0"><q-btn color="primary" icon="print" v-print="printObj">print</q-btn></div>
    </q-dialog>
  </div>
</template>
<router-view />

<script>
import { getauth, postauth, putauth, deleteauth, getfile } from 'boot/axios_request'
import { date, exportFile, LocalStorage } from 'quasar'
import JsBarcode from 'jsbarcode'

export default {
  name: 'Pagegoodslist',
  data () {
    return {
      goods_code: '',
      goods_desc: '',
      openid: '',
      login_name: '',
      authin: '0',
      pathname: 'goods/',
      pathname_previous: '',
      pathname_next: '',
      separator: 'cell',
      loading: false,
      height: '',
      viewForm: false,
      printObj: {
        id: 'printMe',
        popTitle: this.$t('inbound.asn')
      },
      table_list: [],
      goods_unit_list: [],
      goods_class_list: [],
      goods_brand_list: [],
      goods_color_list: [],
      goods_shape_list: [],
      goods_specs_list: [],
      goods_origin_list: [],
      supplier_list: [],
      columns: [
        { name: 'goods_code', required: true, label: this.$t('goods.view_goodslist.goods_code'), align: 'left', field: 'goods_code' },
        { name: 'goods_unit', label: this.$t('goods.view_goodslist.goods_unit'), field: 'goods_unit', align: 'center' },
        { name: 'goods_desc', label: this.$t('goods.view_goodslist.goods_desc'), field: 'goods_desc', align: 'center' },
        { name: 'light_guidance', label: this.$t('goods.view_goodslist.light_guidance'), field: 'light_guidance', align: 'center' },
        { name: 'creater', label: this.$t('creater'), field: 'creater', align: 'center' },
        { name: 'create_time', label: this.$t('createtime'), field: 'create_time', align: 'center' },
        { name: 'update_time', label: this.$t('updatetime'), field: 'update_time', align: 'center' },
        { name: 'action', label: this.$t('action'), align: 'right' }
      ],
      filter: '',
      pagination: {
        page: 1,
        rowsPerPage: '30'
      },
      newForm: false,
      newFormData: {
        goods_code: '',
        goods_desc: '',
        light_guidance: false,
        creater: ''
      },
      editid: 0,
      editFormData: {},
      editMode: false,
      deleteForm: false,
      deleteid: 0,
      error1: this.$t('goods.view_goodslist.error1'),
      error2: this.$t('goods.view_goodslist.error2'),
      error3: this.$t('goods.view_goodslist.error3'),
      error4: this.$t('goods.view_goodslist.error4'),
      error5: this.$t('goods.view_goodslist.error5'),
      error6: this.$t('goods.view_goodslist.error6'),
      error7: this.$t('goods.view_goodslist.error7'),
      error8: this.$t('goods.view_unit.error1'),
      error9: this.$t('goods.view_class.error1'),
      error10: this.$t('goods.view_brand.error1'),
      error11: this.$t('goods.view_color.error1'),
      error12: this.$t('goods.view_shape.error1'),
      error13: this.$t('goods.view_specs.error1'),
      error14: this.$t('goods.view_origin.error1'),
      error15: this.$t('goods.view_goodslist.error8'),
      error16: this.$t('goods.view_goodslist.error9'),
      bindBarCode (data) {
        JsBarcode('#barCode', data, {
          background: '#fff',
          displayValue: false,
          // width: 2, //
          height: 30, // 一维码的高度
          margin: 0 // 一维码与容器的margin
        })
      }
    }
  },
  methods: {
    getList () {
      var _this = this
      getauth(_this.pathname, {})
        .then(res => {
          _this.table_list = res.results
          _this.goods_unit_list = res.goods_unit_list
          _this.goods_class_list = res.goods_class_list
          _this.goods_brand_list = res.goods_brand_list
          _this.goods_color_list = res.goods_color_list
          _this.goods_shape_list = res.goods_shape_list
          _this.goods_specs_list = res.goods_specs_list
          _this.goods_origin_list = res.goods_origin_list
          _this.supplier_list = res.supplier_list
          _this.pathname_previous = res.previous
          _this.pathname_next = res.next
        })
        .catch(err => {
          _this.$q.notify({
            message: err.detail,
            icon: 'close',
            color: 'negative'
          })
        })
    },
    getSearchList () {
      var _this = this
      if (LocalStorage.has('auth')) {
        getauth(_this.pathname + '?goods_desc__icontains=' + _this.filter, {})
          .then(res => {
            _this.table_list = res.results
            _this.goods_unit_list = res.goods_unit_list
            _this.goods_class_list = res.goods_class_list
            _this.goods_brand_list = res.goods_brand_list
            _this.goods_color_list = res.goods_color_list
            _this.goods_shape_list = res.goods_shape_list
            _this.goods_specs_list = res.goods_specs_list
            _this.goods_origin_list = res.goods_origin_list
            _this.supplier_list = res.supplier_list
            _this.pathname_previous = res.previous
            _this.pathname_next = res.next
          })
          .catch(err => {
            _this.$q.notify({
              message: err.detail,
              icon: 'close',
              color: 'negative'
            })
          })
      } else {
      }
    },
    getListPrevious () {
      var _this = this
      if (LocalStorage.has('auth')) {
        getauth(_this.pathname_previous, {})
          .then(res => {
            _this.table_list = res.results
            _this.goods_unit_list = res.goods_unit_list
            _this.goods_class_list = res.goods_class_list
            _this.goods_brand_list = res.goods_brand_list
            _this.goods_color_list = res.goods_color_list
            _this.goods_shape_list = res.goods_shape_list
            _this.goods_specs_list = res.goods_specs_list
            _this.goods_origin_list = res.goods_origin_list
            _this.supplier_list = res.supplier_list
            _this.pathname_previous = res.previous
            _this.pathname_next = res.next
          })
          .catch(err => {
            _this.$q.notify({
              message: err.detail,
              icon: 'close',
              color: 'negative'
            })
          })
      } else {
      }
    },
    getListNext () {
      var _this = this
      if (LocalStorage.has('auth')) {
        getauth(_this.pathname_next, {})
          .then(res => {
            _this.table_list = res.results
            _this.goods_unit_list = res.goods_unit_list
            _this.goods_class_list = res.goods_class_list
            _this.goods_brand_list = res.goods_brand_list
            _this.goods_color_list = res.goods_color_list
            _this.goods_shape_list = res.goods_shape_list
            _this.goods_specs_list = res.goods_specs_list
            _this.goods_origin_list = res.goods_origin_list
            _this.supplier_list = res.supplier_list
            _this.pathname_previous = res.previous
            _this.pathname_next = res.next
          })
          .catch(err => {
            _this.$q.notify({
              message: err.detail,
              icon: 'close',
              color: 'negative'
            })
          })
      } else {
      }
    },
    reFresh () {
      var _this = this
      _this.getList()
    },
    newDataSubmit () {
      var _this = this
      var goodscodes = []
      _this.table_list.forEach(i => {
        goodscodes.push(i.goods_code)
      })
      if (goodscodes.indexOf(_this.newFormData.goods_code) === -1 && _this.newFormData.goods_code.length !== 0) {
        _this.newFormData.creater = _this.login_name
        postauth(_this.pathname, _this.newFormData)
          .then(res => {
            _this.getList()
            _this.newDataCancel()
            if (res.status_code != 500) {
              _this.$q.notify({
                message: 'Success Create',
                icon: 'check',
                color: 'green'
              })
            }
          })
          .catch(err => {
            _this.$q.notify({
              message: err.detail,
              icon: 'close',
              color: 'negative'
            })
          })
      } else if (goodscodes.indexOf(_this.newFormData.goods_code) !== -1) {
        _this.$q.notify({
          message: _this.$t('notice.goodserror.goods_listerror'),
          icon: 'close',
          color: 'negative'
        })
      } else if (_this.newFormData.goods_code.length === 0) {
        _this.$q.notify({
          message: _this.$t('goods.view_goodslist.error1'),
          icon: 'close',
          color: 'negative'
        })
      }
      goodscodes = []
    },
    newDataCancel () {
      var _this = this
      _this.newForm = false
      _this.newFormData = {
        goods_code: '',
        goods_desc: '',
        light_guidance: false,
        creater: ''
      }
    },
    editData (e) {
      var _this = this
      _this.editMode = true
      _this.editid = e.id
      _this.editFormData = {
        goods_code: e.goods_code,
        goods_desc: e.goods_desc,
        light_guidance: e.light_guidance,
        goods_weight: e.goods_weight,
        goods_w: e.goods_w,
        goods_d: e.goods_d,
        goods_h: e.goods_h,
        goods_unit: e.goods_unit,
        goods_cost: e.goods_cost,
        goods_price: e.goods_price,
        creater: _this.login_name,
        bar_code: e.bar_code
      }
    },
    editDataSubmit () {
      var _this = this
      putauth(_this.pathname + _this.editid + '/', _this.editFormData)
        .then(res => {
          _this.editDataCancel()
          _this.getList()
          if (res.status_code !== 500) {
            _this.$q.notify({
              message: 'Success Edit Data',
              icon: 'check',
              color: 'green'
            })
          }
        })
        .catch(err => {
          _this.$q.notify({
            message: err.detail,
            icon: 'close',
            color: 'negative'
          })
        })
    },
    editDataCancel () {
      var _this = this
      _this.editMode = false
      _this.editid = 0
      _this.editFormData = {
        goods_code: '',
        goods_desc: '',
        goods_weight: '',
        goods_w: '',
        goods_d: '',
        goods_h: '',
        goods_unit: '',
        goods_cost: '',
        goods_price: '',
        creater: ''
      }
    },
    deleteData (e) {
      var _this = this
      _this.deleteForm = true
      _this.deleteid = e
    },
    deleteDataSubmit () {
      var _this = this
      deleteauth(_this.pathname + _this.deleteid + '/')
        .then(res => {
          _this.deleteDataCancel()
          _this.getList()
          _this.$q.notify({
            message: 'Success Edit Data',
            icon: 'check',
            color: 'green'
          })
        })
        .catch(err => {
          _this.$q.notify({
            message: err.detail,
            icon: 'close',
            color: 'negative'
          })
        })
    },
    deleteDataCancel () {
      var _this = this
      _this.deleteForm = false
      _this.deleteid = 0
    },
    viewData (e) {
      this.viewForm = true
      this.goods_code = e.goods_code
      this.goods_desc = e.goods_desc
      this.$nextTick(() => {
        this.bindBarCode(e.goods_code)
      })
    }
  },
  created () {
    var _this = this
    if (LocalStorage.has('openid')) {
      _this.openid = LocalStorage.getItem('openid')
    } else {
      _this.openid = ''
      LocalStorage.set('openid', '')
    }
    if (LocalStorage.has('login_name')) {
      _this.login_name = LocalStorage.getItem('login_name')
    } else {
      _this.login_name = ''
      LocalStorage.set('login_name', '')
    }
    if (LocalStorage.has('auth')) {
      _this.authin = '1'
      _this.getList()
    } else {
      _this.authin = '0'
    }
  },
  mounted () {
    var _this = this
    if (_this.$q.platform.is.electron) {
      _this.height = String(_this.$q.screen.height - 290) + 'px'
    } else {
      _this.height = _this.$q.screen.height - 290 + '' + 'px'
    }
  },
  updated () {},
  destroyed () {}
}
</script>
