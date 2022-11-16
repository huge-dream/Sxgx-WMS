<template>
  <q-page class="flex flex-center">
    <div style="margin-top: -7%;">
      <div class="q-mb-xl" style="color: #4C5875;text-align: center;">
        <div style="font-weight: bold;font-size: 100px;letter-spacing: 10px;">WELCOME</div>
        <div style="font-size: 22px;letter-spacing: 2px;">
          中物汇智
          <span v-if="isEnglish">&nbsp</span>
          {{ $t('index.index_title') }}
        </div>
      </div>
      <div class="flex flex-center">
        <lottie-web-cimo ref="lottie_web" style="width: 50%; max-width: 80%" />
      </div>
      <br>
      <br>
      <br>
      <br>
      <div class="flex flex-center">
        <q-btn push color="primary" label="扫码入库" size="lg" :ripple="{ center: true }" icon="cloud_upload" style="margin-right: 50px" @click="inWarehouseClick"/>
        <q-btn push color="secondary" label="扫码出库" size="lg" :ripple="{ center: true }" icon="local_shipping" @click="outWarehouseClick"/>
      </div>
    </div>
    <div style="position: absolute;right: 2%;bottom: 8%;font-family:SourceHanSansCN; font-size: 16px;color: #4C5875;">—— &nbsp;&nbsp; ZWHZ-WMS-PC-V1.0 &nbsp; &nbsp;——</div>
<!--  验证扫码登录  -->
    <verify-user :value.sync="verifyDialog" :type="type"></verify-user>
  </q-page>
</template>
<script>
import LottieWebCimo from 'components/lottie-web-cimo'
import { database } from '../db/database'
import { Platform, LocalStorage, Screen, SessionStorage } from 'quasar'
import VerifyUser from 'pages/verifyUser/index'

export default {
  name: 'PageIndex',
  components: { VerifyUser, LottieWebCimo },
  data () {
    return {
      isEnglish: false,
      cleardata: [],
      height: '',
      width: '100%',
      verifyDialog: false,
      type: ''
    }
  },
  methods: {
    outWarehouseClick () {
      this.verifyDialog = true
      this.type = 'out'
    },
    inWarehouseClick () {
      this.verifyDialog = true
      this.type = 'in'
    }
  },
  beforeCreate: function () {
  },
  created: function () {
    LocalStorage.set('menulink', '')
    this.isEnglish = this.$q.localStorage.getItem('lang') === 'en-us'
  },
  beforeMount: function () {
  },
  mounted: function () {
    var _this = this
    var page = database.getInstance().get().test
    page.toArray().then(res => {
      if (res.length > 0) {
        this.cleardata = []
        page.each(result => {
          this.cleardata.push(result.id)
        })
        page.bulkDelete(this.cleardata)
        this.cleardata = []
      } else {
        page.add({
          id: 1,
          test: 'next'
        })
      }
    })
    if (Platform.is.electron) {
      _this.height = String(Screen.height) + 'px'
    } else {
      _this.height = Screen.height + '' + 'px'
    }
  }
}
</script>
