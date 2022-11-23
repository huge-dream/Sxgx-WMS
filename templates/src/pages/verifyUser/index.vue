<template>
  <q-page class="flex flex-center">
    <q-dialog v-model="value" persistent>
      <q-card style="min-width: 350px">
        <q-card-section>
          <div class="text-h6">请进行扫码验证</div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <q-input dense v-model="loginCode" autofocus hint="请使用扫码枪进行扫码识别身份"
                   @keyup.enter="loginCodeOk">
            <template v-slot:before>
              <q-icon name="filter_center_focus"/>
            </template>
          </q-input>
        </q-card-section>

        <q-card-actions align="right" class="text-primary">
          <q-btn flat label="取消" @click="cancel"/>
          <q-btn flat label="确定" @click="loginCodeOk"/>
        </q-card-actions>
      </q-card>
    </q-dialog>
    <!--  入库  -->
    <in-library v-if="inDialog" :openid="openid" :login_name="username" :postauth="postauth" :getauth="getauth"
                :putauth="putauth" @cancel="inDialog=false"></in-library>
    <out-library v-if="outDialog" :openid="openid" :login_name="username" :postauth="postauth" :getauth="getauth"
                 :putauth="putauth" @cancel="outDialog=false"></out-library>

  </q-page>
</template>

<script>
import { getauth, post, baseurl } from 'boot/axios_request'
import InLibrary from 'pages/verifyUser/inLibrary'
import OutLibrary from 'pages/verifyUser/outLibrary'
import { LocalStorage, Notify, SessionStorage } from 'quasar'
import Bus from 'boot/bus'
import axios from 'axios'
import { i18n } from 'boot/i18n'

export default {
  name: 'verifyUser',
  components: { OutLibrary, InLibrary },
  props: {
    // 滚动优化的选项
    value: {
      type: Boolean,
      required: false,
      default: false
    },
    type: {
      type: String,
      required: true
    }
  },
  data () {
    return {
      loginCode: '',
      inDialog: false,
      outDialog: false,
      username: '',
      openid: '',
      postauth: '',
      getauth: '',
      putauth: ''
    }
  },
  created () {
  },
  mounted () {
  },
  methods: {
    cancel () {
      this.$emit('update:value', !this.value)
      this.loginCode = ''
    },
    // 进行登录获取token
    loginCodeOk () {
      if (!this.loginCode) {
        this.$q.notify({
          message: '请使用扫码枪进行扫码识别身份',
          icon: 'close',
          color: 'negative'
        })
        return
      }
      // 进行登录获取token
      this.$axios.post(
        baseurl + '/staff/code_login',
        { code: this.loginCode }
      ).then((res) => {
        if (res.data.status_code === 200) {
          this.$emit('update:value', !this.value)
          this.loginCode = ''
          // 弹出入库或出库需要填写信息
          if (this.type === 'in') {
            this.inDialog = true
          } else {
            this.outDialog = true
          }
          this.username = res.data.name
          this.openid = res.data.openid
          const axiosVersion = axios.create({
            timeout: 60 * 1000,
            baseURL: baseurl
          })
          axiosVersion.interceptors.request.use(
            function (config) {
              var lang = LocalStorage.getItem('lang')
              if (LocalStorage.has('lang')) {
                lang = lang || 'en-US'
              } else {
                LocalStorage.set('lang', 'en-US')
                lang = 'en-US'
              }
              config.headers.post['Content-Type'] = 'application/json, charset="utf-8"'
              config.headers.patch['Content-Type'] = 'application/json, charset="utf-8"'
              config.headers.put['Content-Type'] = 'application/json, charset="utf-8"'
              config.headers.token = LocalStorage.getItem('openid')
              config.headers.operator = LocalStorage.getItem('login_id')
              config.headers.language = lang
              return config
            },
            function (error) {
              return Promise.reject(error)
            }
          )
          axiosVersion.interceptors.response.use(
            function (response) {
              if (response.data.detail) {
                if (response.data.detail !== 'success') {
                  Notify.create({
                    message: response.data.detail,
                    icon: 'close',
                    color: 'negative',
                    timeout: 1500
                  })
                }
              }
              if (response.data.results) {
                var sslcheck = baseurl.split(':')
                if (response.data.next !== null) {
                  if (sslcheck.length === 2) {
                    var nextlinkcheck = (response.data.next).toString().split(sslcheck[1])
                    response.data.next = nextlinkcheck[1]
                  } else {
                    var nextlinkcheck1 = (response.data.next).toString().split(sslcheck[1] + ':' + sslcheck[2])
                    response.data.next = nextlinkcheck1[1]
                  }
                } else {
                  response.data.next = null
                }
                if (response.data.previous !== null) {
                  if (sslcheck.length === 2) {
                    var previouslinkcheck = (response.data.previous).toString().split(sslcheck[1])
                    response.data.previous = previouslinkcheck[1]
                  } else {
                    var previouslinkcheck1 = (response.data.previous).toString().split(sslcheck[1] + ':' + sslcheck[2])
                    response.data.previous = previouslinkcheck1[1]
                  }
                } else {
                  response.data.previous = null
                }
                return response.data
              }
              return response.data
            },
            function (error) {
              const defaultNotify = {
                message: i18n.t('notice.unknow_error'),
                icon: 'close',
                color: 'negative',
                timeout: 1500
              }
              if (error.code === 'ECONNABORTED' || error.message.indexOf('timeout') !== -1 || error.message === 'Network Error') {
                defaultNotify.message = i18n.t('notice.network_error')
                Notify.create(defaultNotify)
                return Promise.reject(error)
              }
              switch (error.response && error.response.status) {
                case 400:
                  defaultNotify.message = i18n.t('notice.400')
                  Notify.create(defaultNotify)
                  break
                case 401:
                  defaultNotify.message = i18n.t('notice.401')
                  Notify.create(defaultNotify)
                  break
                case 403:
                  defaultNotify.message = i18n.t('notice.403')
                  Notify.create(defaultNotify)
                  break
                case 404:
                  defaultNotify.message = i18n.t('notice.404')
                  Notify.create(defaultNotify)
                  break
                case 405:
                  defaultNotify.message = i18n.t('notice.405')
                  Notify.create(defaultNotify)
                  break
                case 408:
                  defaultNotify.message = i18n.t('notice.408')
                  Notify.create(defaultNotify)
                  break
                case 409:
                  defaultNotify.message = i18n.t('notice.409')
                  Notify.create(defaultNotify)
                  break
                case 410:
                  defaultNotify.message = i18n.t('notice.410')
                  Notify.create(defaultNotify)
                  break
                case 500:
                  defaultNotify.message = i18n.t('notice.500')
                  Notify.create(defaultNotify)
                  break
                case 501:
                  defaultNotify.message = i18n.t('notice.501')
                  Notify.create(defaultNotify)
                  break
                case 502:
                  defaultNotify.message = i18n.t('notice.502')
                  Notify.create(defaultNotify)
                  break
                case 503:
                  defaultNotify.message = i18n.t('notice.503')
                  Notify.create(defaultNotify)
                  break
                case 504:
                  defaultNotify.message = i18n.t('notice.504')
                  Notify.create(defaultNotify)
                  break
                case 505:
                  defaultNotify.message = i18n.t('notice.505')
                  Notify.create(defaultNotify)
                  break
                default:
                  Notify.create(defaultNotify)
                  break
              }
              return Promise.reject(error)
            }
          )
          this.getauth = function (url) {
            return axiosVersion.get(url)
          }
          this.postauth = function (url, data) {
            return axiosVersion.post(url, data)
          }
          this.putauth = function (url, data) {
            return axiosVersion.put(url, data)
          }
          this.$q.notify({
            message: '认证成功',
            icon: 'close',
            color: 'green'
          })
        } else {
          this.$q.notify({
            message: res.data.detail,
            icon: 'close',
            color: 'negative'
          })
          this.loginCode = ''
        }
      }).catch((err) => {
        console.log(3333, err)
        this.loginCode = ''
        this.$q.notify({
          message: err.detail,
          icon: 'close',
          color: 'negative'
        })
      })
    },
    inDialogCancel () {
      this.inDialog = false
      this.username = ''
      this.token = ''
    },
    outDialogCancel () {
      this.outDialog = false
      this.username = ''
      this.token = ''
    },
    inDialogOk () {
      this.inDialog = false
      this.username = ''
      this.token = ''
    },
    outDialogOk () {
      this.outDialog = false
      this.username = ''
      this.token = ''
    }
  }

}
</script>

<style scoped>

</style>
