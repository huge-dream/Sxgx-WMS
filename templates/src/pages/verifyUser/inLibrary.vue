<template>
  <q-page class="flex flex-center">
    <q-dialog v-model="newForm" persistent maximized>
      <q-card class="shadow-24" style="width: 700px;height: 425px;">
        <q-bar class="bg-light-blue-10 text-white rounded-borders" style="height: 50px">
           <div>入库</div>
          <q-space/>
          <q-btn dense flat icon="close" v-close-popup>
            <q-tooltip content-class="bg-amber text-black shadow-4">{{ $t('index.close') }}</q-tooltip>
          </q-btn>
        </q-bar>
        <q-card-section style="max-height: 325px; width:700px" class="scroll">
          <q-input
            dense
            outlined
            square
            debounce="500"
            v-for="(item,index) in tableFromNum"
            v-model.number="data[`goodsData${index+1}`].qty"
            :key="index"
            type="number"
            :label="$t('stock.view_stocklist.goods_qty')"
            style="margin-bottom: 5px"
          >
            <template v-slot:before>
              <q-select
                :ref="`goodsData${index}Code`"
                dense
                outlined
                square
                use-input
                hide-selected
                fill-input
                v-model="data[`goodsData${index+1}`].code"
                :label="$t('goods.view_goodslist.goods_code')"
                :options="options"
                @focus="getFocus(index+1)"
                @input-value="setModel($event,index)"
                autofocus
                @filter="filterFn"
                @blur="goodsCodeEnter(index)"
                @keyup.enter="goodsCodeEnter(index)"
              >
                <template v-slot:no-option>
                  <q-item>
                    <q-item-section class="text-grey">No results</q-item-section>
                  </q-item>
                </template>
              </q-select>
              <q-select
                :ref="`goodsData${index}BinName`"
                dense
                outlined
                square
                use-input
                hide-selected
                fill-input
                v-model="data[`goodsData${index+1}`].bin_name"
                :label="$t('inbound.view_asn.bin_name')"
                :options="binSetOptions"
                option-label="bin_name"
                option-value="id"
                @focus="getFocus(index+1)"
                autofocus
              >
                <template v-slot:no-option>
                  <q-item>
                    <q-item-section class="text-grey">No results</q-item-section>
                  </q-item>
                </template>
                <template v-if="data[`goodsData${index+1}`].bin_name" v-slot:append>
                  <q-icon name="cancel" @click.stop="data[`goodsData${index+1}`].bin_name = ''" class="cursor-pointer"/>
                </template>
              </q-select>
            </template>
          </q-input>
        </q-card-section>
        <div style="float: right; padding: 15px 15px 15px 0">
          <q-btn color="white" text-color="black" style="margin-right: 25px"
                 @click="newDataCancel()">{{ $t('cancel') }}
          </q-btn>
          <q-btn color="primary" @click="newDataSubmit()">{{ $t('submit') }}</q-btn>
        </div>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script>
import { getauth, putauth } from 'boot/axios_request'
import { SessionStorage } from 'quasar'

export default {
  name: 'inLibrary',
  props: {
    // 滚动优化的选项
    login_name: {
      type: String,
      required: false
    },
    openid: {
      type: String,
      required: true
    },
    getauth: {
      type: Function,
      required: true
    },
    postauth: {
      type: Function,
      required: true
    },
    putauth: {
      type: Function,
      required: true
    }
  },
  data () {
    return {
      authin: '0',
      tableFromNum: 10,
      pathname: 'asn/',
      pathname_previous: '',
      pathname_next: '',
      newForm: true,
      newFormData: {
        asn_code: '',
        supplier: '',
        goods_code: [],
        goods_qty: [],
        creater: ''
      },
      table_list: [],
      data: {
        goodsData1: { code: '', qty: '' },
        goodsData2: { code: '', qty: '' },
        goodsData3: { code: '', qty: '' },
        goodsData4: { code: '', qty: '' },
        goodsData5: { code: '', qty: '' },
        goodsData6: { code: '', qty: '' },
        goodsData7: { code: '', qty: '' },
        goodsData8: { code: '', qty: '' },
        goodsData9: { code: '', qty: '' },
        goodsData10: { code: '', qty: '' }
      },
      isEdit: false,
      options: SessionStorage.getItem('goods_code'),
      options1: [],
      goodsListData: [],
      binSetOptions: []
    }
  },
  created () {
    this.getAllGoodsCode()
  },
  mounted () {
  },
  methods: {
    newDataSubmit () {
      var _this = this
      _this.newFormData.creater = _this.login_name
      let cancelRequest = false
      const submitForm = [] // 用于提交的form
      // if (_this.newFormData.supplier !== '') {
      _this.newFormData.goods_code = []
      _this.newFormData.goods_qty = []
      let goodsDataCheck = 0
      for (let i = 0; i < 10; i++) {
        const goodsData = `goodsData${i + 1}`
        if (_this.data[goodsData].code !== '' && _this.data[goodsData].qty !== '') {
          if (_this.data[goodsData].qty < 1) {
            cancelRequest = true
            _this.$q.notify({
              message: 'Total Quantity Must Be > 0',
              icon: 'close',
              color: 'negative'
            })
          } else {
            _this.newFormData.goods_code.push(_this.data[goodsData].code)
            _this.newFormData.goods_qty.push(_this.data[goodsData].qty)
            const dict = {
              goods_code: _this.data[goodsData].code,
              number: _this.data[goodsData].qty,
              bin_name: _this.data[goodsData].bin_name.bin_name,
              type: 0,
              creater: _this.login_name
            }
            submitForm.push(dict)
          }
          goodsDataCheck += 1
        }
      }
      if (goodsDataCheck === 0) {
        cancelRequest = true
        _this.$q.notify({
          message: 'Please Enter The Goods & Qty',
          icon: 'close',
          color: 'negative'
        })
      }
      // } else {
      //   cancelRequest = true
      //   _this.$q.notify({
      //     message: 'Please Enter The Supplier',
      //     icon: 'close',
      //     color: 'negative'
      //   })
      // }
      console.log(11, cancelRequest)
      if (!cancelRequest) {
        console.log(3333, submitForm)
        this.postauth('in_out_warehouse/in_out_warehouse/', submitForm)
          .then(res => {
            this.table_list = []
            _this.newDataCancel()
            _this.$q.notify({
              message: 'Success Create',
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
      }
    },
    getFocus (number) {
      this.listNumber = number
    },
    filterFn (val, update, abort) {
      if (this.options.indexOf(val) !== -1) {
        abort()
        return
      }
      update(() => {
        this.options = this.allOptions
      })
    },
    getAllGoodsCode () {
      this.getauth('goods/').then(res => {
        const goodscodelist = []
        for (let i = 0; i < res.results.length; i++) {
          goodscodelist.push(res.results[i].goods_code)
        }
        this.allOptions = goodscodelist
      })
    },
    setBinSetOptions (val) {
      const _this = this
      if (!val) {
        this.data[`goodsData${this.listNumber}`].bin = ''
      }
      const needle = val.toLowerCase()
      this.getauth('/binset/?empty_label=true&bin_name__icontains=' + needle).then(res => {
        for (let i = 0; i < res.results.length; i++) {
          if (this.listNumber) {
            if (res.results[i].bin_name === val) {
              this.data[`goodsData${this.listNumber}`].bin = res.results[i].id
            }
          }
        }
        _this.binSetOptions = res.results
      })
    },
    newDataCancel () {
      this.$emit('cancel', !this.value)
      var _this = this
      _this.newForm = false
      _this.newFormData = {
        asn_code: '',
        supplier: '',
        goods_code: [],
        goods_qty: [],
        creater: ''
      }
      _this.goodsDataClear()
    },
    goodsDataClear () {
      var _this = this
      for (let i = 1; i <= this.tableFromNum; i++) {
        _this.data[`goodsData${i}`] = { code: '', qty: '' }
      }
    },
    goodsCodeEnter (index) {
      if (!this.data[`goodsData${index + 1}`].code) return
      if (this.options.indexOf(this.data[`goodsData${index + 1}`].code) !== -1) {
        this.$refs[`goodsData${index}BinName`][0].showPopup()
        this.getauth('/binset/?empty_label=true&goods_code=' + this.data[`goodsData${index + 1}`].code.toLowerCase()).then(res => {
          this.binSetOptions = res.results
        })
      } else {
        this.$refs[`goodsData${index}Code`][0].focus()
        this.$q.notify({
          message: '未查询到该商品编码',
          icon: 'close',
          color: 'negative'
        })
      }
    },
    setModel (val, index) {
      this.data[`goodsData${index + 1}`].code = val
    }

  }

}
</script>

<style scoped>

</style>
